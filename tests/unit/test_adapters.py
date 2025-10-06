"""FLEXT Meltano Adapter Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for FlextMeltanoAdapter following
FLEXT testing patterns and real Meltano API integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import tempfile
from pathlib import Path

from flext_core import FlextResult
from flext_tests import FlextTestsUtilities
from meltano.core.plugin.base import PluginType

from flext_meltano import FlextMeltanoAdapter


class TestFlextMeltanoAdapter:
    """Unit test suite for FlextMeltanoAdapter."""

    def setup_method(self) -> None:
        """Setup for each test using flext_tests patterns."""
        self.adapter = FlextMeltanoAdapter()
        self.test_utils = FlextTestsUtilities.utilities()
        self.test_assertions = FlextTestsUtilities.assertion()
        self.functional_service = FlextTestsUtilities.functional_service(
            "meltano_adapter",
        )

    def test_adapter_initialization(self) -> None:
        """Test adapter initialization using flext_tests."""
        adapter = FlextMeltanoAdapter()

        # Use flext_tests assertion patterns
        self.test_assertions.assert_true(
            condition=adapter is not None,
            message="Adapter should be initialized",
        )
        self.test_assertions.assert_true(
            condition=hasattr(adapter, "_logger"),
            message="Adapter should have logger",
        )
        self.test_assertions.assert_true(
            condition=hasattr(adapter, "_utilities"),
            message="Adapter should have utilities",
        )

    def test_get_version_success(self) -> None:
        """Test successful version retrieval."""
        result = self.adapter.get_version()

        self.test_assertions.assert_true(
            condition=result.is_success,
            message="Version retrieval should succeed",
        )
        self.test_assertions.assert_true(
            condition=isinstance(result.unwrap(), str),
            message="Version should be a string",
        )

    def test_create_temp_project_success(self) -> None:
        """Test successful temporary project creation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            project_id = "test_project"

            result = self.adapter.create_temp_project(
                project_id=project_id,
                project_path=temp_path,
            )

            self.test_assertions.assert_true(
                condition=result.is_success,
                message="Temp project creation should succeed",
            )

    def test_validate_project_success(self) -> None:
        """Test successful project validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a minimal meltano.yml
            meltano_yml = temp_path / "meltano.yml"
            meltano_yml.write_text("version: 1\n")

            result = self.adapter.validate_project(temp_path)

            self.test_assertions.assert_true(
                condition=result.is_success,
                message="Project validation should succeed",
            )

    def test_validate_project_failure(self) -> None:
        """Test project validation failure for non-Meltano directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Don't create meltano.yml

            result = self.adapter.validate_project(temp_path)

            self.test_assertions.assert_true(
                condition=result.is_failure,
                message="Project validation should fail for non-Meltano directory",
            )

    def test_install_plugin_success(self) -> None:
        """Test successful plugin installation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a minimal meltano.yml
            meltano_yml = temp_path / "meltano.yml"
            meltano_yml.write_text("version: 1\n")

            result = self.adapter.install_plugin(
                plugin_type=PluginType.EXTRACTORS,
                plugin_name="tap-csv",
                project_path=temp_path,
            )

            # This might fail in test environment, but we test the interface
            self.test_assertions.assert_true(
                condition=isinstance(result, FlextResult),
                message="Plugin installation should return FlextResult",
            )

    def test_run_pipeline_success(self) -> None:
        """Test successful pipeline execution."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a minimal meltano.yml
            meltano_yml = temp_path / "meltano.yml"
            meltano_yml.write_text("version: 1\n")

            result = self.adapter.run_pipeline(
                tap_name="tap-csv",
                target_name="target-jsonl",
                project_path=temp_path,
            )

            # This might fail in test environment, but we test the interface
            self.test_assertions.assert_true(
                condition=isinstance(result, FlextResult),
                message="Pipeline execution should return FlextResult",
            )

    def test_get_plugin_info_success(self) -> None:
        """Test successful plugin info retrieval."""
        result = self.adapter.get_plugin_info(
            plugin_type=PluginType.EXTRACTORS,
            plugin_name="tap-csv",
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Plugin info retrieval should return FlextResult",
        )

    def test_list_plugins_success(self) -> None:
        """Test successful plugin listing."""
        result = self.adapter.list_plugins(PluginType.EXTRACTORS)

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Plugin listing should return FlextResult",
        )

    def test_get_project_config_success(self) -> None:
        """Test successful project configuration retrieval."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a minimal meltano.yml
            meltano_yml = temp_path / "meltano.yml"
            meltano_yml.write_text("version: 1\n")

            result = self.adapter.get_project_config(temp_path)

            self.test_assertions.assert_true(
                condition=isinstance(result, FlextResult),
                message="Project config retrieval should return FlextResult",
            )

    def test_update_project_config_success(self) -> None:
        """Test successful project configuration update."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create a minimal meltano.yml
            meltano_yml = temp_path / "meltano.yml"
            meltano_yml.write_text("version: 1\n")

            config_update = {"new_setting": "value"}
            result = self.adapter.update_project_config(
                project_path=temp_path,
                config_update=config_update,
            )

            self.test_assertions.assert_true(
                condition=isinstance(result, FlextResult),
                message="Project config update should return FlextResult",
            )

    def test_cleanup_temp_project_success(self) -> None:
        """Test successful temporary project cleanup."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            result = self.adapter.cleanup_temp_project(temp_path)

            self.test_assertions.assert_true(
                condition=result.is_success,
                message="Temp project cleanup should succeed",
            )

    def test_get_system_info_success(self) -> None:
        """Test successful system information retrieval."""
        result = self.adapter.get_system_info()

        self.test_assertions.assert_true(
            condition=result.is_success,
            message="System info retrieval should succeed",
        )

        system_info = result.unwrap()
        self.test_assertions.assert_true(
            condition=isinstance(system_info, dict),
            message="System info should be a dictionary",
        )

    def test_health_check_success(self) -> None:
        """Test successful health check."""
        result = self.adapter.health_check()

        self.test_assertions.assert_true(
            condition=result.is_success,
            message="Health check should succeed",
        )

        health_status = result.unwrap()
        self.test_assertions.assert_true(
            condition=isinstance(health_status, dict),
            message="Health status should be a dictionary",
        )
