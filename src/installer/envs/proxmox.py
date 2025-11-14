from __future__ import annotations

from logging import getLogger
from pathlib import Path

from installer.constants import CONFIGS
from installer.utilities import copy, dpkg_install, is_copied, yield_github_download

_LOGGER = getLogger(__name__)
_CONFIGS_PROXMOX = CONFIGS / "proxmox"


def setup_proxmox(
    *,
    storage_cfg: Path = _CONFIGS_PROXMOX / "storage.cfg",
    pbs_password: str | None = None,
) -> None:
    _LOGGER.info("Setting up Proxmox...")
    _remove_sources()
    _setup_pve_fake_subscription()
    _setup_storage_cfg(src=storage_cfg)
    _setup_pbs_data_pw(password=pbs_password)
    _LOGGER.info("Finished setting up Proxmox")


def _remove_sources() -> None:
    paths = {
        p
        for n in ["ceph", "pve-enterprise"]
        if (p := Path(f"/etc/apt/sources.list.d/{n}.sources")).is_file()
    }
    if len(paths) == 0:
        _LOGGER.info("'apt' sources already removed")
    else:
        _LOGGER.info("Removing 'apt' sources...")
        for p in paths:
            p.unlink(missing_ok=True)


def _setup_pve_fake_subscription() -> None:
    path = Path("/etc/pve/.pve_fake_subscription_ran")
    if not path.exists():
        with yield_github_download(
            "jamesits",
            "pve-fake-subscription",
            "pve-fake-subscription_${tag_without}+git-1_all.deb",
        ) as binary:
            dpkg_install(binary)
        path.touch()


def _setup_storage_cfg(*, src: Path = _CONFIGS_PROXMOX / "storage.cfg") -> None:
    dest = Path("/etc/pve/storage.cfg")
    if is_copied(src, dest):
        _LOGGER.info("%r is already copied", str(str))
    else:
        _LOGGER.info("Copying %r...", str(str))
        copy(src, dest)


def _setup_pbs_data_pw(*, password: str | None = None) -> None:
    if password is None:
        _LOGGER.info("Skipping 'pbs-data.pw'...")
    else:
        _LOGGER.info("Writing 'pbs-data.pw'...")
        copy(
            _CONFIGS_PROXMOX / "pbs-data.pw",
            Path("/etc/pve/priv/storage/pbs-data.pw"),
            password=password,
        )


__all__ = ["setup_proxmox"]
