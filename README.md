# 3D object batch generation

## Directory layout
```
prompts/batch_01.jsonl   001–010
prompts/batch_02.jsonl   011–020
prompts/batch_03.jsonl … batch_10.jsonl   021–100 (100 objects total)
prompts/INDEX.md         all 100 prompts at a glance: overview table + category counts + full prompts per batch
                         (for a new batch, just add a new file; ids must be unique across batches)
batches/batch_XX/        generated code, raw logs, and runs.csv for each batch (archived per batch)
catalog/                 combined record for all batches (catalog.csv / CATALOG.md / gallery.html)
```

## One-time step: archive the first 10 you already generated
If you ran the previous version, `outputs/`, `logs/`, and `runs.csv` are in the root directory:
```
python migrate_v1.py      # moves them into batches/batch_01/; ones already generated will not be regenerated
```

## Workflow for each batch (same every time)
```
python gen_batch.py --all --jobs 4     # runs every prompt not yet generated, across all batches
python catalog.py                      # rebuilds the combined record
```
- Check what has been run: `python gen_batch.py --list`
- Run a chosen 10: `python gen_batch.py --batch batch_05`, or by number `python gen_batch.py --ids 041-050`
- Mix and match: `--ids 003,017,041-045`, or several batches `--batch batch_05 --batch batch_06`
- Failed ones (`*.FAILED.txt`) are retried automatically on the next run with `--all`; the cost of failed attempts also counts toward the total.
- Try a small run first: `--limit 2`
- To view: run `python -m http.server` in this directory, then open http://localhost:8000/catalog/gallery.html
