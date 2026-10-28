#!/usr/bin/env python3
"""Optional synthetic review export; all output remains untrusted."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'src'))
from akor.tandem_intent import main
if __name__=='__main__':raise SystemExit(main())
