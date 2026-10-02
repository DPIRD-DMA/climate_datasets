# Repository Guidelines

## Project Structure & Module Organization
This repository is a catalog of climate datasets. `data/datasets.json` is the single source of truth.
- `data/datasets.json`: dataset registry (one object per dataset).
- `data/vocab.json`: allowed values and display order for the structured fields. The validator, the helpers and the dashboard all read it.
- `docs/`: static dashboard published to GitHub Pages (https://dpird-dma.github.io/climate_datasets/). `docs/data/datasets.json` and `docs/data/vocab.json` are generated copies.
- `README.md`: overview plus a generated preview of the first three registry entries, between the `DATASET_TABLE_*` and `DATASET_REFERENCES_*` markers. Do not edit inside the markers by hand.
- `scripts/`: README generation, dashboard sync, reference-label check, registry validation. `scripts/registry.py` holds the field definitions and validation shared by the validator and both helpers.
- `.agents/skills/`: repo-scoped `add-dataset` and `update-dataset` skills and their helper scripts.
- `tests/`: regression tests for the skill helper scripts.
- `audits/`: point-in-time audit reports.

## Build, Test, and Development Commands
- `make all`: regenerate the README preview, sync dashboard data, check reference labels, validate the registry, run the tests. Run it after every registry change.
- `make test`: run the helper-script tests only.
- `make preview`: serve `docs/` at http://localhost:8000.
- CI runs `make all` on every pull request and push to `main`, then fails if any generated file differs from what is committed. Commit the regenerated `README.md`, `docs/data/datasets.json` and `docs/data/vocab.json` with your change.

## Editing the Registry
- Prefer the skill helpers over hand edits: `add_dataset.py` and `update_dataset.py` with `--dry-run` first. They validate fields, reject duplicates and write atomically.
- Required fields: `name`, `category`, `resolution`, `format`, `variables`, `method`, `access_conditions`, `temporal_coverage`, `spatial_domain`, `update_frequency`, `source_url`, plus the structured fields `access_types`, `formats`, `timesteps`, `variable_tags`, `resolution_km`, `start_year`, `end_year`, `domain` and `last_checked`. Optional: `license`, `provider_contact`, `station_count`.
- Structured fields are JSON lists and numbers, not strings. List values and `domain` must come from `data/vocab.json`. Extend the vocabulary there only. `CONTRIBUTING.md` has the field table.
- Do not invent metadata. Every value should come from the provider's page, catalogue record or documentation.
- Set `last_checked` only on entries you verified against the provider.

## Coding Style & Naming Conventions
- Python scripts use the standard library only and need Python 3.10 or later. CI uses 3.11.
- Use clear, sentence-case headers in Markdown.
- `name` follows the provider's official naming.
- `resolution` is grid spacing, not area: `~5 km (0.05°)`. Use a station count for station data.
- `category` uses the values listed in `CONTRIBUTING.md`, so dashboard filters stay clean.
- `resolution_km` is the finest grid spacing. Keep the other grids in the `resolution` prose.

## Testing Guidelines
- `make all` must pass before a PR.
- `validate-datasets.py` checks structure, field types, vocabulary values and URL syntax. It does not check that a URL resolves or that a value matches the provider. Check new `source_url` values and structured values by hand.

## Commit & Pull Request Guidelines
Recent commit messages are short, imperative-style summaries (e.g., "update DPIRD access", "clean up table details"). Keep them under ~72 characters.
A PR should include:
- A brief description of the dataset changes.
- Any access restrictions or credentials needed.
- Source links for new datasets and the rationale for inclusion.

## Data Curation Notes
- Prefer authoritative sources (government agencies, research institutions, official portals).
- State non-commercial (`CC BY-NC`) and share-alike (`CC BY-SA`) licences explicitly in `license`. They restrict downstream use.
- Leave `license` empty when the provider does not state one, rather than guessing.
