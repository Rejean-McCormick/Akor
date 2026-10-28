#!/usr/bin/env python3
"""Optional Tandem synthetic handoff gate; legacy run_akor.py stays intact."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent/'src'))
from akor.tandem_gate import main
if __name__=='__main__':
    raise SystemExit(main())
