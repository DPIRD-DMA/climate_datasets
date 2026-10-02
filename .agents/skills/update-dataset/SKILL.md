---
name: update-dataset
description: Update a climate dataset in data/datasets.json in the climate_datasets repository, then regenerate and validate the README and dashboard. Use only when working in this repository. Do not use for datasets in other projects.
---

# Update Dataset

Use this repo-scoped skill only from the `climate_datasets` repository root.

## Workflow

1. Confirm `data/datasets.json` and `.agents/skills/update-dataset/scripts/update_dataset.py` exist.
2. Check `git status --short` and preserve unrelated work.
3. Identify the intended dataset and obtain only the fields the user wants changed.
4. Run the helper with `--dry-run` first. Fuzzy matches require an explicit selection.
5. Run it again without `--dry-run` only after checking the complete proposed object.
6. Run `make all` and review `git diff`; never commit for the user.

## Patch Existing Fields

```bash
python3 .agents/skills/update-dataset/scripts/update_dataset.py \
  --name "SILO" --dry-run <<'JSON'
{
  "access_conditions": "Accessible via SILO network (free)",
  "update_frequency": "Daily"
}
JSON
```

After reviewing the output, repeat without `--dry-run`.

If fuzzy matching returns several candidates, rerun with the displayed one-based selection:

```bash
python3 .agents/skills/update-dataset/scripts/update_dataset.py \
  --name "SILO" --select 1 --dry-run <<'JSON'
{ "access_conditions": "..." }
JSON
```

## Replacement Mode

`--replace` requires a complete valid dataset object. It does not accept a partial object.

## Guardrails

- Unknown fields, empty required fields, non-string values, invalid source URLs, and duplicate names are rejected.
- Fuzzy matches never update a dataset without exact matching or explicit selection.
- The helper preserves all top-level registry keys and writes atomically.
- Existing output is never changed by `--dry-run` or failed validation.

