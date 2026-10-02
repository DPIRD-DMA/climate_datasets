#!/usr/bin/env python3
import json
import sys
from pathlib import Path

import registry

DATA_PATH = Path("data/datasets.json")


def main() -> int:
    if not DATA_PATH.exists():
        print("data/datasets.json not found.")
        return 1

    try:
        vocab = registry.load_vocab()
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Vocabulary error: {exc}")
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

        label = ds.get("name") or f"Entry {idx}"
        for message in registry.validate_entry(ds, vocab, require_complete=True):
            errors.append(f"{label}: {message}")

        name = ds.get("name", "")
        if name:
            names.append(name)

        fmt = ds.get("format", "")
        if isinstance(fmt, str) and "  " in fmt:
            errors.append(f"{label}: format contains double spaces.")

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
