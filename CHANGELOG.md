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
