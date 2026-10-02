# Repository Guidelines

## Project Structure & Module Organization
This repository is a catalog of climate datasets. `data/datasets.json` is the single source of truth.
- `data/datasets.json`: dataset registry (one object per dataset).
- `docs/`: static dashboard published to GitHub Pages (https://dpird-dma.github.io/climate_datasets/). `docs/data/datasets.json` is a generated copy of the registry.
- `README.md`: overview plus a generated preview of the first three registry entries, between the `DATASET_TABLE_*` and `DATASET_REFERENCES_*` markers. Do not edit inside the markers by hand.
- `scripts/`: README generation, dashboard sync, reference-label check, registry validation.
- `.agents/skills/`: repo-scoped `add-dataset` and `update-dataset` skills and their helper scripts.
- `tests/`: regression tests for the skill helper scripts.
- `audits/`: point-in-time audit reports.

## Build, Test, and Development Commands
- `make all`: regenerate the README preview, sync dashboard data, check reference labels, validate the registry, run the tests. Run it after every registry change.
- `make test`: run the helper-script tests only.
- `make preview`: serve `docs/` at http://localhost:8000.
- CI runs `make all` on every pull request and push to `main`, then fails if any generated file differs from what is committed. Commit the regenerated `README.md` and `docs/data/datasets.json` with your change.

## Editing the Registry
- Prefer the skill helpers over hand edits: `add_dataset.py` and `update_dataset.py` with `--dry-run` first. They validate fields, reject duplicates and write atomically.
- Required fields: `name`, `category`, `resolution`, `format`, `variables`, `method`, `access_conditions`, `temporal_coverage`, `spatial_domain`, `update_frequency`, `source_url`. Optional: `license`, `provider_contact`.
- Do not invent metadata. Every value should come from the provider's page, catalogue record or documentation.

## Coding Style & Naming Conventions
- Python scripts use the standard library only and need Python 3.10 or later. CI uses 3.11.
- Use clear, sentence-case headers in Markdown.
- `name` follows the provider's official naming.
- `resolution` is grid spacing, not area: `~5 km (0.05°)`. Use a station count for station data.
- `category` uses the values listed in `CONTRIBUTING.md`, so dashboard filters stay clean.

## Testing Guidelines
- `make all` must pass before a PR.
- `validate-datasets.py` checks structure and URL syntax only. It does not check that a URL resolves. Check new `source_url` values by hand.

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
