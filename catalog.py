#!/usr/bin/env python3
"""
Rebuild the combined record of ALL batches:
  catalog/catalog.csv   one row per object (prompt, status, tokens, cost, code stats)
  catalog/CATALOG.md    cumulative summary, per-batch table, per-category table, per-object table
  catalog/gallery.html  click through every generated object in one page
Run after every generation run; it always rebuilds from batches/*/runs.csv, so nothing is lost.
"""
import csv, html, json, re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "catalog"; OUT.mkdir(exist_ok=True)

def num(x):
    try: return float(x)
    except (TypeError, ValueError): return 0.0

# prompts (source of truth for what each batch contains)
prompts = {}
for pf in sorted((ROOT / "prompts").glob("*.jsonl")):
    for line in open(pf):
        if line.strip():
            it = json.loads(line); it["batch"] = pf.stem; prompts[it["id"]] = it

# latest attempt per id + attempt counts
latest, attempts = {}, defaultdict(int)
for rc in sorted((ROOT / "batches").glob("*/runs.csv")):
    for r in csv.DictReader(open(rc)):
        attempts[r["id"]] += 1
        latest[r["id"]] = r
# total spend includes failed / retried attempts
all_cost = defaultdict(float)
for rc in (ROOT / "batches").glob("*/runs.csv"):
    for r in csv.DictReader(open(rc)):
        all_cost[r["id"]] += num(r["cost_usd"])

def code_stats(path):
    s = path.read_text()
    return {
        "meshes": len(re.findall(r"new THREE\.Mesh\b", s)),
        "groups": len(re.findall(r"new THREE\.Group\b", s)),
        "animated": "y" if ("requestAnimationFrame" in s or "setAnimationLoop" in s) else "n",
        "controls_ui": "y" if re.search(r"<input|<button|lil-gui|GUI\(", s) else "n",
        "shadows": "y" if "castShadow" in s else "n",
        "geometries": " ".join(sorted({g.replace("Geometry", "") for g in re.findall(r"new THREE\.(\w+Geometry)", s)})),
    }

rows = []
for oid, p in sorted(prompts.items()):
    r = latest.get(oid, {})
    html_path = ROOT / "batches" / p["batch"] / "outputs" / f"{oid}.html"
    row = {"id": oid, "batch": p["batch"], "category": p.get("category", ""),
           "status": r.get("status", "not_run") if html_path.exists() or r else "not_run",
           "attempts": attempts.get(oid, 0), "model": r.get("model", ""),
           "input_tokens": int(num(r.get("input_tokens")) + num(r.get("cache_creation_tokens")) + num(r.get("cache_read_tokens"))),
           "output_tokens": int(num(r.get("output_tokens"))),
           "cost_usd": round(num(r.get("cost_usd")), 5), "cost_all_attempts_usd": round(all_cost.get(oid, 0), 5),
           "duration_s": num(r.get("duration_s")), "html_lines": int(num(r.get("html_lines"))),
           "file": str(html_path.relative_to(ROOT)) if html_path.exists() else "",
           "prompt": p["prompt"]}
    if html_path.exists():
        row["status"] = "ok"
        row.update(code_stats(html_path))
    rows.append(row)

fields = ["id", "batch", "category", "status", "attempts", "model", "input_tokens", "output_tokens",
          "cost_usd", "cost_all_attempts_usd", "duration_s", "html_lines", "meshes", "groups",
          "animated", "controls_ui", "shadows", "geometries", "file", "prompt"]
with open(OUT / "catalog.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore"); w.writeheader(); w.writerows(rows)

# ---------- markdown report ----------
def agg(rs):
    ran = [r for r in rs if r["status"] != "not_run"]
    ok = [r for r in rs if r["status"] == "ok"]
    cost = sum(r["cost_all_attempts_usd"] for r in rs)
    return {"n": len(rs), "ran": len(ran), "ok": len(ok),
            "in": sum(r["input_tokens"] for r in ran), "out": sum(r["output_tokens"] for r in ran),
            "cost": cost, "avg_cost": cost / len(ran) if ran else 0,
            "avg_out": sum(r["output_tokens"] for r in ran) / len(ran) if ran else 0,
            "avg_lines": sum(r["html_lines"] for r in ok) / len(ok) if ok else 0,
            "avg_t": sum(r["duration_s"] for r in ran) / len(ran) if ran else 0}

