#!/usr/bin/env python3
"""
Batch-generate three.js 3D objects with Claude, organized by batch, with token/cost logging.

Layout:
  prompts/batch_XX.jsonl          one prompt file per batch (you add new ones here)
  batches/batch_XX/outputs/*.html generated code
  batches/batch_XX/logs/*.json    raw responses
  batches/batch_XX/runs.csv       every attempt for that batch (tokens, cost, time)

Usage:
  python gen_batch.py --list                  # show every batch / object and whether it's done
  python gen_batch.py --all --jobs 4          # run everything not yet generated, across all batches
  python gen_batch.py --batch batch_05        # just one batch (repeat --batch for several)
  python gen_batch.py --ids 041-050           # pick objects by number: ranges and/or lists, e.g. 041-045,052,060
  python gen_batch.py --batch batch_02 --force  # regenerate
  python gen_batch.py --all --backend api --model claude-sonnet-5
Then: python catalog.py   (rebuilds the combined record for all batches)
"""
import argparse, csv, json, os, re, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

SPEC = """You are generating a single 3D object as a web page.

Object to build:
{prompt}

Hard requirements:
- Output ONE complete, self-contained HTML file inside a single ```html code block, and nothing else.
- Use three.js loaded via an import map from https://cdn.jsdelivr.net/npm/three@0.160.0/ (build/three.module.js and examples/jsm/ addons).
- Build all geometry procedurally in code (no external models, textures or images).
- Include OrbitControls, a ground plane or subtle backdrop, soft lighting with shadows, and resize handling.
- Use MeshStandardMaterial / MeshPhysicalMaterial with sensible roughness/metalness.
- Group parts logically (THREE.Group per sub-part) with descriptive names.
- Do not use any tools and do not write files; just reply with the code block.
"""

ROOT = Path(__file__).parent
PROMPTS_DIR, BATCHES_DIR = ROOT / "prompts", ROOT / "batches"
FIELDS = ["id", "batch", "category", "backend", "model", "status", "input_tokens", "output_tokens",
          "cache_creation_tokens", "cache_read_tokens", "cost_usd", "duration_s",
          "html_bytes", "html_lines", "timestamp"]
lock = Lock()


def extract_html(text):
    m = re.search(r"```html\s*(.*?)```", text, re.S)
    if m:
        return m.group(1).strip()
    return text.strip() if "<html" in text.lower() else None


def run_claude_code(full_prompt, model):
    cmd = ["claude", "-p", full_prompt, "--output-format", "json", "--max-turns", "1"]
    if model:
        cmd += ["--model", model]
    t0 = time.time()
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    dt = time.time() - t0
    if p.returncode != 0 and not p.stdout.strip():
        raise RuntimeError(p.stderr[-2000:])
    data = json.loads(p.stdout)
    u = data.get("usage", {}) or {}
    return {"text": data.get("result", ""), "raw": data,
            "input_tokens": u.get("input_tokens", 0), "output_tokens": u.get("output_tokens", 0),
            "cache_creation_tokens": u.get("cache_creation_input_tokens", 0),
            "cache_read_tokens": u.get("cache_read_input_tokens", 0),
            "cost_usd": data.get("total_cost_usd"), "duration_s": round(dt, 1)}


def run_api(full_prompt, model):
    import anthropic
    client = anthropic.Anthropic()
    t0 = time.time()
    with client.messages.stream(model=model, max_tokens=16000,
                                messages=[{"role": "user", "content": full_prompt}]) as s:
        msg = s.get_final_message()
    dt = time.time() - t0
    u = msg.usage
    pin, pout = float(os.getenv("PRICE_IN_PER_MTOK", "0")), float(os.getenv("PRICE_OUT_PER_MTOK", "0"))
    cost = (u.input_tokens * pin + u.output_tokens * pout) / 1e6 if (pin or pout) else None
    return {"text": "".join(b.text for b in msg.content if b.type == "text"), "raw": msg.model_dump(),
            "input_tokens": u.input_tokens, "output_tokens": u.output_tokens,
            "cache_creation_tokens": getattr(u, "cache_creation_input_tokens", 0) or 0,
            "cache_read_tokens": getattr(u, "cache_read_input_tokens", 0) or 0,
            "cost_usd": cost, "duration_s": round(dt, 1)}


def batch_dirs(batch):
    d = BATCHES_DIR / batch
    (d / "outputs").mkdir(parents=True, exist_ok=True)
    (d / "logs").mkdir(parents=True, exist_ok=True)
    return d


