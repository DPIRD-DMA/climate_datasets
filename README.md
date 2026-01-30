# Climate Datasets

A curated catalog of climate and weather datasets, focused on accessibility and clear metadata.

## Dashboard
The interactive dashboard lives in `docs/index.html` and lets you filter by category, format, access conditions, and license.
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

See `CONTRIBUTING.md` for detailed guidance.

## Skills
The repository ships two Codex skills to streamline dataset edits:
- `add-dataset`: adds a dataset from a required JSON snippet (or interactive prompts).
- `update-dataset`: updates a dataset with fuzzy name matching.

To use them directly from the repo:
- `python skills/add-dataset/scripts/add_dataset.py` (paste JSON on stdin)
- `python skills/update-dataset/scripts/update_dataset.py --name "SILO"` (paste JSON on stdin)

After edits, run `make all` to sync the README and dashboard data.

## Dataset Catalog (Snapshot)
The table below is generated from `data/datasets.json`.

<!-- DATASET_TABLE_START -->
| Dataset | Resolution | Format | Variables | Method | Access Conditions | Temporal Coverage |
|---|---|---|---|---|---|---|
| [DPIRD][DPIRD] | station observations (~200 stations) | web, json, csv | Time series data - Evaporation, rainfall, solar radiation, air temperature, and others | Ad hoc handling of technical issues and missing values | API key registration | Minute to yearly intervals |
| [SILO (BOM)][SILO (BOM)] | station observations (~8000 stations) | web, json, csv, apsim | Continuous daily time series Evaporation, rainfall, solar radiation, air temperature, and others | Observational records or interpolated estimates for missing records | Accessible via SILO network | daily, from 1889 to current year |
| [SILO Gridded Data][SILO Gridded Data] | ~5 km² | NetCDF, GeoTiff | Evaporation, rainfall, solar radiation, air temperature, and others | Gridded daily climate surfaces derived either by splining or kriging the observational data | Valid email required | Daily, monthly, yearly |
| [ANUClimate 2.0][ANUClimate 2.0] | ~1 km² | NetCDF | Evaporation, rainfall, solar radiation, air temperature, and others | Derived from observational records, ANUSPLIN Version 4.6 spatial models | NCI account and membership of the research project | At least daily, from 1970 to present |
| [AGCD v1.0.1][AGCD v1.0.1] | ~1 km², ~5 km² | NetCDF | Rainfall, air temperature, vapour pressure | Consistent temporal and spatial analyses across Australia | NCI account and membership of the research project | Daily |
| [AGCD v2.0.2][AGCD v2.0.2] | ~1 km², ~5 km² | NetCDF | Monthly rainfall | Updated version of AGCD v1.0.1 | NCI account and membership of the research project | monthly, from 1900 to 2022 inclusive |
| [BOM Water Outlook][BOM Water Outlook] | ~5 km² | NetCDF | Precipitation, soil moisture, runoff, deep drainage and evapotranspiration | AWO is produced using a range of climate inputs, static grids and satellite observations as input into the Australian Water Resources Assessment Landscape model (AWRA-L) | NCI account and membership of the research project | daily gridded from 1911 until yesterday (historical), and water balance information, seasonal forecasts, and hydrological projections to 2100 |
| [Near surface air temperature][Near surface air temperature] | ~1 km² | GeoTiff | Hourly air temperature and air temperature climatologies | Near-surface (1.5 m) air temperature grids for Australia. These data are spatially interpolated using quart-variate thin plate splines (full spline dependence on easting, northing, elevation, and time-varying coastal distance index). | CSIRO Data Access Portal | hourly air temperature data from January 2015 and climatologies 1990-2019 (every 5th DOY) |
| [BARRA v2][BARRA v2] | ~11 km², ~22 km | NetCDF | Temperature, moisture, wind and flux variables at sub-surface, surface, and pressure levels, and heights above surface | BOM's higher resolution regional atmospheric reanalysis over Australia | NCI account and membership of the research project | sub-daily, daily and monthly, from 1979-present day |
| [CMIP6 QLD][CMIP6 QLD] | ~10 km², ~20 km | NetCDF | Evaporation, rainfall, solar radiation, air temperature, and others | Gridded climate surfaces derived from regional projection models (QLD-DEC) | NCI account and membership of the research project | hourly to monthly from several GCMs, historical (1970-2014) and SSP (2.6, 4.5, 7.0) |
| [Chelseaclim][Chelseaclim] | ~1 km² | GeoTIFF | Atmosphere, Air Temperature, Precipitation | Combines mechanistic and statistical downscaling of GCMs | CC BY 4.0, with credit to sources | 1979-01 to 2013-12 |
| [NASA POWER][NASA POWER] | ~111 km², ~55 km² x ~69 km² | NetCDF, AWS Bucket | Solar and meteorological data sets for support of renewable energy, building energy efficiency and agricultural needs | Derived from NASA research for renewable energy, building energy efficiency, and agricultural needs | Free and publicly accessible | Varies, includes near-real time |
| [WorldClim][WorldClim] | Up to ~1 km² | GeoTiff | Temperature, precipitation, solar radiation, wind speed, water vapour pressure, bioclimatic variables | Historical and future climate scenarios | Free for ecological modelling and GIS | 1970-2000 |
<!-- DATASET_TABLE_END -->

## Dataset References
<!-- DATASET_REFERENCES_START -->
[DPIRD]: https://www.agric.wa.gov.au/weather-api-20
[SILO (BOM)]: https://www.longpaddock.qld.gov.au/silo/point-data/
[SILO Gridded Data]: https://www.longpaddock.qld.gov.au/silo/gridded-data/
[ANUClimate 2.0]: https://geonetwork.nci.org.au/geonetwork/srv/eng/catalog.search#/metadata/f2576_7854_4065_1457
[AGCD v1.0.1]: https://geonetwork.nci.org.au/geonetwork/srv/eng/catalog.search#/metadata/f1801_8183_3094_1341
[AGCD v2.0.2]: https://geonetwork.nci.org.au/geonetwork/srv/eng/catalog.search#/metadata/f2506_1525_9066_1679
[BOM Water Outlook]: https://geonetwork.nci.org.au/geonetwork/srv/eng/catalog.search#/metadata/f6683_9441_8676_1139
[Near surface air temperature]: https://data.csiro.au/collection/csiro:60405
[BARRA v2]: https://geonetwork.nci.org.au/geonetwork/srv/eng/catalog.search#/metadata/f9057_2475_0540_0329
[CMIP6 QLD]: https://geonetwork.nci.org.au/geonetwork/srv/eng/catalog.search#/metadata/f2922_1827_1104_4111
[Chelseaclim]: https://chelsa-climate.org
[NASA POWER]: https://power.larc.nasa.gov
[WorldClim]: https://www.worldclim.org/data/worldclim21.html
<!-- DATASET_REFERENCES_END -->
