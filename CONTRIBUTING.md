# Contributing Guide

Thanks for helping maintain the climate datasets catalog. This repo is documentation-first, with a JSON registry as the single source of truth.

## Quick Start
1. Add or update an entry in `data/datasets.json`, preferably with the helper scripts (see Skills below).
2. Run `make all`. It regenerates the README preview, syncs `docs/data/datasets.json`, checks README reference labels, validates the registry and runs the tests.
3. Commit the registry change together with the regenerated `README.md` and `docs/data/datasets.json`. CI fails if generated files are out of date.

The validator checks structure and URL syntax only. Open each new `source_url` to confirm it resolves.

## Skills
Two repo-scoped skills live under `.agents/skills/`, and their scripts can be run directly:
- Add: `python3 .agents/skills/add-dataset/scripts/add_dataset.py --dry-run` with the JSON object on stdin. Repeat without `--dry-run` once the output looks right.
- Update: `python3 .agents/skills/update-dataset/scripts/update_dataset.py --name "SILO Point Data" --dry-run` with only the changed fields on stdin. Fuzzy name matches need `--select N`.

Both reject unknown fields, empty required fields, non-string values, invalid URLs and duplicate names (case-insensitive).

## Dataset Entry Template
Add one object per dataset:

```json
{
  "name": "Dataset name",
  "category": "Station observations | Gridded products | Reanalysis | Climate projections | Climate scenarios | Hydrological modeling | Derived products",
  "resolution": "~5 km (0.05°) grid spacing, or station count",
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
- Keep `name` consistent with the provider's official naming.
- Give `resolution` as grid spacing in km with degrees where the provider states them, for example `~12 km (0.11°)`. Not as area (km²).
- Use sentence case for descriptions and avoid long paragraphs.
- Keep `format` and `category` values consistent so filters stay clean.

## Access & Licensing Notes
- If access requires credentials, state it explicitly in `access_conditions`.
- Fill `license` with the provider's stated licence. Call out non-commercial (`CC BY-NC`) and share-alike (`CC BY-SA`) terms, because they restrict reuse.
- Leave `license` empty if the provider does not state one.

## Updating Existing Entries
- Use the update helper, or edit the JSON entry directly and run `make all`.
- Changing a dataset `name` also changes its generated README reference label.

## Questions or Proposals
Open a PR with a short rationale and sources for any new dataset.
