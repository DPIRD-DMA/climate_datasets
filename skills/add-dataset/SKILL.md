---
name: add-dataset
description: Add a new climate dataset entry to data/datasets.json and keep README/dashboard in sync. Use when a user asks to add a dataset, insert a new dataset row, or register a new data source in this repository.
---

# Add Dataset

## Workflow
1. Confirm you are in the repo root and `data/datasets.json` exists.
2. Require a JSON object snippet from the user, or use `--interactive` if they prefer prompts.
3. Add the dataset via the bundled script.
4. Regenerate README and sync the dashboard data.
5. Run the reference label check.

## Commands
Add from JSON snippet (stdin):

```bash
python skills/add-dataset/scripts/add_dataset.py <<'JSON'
{
  "name": "Dataset name",
  "category": "Station observations",
  "resolution": "~1 km²",
  "format": "NetCDF",
  "variables": "Key variables",
  "method": "Short methodology summary",
  "access_conditions": "Free or registration",
  "temporal_coverage": "Daily, monthly, years",
  "spatial_domain": "Australia",
  "update_frequency": "Daily",
  "license": "",
  "provider_contact": "",
  "source_url": "https://..."
}
JSON
```

Interactive add:

```bash
python skills/add-dataset/scripts/add_dataset.py --interactive
```

Post-add sync:

```bash
scripts/generate-readme-table.py
scripts/sync-dashboard-data.py
scripts/check-reference-labels.py
```

## Notes
- `license` and `provider_contact` may be empty; all other fields must be present.
- Keep `category` and `format` consistent with existing entries so dashboard filters stay clean.
