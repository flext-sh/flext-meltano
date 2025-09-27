"""Comprehensive unit tests for FlextMeltanoService.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from unittest.mock import patch

from flext_core import FlextLogger, FlextService
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.services import FlextMeltanoService


class TestFlextMeltanoServiceInitialization:
    """Test FlextMeltanoService initialization and basic functionality."""

    def test_service_initialization_with_name_and_version(self) -> None:
        """Test service initializes correctly with name and version."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        assert service.service_name == "test_service"
        assert service.version == "1.0.0"
        assert service.logger is not None
        assert isinstance(service.logger, FlextLogger)

    def test_service_initialization_with_config(self) -> None:
        """Test service initializes correctly with configuration."""
        config = {
            "environment": "development",
            "project_root": "/tmp/test_project",
            "plugins": ["tap-postgres", "target-postgres"],
        }

        service = FlextMeltanoService(
            service_name="test_service", version="1.0.0", config=config
        )

        assert service.config == config
        assert service.config["environment"] == "development"

    def test_service_initialization_default_values(self) -> None:
        """Test service initializes with default values."""
        service = FlextMeltanoService()

        assert service.service_name == FlextMeltanoConstants.SERVICE_DEFAULT_NAME
        assert service.version == FlextMeltanoConstants.SERVICE_DEFAULT_VERSION
        assert service.config == {}

    def test_service_inheritance(self) -> None:
        """Test service properly inherits from FlextService."""
        service = FlextMeltanoService()

        assert isinstance(service, FlextService)
        assert hasattr(service, "execute")
        assert hasattr(service, "validate")
        assert hasattr(service, "get_status")


class TestFlextMeltanoServiceExecution:
    """Test service execution functionality."""

    def test_execute_success(self) -> None:
        """Test successful service execution."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        result = service.execute()

        assert result.is_success
        assert result.data is not None
        assert "execution_time" in result.data
        assert "status" in result.data

    def test_execute_with_config(self) -> None:
        """Test service execution with configuration."""
        config = {"environment": "development", "project_root": "/tmp/test_project"}

        service = FlextMeltanoService(
            service_name="test_service", version="1.0.0", config=config
        )

        result = service.execute()

        assert result.is_success
        assert result.data["config"] == config

    def test_execute_with_exception(self) -> None:
        """Test service execution with exception handling."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        with patch.object(service, "_execute_internal") as mock_execute:
            mock_execute.side_effect = Exception("Execution failed")

            result = service.execute()

            assert result.is_failure
            assert "Execution failed" in result.error


