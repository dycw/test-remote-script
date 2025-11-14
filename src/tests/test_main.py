from __future__ import annotations

from installer import __version__


def test_main() -> None:
    assert isinstance(__version__, str)
