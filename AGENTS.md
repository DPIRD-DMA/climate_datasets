# Repository Guidelines

## Project Structure & Module Organization
This repository is a lightweight catalog of climate datasets. The primary content lives in `README.md`, which contains the dataset table and reference links. There are no source code modules, build artifacts, or test suites in the current tree. If you add new materials, keep them close to the README (for example, `docs/` for longer notes or `data/` for sample files).

## Build, Test, and Development Commands
There are currently no build or runtime commands.
- `git status` to confirm what changed before committing.
- `rg "SILO|BOM|AGCD" README.md` to quickly locate entries when editing the table.

## Coding Style & Naming Conventions
- Markdown only. Use clear, sentence-case headers and keep table cells concise.
- Preserve the existing table columns and ordering when adding datasets.
- Link references go at the bottom of `README.md`, one per line, using the existing label style (e.g., `[DPIRD]: https://...`).

## Testing Guidelines
No automated tests are configured. Validate changes by reviewing the rendered Markdown (GitHub preview) and confirming all reference links resolve.

## Commit & Pull Request Guidelines
Recent commit messages are short, imperative-style summaries (e.g., “update DPIRD access”, “clean up table details”). Match this tone and keep messages under ~72 characters.
If you open a PR, include:
- A brief description of the dataset changes.
- Any access restrictions or credentials needed.
- Source links for new datasets and the rationale for inclusion.

## Data Curation Notes
- Prefer authoritative sources (government agencies, research institutions, official portals).
- Capture resolution, format, variables, method, access conditions, and temporal coverage in the table.
- If a dataset has special licensing or usage constraints, call them out explicitly.
