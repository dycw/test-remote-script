from __future__ import annotations

from logging import getLogger
from pathlib import Path

from installer.constants import CONFIGS, NONROOT, ROOT
from installer.utilities import copy, has_non_root, run

_LOGGER = getLogger(__name__)


def create_non_root() -> None:
    if has_non_root():
        _LOGGER.info("%r already exists", NONROOT)
        return
    _LOGGER.info("Creating %r...", NONROOT)
    run(f"useradd --create-home --shell /bin/bash {NONROOT}")
    run(f"usermod -aG sudo {NONROOT}")


def set_password(*, password: str | None = None) -> None:
    if password is None:
        _LOGGER.info("Skipping password(s)")
        return
    _LOGGER.info("Setting %r password...", ROOT)
    _set_password_one(ROOT, password)
    if has_non_root():
        _LOGGER.info("Setting %r password...", NONROOT)
        _set_password_one(NONROOT, password)
    else:
        _LOGGER.info("Skipping %r; user does not exist", NONROOT)


def _set_password_one(username: str, password: str, /) -> None:
    run(f"echo '{username}:{password}' | chpasswd")


def setup_ssh_config_d() -> None:
    copy(CONFIGS / "ssh/config.d/default", Path("/etc/ssh/ssh_config.d/default"))


__all__ = ["create_non_root", "set_password", "setup_ssh_config_d"]
