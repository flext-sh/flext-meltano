"""FLEXT Meltano Typings Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for t following
FLEXT testing patterns and namespace organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from flext_meltano import t


class TestFlextMeltanoTypes:
    """Unit test suite for FlextMeltanoTypes."""

    def test_meltano_namespace_exists(self) -> None:
        """Test that Meltano namespace exists as top-level namespace."""
        tm.that(hasattr(t, "Meltano"), eq=True)

    def test_plugin_namespace(self) -> None:
        """Test Plugin types exist directly on Meltano namespace."""
        tm.that(hasattr(t.Meltano, "PluginDefinition"), eq=True)
        tm.that(hasattr(t.Meltano, "PluginConfiguration"), eq=True)
        tm.that(hasattr(t.Meltano, "PluginCatalog"), eq=True)

    def test_plugin_types_direct(self) -> None:
        """Test Plugin types are also directly on Meltano namespace."""
        tm.that(hasattr(t.Meltano, "PluginDefinition"), eq=True)
        tm.that(hasattr(t.Meltano, "PluginType"), eq=True)
        tm.that(hasattr(t.Meltano, "PluginVariant"), eq=True)

    def test_singer_namespace(self) -> None:
        """Test Singer namespace types."""
        tm.that(hasattr(t.Meltano, "Singer"), eq=True)
        singer_types = t.Meltano.Singer
        tm.that(hasattr(singer_types, "Record"), eq=True)
        tm.that(hasattr(singer_types, "Schema"), eq=True)
        tm.that(hasattr(singer_types, "State"), eq=True)

    def test_dbt_namespace(self) -> None:
        """Test DBT namespace types."""
        tm.that(hasattr(t.Meltano, "Dbt"), eq=True)
        dbt_types = t.Meltano.Dbt
        tm.that(hasattr(dbt_types, "ModelConfiguration"), eq=True)
        tm.that(hasattr(dbt_types, "TestConfiguration"), eq=True)
        tm.that(hasattr(dbt_types, "Project"), eq=True)

    def test_project_namespace(self) -> None:
        """Test Project namespace types."""
        tm.that(hasattr(t.Meltano, "Project"), eq=True)
        project_types = t.Meltano.Project
        tm.that(hasattr(project_types, "ProjectConfig"), eq=True)
        tm.that(hasattr(project_types, "ProjectMetadata"), eq=True)

    def test_pipeline_namespace(self) -> None:
        """Test Pipeline namespace types."""
        tm.that(hasattr(t.Meltano, "Pipeline"), eq=True)
        pipeline_types = t.Meltano.Pipeline
        tm.that(hasattr(pipeline_types, "PipelineConfig"), eq=True)
        tm.that(hasattr(pipeline_types, "PipelineStatus"), eq=True)

    def test_bridge_namespace(self) -> None:
        """Test Bridge namespace types."""
        tm.that(hasattr(t.Meltano, "Bridge"), eq=True)
        bridge_types = t.Meltano.Bridge
        tm.that(hasattr(bridge_types, "BridgeMessage"), eq=True)
        tm.that(hasattr(bridge_types, "BridgeResponse"), eq=True)

    def test_cli_namespace(self) -> None:
        """Test CLI namespace types."""
        tm.that(hasattr(t.Meltano, "CLI"), eq=True)
        cli_types = t.Meltano.CLI
        tm.that(hasattr(cli_types, "Command"), eq=True)
        tm.that(hasattr(cli_types, "CommandResult"), eq=True)

    def test_elt_namespace(self) -> None:
        """Test ELT namespace types."""
        tm.that(hasattr(t.Meltano, "ELT"), eq=True)
        elt_types = t.Meltano.ELT
        tm.that(hasattr(elt_types, "ExtractConfig"), eq=True)
        tm.that(hasattr(elt_types, "LoadConfig"), eq=True)
        tm.that(hasattr(elt_types, "TransformConfig"), eq=True)

    def test_processing_namespace(self) -> None:
        """Test Processing namespace types."""
        tm.that(hasattr(t.Meltano, "Processing"), eq=True)
        processing_types = t.Meltano.Processing
        tm.that(hasattr(processing_types, "SingerExecutionResult"), eq=True)
        tm.that(hasattr(processing_types, "DbtTransformationResult"), eq=True)
        tm.that(hasattr(processing_types, "EltPipelineResult"), eq=True)

    def test_meltano_core_types(self) -> None:
        """Test Meltano core types (previously MeltanoCore)."""
        meltano_types = t.Meltano
        tm.that(hasattr(meltano_types, "MeltanoConfigDict"), eq=True)
        tm.that(hasattr(meltano_types, "PluginConfigDict"), eq=True)

    def test_type_annotations(self) -> None:
        """Test that type annotations are properly defined."""
        plugin_definition = t.Meltano.PluginDefinition
        tm.that(plugin_definition, none=False)
        singer_catalog = t.Meltano.Singer.CatalogEntry
        tm.that(singer_catalog, none=False)

    def test_namespace_organization(self) -> None:
        """Test that all expected sub-namespaces exist under Meltano."""
        expected_sub_namespaces = [
            "Singer",
            "Dbt",
            "Project",
            "Pipeline",
            "Bridge",
            "CLI",
            "ELT",
            "Processing",
        ]
        for namespace in expected_sub_namespaces:
            tm.that(hasattr(t.Meltano, namespace), eq=True)

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
        project = {"name": "elt-project", "enabled": True}
        tm.that(plugin_def["name"], eq="tap-users")
        tm.that(isinstance(plugin_def["variants"], list), eq=True)
        tm.that(catalog["tap_stream_id"], eq="users")
        tm.that(isinstance(catalog["schema"], dict), eq=True)
        tm.that(project["enabled"] is True, eq=True)

    def test_export_completeness(self) -> None:
        """Test that all necessary types are exported."""
        tm.that(t, none=False)

    def test_type_hierarchy(self) -> None:
        """Test that type hierarchy is properly structured."""
        tm.that(hasattr(t.Meltano, "PluginDefinition"), eq=True)
        singer_namespace = t.Meltano.Singer
        tm.that(hasattr(singer_namespace, "Record"), eq=True)

    def test_type_consistency(self) -> None:
        """Test that types are consistent across the namespace."""
        plugin_definition = t.Meltano.PluginDefinition
        singer_catalog = t.Meltano.Singer.CatalogEntry
        tm.that(plugin_definition, none=False)
        tm.that(singer_catalog, none=False)
