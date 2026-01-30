#!/usr/bin/env python3
import json
from pathlib import Path

DATA_PATH = Path("data/datasets.json")
README_PATH = Path("README.md")

TABLE_START = "<!-- DATASET_TABLE_START -->"
TABLE_END = "<!-- DATASET_TABLE_END -->"
REF_START = "<!-- DATASET_REFERENCES_START -->"
REF_END = "<!-- DATASET_REFERENCES_END -->"

columns = [
    "Dataset",
    "Resolution",
    "Format",
    "Variables",
    "Method",
    "Access Conditions",
    "Temporal Coverage",
]

with DATA_PATH.open() as f:
    data = json.load(f)["datasets"]

# Show only a small preview in README.
preview_count = 3
data = data[:preview_count]

def md_escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")

def row_for(ds):
    name = ds["name"]
    label = name
    dataset_cell = f"[{md_escape(name)}][{md_escape(label)}]"
    return [
        dataset_cell,
        md_escape(ds.get("resolution", "")),
        md_escape(ds.get("format", "")),
        md_escape(ds.get("variables", "")),
        md_escape(ds.get("method", "")),
        md_escape(ds.get("access_conditions", "")),
        md_escape(ds.get("temporal_coverage", "")),
    ]

rows = [row_for(ds) for ds in data]

header = "| " + " | ".join(columns) + " |"
sep = "|" + "|".join(["---"] * len(columns)) + "|"
body = "\n".join("| " + " | ".join(r) + " |" for r in rows)

references = []
for ds in data:
    name = ds["name"]
    url = ds.get("source_url", "").strip()
    if url:
        references.append(f"[{name}]: {url}")

new_table_block = "\n".join([TABLE_START, header, sep, body, TABLE_END])
new_ref_block = "\n".join([REF_START, *references, REF_END])

readme = README_PATH.read_text()

def replace_block(text, start, end, replacement):
    pattern = re.compile(rf"{re.escape(start)}.*?{re.escape(end)}", re.S)
    if not pattern.search(text):
        raise SystemExit(f"Missing block markers: {start} ... {end}")
    return pattern.sub(replacement, text)

import re
readme = replace_block(readme, TABLE_START, TABLE_END, new_table_block)
readme = replace_block(readme, REF_START, REF_END, new_ref_block)
README_PATH.write_text(readme)

print("README dataset table and references updated.")
