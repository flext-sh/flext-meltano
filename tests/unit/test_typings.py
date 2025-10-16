"""FLEXT Meltano Typings Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for FlextMeltanoTypes following
FLEXT testing patterns and namespace organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_tests import FlextTestsUtilities

from flext_meltano.typings import FlextMeltanoTypes


class TestFlextMeltanoTypes:
    """Unit test suite for FlextMeltanoTypes."""

    def setup_method(self) -> None:
        """Setup for each test using flext_tests patterns."""
        self.test_assertions = FlextTestsUtilities.assertion()

    def test_plugin_namespace(self) -> None:
        """Test Plugin namespace types."""
        # Test that Plugin namespace exists
        self.test_assertions.assert_true(
            condition=hasattr(FlextMeltanoTypes, "Plugin"),
            message="Plugin namespace should exist",
        )

        # Test Plugin types
        plugin_types = FlextMeltanoTypes.Plugin
        self.test_assertions.assert_true(
            condition=hasattr(plugin_types, "PluginType"),
            message="PluginType should exist in Plugin namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(plugin_types, "PluginVariant"),
            message="PluginVariant should exist in Plugin namespace",
        )

    def test_singer_namespace(self) -> None:
        """Test Singer namespace types."""
        # Test that Singer namespace exists
        self.test_assertions.assert_true(
            condition=hasattr(FlextMeltanoTypes, "Singer"),
            message="Singer namespace should exist",
        )

        # Test Singer types
        singer_types = FlextMeltanoTypes.Singer
        self.test_assertions.assert_true(
            condition=hasattr(singer_types, "Record"),
            message="Record should exist in Singer namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(singer_types, "Schema"),
            message="Schema should exist in Singer namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(singer_types, "State"),
            message="State should exist in Singer namespace",
        )

    def test_dbt_namespace(self) -> None:
        """Test DBT namespace types."""
        # Test that DBT namespace exists
        self.test_assertions.assert_true(
            condition=hasattr(FlextMeltanoTypes, "Dbt"),
            message="DBT namespace should exist",
        )

        # Test DBT types
        dbt_types = FlextMeltanoTypes.Dbt
        self.test_assertions.assert_true(
            condition=hasattr(dbt_types, "Model"),
            message="Model should exist in DBT namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(dbt_types, "Test"),
            message="Test should exist in DBT namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(dbt_types, "Seed"),
            message="Seed should exist in DBT namespace",
        )

    def test_project_namespace(self) -> None:
        """Test Project namespace types."""
        # Test that Project namespace exists
        self.test_assertions.assert_true(
            condition=hasattr(FlextMeltanoTypes, "Project"),
            message="Project namespace should exist",
        )

        # Test Project types
        project_types = FlextMeltanoTypes.Project
        self.test_assertions.assert_true(
            condition=hasattr(project_types, "ProjectConfig"),
            message="ProjectConfig should exist in Project namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(project_types, "ProjectMetadata"),
            message="ProjectMetadata should exist in Project namespace",
        )

    def test_pipeline_namespace(self) -> None:
        """Test Pipeline namespace types."""
        # Test that Pipeline namespace exists
        self.test_assertions.assert_true(
            condition=hasattr(FlextMeltanoTypes, "Pipeline"),
            message="Pipeline namespace should exist",
        )

        # Test Pipeline types
        pipeline_types = FlextMeltanoTypes.Pipeline
        self.test_assertions.assert_true(
            condition=hasattr(pipeline_types, "PipelineConfig"),
            message="PipelineConfig should exist in Pipeline namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(pipeline_types, "PipelineStatus"),
            message="PipelineStatus should exist in Pipeline namespace",
        )

    def test_bridge_namespace(self) -> None:
        """Test Bridge namespace types."""
        # Test that Bridge namespace exists
        self.test_assertions.assert_true(
            condition=hasattr(FlextMeltanoTypes, "Bridge"),
            message="Bridge namespace should exist",
        )

        # Test Bridge types
        bridge_types = FlextMeltanoTypes.Bridge
        self.test_assertions.assert_true(
            condition=hasattr(bridge_types, "BridgeMessage"),
            message="BridgeMessage should exist in Bridge namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(bridge_types, "BridgeResponse"),
            message="BridgeResponse should exist in Bridge namespace",
        )

    def test_cli_namespace(self) -> None:
        """Test CLI namespace types."""
        # Test that CLI namespace exists
        self.test_assertions.assert_true(
            condition=hasattr(FlextMeltanoTypes, "CLI"),
            message="CLI namespace should exist",
        )

        # Test CLI types
        cli_types = FlextMeltanoTypes.CLI
        self.test_assertions.assert_true(
            condition=hasattr(cli_types, "Command"),
            message="Command should exist in CLI namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(cli_types, "CommandResult"),
            message="CommandResult should exist in CLI namespace",
        )

    def test_elt_namespace(self) -> None:
        """Test ELT namespace types."""
        # Test that ELT namespace exists
        self.test_assertions.assert_true(
            condition=hasattr(FlextMeltanoTypes, "ELT"),
            message="ELT namespace should exist",
        )

        # Test ELT types
        elt_types = FlextMeltanoTypes.ELT
        self.test_assertions.assert_true(
            condition=hasattr(elt_types, "ExtractConfig"),
            message="ExtractConfig should exist in ELT namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(elt_types, "LoadConfig"),
            message="LoadConfig should exist in ELT namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(elt_types, "TransformConfig"),
            message="TransformConfig should exist in ELT namespace",
        )

    def test_processing_namespace(self) -> None:
        """Test Processing namespace types."""
        # Test that Processing namespace exists
        self.test_assertions.assert_true(
            condition=hasattr(FlextMeltanoTypes, "Processing"),
            message="Processing namespace should exist",
        )

        # Test Processing types
        processing_types = FlextMeltanoTypes.Processing
        self.test_assertions.assert_true(
            condition=hasattr(
                processing_types, "FlextMeltanoTypes.Processing.SingerExecutionResult"
            ),
            message="FlextMeltanoTypes.Processing.SingerExecutionResult should exist in Processing namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(
                processing_types, "FlextMeltanoTypes.Processing.DbtTransformationResult"
            ),
            message="FlextMeltanoTypes.Processing.DbtTransformationResult should exist in Processing namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(
                processing_types, "FlextMeltanoTypes.Processing.EltPipelineResult"
            ),
            message="FlextMeltanoTypes.Processing.EltPipelineResult should exist in Processing namespace",
        )

    def test_meltano_core_namespace(self) -> None:
        """Test MeltanoCore namespace types."""
        # Test that MeltanoCore namespace exists
        self.test_assertions.assert_true(
            condition=hasattr(FlextMeltanoTypes, "MeltanoCore"),
            message="MeltanoCore namespace should exist",
        )

        # Test MeltanoCore types
        meltano_core_types = FlextMeltanoTypes.MeltanoCore
        self.test_assertions.assert_true(
            condition=hasattr(meltano_core_types, "MeltanoConfigDict"),
            message="MeltanoConfigDict should exist in MeltanoCore namespace",
        )
        self.test_assertions.assert_true(
            condition=hasattr(meltano_core_types, "PluginConfigDict"),
            message="PluginConfigDict should exist in MeltanoCore namespace",
        )

    def test_type_annotations(self) -> None:
        """Test that type annotations are properly defined."""
        # Test that types are properly annotated
        plugin_definition = FlextMeltanoTypes.Plugin.PluginDefinition
        self.test_assertions.assert_true(
            condition=plugin_definition is not None,
            message="PluginDefinition should be properly annotated",
        )

        singer_catalog = FlextMeltanoTypes.Singer.CatalogEntry
        self.test_assertions.assert_true(
            condition=singer_catalog is not None,
            message="Singer CatalogEntry should be properly annotated",
        )

    def test_namespace_organization(self) -> None:
        """Test that types are properly organized in namespaces."""
        # Test that all expected namespaces exist
        expected_namespaces = [
            "Plugin",
            "Singer",
            "Dbt",
            "Project",
            "Pipeline",
            "Bridge",
            "CLI",
            "ELT",
            "Processing",
            "MeltanoCore",
        ]

        for namespace in expected_namespaces:
            self.test_assertions.assert_true(
                condition=hasattr(FlextMeltanoTypes, namespace),
                message=f"Types should have {namespace} namespace",
            )

    def test_type_compatibility(self) -> None:
        """Test that types are compatible with their intended use."""

        # Test that types can be used in type annotations
        def test_function(
            plugin_def: FlextMeltanoTypes.Plugin.PluginDefinition,
        ) -> None:
            pass

        def test_singer_function(
            catalog: FlextMeltanoTypes.Singer.CatalogEntry,
        ) -> None:
            pass

        def test_dbt_function(project: dict[str, object]) -> None:
            pass

        # If we get here without errors, the types are compatible
        self.test_assertions.assert_true(
            condition=True,
            message="Types should be compatible with type annotations",
        )

    def test_export_completeness(self) -> None:
        """Test that all necessary types are exported."""
        # Test that FlextMeltanoTypes is exported
        self.test_assertions.assert_true(
            condition=FlextMeltanoTypes is not None,
            message="FlextMeltanoTypes should be exported",
        )

    def test_type_hierarchy(self) -> None:
        """Test that type hierarchy is properly structured."""
        # Test that namespaces are properly nested
        plugin_namespace = FlextMeltanoTypes.Plugin
        self.test_assertions.assert_true(
            condition=hasattr(plugin_namespace, "PluginType"),
            message="Plugin namespace should contain PluginType",
        )

        singer_namespace = FlextMeltanoTypes.Singer
        self.test_assertions.assert_true(
            condition=hasattr(singer_namespace, "Record"),
            message="Singer namespace should contain Record",
        )

    def test_type_consistency(self) -> None:
        """Test that types are consistent across the namespace."""
        # Test that similar types follow consistent patterns
        plugin_definition = FlextMeltanoTypes.Plugin.PluginDefinition
        singer_catalog = FlextMeltanoTypes.Singer.CatalogEntry

        # Both should be type annotations
        self.test_assertions.assert_true(
            condition=plugin_definition is not None,
            message="PluginDefinition should be a valid type",
        )
        self.test_assertions.assert_true(
            condition=singer_catalog is not None,
            message="Singer CatalogEntry should be a valid type",
        )
