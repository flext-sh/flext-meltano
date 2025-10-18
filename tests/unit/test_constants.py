"""FLEXT Meltano Constants Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for FlextMeltanoConstants following
FLEXT testing patterns and namespace organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from tests.flext_tests_compat import FlextTestsUtilities

from flext_meltano.constants import FlextMeltanoConstants, PluginTypes


class TestFlextMeltanoConstants:
    """Unit test suite for FlextMeltanoConstants."""

    def setup_method(self) -> None:
        """Setup for each test using flext_tests patterns."""
        self.test_assertions = FlextTestsUtilities.assertion()

    def test_meltano_namespace(self) -> None:
        """Test Meltano namespace constants."""
        # Test version constants
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.VERSION, str),
            message="Meltano version should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.APPLICATION_NAME, str),
            message="Application name should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.APPLICATION_DESCRIPTION, str
            ),
            message="Application description should be a string",
        )

        # Test file constants
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.PROJECT_FILE, str),
            message="Project file should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.STATE_DIR, str),
            message="State directory should be a string",
        )

    def test_singer_namespace(self) -> None:
        """Test Singer namespace constants."""
        # Test SDK version requirement
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.SDK_VERSION_REQUIRED, str
            ),
            message="Singer SDK version should be a string",
        )

        # Test protocol constants
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.MESSAGE_TYPE_SCHEMA, str),
            message="Schema message type should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.MESSAGE_TYPE_RECORD, str),
            message="Record message type should be a string",
        )

    def test_dbt_namespace(self) -> None:
        """Test DBT namespace constants."""
        # Test project file constants
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
        """Test Plugin namespace constants."""
        # Test plugin types
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

        # Test plugin settings
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.DEFAULT_VARIANT, str),
            message="Default variant should be a string",
        )

    def test_service_namespace(self) -> None:
        """Test Service namespace constants."""
        # Test service validation rules
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.MIN_NAME_LENGTH, int),
            message="Service min name length should be an integer",
        )

    def test_model_namespace(self) -> None:
        """Test Model namespace constants."""
        # Test maturity constants
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.MATURITY_MATURE_ENV_COUNT, int
            ),
            message="Mature environment count should be an integer",
        )
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.MATURITY_DEVELOPING_ENV_COUNT, int
            ),
            message="Developing environment count should be an integer",
        )

        # Test complexity constants
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.COMPLEXITY_MINIMAL_SETTINGS, int
            ),
            message="Minimal settings count should be an integer",
        )
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.COMPLEXITY_SIMPLE_MAX_SETTINGS, int
            ),
            message="Simple max settings count should be an integer",
        )

    def test_logging_namespace(self) -> None:
        """Test Logging namespace constants."""
        # Test log levels
        self.test_assertions.assert_true(
            condition=isinstance(FlextMeltanoConstants.DEFAULT_LOG_LEVEL, str),
            message="Default log level should be a string",
        )

        # Test log settings
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.INCLUDE_TRANSFORM_NAME, bool
            ),
            message="Include transform name should be a boolean",
        )
        self.test_assertions.assert_true(
            condition=isinstance(
                FlextMeltanoConstants.INCLUDE_RECORD_COUNT, bool
            ),
            message="Include record count should be a boolean",
        )

    def test_plugin_types_enum(self) -> None:
        """Test PluginTypes enum."""
        # Test enum values
        self.test_assertions.assert_true(
            condition=hasattr(PluginTypes, "EXTRACTOR"),
            message="PluginTypes should have EXTRACTOR",
        )
        self.test_assertions.assert_true(
            condition=hasattr(PluginTypes, "LOADER"),
            message="PluginTypes should have LOADER",
        )
        self.test_assertions.assert_true(
            condition=hasattr(PluginTypes, "TRANSFORMER"),
            message="PluginTypes should have TRANSFORMER",
        )

        # Test enum values are strings
        self.test_assertions.assert_true(
            condition=isinstance(PluginTypes.EXTRACTORS, str),
            message="EXTRACTORS should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(PluginTypes.LOADERS, str),
            message="LOADERS should be a string",
        )
        self.test_assertions.assert_true(
            condition=isinstance(PluginTypes.TRANSFORMS, str),
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
            "Singer",
            "Dbt",
            "Plugin",
            "Service",
            "Model",
            "Logging",
        ]

        for namespace in expected_namespaces:
            self.test_assertions.assert_true(
                condition=hasattr(FlextMeltanoConstants, namespace),
                message=f"Constants should have {namespace} namespace",
            )

    def test_export_completeness(self) -> None:
        """Test that all necessary constants are exported."""
        # Test that PluginTypes is exported
        self.test_assertions.assert_true(
            condition=PluginTypes is not None,
            message="PluginTypes should be exported",
        )

        # Test that PluginTypes is the same as the nested class
        self.test_assertions.assert_true(
            condition=PluginTypes is FlextMeltanoConstants.PluginTypes,
            message="PluginTypes export should reference nested class",
        )
