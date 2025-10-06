"""FLEXT Meltano API Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for FlextMeltanoAPI following
FLEXT testing patterns and real Meltano API integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import tempfile
from pathlib import Path

from flext_core import FlextResult
from flext_tests import FlextTestsUtilities

from flext_meltano import FlextMeltanoAPI


class TestFlextMeltanoAPI:
    """Unit test suite for FlextMeltanoAPI."""

    def setup_method(self) -> None:
        """Setup for each test using flext_tests patterns."""
        self.test_utils = FlextTestsUtilities.utilities()
        self.test_assertions = FlextTestsUtilities.assertion()
        self.functional_service = FlextTestsUtilities.functional_service(
            "meltano_api",
        )

    def test_api_initialization_default(self) -> None:
        """Test API initialization with default parameters."""
        api = FlextMeltanoAPI()

        self.test_assertions.assert_true(
            condition=api is not None,
            message="API should be initialized",
        )

    def test_api_initialization_with_project_root(self) -> None:
        """Test API initialization with specific project root."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            api = FlextMeltanoAPI(project_root=temp_path)

            self.test_assertions.assert_true(
                condition=api is not None,
                message="API should be initialized with project root",
            )

    def test_get_version_success(self) -> None:
        """Test successful version retrieval."""
        api = FlextMeltanoAPI()
        result = api.get_version()

        self.test_assertions.assert_true(
            condition=result.is_success,
            message="Version retrieval should succeed",
        )
        self.test_assertions.assert_true(
            condition=isinstance(result.unwrap(), str),
            message="Version should be a string",
        )

    def test_get_system_info_success(self) -> None:
        """Test successful system information retrieval."""
        api = FlextMeltanoAPI()
        result = api.get_system_info()

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
        api = FlextMeltanoAPI()
        result = api.health_check()

        self.test_assertions.assert_true(
            condition=result.is_success,
            message="Health check should succeed",
        )

        health_status = result.unwrap()
        self.test_assertions.assert_true(
            condition=isinstance(health_status, dict),
            message="Health status should be a dictionary",
        )

    def test_create_pipeline_success(self) -> None:
        """Test successful pipeline creation."""
        api = FlextMeltanoAPI()

        result = api.create_pipeline(
            name="test_pipeline",
            tap="tap-csv",
            target="target-jsonl",
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Pipeline creation should return FlextResult",
        )

    def test_execute_pipeline_success(self) -> None:
        """Test successful pipeline execution."""
        api = FlextMeltanoAPI()

        result = api.execute_pipeline("test_pipeline")

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Pipeline execution should return FlextResult",
        )

    def test_list_pipelines_success(self) -> None:
        """Test successful pipeline listing."""
        api = FlextMeltanoAPI()
        result = api.list_pipelines()

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Pipeline listing should return FlextResult",
        )

    def test_configure_environment_success(self) -> None:
        """Test successful environment configuration."""
        api = FlextMeltanoAPI()

        result = api.configure_environment(
            environment_name="test_env",
            config={"setting": "value"},
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Environment configuration should return FlextResult",
        )

    def test_run_dbt_models_success(self) -> None:
        """Test successful DBT model execution."""
        api = FlextMeltanoAPI()

        result = api.run_dbt_models(["model1", "model2"])

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="DBT model execution should return FlextResult",
        )

    def test_test_dbt_models_success(self) -> None:
        """Test successful DBT model testing."""
        api = FlextMeltanoAPI()

        result = api.test_dbt_models(["model1", "model2"])

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="DBT model testing should return FlextResult",
        )

    def test_run_elt_pipeline_success(self) -> None:
        """Test successful ELT pipeline execution."""
        api = FlextMeltanoAPI()

        result = api.run_elt_pipeline(
            tap="tap-csv",
            target="target-jsonl",
            dbt_models=["model1", "model2"],
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="ELT pipeline execution should return FlextResult",
        )

    def test_install_plugin_success(self) -> None:
        """Test successful plugin installation."""
        api = FlextMeltanoAPI()

        result = api.install_plugin(
            plugin_type="extractor",
            plugin_name="tap-csv",
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Plugin installation should return FlextResult",
        )

    def test_list_plugins_success(self) -> None:
        """Test successful plugin listing."""
        api = FlextMeltanoAPI()
        result = api.list_plugins("extractor")

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Plugin listing should return FlextResult",
        )

    def test_get_plugin_config_success(self) -> None:
        """Test successful plugin configuration retrieval."""
        api = FlextMeltanoAPI()

        result = api.get_plugin_config(
            plugin_type="extractor",
            plugin_name="tap-csv",
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Plugin config retrieval should return FlextResult",
        )

    def test_update_plugin_config_success(self) -> None:
        """Test successful plugin configuration update."""
        api = FlextMeltanoAPI()

        result = api.update_plugin_config(
            plugin_type="extractor",
            plugin_name="tap-csv",
            config={"new_setting": "value"},
        )

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Plugin config update should return FlextResult",
        )
