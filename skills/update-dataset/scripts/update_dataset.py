#!/usr/bin/env python3
import argparse
import difflib
import json
import sys
from pathlib import Path

DATA_PATH = Path("data/datasets.json")

FIELDS = [
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
    "license",
    "provider_contact",
    "source_url",
]


def load_dataset_from_input(path=None):
    if path:
        return json.loads(Path(path).read_text())
    raw = sys.stdin.read()
    if not raw.strip():
        raise ValueError("No JSON provided on stdin.")
    return json.loads(raw)


def prompt_update(current):
    updated = {}
    for field in FIELDS:
        current_value = current.get(field, "")
        prompt = f"{field} [{current_value}]: "
        value = input(prompt).strip()
        if value:
            updated[field] = value
    return updated


def choose_dataset(datasets, name_query, selection=None, interactive=False):
    names = [ds.get("name", "") for ds in datasets]
    if name_query in names:
        return names.index(name_query)

    matches = difflib.get_close_matches(name_query, names, n=5, cutoff=0.3)
    if not matches:
        raise SystemExit(f"No close matches found for: {name_query}")

    if selection is not None:
        try:
            idx = names.index(matches[selection - 1])
            return idx
        except (IndexError, ValueError):
            raise SystemExit("Invalid selection index.")

    if interactive:
        print("Select a dataset to update:")
        for i, match in enumerate(matches, start=1):
            print(f"{i}. {match}")
        choice = input("Enter number: ").strip()
        if not choice.isdigit():
            raise SystemExit("Invalid selection.")
        choice_idx = int(choice)
        if choice_idx < 1 or choice_idx > len(matches):
            raise SystemExit("Selection out of range.")
        return names.index(matches[choice_idx - 1])

    raise SystemExit(
        "Multiple close matches found. Re-run with --select N or --interactive."
    )


def main():
    parser = argparse.ArgumentParser(
        description="Update a dataset in data/datasets.json with fuzzy name matching."
    )
    parser.add_argument("--name", required=True, help="Dataset name or query")
    parser.add_argument("--file", help="Path to JSON object with updates")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Prompt for fields interactively",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace the entire dataset object with provided JSON",
    )
    parser.add_argument(
        "--select",
        type=int,
        help="Select a match index when multiple close matches are found (1-based)",
    )
    parser.add_argument(
        "--sort",
        action="store_true",
        help="Sort datasets by name after updating",
    )

    args = parser.parse_args()

    if not DATA_PATH.exists():
        raise SystemExit("data/datasets.json not found. Run from repo root.")

    data = json.loads(DATA_PATH.read_text())
    datasets = data.get("datasets", [])

    idx = choose_dataset(datasets, args.name, args.select, args.interactive)
    current = datasets[idx]

    updates = {}
    if args.interactive:
        updates.update(prompt_update(current))

    if args.file or not args.interactive:
        if args.file:
            updates.update(load_dataset_from_input(args.file))
        elif not args.interactive:
            updates.update(load_dataset_from_input())

    if not updates:
        raise SystemExit("No updates provided.")

    if args.replace:
        new_obj = updates
    else:
        new_obj = {**current, **updates}

    new_name = new_obj.get("name", current.get("name"))
    if new_name != current.get("name"):
        if any(ds.get("name") == new_name for ds in datasets):
            raise SystemExit(f"Dataset name already exists: {new_name}")

    datasets[idx] = new_obj

    if args.sort:
        datasets.sort(key=lambda d: d.get("name", "").lower())

    DATA_PATH.write_text(json.dumps({"datasets": datasets}, indent=2))
    print(f"Updated dataset: {new_obj.get('name')}")


if __name__ == "__main__":
    main()
