from __future__ import annotations

from logging import getLogger

from click import command, option
from utilities.click import CONTEXT_SETTINGS_HELP_OPTION_NAMES
from utilities.logging import basic_config

from installer import __version__
from installer.constants import NONROOT
from installer.utilities import has_non_root, run

_LOGGER = getLogger(__name__)


@command(**CONTEXT_SETTINGS_HELP_OPTION_NAMES)
@option(
    "--create-non-root",
    is_flag=True,
    default=False,
    show_default=True,
    help="Create 'nonroot'",
)
def _main(*, create_non_root: bool = False) -> None:
    _LOGGER.info("Running installer %s...", __version__)
    if create_non_root:
        _create_non_root()
    _LOGGER.info("Finished running installer %s", __version__)


def _create_non_root() -> None:
    if has_non_root():
        _LOGGER.info("%r already exists", NONROOT)
    else:
        _LOGGER.info("Creating %r...", NONROOT)
        run(f"useradd --create-home --shell /bin/bash {NONROOT}")
        run(f"usermod -aG sudo {NONROOT}")


if __name__ == "__main__":
    basic_config(obj=_LOGGER, hostname=True)
    _main()
