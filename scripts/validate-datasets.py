#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

DATA_PATH = Path("data/datasets.json")

REQUIRED_FIELDS = [
    "name",
    "category",
    "resolution",
    "format",
    "variables",
    "method",
    "access_conditions",
    "temporal_coverage",
    "spatial_domain",
    "update_frequency",
    "source_url",
]

OPTIONAL_FIELDS = ["license", "provider_contact"]


def is_valid_url(value: str) -> bool:
    if not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def main() -> int:
    if not DATA_PATH.exists():
        print("data/datasets.json not found.")
        return 1

    data = json.loads(DATA_PATH.read_text())
    datasets = data.get("datasets")
    if not isinstance(datasets, list):
        print("datasets must be a list.")
        return 1

    errors = []
    names = []

    for idx, ds in enumerate(datasets, start=1):
        if not isinstance(ds, dict):
            errors.append(f"Entry {idx} is not an object.")
            continue

        for field in REQUIRED_FIELDS:
            if not ds.get(field):
                errors.append(f"{ds.get('name', f'Entry {idx}')}: missing {field}.")

        name = ds.get("name", "")
        if name:
            names.append(name)

        url = ds.get("source_url", "")
        if url and not is_valid_url(url):
            errors.append(f"{name or f'Entry {idx}'}: invalid source_url '{url}'.")

        fmt = ds.get("format", "")
        if isinstance(fmt, str) and "  " in fmt:
            errors.append(f"{name or f'Entry {idx}'}: format contains double spaces.")

    dupes = sorted({n for n in names if names.count(n) > 1})
    for name in dupes:
        errors.append(f"Duplicate dataset name: {name}")

    if errors:
        print("Dataset validation errors:")
        for err in errors:
            print(f"- {err}")
        return 1

    print("Dataset validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
