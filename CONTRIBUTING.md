# Contributing Guide

Thanks for helping maintain the climate datasets catalog. This repo is documentation-first, with a JSON registry as the single source of truth.

## Quick Start
1. Edit `data/datasets.json`.
2. Run `scripts/generate-readme-table.py` to refresh the README snapshot.
3. Run `scripts/sync-dashboard-data.py` to update `docs/data/datasets.json`.
4. Run `scripts/check-reference-labels.py` to confirm references.
5. Run `scripts/validate-datasets.py` to validate JSON structure and URLs.

## Dataset Entry Template
Add one object per dataset:

```json
{
  "name": "Dataset name",
  "category": "Station observations | Gridded products | Reanalysis | Climate projections | Climate scenarios | Hydrological modeling | Derived products",
  "resolution": "~1 km² or station count",
  "format": "NetCDF, GeoTiff, CSV",
  "variables": "Key variables",
  "method": "Short methodology summary",
  "access_conditions": "Free, API key, NCI account, etc.",
  "temporal_coverage": "Daily, monthly, years",
  "spatial_domain": "Australia | Global | region",
  "update_frequency": "Daily | Monthly | Varies",
  "license": "CC BY 4.0 | other (optional)",
  "provider_contact": "Optional",
  "source_url": "https://..."
}
```

## Naming & Style
- Keep `name` consistent with the provider’s official naming.
- Use sentence case for descriptions and avoid long paragraphs.
- Keep `format` and `category` values consistent so filters stay clean.

## Access & Licensing Notes
- If access requires credentials, state it explicitly in `access_conditions`.
- If there are licensing constraints, fill `license` and mention any attribution requirements.

## Updating Existing Entries
- Edit the JSON entry directly and keep the table in README in sync via the script.
- If you change the dataset name, the generated reference labels in README will change too.

## Questions or Proposals
Open a PR with a short rationale and sources for any new dataset.
