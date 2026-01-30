#!/usr/bin/env python3
from pathlib import Path
import shutil

src = Path("data/datasets.json")
dst_dir = Path("docs/data")
dst_dir.mkdir(parents=True, exist_ok=True)
dst = dst_dir / "datasets.json"

shutil.copyfile(src, dst)
print(f"Copied {src} -> {dst}")
