# Changelog

All notable changes to this repository are documented here.

## Unreleased
- Add dashboard in `docs/` powered by `data/datasets.json`.
- Add JSON-driven README snapshot generation and sync scripts.
- Add dataset validation, link checks, and Makefile workflow targets.
- Add CI checks and GitHub Pages deployment workflow.
- Add contributor guidance and Codex skills for add/update flows.
- Fix dashboard README button to point to the GitHub README.
- Move the add/update skills from `skills/` to `.agents/skills/`, harden the helpers (unknown-field and non-string rejection, case-insensitive duplicates, explicit fuzzy selection, atomic writes) and remove the packaged `skills/dist/*.skill` files.
- Add regression tests for the helper scripts (`tests/`, `make test`), included in `make all` and CI.
- Add datasets: BARRA-C2, BARPA-R, ERA5, ERA5-Land, SMAP L4 Soil Moisture (SPL4SMGP).
- Rename entries to provider naming: SILO Point Data (was SILO (BOM)), BOM Australian Water Outlook (AWRA-L), CSIRO hourly near-surface air temperature grids, BARRA-R2 and BARRA-RE2 (BARRA2), Queensland Future Climate 10 km CMIP6 projections, CHELSA V2.1.
- Give `resolution` as grid spacing (km and degrees) instead of area, across all entries.
- Fill licences from provider records, including CC BY-NC 4.0 (AGCD) and CC BY-SA 4.0 (ANUClimate 2.0, CSIRO temperature grids).
- Name BARRA2 gust (`wsgsmax`) and surface soil moisture (`mrsos`) variables, and update CHELSA temporal coverage to V2.1.
- Fix the DPIRD `source_url` (old agric.wa.gov.au link returned 404).
- Use `python3` in all Makefile targets.
- Update `AGENTS.md`, `CONTRIBUTING.md` and `README.md` to match the JSON-registry workflow, and link the live dashboard.
- Add a CC BY 4.0 `LICENSE` for catalogue content.
- Add controlled structured fields to every entry: `access_types`, `formats`, `timesteps`, `variable_tags`, `resolution_km`, `station_count` (station data only), `start_year`, `end_year`, `domain` and `last_checked`. The descriptive text fields are unchanged.
- Add `data/vocab.json` for the allowed values and their display order, and `scripts/registry.py` for the shared field definitions and validation. The validator and both skill helpers now use them, and the helpers accept lists, numbers and null.
- Backfill all 18 entries from provider pages, NCI GeoNetwork and NCI THREDDS. Correct AGCD v2.0.2 coverage (to 2023), SILO Gridded access and time steps, Queensland 10 km domain, start year and scenarios, and CHELSA V2.1 licence (CC0 1.0). Name NCI project codes and open THREDDS access for ANUClimate, AGCD, AWO, Queensland and BARRA2. Add 20-minute and 3-hourly time steps to BARRA-C2 coverage.
- Rework the dashboard: compact rows with expandable details, licence badges that flag non-commercial and share-alike terms, and cards below 720 px. Filters for variable, time step, domain, access type, format, licence, category and grid spacing, sorting by name, resolution or start year, and filter state in the URL. A smaller hero and a footer showing when entries were last checked.
- Build dashboard rows with DOM methods instead of `innerHTML`, and copy `data/vocab.json` to `docs/data/` in `make sync`.
