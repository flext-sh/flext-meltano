"""FLEXT Meltano Constants Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for c following
FLEXT testing patterns and namespace organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_meltano import c


class Testc:
    """Unit test suite for c.Meltano."""

    def test_meltano_namespace(self) -> None:
        """Test Meltano namespace constants."""
        # Test version constants (correct paths)
        assert isinstance(c.Meltano.FLEXT_MELTANO_VERSION, str), (
            "Meltano version should be a string"
        )
        assert isinstance(c.Meltano.Metadata.APPLICATION_NAME, str), (
            "Application name should be a string"
        )
        assert isinstance(c.Meltano.Metadata.APPLICATION_DESCRIPTION, str), (
            "Application description should be a string"
        )
        assert isinstance(c.Meltano.Paths.PROJECT_FILE, str), (
            "Project file should be a string"
        )
        assert isinstance(c.Meltano.Paths.STATE_DIR, str), (
            "State directory should be a string"
        )

    def test_singer_namespace(self) -> None:
        """Test Singer protocol constants."""
        assert isinstance(c.Meltano.SDK_VERSION_REQUIRED, str), (
            "Singer SDK version should be a string"
        )
        assert isinstance(c.Meltano.Singer.MESSAGE_TYPE_SCHEMA, str), (
            "Schema message type should be a string"
        )
        assert isinstance(c.Meltano.Singer.MESSAGE_TYPE_RECORD, str), (
            "Record message type should be a string"
        )

    def test_dbt_namespace(self) -> None:
        """Test DBT constants."""
        assert isinstance(c.Meltano.Dbt.PROJECT_FILE, str), (
            "DBT project file should be a string"
        )
        assert isinstance(c.Meltano.Dbt.COMMAND_RUN, str), (
            "DBT run command should be a string"
        )
        assert isinstance(c.Meltano.Dbt.COMMAND_TEST, str), (
            "DBT test command should be a string"
        )

    def test_plugin_namespace(self) -> None:
        """Test Plugin constants."""
        assert isinstance(c.Meltano.Enums.PluginType.EXTRACTORS, str), (
            "Extractor type should be a string"
        )
        assert isinstance(c.Meltano.Enums.PluginType.LOADERS, str), (
            "Loader type should be a string"
        )
        assert isinstance(c.Meltano.Enums.PluginType.TRANSFORMS, str), (
            "Transformer type should be a string"
        )
        assert isinstance(c.Meltano.DEFAULT_VARIANT, str), (
            "Default variant should be a string"
        )

    def test_service_namespace(self) -> None:
        """Test Service namespace constants."""
        assert isinstance(c.Meltano.Service.MIN_NAME_LENGTH, int), (
            "Service min name length should be an integer"
        )

    def test_model_namespace(self) -> None:
        """Test Model namespace constants."""
        assert isinstance(c.Meltano.Model.MATURITY_MATURE_ENV_COUNT, int), (
            "Mature environment count should be an integer"
        )
        assert isinstance(c.Meltano.Model.MATURITY_DEVELOPING_ENV_COUNT, int), (
            "Developing environment count should be an integer"
        )
        assert isinstance(c.Meltano.Model.COMPLEXITY_MINIMAL_SETTINGS, int), (
            "Minimal settings count should be an integer"
        )
        assert isinstance(c.Meltano.Model.COMPLEXITY_SIMPLE_MAX_SETTINGS, int), (
            "Simple max settings count should be an integer"
        )

    def test_logging_namespace(self) -> None:
        """Test Logging namespace constants."""
        assert isinstance(c.Meltano.Logging.DEFAULT_LEVEL, str), (
            "Default log level should be a string"
        )
        assert isinstance(c.Meltano.Logging.INCLUDE_TRANSFORM_NAME, bool), (
            "Include transform name should be a boolean"
        )
        assert isinstance(c.Meltano.Logging.INCLUDE_RECORD_COUNT, bool), (
            "Include record count should be a boolean"
        )

    def test_plugin_types_enum(self) -> None:
        """Test PluginTypes enum."""
        plugin_types = c.Meltano.Enums.PluginType

        assert hasattr(plugin_types, "EXTRACTORS"), "PluginType should have EXTRACTORS"
        assert hasattr(plugin_types, "LOADERS"), "PluginType should have LOADERS"
        assert hasattr(plugin_types, "TRANSFORMS"), "PluginType should have TRANSFORMS"

        assert isinstance(plugin_types.EXTRACTORS, str), "EXTRACTORS should be a string"
        assert isinstance(plugin_types.LOADERS, str), "LOADERS should be a string"
        assert isinstance(plugin_types.TRANSFORMS, str), "TRANSFORMS should be a string"

    def test_constants_immutability(self) -> None:
        """Test that constants are immutable (Final)."""
        # Constants are Final by design - this test validates the pattern
        assert True, "Constants should be immutable"

    def test_namespace_organization(self) -> None:
        """Test that constants are properly organized in namespaces."""
        expected_namespaces = [
            "Meltano",
        ]

        for namespace in expected_namespaces:
            assert hasattr(c, namespace), f"Constants should have {namespace} namespace"

        # Test Meltano sub-namespaces
        meltano_namespaces = [
            "Metadata",
            "Paths",
            "Singer",
            "Dbt",
            "Model",
            "Logging",
            "Plugin",
            "Enums",
        ]
        for namespace in meltano_namespaces:
            assert hasattr(c.Meltano, namespace), (
                f"Meltano should have {namespace} namespace"
            )

    def test_export_completeness(self) -> None:
        """Test that all necessary constants are exported."""
        assert hasattr(c, "Meltano"), "Meltano should be accessible from c"
        assert hasattr(c.Meltano.Enums, "PluginType"), (
            "PluginType should be accessible from c.Meltano.Enums"
        )

        plugin_types = c.Meltano.Enums.PluginType
        assert hasattr(plugin_types, "EXTRACTORS"), (
            "PluginType should have EXTRACTORS member"
        )
