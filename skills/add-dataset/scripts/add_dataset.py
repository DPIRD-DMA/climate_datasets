#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

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

ALL_FIELDS = REQUIRED_FIELDS + OPTIONAL_FIELDS


def prompt_field(field, optional=False):
    label = f"{field}{' (optional)' if optional else ''}: "
    value = input(label).strip()
    return value


def load_dataset_from_input(path=None):
    if path:
        return json.loads(Path(path).read_text())
    raw = sys.stdin.read()
    if not raw.strip():
        raise ValueError("No JSON provided on stdin.")
    return json.loads(raw)


def validate_dataset(ds):
    missing = [field for field in REQUIRED_FIELDS if not ds.get(field)]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Add a dataset to data/datasets.json from JSON or interactive prompts."
    )
    parser.add_argument("--file", help="Path to JSON object file")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt for fields interactively",
    )
    parser.add_argument(
        "--sort",
        action="store_true",
        help="Sort datasets by name after adding",
    )
    args = parser.parse_args()

    if not DATA_PATH.exists():
        raise SystemExit("data/datasets.json not found. Run from repo root.")

    data = json.loads(DATA_PATH.read_text())
    datasets = data.get("datasets", [])

    if args.interactive:
        new_ds = {}
        for field in ALL_FIELDS:
            value = prompt_field(field, optional=field in OPTIONAL_FIELDS)
            if value:
                new_ds[field] = value
            else:
                new_ds[field] = ""
    else:
        new_ds = load_dataset_from_input(args.file)

    validate_dataset(new_ds)

    if any(ds.get("name") == new_ds.get("name") for ds in datasets):
        raise SystemExit(f"Dataset already exists: {new_ds.get('name')}")

    for field in ALL_FIELDS:
        new_ds.setdefault(field, "")

    datasets.append(new_ds)

    if args.sort:
        datasets.sort(key=lambda d: d.get("name", "").lower())

    DATA_PATH.write_text(json.dumps({"datasets": datasets}, indent=2))
    print(f"Added dataset: {new_ds.get('name')}")


if __name__ == "__main__":
    main()
