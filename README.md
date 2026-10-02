# Climate Datasets

A curated catalog of climate and weather datasets, focused on accessibility and clear metadata.

## Dashboard
Browse the full catalogue at **https://dpird-dma.github.io/climate_datasets/**. You can filter by category, format, access conditions and license.

The dashboard lives in `docs/` and is deployed to GitHub Pages on every push to `main`.
- Local preview: `make preview` then open `http://localhost:8000`
- Source of truth: `data/datasets.json` (synced to `docs/data/datasets.json`)

## Project Structure
- `data/datasets.json`: canonical dataset registry
- `.agents/skills/`: repo-scoped Codex workflows for safe dataset edits
- `docs/`: static dashboard (HTML/CSS/JS)
- `scripts/`: helpers for table generation and validation
- `tests/`: regression tests for dataset-editing helpers
- `README.md`: project overview + snapshot of the dataset table

## Contribution Workflow (Short)
1. Add or update entries in `data/datasets.json`, preferably with the skill helpers below.
2. Run `make all`. It regenerates the README preview, syncs the dashboard data, checks reference labels, validates the registry (structure and URL syntax) and runs the tests.
3. Commit the registry change with the regenerated files. CI fails if they are out of date.

See `CONTRIBUTING.md` for detailed guidance.

## Skills
The repository ships two repo-scoped skills under `.agents/skills/`:
- `add-dataset`: adds a dataset from a required JSON snippet (or interactive prompts).
- `update-dataset`: updates a dataset with fuzzy name matching.

To use them directly from the repo:
- `python3 .agents/skills/add-dataset/scripts/add_dataset.py --dry-run` (paste JSON on stdin)
- `python3 .agents/skills/update-dataset/scripts/update_dataset.py --name "SILO Point Data" --dry-run` (paste JSON on stdin)

## License
Catalogue content in this repository is licensed under [CC BY 4.0](LICENSE). The datasets listed here keep their own licences, given per entry in the `license` field.

## Dataset Catalog (Snapshot)
The table below is generated from `data/datasets.json` and previews the first three entries only. The full catalogue is on the [dashboard](https://dpird-dma.github.io/climate_datasets/).

<!-- DATASET_TABLE_START -->
| Dataset | Resolution | Format | Variables | Method | Access Conditions | Temporal Coverage |
|---|---|---|---|---|---|---|
| [DPIRD][DPIRD] | station observations (~200 stations) | web, json, csv | Time series data - Evaporation, rainfall, solar radiation, air temperature, and others | Ad hoc handling of technical issues and missing values | API key registration | Minute to yearly intervals |
| [SILO Point Data][SILO Point Data] | station observations (~8000 stations) | web, json, csv, apsim | Continuous daily time series Evaporation, rainfall, solar radiation, air temperature, and others | Observational records or interpolated estimates for missing records | Accessible via SILO network | daily, from 1889 to current year |
| [SILO Gridded Data][SILO Gridded Data] | ~5 km (0.05°) | NetCDF, GeoTiff | Evaporation, rainfall, solar radiation, air temperature, and others | Gridded daily climate surfaces derived either by splining or kriging the observational data | Free, open download from the AWS Public Data Program (no email or registration) | Daily and monthly, from 1889 to the current year (mean sea level pressure from 1957, Class A pan evaporation from 1970) |
<!-- DATASET_TABLE_END -->

## Dataset References
<!-- DATASET_REFERENCES_START -->
[DPIRD]: https://www.dpird.wa.gov.au/online-tools/apis/
[SILO Point Data]: https://www.longpaddock.qld.gov.au/silo/point-data/
[SILO Gridded Data]: https://www.longpaddock.qld.gov.au/silo/gridded-data/
<!-- DATASET_REFERENCES_END -->
