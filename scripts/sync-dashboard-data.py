#!/usr/bin/env python3
from pathlib import Path
import shutil

SOURCES = [Path("data/datasets.json"), Path("data/vocab.json")]
dst_dir = Path("docs/data")
dst_dir.mkdir(parents=True, exist_ok=True)

for src in SOURCES:
    dst = dst_dir / src.name
    shutil.copyfile(src, dst)
    print(f"Copied {src} -> {dst}")
