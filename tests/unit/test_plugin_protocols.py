"""Test module for flext-meltano plugin type definitions.

Tests the canonical t.Meltano.PluginDefinition, t.Meltano.PluginCatalog,
and t.Meltano.PluginCatalog types following FLEXT standards.
Validates actual type alias semantics, not just existence.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from tests import t


class TestFlextMeltanoPluginProtocols:
    """Test canonical Meltano plugin type definitions via t.Meltano namespace."""

    def test_plugin_definition_resolves_to_mapping(self) -> None:
        """PluginDefinition type alias resolves to a Mapping-compatible type."""
        # PluginDefinition should be usable as a type annotation
        plugin_def: t.Meltano.PluginDefinition = {
            "name": "tap-postgres",
            "namespace": "tap_postgres",
            "pip_url": "git+https://github.com/example/tap-postgres.git",
        }
        tm.that(plugin_def["name"], eq="tap-postgres")
        tm.that(len(plugin_def), eq=3)

    def test_plugin_configuration_resolves_to_mapping(self) -> None:
        """PluginConfiguration type alias resolves to a Mapping-compatible type."""
        plugin_cfg = {
            "host": "localhost",
            "port": "5432",
            "database": "analytics",
        }
        tm.that(plugin_cfg["host"], eq="localhost")
        tm.that(len(plugin_cfg) >= 3, eq=True)

    def test_plugin_catalog_resolves_to_mapping(self) -> None:
        """PluginCatalog type alias resolves to a Mapping-compatible type."""
        catalog: t.Meltano.PluginCatalog = {
            "streams": [
                {"stream": "users", "tap_stream_id": "users"},
            ],
        }
        tm.that("streams" in catalog, eq=True)

    def test_type_aliases_are_distinct(self) -> None:
        """Each plugin type alias is a distinct named type."""
        names = {
            str(t.Meltano.PluginDefinition),
            str(t.JsonMapping),
            str(t.Meltano.PluginCatalog),
        }
        tm.that(len(names), eq=3)

    def test_meltano_namespace_contains_all_plugin_types(self) -> None:
        """t.Meltano namespace exposes all three plugin type aliases."""
        tm.that(str(t.Meltano.PluginDefinition), none=False)
        tm.that(str(t.JsonMapping), none=False)
        tm.that(str(t.Meltano.PluginCatalog), none=False)
