"""Field definitions and validation shared by the validator and the skill helpers."""
import json
import math
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
VOCAB_PATH = REPO_ROOT / "data" / "vocab.json"

STRING_REQUIRED = [
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
STRING_OPTIONAL = ["license", "provider_contact"]
STRING_FIELDS = STRING_REQUIRED + STRING_OPTIONAL

# Structured fields. List fields and `domain` take their values from data/vocab.json,
# keyed by field name.
LIST_FIELDS = ["access_types", "formats", "timesteps", "variable_tags"]
NUMBER_FIELDS = ["resolution_km"]
INT_FIELDS = ["station_count", "start_year", "end_year"]
ENUM_FIELDS = ["domain"]
DATE_FIELDS = ["last_checked"]
NULLABLE_FIELDS = ["resolution_km", "station_count", "end_year"]
STRUCTURED_FIELDS = LIST_FIELDS + NUMBER_FIELDS + INT_FIELDS + ENUM_FIELDS + DATE_FIELDS

REQUIRED_STRUCTURED = [f for f in STRUCTURED_FIELDS if f != "station_count"]

REQUIRED_FIELDS = STRING_REQUIRED + REQUIRED_STRUCTURED
OPTIONAL_FIELDS = STRING_OPTIONAL + [f for f in STRUCTURED_FIELDS if f not in REQUIRED_STRUCTURED]
ALL_FIELDS = STRING_FIELDS + STRUCTURED_FIELDS

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def is_valid_url(value: str) -> bool:
    if not value:
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def vocab_errors(vocab: object) -> list[str]:
    if not isinstance(vocab, dict):
        return ["vocab root must be a JSON object."]
    errors = []
    for key in LIST_FIELDS + ENUM_FIELDS:
        values = vocab.get(key)
        if not isinstance(values, list) or not values:
            errors.append(f"{key} must be a non-empty list.")
        elif not all(isinstance(v, str) and v.strip() for v in values):
            errors.append(f"{key} must contain only non-empty strings.")
        elif len(set(values)) != len(values):
            errors.append(f"{key} contains duplicate values.")
    return errors


def load_vocab(path: Path = VOCAB_PATH) -> dict[str, list[str]]:
    if not path.is_file():
        raise ValueError(f"Vocabulary not found: {path}")
    vocab = json.loads(path.read_text(encoding="utf-8"))
    errors = vocab_errors(vocab)
    if errors:
        raise ValueError(f"Invalid vocabulary: {' '.join(errors)}")
    return vocab


def is_int(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def check_structured(field: str, value: object, vocab: dict[str, list[str]]) -> str | None:
    """Return an error message for one structured field, or None if it is valid."""
    if value is None:
        return None if field in NULLABLE_FIELDS else f"{field} cannot be null."
    if field in LIST_FIELDS:
        if not isinstance(value, list) or not value:
            return f"{field} must be a non-empty list."
        if not all(isinstance(v, str) for v in value):
            return f"{field} must contain only strings."
        unknown = [v for v in value if v not in vocab[field]]
        if unknown:
            return f"{field} has values outside data/vocab.json: {', '.join(unknown)}."
        if len(set(value)) != len(value):
            return f"{field} contains duplicate values."
    elif field in NUMBER_FIELDS:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            return f"{field} must be a number or null."
        if not math.isfinite(value) or value <= 0:
            return f"{field} must be a positive number."
    elif field in INT_FIELDS:
        if not is_int(value):
            return f"{field} must be an integer" + (" or null." if field in NULLABLE_FIELDS else ".")
        if value <= 0:
            return f"{field} must be a positive integer."
    elif field in ENUM_FIELDS:
        if value not in vocab[field]:
            return f"{field} must be one of: {', '.join(vocab[field])}."
    elif field in DATE_FIELDS:
        if not isinstance(value, str) or not ISO_DATE.match(value):
            return f"{field} must be an ISO date (YYYY-MM-DD)."
        try:
            date.fromisoformat(value)
        except ValueError:
            return f"{field} is not a real calendar date: {value}."
    return None


def validate_entry(entry: dict, vocab: dict[str, list[str]], require_complete: bool) -> list[str]:
    """Return error messages for one dataset entry. An empty list means valid."""
    errors = []
    unknown = sorted(set(entry) - set(ALL_FIELDS))
    if unknown:
        errors.append(f"Unknown fields: {', '.join(unknown)}")
    non_strings = sorted(f for f in STRING_FIELDS if f in entry and not isinstance(entry[f], str))
    if non_strings:
        errors.append(f"Fields must contain strings: {', '.join(non_strings)}")
    if require_complete:
        missing = [f for f in STRING_REQUIRED if not entry.get(f)]
        missing += [f for f in REQUIRED_STRUCTURED if f not in entry]
        if missing:
            errors.append(f"Missing required fields: {', '.join(missing)}")

    for field in STRUCTURED_FIELDS:
        if field in entry:
            message = check_structured(field, entry[field], vocab)
            if message:
                errors.append(message)

    url = entry.get("source_url")
    if isinstance(url, str) and url and not is_valid_url(url):
        errors.append("source_url must be an absolute HTTP or HTTPS URL.")

    start, end = entry.get("start_year"), entry.get("end_year")
    if is_int(start) and is_int(end) and end < start:
        errors.append("end_year is earlier than start_year.")
    return errors


def parse_text(field: str, text: str) -> object:
    """Convert interactive text input into the value type the field expects."""
    text = text.strip()
    if field in LIST_FIELDS:
        return [part.strip() for part in text.split(",") if part.strip()]
    if field in NUMBER_FIELDS + INT_FIELDS:
        if text.lower() == "null":
            return None
        try:
            return int(text) if field in INT_FIELDS or text.lstrip("+-").isdigit() else float(text)
        except ValueError:
            kind = "an integer" if field in INT_FIELDS else "a number"
            raise ValueError(f"{field} must be {kind}, or null where allowed.") from None
    return text