class TestFlextMeltanoServiceValidation:
    """Test service validation functionality."""

    def test_validate_success(self) -> None:
        """Test successful service validation."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        result = service.validate()

        assert result.is_success
        assert result.data is not None
        assert "validation_passed" in result.data

    def test_validate_with_config(self) -> None:
        """Test service validation with configuration."""
        config = {
            "environment": "development",
            "project_root": "/tmp/test_project",
            "plugins": ["tap-postgres"],
        }

        service = FlextMeltanoService(
            service_name="test_service", version="1.0.0", config=config
        )

        result = service.validate()

        assert result.is_success
        assert result.data["config_valid"] is True

    def test_validate_invalid_config(self) -> None:
        """Test service validation with invalid configuration."""
        config = {
            "environment": "",  # Invalid empty environment
            "project_root": "/tmp/test_project",
        }

        service = FlextMeltanoService(
            service_name="test_service", version="1.0.0", config=config
        )

        result = service.validate()

        assert result.is_failure
        assert "Invalid configuration" in result.error


class TestFlextMeltanoServiceStatus:
    """Test service status functionality."""

    def test_get_status_success(self) -> None:
        """Test successful status retrieval."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        result = service.get_status()

        assert result.is_success
        assert result.data is not None
        assert "service_name" in result.data
        assert "version" in result.data
        assert "status" in result.data
        assert result.data["service_name"] == "test_service"
        assert result.data["version"] == "1.0.0"

    def test_get_status_with_runtime_info(self) -> None:
        """Test status retrieval with runtime information."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        # Execute service to generate runtime info
        service.execute()

        result = service.get_status()

        assert result.is_success
        assert "last_execution_time" in result.data
        assert "execution_count" in result.data


class TestFlextMeltanoServiceConfiguration:
    """Test service configuration management."""

    def test_update_config_success(self) -> None:
        """Test successful configuration update."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        new_config = {"environment": "production", "project_root": "/tmp/prod_project"}

        result = service.update_config(new_config)

        assert result.is_success
        assert service.config == new_config

    def test_update_config_partial(self) -> None:
        """Test partial configuration update."""
        initial_config = {
            "environment": "development",
            "project_root": "/tmp/dev_project",
            "plugins": ["tap-postgres"],
        }

        service = FlextMeltanoService(
            service_name="test_service", version="1.0.0", config=initial_config
        )

        update_config = {"environment": "staging"}

        result = service.update_config(update_config)

        assert result.is_success
        assert service.config["environment"] == "staging"
        assert (
            service.config["project_root"] == "/tmp/dev_project"
        )  # Should remain unchanged
        assert service.config["plugins"] == ["tap-postgres"]  # Should remain unchanged

    def test_update_config_invalid(self) -> None:
        """Test configuration update with invalid values."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        invalid_config = {
            "environment": "",  # Invalid empty environment
            "project_root": "/tmp/test_project",
        }

        result = service.update_config(invalid_config)

        assert result.is_failure
        assert "Invalid configuration" in result.error

    def test_reset_config(self) -> None:
        """Test configuration reset."""
        initial_config = {
            "environment": "development",
            "project_root": "/tmp/dev_project",
        }

        service = FlextMeltanoService(
            service_name="test_service", version="1.0.0", config=initial_config
        )

        result = service.reset_config()

        assert result.is_success
        assert service.config == {}


class TestFlextMeltanoServicePluginManagement:
    """Test plugin management functionality."""

    def test_install_plugin_success(self) -> None:
        """Test successful plugin installation."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        plugin_config = FlextMeltanoModels.PluginModel(
            name="tap-postgres",
            namespace="tap_postgres",
            pip_url="pipelinewise-tap-postgres",
        )

        result = service.install_plugin(plugin_config)

        assert result.is_success
        assert result.data is not None
        assert "plugin_installed" in result.data

    def test_install_plugin_invalid_config(self) -> None:
        """Test plugin installation with invalid config."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        # Create invalid plugin config
        plugin_config = FlextMeltanoModels.PluginModel(
            name="",  # Invalid empty name
            namespace="tap_postgres",
        )

        result = service.install_plugin(plugin_config)

        assert result.is_failure
        assert "Plugin name cannot be empty" in result.error

    def test_uninstall_plugin_success(self) -> None:
        """Test successful plugin uninstallation."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        result = service.uninstall_plugin("tap-postgres")

        assert result.is_success
        assert result.data is not None
        assert "plugin_uninstalled" in result.data

    def test_uninstall_plugin_empty_name(self) -> None:
        """Test plugin uninstallation with empty name."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        result = service.uninstall_plugin("")

        assert result.is_failure
        assert "Plugin name cannot be empty" in result.error

    def test_list_plugins_success(self) -> None:
        """Test successful plugin listing."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        result = service.list_plugins()

        assert result.is_success
        assert result.data is not None
        assert "plugins" in result.data
        assert isinstance(result.data["plugins"], list)