def process(item, args):
    oid, batch = item["id"], item["batch"]
    d = batch_dirs(batch)
    row = {"id": oid, "batch": batch, "category": item.get("category", ""), "backend": args.backend,
           "model": args.model or "default", "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")}
    try:
        r = (run_claude_code if args.backend == "claude" else run_api)(SPEC.format(prompt=item["prompt"]), args.model)
        (d / "logs" / f"{oid}.json").write_text(json.dumps(r["raw"], indent=2, default=str))
        html = extract_html(r["text"])
        if html:
            (d / "outputs" / f"{oid}.html").write_text(html)
            stale = d / "outputs" / f"{oid}.FAILED.txt"
            if stale.exists():
                stale.unlink()
            row.update(status="ok", html_bytes=len(html.encode()), html_lines=html.count("\n") + 1)
        else:
            (d / "outputs" / f"{oid}.FAILED.txt").write_text(r["text"])
            row.update(status="no_html", html_bytes=0, html_lines=0)
        for k in ["input_tokens", "output_tokens", "cache_creation_tokens", "cache_read_tokens", "cost_usd", "duration_s"]:
            row[k] = r[k]
    except Exception as e:
        row.update(status=f"error: {str(e)[:200]}")
    with lock:
        path = d / "runs.csv"
        new = not path.exists()
        with open(path, "a", newline="") as f:
            w = csv.DictWriter(f, fieldnames=FIELDS)
            if new:
                w.writeheader()
            w.writerow(row)
    return row


def load_items(batches):
    items, seen = [], {}
    for pf in sorted(PROMPTS_DIR.glob("*.jsonl")):
        b = pf.stem
        for line in open(pf):
            if not line.strip():
                continue
            it = json.loads(line)
            if it["id"] in seen:
                sys.exit(f"Duplicate id {it['id']} in {b} and {seen[it['id']]} — ids must be unique across batches.")
            seen[it["id"]] = b
            it["batch"] = b
            if batches is None or b in batches:
                items.append(it)
    return items


def parse_ids(spec):
    nums = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            a, b = part.split("-")
            nums.update(range(int(a), int(b) + 1))
        elif part:
            nums.add(int(part))
    return nums


def is_done(it):
    return (BATCHES_DIR / it["batch"] / "outputs" / f"{it['id']}.html").exists()


def show_list():
    items = load_items(None)
    by = {}
    for it in items:
        by.setdefault(it["batch"], []).append(it)
    for b, its in by.items():
        done = sum(is_done(i) for i in its)
        print(f"\n{b}  ({done}/{len(its)} done)")
        for i in its:
            print(f"  [{'x' if is_done(i) else ' '}] {i['id']:<30} {i.get('category','')}")
    total = sum(is_done(i) for i in items)
    print(f"\nTotal: {total}/{len(items)} done")


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--batch", action="append", help="batch name, e.g. batch_02 (repeatable)")
    g.add_argument("--ids", help="object numbers, e.g. 041-050 or 003,017,041-045")
    g.add_argument("--all", action="store_true", help="all prompt files in prompts/")
    g.add_argument("--list", action="store_true", help="list batches/objects and done status, then exit")
    ap.add_argument("--backend", choices=["claude", "api"], default="claude")
    ap.add_argument("--model", default=None, help="e.g. claude-sonnet-5, claude-opus-5-5")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()
    if args.backend == "api" and not args.model:
        sys.exit("--model is required for the api backend")

    if args.list:
        return show_list()
    if args.ids:
        wanted = parse_ids(args.ids)
        items = [i for i in load_items(None) if int(i["id"].split("_")[0]) in wanted]
    else:
        items = load_items(None if args.all else set(args.batch))
    if not items:
        sys.exit("No prompts matched the selection.")
    if not args.force:
        items = [i for i in items if not is_done(i)]
    items = items[: args.limit] if args.limit else items
    print(f"Generating {len(items)} objects with {args.jobs} workers...")

    with ThreadPoolExecutor(max_workers=args.jobs) as ex:
        for f in as_completed([ex.submit(process, i, args) for i in items]):
            r = f.result()
            print(f"[{r['status'][:8]:>8}] {r['batch']}/{r['id']:<24} out={r.get('output_tokens','-')} "
                  f"cost={r.get('cost_usd','-')} t={r.get('duration_s','-')}s")
    print("\nDone. Run `python catalog.py` to update the combined record.")


if __name__ == "__main__":
    main()
