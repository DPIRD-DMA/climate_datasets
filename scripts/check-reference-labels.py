#!/usr/bin/env python3
import re
from pathlib import Path

readme_path = Path("README.md")
text = readme_path.read_text()

# Reference definitions: [Label]: url
ref_defs = {
    m.group(1).strip(): m.group(2).strip()
    for m in re.finditer(r"^\[([^\]]+)\]:\s*(\S+)\s*$", text, re.M)
}

used_labels = set()

# [text][label]
for m in re.finditer(r"\[([^\]]+)\]\[([^\]]*)\]", text):
    label = m.group(2).strip() or m.group(1).strip()
    used_labels.add(label)

# [label] reference-style (avoid images and links with parentheses)
for m in re.finditer(r"(?<!\!)\[([^\]]+)\](?!\()", text):
    label = m.group(1).strip()
    # Skip headings or plain brackets that aren't intended as refs
    if label in ("DATASET_TABLE_START", "DATASET_TABLE_END", "DATASET_REFERENCES_START", "DATASET_REFERENCES_END"):
        continue
    # Heuristic: if label appears as a reference definition, treat as a ref usage
    if label in ref_defs:
        used_labels.add(label)

missing = sorted(label for label in used_labels if label not in ref_defs)
unused = sorted(label for label in ref_defs if label not in used_labels)

if missing:
    print("Missing reference definitions:")
    for label in missing:
        print(f"- {label}")
if unused:
    print("Unused reference definitions:")
    for label in unused:
        print(f"- {label}")

if not missing and not unused:
    print("All reference labels are defined and used.")

exit(1 if missing else 0)
