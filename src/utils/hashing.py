"""Hashing utilities for reproducible configs and content fingerprints."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import yaml


def load_yaml(path: str | Path) -> dict:
    """Load a YAML file with UTF-8 encoding."""
    with open(Path(path), "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def stable_hash(obj: Any) -> str:
    """Compute a stable sha256 hash for a Python object by YAML-dumping it."""
    raw = yaml.safe_dump(obj, sort_keys=True, allow_unicode=True).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()

