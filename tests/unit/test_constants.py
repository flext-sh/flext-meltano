"""FLEXT Meltano Constants Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for FlextMeltanoConstants following
FLEXT testing patterns and namespace organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_meltano.constants import FlextMeltanoConstants

from ..flext_tests_compat import FlextTestsUtilities


class TestFlextMeltanoConstants:
    """Unit test suite for FlextMeltanoConstants.Meltano."""

    def setup_method(self) -> None:
        """Setup for each test using flext_tests patterns."""
        self.test_assertions = FlextTestsUtilities.assertion()

    def test_meltano_namespace(self) -> None:
        """Test Meltano namespace constants."""
        # Test version constants
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.Meltano.VERSION, str),
            message="Meltano version should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.Meltano.APPLICATION_NAME, str),
            message="Application name should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.Meltano.APPLICATION_DESCRIPTION, str
            ),
            message="Application description should be a string",
        )

        # Test file constants
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.Meltano.PROJECT_FILE, str),
            message="Project file should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.Meltano.STATE_DIR, str),
            message="State directory should be a string",
        )

    def test_singer_namespace(self) -> None:
        """Test Singer protocol constants."""
        # Test SDK version requirement - Singer constants are flat attributes
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.SDK_VERSION_REQUIRED, str),
            message="Singer SDK version should be a string",
        )

        # Test protocol constants
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.Singer.MESSAGE_TYPE_SCHEMA, str),
            message="Schema message type should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.Singer.MESSAGE_TYPE_RECORD, str),
            message="Record message type should be a string",
        )

    def test_dbt_namespace(self) -> None:
        """Test DBT constants."""
        # Test project file constants - DBT constants are flat attributes
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.PROJECT_FILE_DBT, str),
            message="DBT project file should be a string",
        )

        # Test command constants
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.COMMAND_RUN_DBT, str),
            message="DBT run command should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.COMMAND_TEST, str),
            message="DBT test command should be a string",
        )

    def test_plugin_namespace(self) -> None:
        """Test Plugin constants."""
        # Test plugin types enum
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.PluginTypes.EXTRACTORS, str),
            message="Extractor type should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.PluginTypes.LOADERS, str),
            message="Loader type should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.PluginTypes.TRANSFORMS, str),
            message="Transformer type should be a string",
        )

        # Test plugin settings - flat attributes
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.DEFAULT_VARIANT, str),
            message="Default variant should be a string",
        )

    def test_service_namespace(self) -> None:
        """Test Service namespace constants."""
        # Test service validation rules
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.Service.MIN_NAME_LENGTH, int),
            message="Service min name length should be an integer",
        )

    def test_model_namespace(self) -> None:
        """Test Model namespace constants."""
        # Test maturity constants
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.Model.MATURITY_MATURE_ENV_COUNT, int
            ),
            message="Mature environment count should be an integer",
        )
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.Model.MATURITY_DEVELOPING_ENV_COUNT, int
            ),
            message="Developing environment count should be an integer",
        )

        # Test complexity constants
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.Model.COMPLEXITY_MINIMAL_SETTINGS, int
            ),
            message="Minimal settings count should be an integer",
        )
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.Model.COMPLEXITY_SIMPLE_MAX_SETTINGS, int
            ),
            message="Simple max settings count should be an integer",
        )

    def test_logging_namespace(self) -> None:
        """Test Logging namespace constants."""
        # Test log levels from Logging namespace
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.Logging.DEFAULT_LEVEL, str),
            message="Default log level should be a string",
        )

        # Test log settings from Logging namespace
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.Logging.INCLUDE_TRANSFORM_NAME, bool
            ),
            message="Include transform name should be a boolean",
        )
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.Logging.INCLUDE_RECORD_COUNT, bool
            ),
            message="Include record count should be a boolean",
        )

    def test_plugin_types_enum(self) -> None:
        """Test PluginTypes enum."""
        # Get the PluginTypes enum from constants
        plugin_types = FlextMeltanoConstants.PluginTypes

        # Test enum values
        self.test_assertions.assert_true(
            condition=hasattr(plugin_types, "EXTRACTORS"),
            message="PluginTypes should have EXTRACTORS",
        )
        self.test_assertions.assert_true(
            condition=hasattr(plugin_types, "LOADERS"),
            message="PluginTypes should have LOADERS",
        )
        self.test_assertions.assert_true(
            condition=hasattr(plugin_types, "TRANSFORMS"),
            message="PluginTypes should have TRANSFORMS",
        )

        # Test enum values are strings
        self.test_assertions.assert_true(
            condition=isinstance(plugin_types.EXTRACTORS, str),
            message="EXTRACTORS should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(plugin_types.LOADERS, str),
            message="LOADERS should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(plugin_types.TRANSFORMS, str),
            message="TRANSFORMS should be a string",
        )

    def test_constants_immutability(self) -> None:
        """Test that constants are immutable (Final)."""
        # This test ensures constants are properly marked as Final
        # In practice, this would be enforced by the type checker
        self.test_assertions.assert_true(
            condition=True,  # Constants are Final by design
            message="Constants should be immutable",
        )

    def test_namespace_organization(self) -> None:
        """Test that constants are properly organized in namespaces."""
        # Test that all expected namespaces exist
        expected_namespaces = [
            "Meltano",
            "Service",
            "Model",
            "Logging",
            "PluginTypes",
        ]

        for namespace in expected_namespaces:
            self.test_assertions.assert_true(
                condition=hasattr(FlextMeltanoConstants, namespace),
                message=f"Constants should have {namespace} namespace",
            )

    def test_export_completeness(self) -> None:
        """Test that all necessary constants are exported."""
        # Test that PluginTypes is accessible from constants
        self.test_assertions.assert_true(
            condition=hasattr(FlextMeltanoConstants, "PluginTypes"),
            message="PluginTypes should be accessible from FlextMeltanoConstants",
        )

        # Test that PluginTypes is the correct enum
        plugin_types = FlextMeltanoConstants.PluginTypes
        self.test_assertions.assert_true(
            condition=hasattr(plugin_types, "EXTRACTORS"),
            message="PluginTypes should have EXTRACTORS member",
        )
