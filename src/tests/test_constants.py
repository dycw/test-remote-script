from __future__ import annotations

from installer.constants import CONFIGS


class TestConstants:
    def test_configs(self) -> None:
        assert CONFIGS.is_dir()
        assert {p.name for p in CONFIGS.iterdir()} == {"ssh"}
