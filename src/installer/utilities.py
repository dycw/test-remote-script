from __future__ import annotations

from ipaddress import IPv4Address
from logging import getLogger
from os import environ
from pathlib import Path
from socket import AF_INET, SOCK_DGRAM, socket
from string import Template
from subprocess import PIPE, CalledProcessError, check_call, check_output
from typing import Any, Literal, NoReturn, assert_never, overload

from utilities.atomicwrites import writer
from utilities.functools import cache
from utilities.iterables import OneEmptyError, one

from installer.constants import NONROOT
from installer.enums import Subnet

_LOGGER = getLogger(__name__)


def copy(src: Path, dest: Path, /, **kwargs: Any) -> None:
    text = src.read_text()
    if len(kwargs) >= 1:
        text = Template(text).substitute(**kwargs)
    with writer(dest, overwrite=True) as temp_dir:
        _ = temp_dir.write_text(text)


def get_subnet() -> Subnet:
    try:
        return Subnet[environ["SUBNET"]]
    except KeyError:
        with socket(AF_INET, SOCK_DGRAM) as s:
            s.connect(("1.1.1.1", 80))
            ip = IPv4Address(s.getsockname()[0])
        n = int(str(ip).split(".")[2])
        try:
            return one(s for s in Subnet if s.n == n)
        except OneEmptyError:
            msg = f"Invalid IP; got {ip}"
            raise ValueError(msg) from None


def has_non_root() -> bool:
    return run(f"id -u {NONROOT}", failable=True)


@cache
def is_lxc() -> bool:
    try:
        return run("systemd-detect-virt --container", output=True) == "container"
    except CalledProcessError:
        return False


@cache
def is_proxmox() -> bool:
    return Path("/etc/pve").is_dir()


@overload
def run(
    cmd: str,
    /,
    *,
    output: Literal[True],
    failable: Literal[True],
    cwd: Path | None = None,
) -> str | None: ...
@overload
def run(
    cmd: str,
    /,
    *,
    output: Literal[True],
    failable: Literal[False] = False,
    cwd: Path | None = None,
) -> str: ...
@overload
def run(
    cmd: str,
    /,
    *,
    output: Literal[False] = False,
    failable: Literal[True],
    cwd: Path | None = None,
) -> bool: ...
@overload
def run(
    cmd: str,
    /,
    *,
    output: Literal[False] = False,
    failable: Literal[False] = False,
    cwd: Path | None = None,
) -> None: ...
@overload
def run(
    cmd: str,
    /,
    *,
    output: bool = False,
    failable: bool = False,
    cwd: Path | None = None,
) -> bool | str | None: ...
def run(
    cmd: str,
    /,
    *,
    output: bool = False,
    failable: bool = False,
    cwd: Path | None = None,
) -> bool | str | None:
    match output, failable:
        case False, False:
            try:
                _run_check_call(cmd, cwd=cwd)
            except CalledProcessError as error:
                _run_handle_error(cmd, error)
        case False, True:
            try:
                _run_check_call(cmd, cwd=cwd)
            except CalledProcessError:
                return False
            return True
        case True, False:
            try:
                return _run_check_output(cmd, cwd=cwd)
            except CalledProcessError as error:
                _run_handle_error(cmd, error)
        case True, True:
            try:
                return _run_check_output(cmd, cwd=cwd)
            except CalledProcessError:
                return None
        case never:
            assert_never(never)


def _run_check_call(cmd: str, /, *, cwd: Path | None = None) -> None:
    _ = check_call(cmd, stdout=PIPE, stderr=PIPE, shell=True, cwd=cwd)


def _run_check_output(cmd: str, /, *, cwd: Path | None = None) -> str:
    return check_output(cmd, stderr=PIPE, shell=True, cwd=cwd, text=True).rstrip("\n")


def _run_handle_error(cmd: str, error: CalledProcessError, /) -> NoReturn:
    lines: list[str] = [f"Error running {cmd!r}"]
    divider = 80 * "-"
    if isinstance(stdout := error.stdout, str) and (stdout != ""):
        lines.extend([divider, "stdout " + 73 * "-", stdout, divider])
    if isinstance(stderr := error.stderr, str) and (stderr != ""):
        lines.extend([divider, "stderr " + 73 * "-", stderr, divider])
    _LOGGER.exception("\n".join(lines))
    raise error


__all__ = ["copy", "has_non_root", "is_lxc", "is_proxmox", "run"]
