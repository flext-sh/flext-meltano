"""Behavioral contract for Meltano service settings resolution.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from pathlib import Path

import pytest
from flext_cli import config as cli_config

from flext_meltano import FlextMeltanoConfig, config, settings
from tests import m, meltano, tm, u


class TestsFlextMeltanoServiceSettingsContract:
    """Tests for the settings contract of ``FlextMeltanoServiceBase`` services."""

    pytestmark = pytest.mark.unit

    class YamlConfig(FlextMeltanoConfig):
        """Real config subclass consuming the typed SSOT round-trip payload."""

    @staticmethod
    def test_facade_settings_resolve_project_settings() -> None:
        """The public facade resolves the project settings type and SSOT values."""
        tm.that(meltano.settings_type, eq=type(settings))
        resolved = meltano.settings
        tm.that(resolved, is_=type(settings))
        tm.that(resolved.model_dump(), eq=settings.model_dump())

    @staticmethod
    def test_config_has_frozen_per_subclass_identity() -> None:
        """Public config access stays frozen and distinct from upstream settings."""
        current = FlextMeltanoConfig.fetch_global()
        tm.that(current is config, truth=True)
        tm.that(FlextMeltanoConfig.fetch_global() is current, truth=True)
        tm.that(cli_config is not current, truth=True)
        before = current.model_dump()
        for field_name, value in before.items():
            with pytest.raises(m.ValidationError, match="frozen_instance"):
                setattr(current, field_name, value)
        tm.that(current.model_dump(), eq=before)

    @staticmethod
    def test_adjustable_settings_do_not_change_config() -> None:
        """Runtime settings can be adjusted without changing business-rule config."""
        before = config.model_dump()
        adjusted = settings.clone(debug=not settings.debug)
        tm.that(adjusted.debug, eq=not settings.debug)
        tm.that(adjusted is not settings, truth=True)
        tm.that(FlextMeltanoConfig.fetch_global() is config, truth=True)
        tm.that(config.model_dump(), eq=before)

    @staticmethod
    def test_config_fetch_global_loads_yaml_roundtrip(tmp_path: Path) -> None:
        """A child config loads YAML independently without changing its parent."""
        owner = TestsFlextMeltanoServiceSettingsContract.YamlConfig
        namespace = config.Meltano.model_copy(
            update={"lifecycle_probe": "yaml-roundtrip"},
        )
        expected = config.model_copy(update={"Meltano": namespace})
        tm.ok(
            u.Cli.yaml_dump(
                tmp_path / "roundtrip.yaml",
                {
                    "Meltano": namespace.model_dump(
                        mode="json",
                        include={"lifecycle_probe"},
                    ),
                },
            ),
        )
        prefix = owner.__module__.split(".", 1)[0].upper()
        with u.Tests.env_vars_context({f"{prefix}_CONFIG_DIR": str(tmp_path)}):
            owner.reset_for_testing()
            try:
                loaded = owner.fetch_global()
                tm.that(loaded is owner.fetch_global(), truth=True)
                tm.that(loaded is not config, truth=True)
                tm.that(loaded.model_dump(), eq=expected.model_dump())
                for field_name, value in loaded.model_dump().items():
                    with pytest.raises(m.ValidationError, match="frozen_instance"):
                        setattr(loaded, field_name, value)
            finally:
                owner.reset_for_testing()
        tm.that(FlextMeltanoConfig.fetch_global() is config, truth=True)
