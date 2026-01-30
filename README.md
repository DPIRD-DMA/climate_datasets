# Climate Datasets

A curated catalog of climate and weather datasets, focused on accessibility and clear metadata.

## Dashboard
The interactive dashboard lives in `docs/index.html` and lets you filter by category, format, access conditions, and license. It is published via GitHub Pages from the `docs/` directory.
- Local preview: `python -m http.server -d docs 8000` then open `http://localhost:8000`
- Source of truth: `data/datasets.json` (synced to `docs/data/datasets.json`)

## Project Structure
- `data/datasets.json`: canonical dataset registry
- `docs/`: static dashboard (HTML/CSS/JS)
- `scripts/`: helpers for table generation and validation
- `README.md`: project overview + snapshot of the dataset table

## Contribution Workflow (Short)
1. Update or add entries in `data/datasets.json`.
2. Run `scripts/generate-readme-table.py` to refresh the README snapshot.
3. Run `scripts/sync-dashboard-data.py` to update the dashboard data.
4. Run `scripts/check-reference-labels.py` to confirm link references.
5. Run `scripts/validate-datasets.py` to validate JSON structure and URLs.

See `CONTRIBUTING.md` for detailed guidance.

## Skills
The repository ships two Codex skills to streamline dataset edits:
- `add-dataset`: adds a dataset from a required JSON snippet (or interactive prompts).
- `update-dataset`: updates a dataset with fuzzy name matching.

To use them directly from the repo:
- `python skills/add-dataset/scripts/add_dataset.py` (paste JSON on stdin)
- `python skills/update-dataset/scripts/update_dataset.py --name "SILO"` (paste JSON on stdin)

After edits, run `make all` to sync the README, dashboard data, and validations.

## Dataset Catalog (Snapshot)
The table below is generated from `data/datasets.json`.

<!-- DATASET_TABLE_START -->
| Dataset | Resolution | Format | Variables | Method | Access Conditions | Temporal Coverage |
|---|---|---|---|---|---|---|
| [DPIRD][DPIRD] | station observations (~200 stations) | web, json, csv | Time series data - Evaporation, rainfall, solar radiation, air temperature, and others | Ad hoc handling of technical issues and missing values | API key registration | Minute to yearly intervals |
| [SILO (BOM)][SILO (BOM)] | station observations (~8000 stations) | web, json, csv, apsim | Continuous daily time series Evaporation, rainfall, solar radiation, air temperature, and others | Observational records or interpolated estimates for missing records | Accessible via SILO network | daily, from 1889 to current year |
| [SILO Gridded Data][SILO Gridded Data] | ~5 km² | NetCDF, GeoTiff | Evaporation, rainfall, solar radiation, air temperature, and others | Gridded daily climate surfaces derived either by splining or kriging the observational data | Valid email required | Daily, monthly, yearly |
<!-- DATASET_TABLE_END -->

## Dataset References
<!-- DATASET_REFERENCES_START -->
[DPIRD]: https://www.agric.wa.gov.au/weather-api-20
[SILO (BOM)]: https://www.longpaddock.qld.gov.au/silo/point-data/
[SILO Gridded Data]: https://www.longpaddock.qld.gov.au/silo/gridded-data/
<!-- DATASET_REFERENCES_END -->
