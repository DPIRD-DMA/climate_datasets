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

Both validate against `scripts/registry.py` and `data/vocab.json`. They reject unknown fields, missing required fields, wrong value types, values outside the vocabulary, invalid URLs and duplicate names (case-insensitive). Structured values go in as real JSON lists and numbers, for example `"timesteps": ["hourly", "daily"]` and `"resolution_km": 4.4`.

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
  "access_conditions": "Free, API key, NCI project, etc.",
  "temporal_coverage": "Daily, monthly, years",
  "spatial_domain": "Australia | Global | region",
  "update_frequency": "Daily | Monthly | Varies",
  "license": "CC BY 4.0 | other (optional)",
  "provider_contact": "Optional",
  "source_url": "https://...",

  "access_types": ["Open", "NCI project"],
  "formats": ["NetCDF"],
  "timesteps": ["hourly", "daily"],
  "variable_tags": ["rainfall", "temperature"],
  "resolution_km": 5,
  "station_count": 200,
  "start_year": 1979,
  "end_year": null,
  "domain": "Australia",
  "last_checked": "2026-10-02"
}
```

The descriptive strings are for people reading an entry. The structured fields below drive the dashboard filters and sorting. Keep them consistent with the prose.

## Structured fields
| Field | Type | Rule |
|---|---|---|
| `access_types` | list | Values from `data/vocab.json`. List every route, for example Open and NCI project. |
| `formats` | list | Values from `data/vocab.json`. |
| `timesteps` | list | Values from `data/vocab.json`. List every time step the provider offers. |
| `variable_tags` | list | Values from `data/vocab.json`. Tag only variables the provider documents. |
| `resolution_km` | number or null | Finest grid spacing in km. Use null for station data. |
| `station_count` | integer | Optional. Station data only. |
| `start_year` | integer | Earliest year of any variable in the product. |
| `end_year` | integer or null | Last year covered. Null means ongoing. |
| `domain` | string | One value from `data/vocab.json`. The dashboard matches it exactly. |
| `last_checked` | date | ISO date (`YYYY-MM-DD`) on which you verified the entry against the provider. |

All of these except `station_count` are required. Lists must not be empty or contain duplicates, and `end_year` cannot be earlier than `start_year`.

### Access types
- `Open`: downloadable without an account. Providing an email address does not count as an account.
- `Free registration`: needs a free account or login.
- `API key`: needs a key issued by the provider.
- `NCI project`: needs membership of an NCI project. Also list `Open` when the same data is open on NCI THREDDS, and name the project code in `access_conditions`.

### Extending the vocabulary
`data/vocab.json` holds the allowed values and their display order. It is the only place values are defined. Add a value only when an entry needs it, put it where it should appear in the dashboard, then run `make all`. The dashboard hides values that no entry uses.

## Naming & Style
- Keep `name` consistent with the provider's official naming.
- Give `resolution` as grid spacing in km with degrees where the provider states them, for example `~12 km (0.11°)`. Not as area (km²).
- Use sentence case for descriptions and avoid long paragraphs.
- Keep `category` values consistent so filters stay clean. For `format`, `timesteps` and the other structured fields, use the values in `data/vocab.json`.

## Access & Licensing Notes
- If access requires credentials, state it explicitly in `access_conditions` and set `access_types` to match.
- Fill `license` with the provider's stated licence. Call out non-commercial (`CC BY-NC`) and share-alike (`CC BY-SA`) terms, because they restrict reuse.
- Leave `license` empty if the provider does not state one.

## Verifying values
- Take every value from the provider's page, catalogue record or documentation. Do not infer it.
- Set `last_checked` only for entries you checked. Update it whenever you re-verify an entry.
- Check that `source_url` resolves. The validator checks syntax only.

## Updating Existing Entries
- Use the update helper, or edit the JSON entry directly and run `make all`.
- Changing a dataset `name` also changes its generated README reference label.

## Questions or Proposals
Open a PR with a short rationale and sources for any new dataset.
