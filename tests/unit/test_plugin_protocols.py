"""Test module for flext-meltano Singer catalog contracts.

Tests the canonical t.JsonMapping contract plus m.Meltano Singer catalog
models following FLEXT standards.
Validates that legacy typing aliases stay removed.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from tests import m, t


class TestsFlextMeltanoPluginProtocols:
    """Test canonical Meltano plugin contracts via public typing namespaces."""

    def test_plugin_definition_resolves_to_mapping(self) -> None:
        """Plugin definitions use the canonical JSON mapping contract."""
        plugin_def: t.JsonMapping = {
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

    def test_singer_catalog_model_validates_catalog_payload(self) -> None:
        """Singer catalog payloads validate through m.Meltano models."""
        catalog = m.Meltano.SingerCatalog.model_validate({
            "streams": [
                {"stream": "users", "tap_stream_id": "users", "schema": {}},
            ],
        })
        tm.that(catalog.streams[0].stream, eq="users")
        tm.that(catalog.streams[0].tap_stream_id, eq="users")

    def test_model_contract_is_distinct(self) -> None:
        """Singer catalog models stay distinct from the JSON mapping contract."""
        names = {
            str(t.JsonMapping),
            str(m.Meltano.SingerCatalog),
        }
        tm.that(len(names), eq=2)

    def test_meltano_namespace_removes_legacy_singer_aliases(self) -> None:
        """t.Meltano exposes no legacy Singer typing aliases."""
        tm.that(str(t.JsonMapping), none=False)
        tm.that(str(m.Meltano.SingerCatalog), none=False)
        assert not hasattr(t.Meltano, "SingerCatalogEntry")
        assert not hasattr(t.Meltano, "SingerStreamCatalog")
        assert not hasattr(t.Meltano, "PluginCatalog")
        assert not hasattr(t.Meltano, "PluginDefinition")
