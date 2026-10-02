---
name: add-dataset
description: Add a climate dataset to data/datasets.json in the climate_datasets repository, then regenerate and validate the README and dashboard. Use only when working in this repository. Do not use for datasets in other projects.
---

# Add Dataset

Use this repo-scoped skill only from the `climate_datasets` repository root.

## Workflow

1. Confirm `data/datasets.json` and `.agents/skills/add-dataset/scripts/add_dataset.py` exist.
2. Check `git status --short` and preserve unrelated work.
3. Obtain a complete dataset object from the user. Do not invent metadata.
4. Run the helper with `--dry-run` first and inspect the proposed object.
5. Run it again without `--dry-run` only after the proposal is sound.
6. Run `make all` to regenerate the README, sync dashboard data, and validate the registry.
7. Review `git diff`; never commit for the user.

## Add From JSON

```bash
python3 .agents/skills/add-dataset/scripts/add_dataset.py --dry-run <<'JSON'
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
  "source_url": "https://...",
  "access_types": ["Open"],
  "formats": ["NetCDF"],
  "timesteps": ["daily"],
  "variable_tags": ["rainfall"],
  "resolution_km": 5,
  "start_year": 1900,
  "end_year": null,
  "domain": "Australia",
  "last_checked": "2026-10-02"
}
JSON
```

After reviewing the output, repeat without `--dry-run`.

Interactive entry is also available:

```bash
python3 .agents/skills/add-dataset/scripts/add_dataset.py --interactive --dry-run
```

## Guardrails

- Required text fields must be non-empty strings. Optional fields are `license`, `provider_contact` and `station_count`.
- Structured fields are JSON lists, numbers, `null` or ISO dates, not strings. List values and `domain` must come from `data/vocab.json`. `CONTRIBUTING.md` has the field table.
- Set `last_checked` only for a dataset verified against the provider. Do not invent values.
- Unknown fields, values outside the vocabulary and case-insensitive duplicate names are rejected.
- The helper preserves all top-level registry keys and writes atomically.
- Existing output is never changed by `--dry-run`.

