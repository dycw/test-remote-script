from __future__ import annotations

from logging import basicConfig, getLogger
from pathlib import Path
from socket import gethostname
from subprocess import check_call

# THIS MODULE CANNOT CONTAIN ANY THIRD PARTY IMPORTS


_FORMAT = (
    f"[{{asctime}} ❯ {gethostname()} ❯ {{module}}:{{funcName}}:{{lineno}}] {{message}}"  # noqa: RUF001
)
basicConfig(format=_FORMAT, datefmt="%Y-%m-%d %H:%M:%S", style="{", level="INFO")
_LOGGER = getLogger(__name__)
__version__ = "0.1.3"


def main() -> None:
    _LOGGER.info("Running entrypoint %s...", __version__)
    Path("~/test-remote-script")
    _ = check_call("cd ~/test-remote-script", shell=True, text=True)


if __name__ == "__main__":
    _ = check_call("cd ~/test-remote-script", shell=True, text=True)
