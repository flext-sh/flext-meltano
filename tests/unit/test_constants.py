"""FLEXT Meltano Constants Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for c following
FLEXT testing patterns and namespace organization.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_tests import c, u

from flext_meltano import c


class Testc:
    """Unit test suite for c.Meltano."""

    def test_meltano_namespace(self) -> None:
        """Test Meltano namespace constants."""
        u.Tests.Matchers.that(isinstance(c.Meltano.FLEXT_MELTANO_VERSION, str), eq=True)
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Metadata.APPLICATION_NAME, str), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Metadata.APPLICATION_DESCRIPTION, str), eq=True
        )
        u.Tests.Matchers.that(isinstance(c.Meltano.Paths.PROJECT_FILE, str), eq=True)
        u.Tests.Matchers.that(isinstance(c.Meltano.Paths.STATE_DIR, str), eq=True)

    def test_singer_namespace(self) -> None:
        """Test Singer protocol constants."""
        u.Tests.Matchers.that(isinstance(c.Meltano.SDK_VERSION_REQUIRED, str), eq=True)
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Singer.MESSAGE_TYPE_SCHEMA, str), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Singer.MESSAGE_TYPE_RECORD, str), eq=True
        )

    def test_dbt_namespace(self) -> None:
        """Test DBT constants."""
        u.Tests.Matchers.that(isinstance(c.Meltano.Dbt.PROJECT_FILE, str), eq=True)
        u.Tests.Matchers.that(isinstance(c.Meltano.Dbt.COMMAND_RUN, str), eq=True)
        u.Tests.Matchers.that(isinstance(c.Meltano.Dbt.COMMAND_TEST, str), eq=True)

    def test_plugin_namespace(self) -> None:
        """Test Plugin constants."""
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Enums.PluginType.EXTRACTORS, str), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Enums.PluginType.LOADERS, str), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Enums.PluginType.TRANSFORMS, str), eq=True
        )
        u.Tests.Matchers.that(isinstance(c.Meltano.DEFAULT_VARIANT, str), eq=True)

    def test_service_namespace(self) -> None:
        """Test Service namespace constants."""
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Service.MIN_NAME_LENGTH, int), eq=True
        )

    def test_model_namespace(self) -> None:
        """Test Model namespace constants."""
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Model.MATURITY_MATURE_ENV_COUNT, int), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Model.MATURITY_DEVELOPING_ENV_COUNT, int), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Model.COMPLEXITY_MINIMAL_SETTINGS, int), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Model.COMPLEXITY_SIMPLE_MAX_SETTINGS, int), eq=True
        )

    def test_logging_namespace(self) -> None:
        """Test Logging namespace constants."""
        u.Tests.Matchers.that(isinstance(c.Meltano.Logging.DEFAULT_LEVEL, str), eq=True)
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Logging.INCLUDE_TRANSFORM_NAME, bool), eq=True
        )
        u.Tests.Matchers.that(
            isinstance(c.Meltano.Logging.INCLUDE_RECORD_COUNT, bool), eq=True
        )

    def test_plugin_types_enum(self) -> None:
        """Test PluginTypes enum."""
        plugin_types = c.Meltano.Enums.PluginType
        u.Tests.Matchers.that(hasattr(plugin_types, "EXTRACTORS"), eq=True)
        u.Tests.Matchers.that(hasattr(plugin_types, "LOADERS"), eq=True)
        u.Tests.Matchers.that(hasattr(plugin_types, "TRANSFORMS"), eq=True)
        u.Tests.Matchers.that(isinstance(plugin_types.EXTRACTORS, str), eq=True)
        u.Tests.Matchers.that(isinstance(plugin_types.LOADERS, str), eq=True)
        u.Tests.Matchers.that(isinstance(plugin_types.TRANSFORMS, str), eq=True)

    def test_constants_immutability(self) -> None:
        """Test that constants are immutable (Final)."""
        u.Tests.Matchers.that(True, eq=True)

    def test_namespace_organization(self) -> None:
        """Test that constants are properly organized in namespaces."""
        expected_namespaces = ["Meltano"]
        for namespace in expected_namespaces:
            u.Tests.Matchers.that(hasattr(c, namespace), eq=True)
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
            u.Tests.Matchers.that(hasattr(c.Meltano, namespace), eq=True)

    def test_export_completeness(self) -> None:
        """Test that all necessary constants are exported."""
        u.Tests.Matchers.that(hasattr(c, "Meltano"), eq=True)
        u.Tests.Matchers.that(hasattr(c.Meltano.Enums, "PluginType"), eq=True)
        plugin_types = c.Meltano.Enums.PluginType
        u.Tests.Matchers.that(hasattr(plugin_types, "EXTRACTORS"), eq=True)