class TestFlextMeltanoServicePipelineManagement:
    """Test pipeline management functionality."""

    def test_create_pipeline_success(self) -> None:
        """Test successful pipeline creation."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        tap_config = FlextMeltanoModels.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost", "port": 5432},
        )

        target_config = FlextMeltanoModels.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "localhost", "port": 5432},
        )

        result = service.create_pipeline(tap_config, target_config)

        assert result.is_success
        assert result.data is not None
        assert "pipeline_created" in result.data

    def test_create_pipeline_invalid_configs(self) -> None:
        """Test pipeline creation with invalid configs."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        # Create invalid tap config
        tap_config = FlextMeltanoModels.TapConfig(
            tap_type="tap-postgres",
            connection_config={},  # Invalid empty config
        )

        target_config = FlextMeltanoModels.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "localhost", "port": 5432},
        )

        result = service.create_pipeline(tap_config, target_config)

        assert result.is_failure
        assert "Connection configuration cannot be empty" in result.error

    def test_run_pipeline_success(self) -> None:
        """Test successful pipeline execution."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        tap_config = FlextMeltanoModels.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost", "port": 5432},
        )

        target_config = FlextMeltanoModels.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "localhost", "port": 5432},
        )

        result = service.run_pipeline(tap_config, target_config)

        assert result.is_success
        assert result.data is not None
        assert "pipeline_executed" in result.data

    def test_run_pipeline_invalid_configs(self) -> None:
        """Test pipeline execution with invalid configs."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        # Create invalid target config
        tap_config = FlextMeltanoModels.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost", "port": 5432},
        )

        target_config = FlextMeltanoModels.TargetConfig(
            target_type="target-postgres",
            connection_config={},  # Invalid empty config
        )

        result = service.run_pipeline(tap_config, target_config)

        assert result.is_failure
        assert "Connection configuration cannot be empty" in result.error

    def test_get_pipeline_status_success(self) -> None:
        """Test successful pipeline status retrieval."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        result = service.get_pipeline_status("pipeline-001")

        assert result.is_success
        assert result.data is not None
        assert "pipeline_id" in result.data
        assert "status" in result.data

    def test_get_pipeline_status_empty_id(self) -> None:
        """Test pipeline status retrieval with empty ID."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        result = service.get_pipeline_status("")

        assert result.is_failure
        assert "Pipeline ID cannot be empty" in result.error


class TestFlextMeltanoServiceErrorHandling:
    """Test error handling and edge cases."""

    def test_service_exception_handling(self) -> None:
        """Test service handles exceptions gracefully."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        with patch.object(service, "_execute_internal") as mock_execute:
            mock_execute.side_effect = Exception("Unexpected error")

            result = service.execute()

            assert result.is_failure
            assert "Unexpected error" in result.error

    def test_service_timeout_handling(self) -> None:
        """Test service handles timeouts gracefully."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        with patch.object(service, "_execute_internal") as mock_execute:
            mock_execute.side_effect = TimeoutError("Operation timed out")

            result = service.execute()

            assert result.is_failure
            assert "Operation timed out" in result.error

    def test_service_validation_error_handling(self) -> None:
        """Test service handles validation errors gracefully."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        with patch.object(service, "_validate_internal") as mock_validate:
            mock_validate.side_effect = ValueError("Validation failed")

            result = service.validate()

            assert result.is_failure
            assert "Validation failed" in result.error


class TestFlextMeltanoServiceIntegration:
    """Integration tests for FlextMeltanoService."""

    def test_complete_service_lifecycle(self) -> None:
        """Test complete service lifecycle."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        # 1. Validate service
        validation_result = service.validate()
        assert validation_result.is_success

        # 2. Execute service
        execution_result = service.execute()
        assert execution_result.is_success

        # 3. Get status
        status_result = service.get_status()
        assert status_result.is_success
        assert status_result.data["service_name"] == "test_service"

        # 4. Update configuration
        config_update = {"environment": "production"}
        update_result = service.update_config(config_update)
        assert update_result.is_success
        assert service.config["environment"] == "production"

        # 5. Reset configuration
        reset_result = service.reset_config()
        assert reset_result.is_success
        assert service.config == {}

    def test_service_with_plugin_workflow(self) -> None:
        """Test service with plugin management workflow."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        # 1. Install plugin
        plugin_config = FlextMeltanoModels.PluginModel(
            name="tap-postgres", namespace="tap_postgres"
        )
        install_result = service.install_plugin(plugin_config)
        assert install_result.is_success

        # 2. List plugins
        list_result = service.list_plugins()
        assert list_result.is_success
        assert "plugins" in list_result.data

        # 3. Uninstall plugin
        uninstall_result = service.uninstall_plugin("tap-postgres")
        assert uninstall_result.is_success

    def test_service_with_pipeline_workflow(self) -> None:
        """Test service with pipeline management workflow."""
        service = FlextMeltanoService(service_name="test_service", version="1.0.0")

        # 1. Create pipeline
        tap_config = FlextMeltanoModels.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost", "port": 5432},
        )
        target_config = FlextMeltanoModels.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "localhost", "port": 5432},
        )

        create_result = service.create_pipeline(tap_config, target_config)
        assert create_result.is_success

        # 2. Run pipeline
        run_result = service.run_pipeline(tap_config, target_config)
        assert run_result.is_success

        # 3. Get pipeline status
        status_result = service.get_pipeline_status("pipeline-001")
        assert status_result.is_success
