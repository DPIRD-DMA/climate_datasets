#!/usr/bin/env python3
import argparse
import difflib
import json
import os
import stat
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[4] / "scripts"))
import registry  # noqa: E402

DEFAULT_DATA_PATH = Path("data/datasets.json")
ALL_FIELDS = registry.ALL_FIELDS


def load_object_from_input(path: str | None = None) -> dict:
    raw = Path(path).read_text(encoding="utf-8") if path else sys.stdin.read()
    if not raw.strip():
        raise ValueError("No JSON object provided.")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("Updates must be a JSON object.")
    return value


def load_registry(path: Path) -> tuple[dict, list[dict]]:
    if not path.is_file():
        raise ValueError(f"Registry not found: {path}. Run from the repository root.")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("Registry root must be a JSON object.")
    datasets = data.get("datasets")
    if not isinstance(datasets, list):
        raise ValueError("Registry key 'datasets' must be a list.")
    if not all(isinstance(item, dict) for item in datasets):
        raise ValueError("Every dataset entry must be a JSON object.")
    return data, datasets


def validate_fields(value: dict, require_complete: bool) -> None:
    errors = registry.validate_entry(value, registry.load_vocab(), require_complete)
    if errors:
        raise ValueError("; ".join(errors))


def prompt_update(current: dict) -> dict:
    updates: dict = {}
    for field in ALL_FIELDS:
        value = input(f"{field} [{current.get(field, '')}]: ").strip()
        if value:
            updates[field] = registry.parse_text(field, value)
    return updates


def match_candidates(datasets: list[dict], query: str) -> tuple[int | None, list[int]]:
    names = [item.get("name", "") for item in datasets]
    folded = [name.casefold() for name in names]
    query_folded = query.casefold()
    if query_folded in folded:
        return folded.index(query_folded), []
    close = difflib.get_close_matches(query_folded, folded, n=5, cutoff=0.3)
    indexes = [folded.index(name) for name in close]
    return None, indexes


def choose_dataset(
    datasets: list[dict], query: str, selection: int | None, interactive: bool
) -> int:
    exact, candidates = match_candidates(datasets, query)
    if exact is not None:
        return exact
    if not candidates:
        raise ValueError(f"No close matches found for: {query}")

    if selection is not None:
        if selection < 1 or selection > len(candidates):
            raise ValueError(f"Selection must be between 1 and {len(candidates)}.")
        return candidates[selection - 1]

    if interactive:
        print("Select a dataset to update:")
        for number, index in enumerate(candidates, start=1):
            print(f"{number}. {datasets[index].get('name', '')}")
        choice = input("Enter number: ").strip()
        if not choice.isdigit() or not 1 <= int(choice) <= len(candidates):
            raise ValueError("Invalid selection.")
        return candidates[int(choice) - 1]

    choices = ", ".join(
        f"{number}={datasets[index].get('name', '')}"
        for number, index in enumerate(candidates, start=1)
    )
    raise ValueError(f"Fuzzy matches: {choices}. Re-run with --select N or --interactive.")


def write_registry_atomic(path: Path, data: dict) -> None:
    payload = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    original_mode = stat.S_IMODE(path.stat().st_mode)
    temp_name: str | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
            temp_name = handle.name
        os.chmod(temp_name, original_mode)
        os.replace(temp_name, path)
    finally:
        if temp_name and Path(temp_name).exists():
            Path(temp_name).unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description="Update the climate dataset registry.")
    parser.add_argument("--name", required=True, help="Dataset name or fuzzy query")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--file", help="Path to a JSON object with updates")
    source.add_argument("--interactive", action="store_true", help="Prompt for fields")
    parser.add_argument("--replace", action="store_true", help="Require and use a full object")
    parser.add_argument("--select", type=int, help="Select a displayed fuzzy match (1-based)")
    parser.add_argument("--sort", action="store_true", help="Sort datasets by name")
    parser.add_argument("--dry-run", action="store_true", help="Validate and print without writing")
    parser.add_argument(
        "--data-path",
        type=Path,
        default=DEFAULT_DATA_PATH,
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()

    try:
        data, datasets = load_registry(args.data_path)
        index = choose_dataset(datasets, args.name, args.select, args.interactive)
        current = datasets[index]
        updates = prompt_update(current) if args.interactive else load_object_from_input(args.file)
        if not updates:
            raise ValueError("No updates provided.")
        validate_fields(updates, require_complete=args.replace)

        if args.replace:
            proposed = dict(updates)
            for field in registry.STRING_OPTIONAL:
                proposed.setdefault(field, "")
        else:
            proposed = {**current, **updates}
        validate_fields(proposed, require_complete=True)

        proposed_name = proposed["name"].casefold()
        if any(
            other_index != index and item.get("name", "").casefold() == proposed_name
            for other_index, item in enumerate(datasets)
        ):
            raise ValueError(f"Dataset name already exists: {proposed['name']}")

        datasets[index] = proposed
        if args.sort:
            datasets.sort(key=lambda item: item.get("name", "").casefold())

        if args.dry_run:
            print(json.dumps(proposed, indent=2, ensure_ascii=False))
            print("Dry run: registry not changed.", file=sys.stderr)
            return 0

        write_registry_atomic(args.data_path, data)
        print(f"Updated dataset: {proposed['name']}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
