"""Stable machine-readable Recovery Organ report."""
from __future__ import annotations

import json
from pathlib import Path


def save_report(report: dict, path: str) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
