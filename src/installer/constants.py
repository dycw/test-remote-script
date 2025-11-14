from __future__ import annotations

from importlib.resources import files
from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from pathlib import Path


CONFIGS = cast("Path", files("configs").joinpath("z")).parent
NONROOT = "nonroot"


__all__ = ["CONFIGS", "NONROOT"]
