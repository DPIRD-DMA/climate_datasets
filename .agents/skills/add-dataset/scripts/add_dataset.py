#!/usr/bin/env python3
import argparse
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
OPTIONAL_FIELDS = registry.OPTIONAL_FIELDS


def prompt_field(field: str, optional: bool = False) -> str:
    label = f"{field}{' (optional)' if optional else ''}: "
    return input(label).strip()


def load_object_from_input(path: str | None = None) -> dict:
    raw = Path(path).read_text(encoding="utf-8") if path else sys.stdin.read()
    if not raw.strip():
        raise ValueError("No JSON object provided.")
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("Dataset input must be a JSON object.")
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


def validate_dataset(dataset: dict) -> None:
    errors = registry.validate_entry(dataset, registry.load_vocab(), require_complete=True)
    if errors:
        raise ValueError("; ".join(errors))


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
    parser = argparse.ArgumentParser(description="Add a dataset to the climate dataset registry.")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--file", help="Path to a JSON object file")
    source.add_argument("--interactive", action="store_true", help="Prompt for fields")
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
        if args.interactive:
            new_dataset = {}
            for field in ALL_FIELDS:
                text = prompt_field(field, optional=field in OPTIONAL_FIELDS)
                if text or field in registry.STRING_FIELDS:
                    new_dataset[field] = registry.parse_text(field, text)
        else:
            new_dataset = load_object_from_input(args.file)

        for field in registry.STRING_OPTIONAL:
            new_dataset.setdefault(field, "")
        validate_dataset(new_dataset)

        wanted_name = new_dataset["name"].casefold()
        if any(item.get("name", "").casefold() == wanted_name for item in datasets):
            raise ValueError(f"Dataset already exists: {new_dataset['name']}")

        datasets.append(new_dataset)
        if args.sort:
            datasets.sort(key=lambda item: item.get("name", "").casefold())

        if args.dry_run:
            print(json.dumps(new_dataset, indent=2, ensure_ascii=False))
            print("Dry run: registry not changed.", file=sys.stderr)
            return 0

        write_registry_atomic(args.data_path, data)
        print(f"Added dataset: {new_dataset['name']}")
        return 0
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