T = agg(rows)
md = ["# 3D object generation — combined record", "",
      f"Objects defined: **{T['n']}** · run: **{T['ran']}** · succeeded: **{T['ok']}**  ",
      f"Tokens: {T['in']:,} in / {T['out']:,} out · Total cost (incl. retries): **${T['cost']:.4f}**  ",
      f"Avg per object: ${T['avg_cost']:.4f}, {T['avg_out']:,.0f} output tokens, {T['avg_t']:.1f}s, "
      f"{T['avg_lines']:.0f} lines of code  ",
      f"Projected cost for 100 objects at this average: **${T['avg_cost']*100:.2f}**", ""]

def table(title, key):
    groups = defaultdict(list)
    for r in rows: groups[r[key]].append(r)
    out = [f"## {title}", "", f"| {key} | defined | ok | total cost | avg cost | avg out tokens | avg lines | avg time |",
           "|---|---|---|---|---|---|---|---|"]
    for k, rs in sorted(groups.items()):
        a = agg(rs)
        out.append(f"| {k} | {a['n']} | {a['ok']} | ${a['cost']:.4f} | ${a['avg_cost']:.4f} | "
                   f"{a['avg_out']:,.0f} | {a['avg_lines']:.0f} | {a['avg_t']:.1f}s |")
    return out + [""]

md += table("By batch", "batch") + table("By category", "category")
md += ["## All objects", "",
       "| id | batch | category | status | out tokens | cost | lines | meshes | anim | UI | geometries |",
       "|---|---|---|---|---|---|---|---|---|---|---|"]
for r in rows:
    md.append(f"| {r['id']} | {r['batch']} | {r['category']} | {r['status']} | {r['output_tokens']:,} | "
              f"${r['cost_usd']:.4f} | {r['html_lines']} | {r.get('meshes','')} | {r.get('animated','')} | "
              f"{r.get('controls_ui','')} | {r.get('geometries','')} |")
(OUT / "CATALOG.md").write_text("\n".join(md) + "\n")

# ---------- gallery ----------
items = [{"id": r["id"], "batch": r["batch"], "category": r["category"], "status": r["status"],
          "cost": r["cost_usd"], "out": r["output_tokens"], "lines": r["html_lines"],
          "src": "../" + r["file"] if r["file"] else "", "prompt": r["prompt"]} for r in rows]
gallery = """<!doctype html><html><head><meta charset="utf-8"><title>3D object gallery</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{margin:0;font:14px system-ui,sans-serif;display:flex;height:100vh;background:#f4f4f2;color:#222}
#side{width:320px;overflow:auto;border-right:1px solid #ddd;background:#fff}
#side h3{margin:12px 12px 4px;font-size:12px;text-transform:uppercase;color:#888}
.it{padding:8px 12px;cursor:pointer;border-bottom:1px solid #f0f0f0}
.it:hover,.it.on{background:#eef3ff}.it small{color:#888;display:block}
.bad{color:#b33}#main{flex:1;display:flex;flex-direction:column}
#info{padding:10px 14px;border-bottom:1px solid #ddd;background:#fff}
iframe{flex:1;border:0;background:#ddd}
</style></head><body><div id="side"></div><div id="main"><div id="info">Select an object</div>
<iframe id="view"></iframe></div>
<script>
const items = __DATA__;
const side = document.getElementById('side'); let last = null;
for (const it of items) {
  if (it.batch !== last) { side.insertAdjacentHTML('beforeend', `<h3>${it.batch}</h3>`); last = it.batch; }
  const d = document.createElement('div'); d.className = 'it';
  d.innerHTML = `<b class="${it.status==='ok'?'':'bad'}">${it.id}</b><small>${it.category} · ${it.status} · $${it.cost.toFixed(4)} · ${it.out.toLocaleString()} tok · ${it.lines} lines</small>`;
  d.onclick = () => {
    document.querySelectorAll('.it').forEach(e => e.classList.remove('on')); d.classList.add('on');
    document.getElementById('info').textContent = it.prompt;
    document.getElementById('view').src = it.src || 'about:blank';
  };
  side.appendChild(d);
}
</script></body></html>"""
(OUT / "gallery.html").write_text(gallery.replace("__DATA__", json.dumps(items)))

print("\n".join(md[:7]))
print(f"\nWrote {OUT/'catalog.csv'}, {OUT/'CATALOG.md'}, {OUT/'gallery.html'}")
