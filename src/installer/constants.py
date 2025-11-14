from __future__ import annotations

from importlib.resources import files

CONFIGS = files("configs")
NONROOT = "nonroot"


__all__ = ["CONFIGS", "NONROOT"]
