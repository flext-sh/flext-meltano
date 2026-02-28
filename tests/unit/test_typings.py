"""FLEXT Meltano Typings Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for t following
FLEXT testing patterns and namespace organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_meltano import t


class TestFlextMeltanoTypes:
    """Unit test suite for FlextMeltanoTypes."""

    def test_meltano_namespace_exists(self) -> None:
        """Test that Meltano namespace exists as top-level namespace."""
        assert hasattr(t, "Meltano"), "Meltano namespace should exist"

    def test_plugin_namespace(self) -> None:
        """Test Plugin sub-namespace within Meltano."""
        assert hasattr(t.Meltano, "Plugin"), (
            "Plugin namespace should exist under Meltano"
        )
        plugin_types = t.Meltano.Plugin
        assert hasattr(plugin_types, "PluginDefinition"), (
            "PluginDefinition should exist in Plugin namespace"
        )

    def test_plugin_types_direct(self) -> None:
        """Test Plugin types are also directly on Meltano namespace."""
        assert hasattr(t.Meltano, "PluginDefinition"), (
            "PluginDefinition should exist directly on Meltano"
        )
        assert hasattr(t.Meltano, "PluginType"), (
            "PluginType should exist directly on Meltano"
        )
        assert hasattr(t.Meltano, "PluginVariant"), (
            "PluginVariant should exist directly on Meltano"
        )

    def test_singer_namespace(self) -> None:
        """Test Singer namespace types."""
        assert hasattr(t.Meltano, "Singer"), (
            "Singer namespace should exist under Meltano"
        )
        singer_types = t.Meltano.Singer
        assert hasattr(singer_types, "Record"), (
            "Record should exist in Singer namespace"
        )
        assert hasattr(singer_types, "Schema"), (
            "Schema should exist in Singer namespace"
        )
        assert hasattr(singer_types, "State"), "State should exist in Singer namespace"

    def test_dbt_namespace(self) -> None:
        """Test DBT namespace types."""
        assert hasattr(t.Meltano, "Dbt"), "Dbt namespace should exist under Meltano"
        dbt_types = t.Meltano.Dbt
        assert hasattr(dbt_types, "ModelConfiguration"), (
            "ModelConfiguration should exist in Dbt namespace"
        )
        assert hasattr(dbt_types, "TestConfiguration"), (
            "TestConfiguration should exist in Dbt namespace"
        )
        assert hasattr(dbt_types, "Project"), "Project should exist in Dbt namespace"

    def test_project_namespace(self) -> None:
        """Test Project namespace types."""
        assert hasattr(t.Meltano, "Project"), (
            "Project namespace should exist under Meltano"
        )
        project_types = t.Meltano.Project
        assert hasattr(project_types, "ProjectConfig"), (
            "ProjectConfig should exist in Project namespace"
        )
        assert hasattr(project_types, "ProjectMetadata"), (
            "ProjectMetadata should exist in Project namespace"
        )

    def test_pipeline_namespace(self) -> None:
        """Test Pipeline namespace types."""
        assert hasattr(t.Meltano, "Pipeline"), (
            "Pipeline namespace should exist under Meltano"
        )
        pipeline_types = t.Meltano.Pipeline
        assert hasattr(pipeline_types, "PipelineConfig"), (
            "PipelineConfig should exist in Pipeline namespace"
        )
        assert hasattr(pipeline_types, "PipelineStatus"), (
            "PipelineStatus should exist in Pipeline namespace"
        )

    def test_bridge_namespace(self) -> None:
        """Test Bridge namespace types."""
        assert hasattr(t.Meltano, "Bridge"), (
            "Bridge namespace should exist under Meltano"
        )
        bridge_types = t.Meltano.Bridge
        assert hasattr(bridge_types, "BridgeMessage"), (
            "BridgeMessage should exist in Bridge namespace"
        )
        assert hasattr(bridge_types, "BridgeResponse"), (
            "BridgeResponse should exist in Bridge namespace"
        )

    def test_cli_namespace(self) -> None:
        """Test CLI namespace types."""
        assert hasattr(t.Meltano, "CLI"), "CLI namespace should exist under Meltano"
        cli_types = t.Meltano.CLI
        assert hasattr(cli_types, "Command"), "Command should exist in CLI namespace"
        assert hasattr(cli_types, "CommandResult"), (
            "CommandResult should exist in CLI namespace"
        )

    def test_elt_namespace(self) -> None:
        """Test ELT namespace types."""
        assert hasattr(t.Meltano, "ELT"), "ELT namespace should exist under Meltano"
        elt_types = t.Meltano.ELT
        assert hasattr(elt_types, "ExtractConfig"), (
            "ExtractConfig should exist in ELT namespace"
        )
        assert hasattr(elt_types, "LoadConfig"), (
            "LoadConfig should exist in ELT namespace"
        )
        assert hasattr(elt_types, "TransformConfig"), (
            "TransformConfig should exist in ELT namespace"
        )

    def test_processing_namespace(self) -> None:
        """Test Processing namespace types."""
        assert hasattr(t.Meltano, "Processing"), (
            "Processing namespace should exist under Meltano"
        )
        processing_types = t.Meltano.Processing
        assert hasattr(processing_types, "SingerExecutionResult"), (
            "SingerExecutionResult should exist in Processing namespace"
        )
        assert hasattr(processing_types, "DbtTransformationResult"), (
            "DbtTransformationResult should exist in Processing namespace"
        )
        assert hasattr(processing_types, "EltPipelineResult"), (
            "EltPipelineResult should exist in Processing namespace"
        )

    def test_meltano_core_types(self) -> None:
        """Test Meltano core types (previously MeltanoCore)."""
        meltano_types = t.Meltano
        assert hasattr(meltano_types, "MeltanoConfigDict"), (
            "MeltanoConfigDict should exist in Meltano namespace"
        )
        assert hasattr(meltano_types, "PluginConfigDict"), (
            "PluginConfigDict should exist in Meltano namespace"
        )

    def test_type_annotations(self) -> None:
        """Test that type annotations are properly defined."""
        plugin_definition = t.Meltano.Plugin.PluginDefinition
        assert plugin_definition is not None, (
            "PluginDefinition should be properly annotated"
        )

        singer_catalog = t.Meltano.Singer.CatalogEntry
        assert singer_catalog is not None, (
            "Singer CatalogEntry should be properly annotated"
        )

    def test_namespace_organization(self) -> None:
        """Test that all expected sub-namespaces exist under Meltano."""
        expected_sub_namespaces = [
            "Plugin",
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
            assert hasattr(t.Meltano, namespace), (
                f"Meltano should have {namespace} sub-namespace"
            )

    def test_type_compatibility(self) -> None:
        """Test that types are compatible with their intended use."""
        plugin_def: t.Meltano.Plugin.PluginDefinition = {  # type: ignore[type-arg]
            "name": "tap-users",
            "variants": ["default"],
            "config": {"batch_size": 1000},
        }
        catalog: t.Meltano.Singer.CatalogEntry = {
            "tap_stream_id": "users",
            "schema": {"type": "object"},
        }
        project: dict[str, t.JsonValue] = {
            "name": "elt-project",
            "enabled": True,
        }

        assert plugin_def["name"] == "tap-users"
        assert isinstance(plugin_def["variants"], list)
        assert catalog["tap_stream_id"] == "users"
        assert isinstance(catalog["schema"], dict)
        assert project["enabled"] is True

    def test_export_completeness(self) -> None:
        """Test that all necessary types are exported."""
        assert t is not None, "t should be exported"

    def test_type_hierarchy(self) -> None:
        """Test that type hierarchy is properly structured."""
        plugin_namespace = t.Meltano.Plugin
        assert hasattr(plugin_namespace, "PluginDefinition"), (
            "Plugin namespace should contain PluginDefinition"
        )

        singer_namespace = t.Meltano.Singer
        assert hasattr(singer_namespace, "Record"), (
            "Singer namespace should contain Record"
        )

    def test_type_consistency(self) -> None:
        """Test that types are consistent across the namespace."""
        plugin_definition = t.Meltano.Plugin.PluginDefinition
        singer_catalog = t.Meltano.Singer.CatalogEntry

        assert plugin_definition is not None, "PluginDefinition should be a valid type"
        assert singer_catalog is not None, "Singer CatalogEntry should be a valid type"
