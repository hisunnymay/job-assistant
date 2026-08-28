#!/usr/bin/env python3
import sys
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPOSITORY_ROOT / "backend"))

from app.release.smoke import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main(REPOSITORY_ROOT))
