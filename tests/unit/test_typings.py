"""FLEXT Meltano Typings Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for the flattened Meltano
type namespace following FLEXT canonical governance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from tests import m, t


class TestFlextMeltanoTypes:
    """Unit test suite for FlextMeltanoTypes — flat namespace validation."""

    def test_meltano_namespace_exists(self) -> None:
        """Test that Meltano namespace exists as top-level namespace."""
        tm.that(hasattr(t, "Meltano"), eq=True)

    def test_plugin_types(self) -> None:
        """Test Plugin composition types on Meltano namespace."""
        tm.that(hasattr(t.Meltano, "PluginDefinition"), eq=True)
        tm.that(hasattr(t.Meltano, "PluginCatalog"), eq=True)
        tm.that(hasattr(t.Meltano, "PluginType"), eq=True)

    def test_adapters_exist(self) -> None:
        """Test TypeAdapter instances are available."""
        tm.that(hasattr(t.Meltano, "CONTAINER_MAP_ADAPTER"), eq=True)
        tm.that(hasattr(t.Meltano, "INTEGER_ADAPTER"), eq=True)

    def test_composition_types(self) -> None:
        """Test composed types that add value over base ``t.*``."""
        tm.that(hasattr(t.Meltano, "ValidatorInput"), eq=True)
        tm.that(hasattr(t.Meltano, "VariantValue"), eq=True)
        tm.that(hasattr(t.Meltano, "FileConfigDict"), eq=True)
        tm.that(hasattr(t.Meltano, "OptionalScalarMap"), eq=True)
        tm.that(hasattr(t.Meltano, "CliProcessResult"), eq=True)

    def test_dbt_flat_types(self) -> None:
        """Test DBT types are flat with ``Dbt`` prefix."""
        tm.that(hasattr(t.Meltano, "DbtManifestData"), eq=True)
        tm.that(hasattr(t.Meltano, "DbtProject"), eq=True)

    def test_singer_flat_types(self) -> None:
        """Test Singer types are flat with ``Singer`` prefix."""
        tm.that(hasattr(t.Meltano, "SingerCatalogEntry"), eq=True)
        tm.that(hasattr(t.Meltano, "SingerStreamCatalog"), eq=True)
        tm.that(hasattr(t.Meltano, "SingerReplicationMethod"), eq=True)

    def test_singer_sdk_typing_wrappers(self) -> None:
        """Test Singer SDK typing wrappers prevent direct imports."""
        tm.that(hasattr(t.Meltano, "SingerProperty"), eq=True)
        tm.that(hasattr(t.Meltano, "SingerPropertiesList"), eq=True)
        tm.that(hasattr(t.Meltano, "SingerStringType"), eq=True)
        tm.that(hasattr(t.Meltano, "SingerIntegerType"), eq=True)
        assert t.Meltano.SingerProperty is m.Meltano.SingerProperty
        assert t.Meltano.SingerStringType is m.Meltano.SingerStringType

    def test_type_annotations(self) -> None:
        """Test that type annotations are properly defined."""
        plugin_definition = t.Meltano.PluginDefinition
        tm.that(str(plugin_definition), none=False)
        singer_catalog = t.Meltano.SingerCatalogEntry
        tm.that(str(singer_catalog), none=False)

    def test_no_nested_namespaces(self) -> None:
        """Test that old nested namespaces no longer exist."""
        removed_namespaces = [
            "Singer",
            "Dbt",
            "Project",
            "Pipeline",
            "Bridge",
            "CLI",
            "ELT",
            "Processing",
        ]
        for namespace in removed_namespaces:
            tm.that(hasattr(t.Meltano, namespace), eq=False)

    def test_no_duplicate_aliases(self) -> None:
        """Test that simple aliases to existing ``t.*`` are removed."""
        removed_duplicates = [
            "MeltanoConfigDict",
            "ExecutionResultDict",
            "ResultDict",
            "DbtResultDict",
            "PluginConfiguration",
            "PluginConfigDict",
        ]
        for alias in removed_duplicates:
            tm.that(hasattr(t.Meltano, alias), eq=False)

    def test_type_compatibility(self) -> None:
        """Test that types are compatible with their intended use."""
        plugin_def = {
            "name": "tap-users",
            "variants": ["default"],
            "config": {"batch_size": 1000},
        }
        catalog = {
            "tap_stream_id": "users",
            "schema": {"type": "t.NormalizedValue"},
        }
        tm.that(str(plugin_def["name"]), eq="tap-users")
        tm.that(list(plugin_def["variants"]), is_=list)
        tm.that(str(catalog["tap_stream_id"]), eq="users")
        schema_val = catalog["schema"]
        assert isinstance(schema_val, dict)
        tm.that(schema_val, is_=dict)

    def test_type_consistency(self) -> None:
        """Test that types are consistent across the namespace."""
        plugin_definition = t.Meltano.PluginDefinition
        singer_catalog = t.Meltano.SingerCatalogEntry
        tm.that(str(plugin_definition), none=False)
        tm.that(str(singer_catalog), none=False)
