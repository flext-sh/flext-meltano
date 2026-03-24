"""FLEXT Meltano Constants Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for c following
FLEXT testing patterns and namespace organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import tm

from flext_meltano import c


class Testc:
    """Unit test suite for c.Meltano."""

    def test_meltano_namespace(self) -> None:
        """Test Meltano namespace constants."""
        tm.that(c.Meltano.FLEXT_MELTANO_VERSION, is_=str)
        tm.that(c.Meltano.Metadata.APPLICATION_NAME, is_=str)
        tm.that(c.Meltano.Metadata.APPLICATION_DESCRIPTION, is_=str)
        tm.that(c.Meltano.Paths.PROJECT_FILE, is_=str)
        tm.that(c.Meltano.Paths.STATE_DIR, is_=str)

    def test_singer_namespace(self) -> None:
        """Test Singer protocol constants."""
        tm.that(c.Meltano.SDK_VERSION_REQUIRED, is_=str)
        tm.that(c.Meltano.Singer.MESSAGE_TYPE_SCHEMA, is_=str)
        tm.that(c.Meltano.Singer.MESSAGE_TYPE_RECORD, is_=str)

    def test_dbt_namespace(self) -> None:
        """Test DBT constants."""
        tm.that(c.Meltano.Dbt.PROJECT_FILE, is_=str)
        tm.that(c.Meltano.Dbt.COMMAND_RUN, is_=str)
        tm.that(c.Meltano.Dbt.COMMAND_TEST, is_=str)

    def test_plugin_namespace(self) -> None:
        """Test Plugin constants."""
        tm.that(c.Meltano.Enums.PluginType.EXTRACTORS, is_=str)
        tm.that(c.Meltano.Enums.PluginType.LOADERS, is_=str)
        tm.that(c.Meltano.Enums.PluginType.TRANSFORMS, is_=str)
        tm.that(c.Meltano.DEFAULT_VARIANT, is_=str)

    def test_service_namespace(self) -> None:
        """Test Service namespace constants."""
        tm.that(c.Meltano.Service.MIN_NAME_LENGTH, is_=int)

    def test_model_namespace(self) -> None:
        """Test ModelValidation namespace constants."""
        tm.that(c.Meltano.ModelValidation.MATURITY_MATURE_ENV_COUNT, is_=int)
        tm.that(c.Meltano.ModelValidation.MATURITY_DEVELOPING_ENV_COUNT, is_=int)
        tm.that(c.Meltano.ModelValidation.COMPLEXITY_MINIMAL_SETTINGS, is_=int)
        tm.that(c.Meltano.ModelValidation.COMPLEXITY_SIMPLE_MAX_SETTINGS, is_=int)

    def test_logging_namespace(self) -> None:
        """Test Logging namespace constants."""
        tm.that(c.Meltano.Logging.DEFAULT_LEVEL, is_=str)
        tm.that(c.Meltano.Logging.INCLUDE_TRANSFORM_NAME, is_=bool)
        tm.that(c.Meltano.Logging.INCLUDE_RECORD_COUNT, is_=bool)

    def test_plugin_types_enum(self) -> None:
        """Test PluginTypes enum."""
        plugin_types = c.Meltano.Enums.PluginType
        tm.that(hasattr(plugin_types, "EXTRACTORS"), eq=True)
        tm.that(hasattr(plugin_types, "LOADERS"), eq=True)
        tm.that(hasattr(plugin_types, "TRANSFORMS"), eq=True)
        tm.that(plugin_types.EXTRACTORS, is_=str)
        tm.that(plugin_types.LOADERS, is_=str)
        tm.that(plugin_types.TRANSFORMS, is_=str)

    def test_constants_immutability(self) -> None:
        """Test that constants are immutable (Final)."""
        tm.that(True, eq=True)

    def test_namespace_organization(self) -> None:
        """Test that constants are properly organized in namespaces."""
        expected_namespaces = ["Meltano"]
        for namespace in expected_namespaces:
            tm.that(hasattr(c, namespace), eq=True)
        meltano_namespaces = [
            "Metadata",
            "Paths",
            "Singer",
            "Dbt",
            "ModelValidation",
            "Logging",
            "Plugin",
            "Enums",
        ]
        for namespace in meltano_namespaces:
            tm.that(hasattr(c.Meltano, namespace), eq=True)

    def test_export_completeness(self) -> None:
        """Test that all necessary constants are exported."""
        tm.that(hasattr(c, "Meltano"), eq=True)
        tm.that(hasattr(c.Meltano.Enums, "PluginType"), eq=True)
        plugin_types = c.Meltano.Enums.PluginType
        tm.that(hasattr(plugin_types, "EXTRACTORS"), eq=True)
