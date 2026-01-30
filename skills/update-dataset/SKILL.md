---
name: update-dataset
description: Update an existing climate dataset entry in data/datasets.json with fuzzy name matching and keep README/dashboard in sync. Use when a user asks to edit, update, or correct a dataset entry in this repository.
---

# Update Dataset

## Workflow
1. Confirm you are in the repo root and `data/datasets.json` exists.
2. Use fuzzy matching to select the dataset by name.
3. Apply a JSON snippet or use interactive prompts to update fields.
4. Regenerate README and sync the dashboard data.
5. Run the reference label check.

## Commands
Update from JSON snippet (stdin) with fuzzy match:

```bash
python skills/update-dataset/scripts/update_dataset.py --name "SILO" <<'JSON'
{
  "access_conditions": "Accessible via SILO network (free)",
  "update_frequency": "Daily"
}
JSON
```

Interactive update with fuzzy match:

```bash
python skills/update-dataset/scripts/update_dataset.py --name "SILO" --interactive
```

If multiple matches are found:

```bash
python skills/update-dataset/scripts/update_dataset.py --name "SILO" --select 1 <<'JSON'
{ "access_conditions": "..." }
JSON
```

Post-update sync:

```bash
scripts/generate-readme-table.py
scripts/sync-dashboard-data.py
scripts/check-reference-labels.py
```

## Notes
- Use `--replace` only when you intend to replace the entire dataset object.
- Keep `category` and `format` values aligned with existing entries to preserve filter behavior.
