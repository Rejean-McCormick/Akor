#!/usr/bin/env python3
"""Launch Akor from a source checkout without requiring pip install."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))
from akor.preflight import main

if __name__ == "__main__":
    raise SystemExit(main())
