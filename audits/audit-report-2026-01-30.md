# Audit Report - 2026-01-30

## Assumptions
- Repository scope is documentation-only at present, with `README.md` as the primary artifact.
- No hidden build scripts, tests, or tooling exist beyond what is visible in the repo root.
- The goal is to streamline dataset additions/updates and improve presentation/UX of the dataset table.

## Scope
- In scope: `README.md` dataset table structure, link management, contributor workflow for adding/updating entries, overall presentation.
- Out of scope: External data sources/availability, dataset accuracy verification, and any downstream consumers of this catalog.

## Verification Status
- Static review only (no rendering tools or link checks executed).

## Findings
### Critical
- None observed in the current scope.

### High
- None observed in the current scope.

### Medium
- **No standardized contribution workflow for adding/updating datasets** (Area: Bug/UI-UX)
  - Evidence: Only `README.md` exists; no contributor guide, template, or process file before this audit. Adding entries is manual.
  - Impact: Inconsistent entries, higher chance of omissions (e.g., access conditions or temporal coverage), and slower updates.
  - Conditions/Works when: Works when contributors follow implicit conventions by reading prior rows.
  - Non-happy-path cases: New contributors add rows with missing columns, inconsistent units, or unlinked references.
  - Verification status: Static review only.
  - Recommendation: Add a short, explicit “How to add/update a dataset” checklist and a row template section in `README.md` or a separate `CONTRIBUTING.md`.

- **Single large table reduces scanability and onboarding** (Area: UI-UX)
  - Evidence: One wide table with many columns and varied dataset types.
  - Impact: Harder to compare similar datasets; potential horizontal scrolling on smaller screens.
  - Conditions/Works when: Works when readers use desktop screens and are already familiar with dataset names.
  - Non-happy-path cases: Mobile or narrow screens; users looking for a subset (e.g., gridded vs. station data).
  - Verification status: Static review only.
  - Recommendation: Split the table into categories (e.g., Station Observations, Gridded Products, Reanalysis/Projections) and add a short summary or index at the top.

### Low
- **Link reference consistency may drift over time** (Area: Bug/UX)
  - Evidence: Reference links are all defined at the bottom; no guidance for naming conventions beyond implicit labels.
  - Impact: Inconsistent labels or missing references make entries harder to maintain.
  - Conditions/Works when: Works when contributors always add link references and keep labels aligned with table names.
  - Non-happy-path cases: A row includes a label that isn’t defined in the reference list.
  - Verification status: Static review only.
  - Recommendation: Add a quick validation checklist item (“Verify all reference labels exist at the bottom of README”).

## UI/UX Opportunities (if not covered above)
- Add a brief “Quick Filters” section (e.g., “Use your editor search for `NetCDF`, `GeoTiff`, or `API key`”).
- Provide a compact legend for abbreviations (e.g., BOM, NCI, AWRA-L) to reduce cognitive load for new users.
- Consider a secondary table focused on access conditions (free, registration, NCI membership) for faster decision-making.

## Unverified / Needs Follow-up
- Confirm whether any scripts or data directories exist outside the repo root (not inspected).
- Check whether GitHub renders the large table well on mobile and whether split tables improve readability.

## Next Steps
- Add a contributor checklist + row template to `README.md` or a new `CONTRIBUTING.md`.
- Consider categorizing the dataset table by type and adding a short index.
- Optionally add a lightweight link check script or manual checklist to prevent broken reference labels.
