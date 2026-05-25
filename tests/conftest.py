from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
PATHS = [
    ROOT,
    ROOT / "2_domain",
    ROOT / "3_infrastructure",
    ROOT / "4_presentation",
    ROOT / "5_pipeline",
]

for path in PATHS:
    path_str = str(path)
    if path_str not in sys.path:
        sys.path.insert(0, path_str)
