from __future__ import annotations

from collections.abc import Sequence
from typing import ClassVar

from pydantic import SecretStr
from pydantic_settings import BaseSettings
from utilities.pydantic_settings import PathLikeOrWithSection, load_settings
from utilities.pydantic_settings_sops import SopsBaseSettings

from installer.constants import CONFIGS


class _Settings(SopsBaseSettings):
    toml_files: ClassVar[Sequence[PathLikeOrWithSection]] = [CONFIGS / "config.toml"]
    secret_files: ClassVar[Sequence[PathLikeOrWithSection]] = [
        (CONFIGS / "secrets.json")
    ]

    subnets: _Subnets
    pbs: SecretStr


class _Subnets(BaseSettings):
    qrt: int
    main: int
    test: int


SETTINGS = load_settings(_Settings)


__all__ = ["SETTINGS"]
