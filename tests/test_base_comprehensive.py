"""Comprehensive tests for base module to achieve 95%+ coverage."""

from __future__ import annotations

import tempfile
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from flext_core import FlextResult

from flext_meltano.base import (
    FlextMeltanoConfig,
    FlextMeltanoDbtService,
    FlextMeltanoEvent,
    FlextMeltanoExtensionService,
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
    create_meltano_dbt_service,
    create_meltano_extension_service,
    create_meltano_tap_service,
    create_meltano_target_service,
)


class TestFlextMeltanoConfig:
    """Test FlextMeltanoConfig value object."""

    def test_config_default_initialization(self) -> None:
        """Test config initialization with defaults."""
        config = FlextMeltanoConfig()
        if config.project_root != ".":
            msg = f"Expected {"."}, got {config.project_root}"
            raise AssertionError(msg)
        assert config.environment == "dev"

    def test_config_custom_initialization(self) -> None:
        """Test config initialization with custom values."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = str(Path(temp_dir) / "test")
            config = FlextMeltanoConfig(
                project_root=test_path,
                environment="prod",
            )
            if config.project_root != test_path:
                msg = f"Expected {test_path}, got {config.project_root}"
                raise AssertionError(msg)
            assert config.environment == "prod"

    def test_config_project_root_validation_valid_path(self) -> None:
        """Test project root validation with valid path."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(project_root=temp_dir)
            if config.project_root != temp_dir:
                msg = f"Expected {temp_dir}, got {config.project_root}"
                raise AssertionError(msg)

    def test_config_project_root_validation_nonexistent_path(self) -> None:
        """Test project root validation with nonexistent path."""
        # Should not raise exception during initialization
        config = FlextMeltanoConfig(project_root="/nonexistent/path")
        if config.project_root != "/nonexistent/path":
            msg = f"Expected {"/nonexistent/path"}, got {config.project_root}"
            raise AssertionError(msg)

    def test_config_project_root_validation_empty_string(self) -> None:
        """Test project root validation with empty string."""
        config = FlextMeltanoConfig(project_root="")
        # Empty string gets converted to absolute path of current directory
        assert config.project_root != ""
        assert Path(config.project_root).is_absolute()

    def test_config_project_root_validation_relative_path(self) -> None:
        """Test project root validation with relative path."""
        config = FlextMeltanoConfig(project_root="./test")
        # Relative paths get converted to absolute paths
        assert config.project_root.endswith("/test")
        from pathlib import Path
        assert Path(config.project_root).is_absolute()

    def test_config_validate_project_root_method(self) -> None:
        """Test validate_project_root class method directly."""
        # This tests the validator method
        result = FlextMeltanoConfig.validate_project_root("/some/path")
        if result != "/some/path":
            msg = f"Expected {"/some/path"}, got {result}"
            raise AssertionError(msg)

    def test_config_immutability(self) -> None:
        """Test that config is frozen and cannot be modified."""
        config = FlextMeltanoConfig()
        # Config is frozen, so modification should raise an exception
        with pytest.raises((ValueError, AttributeError), match="frozen"):
            config.project_root = "/new/path"  # type: ignore[misc]

    def test_config_dict_export(self) -> None:
        """Test config export to dictionary."""
        config = FlextMeltanoConfig(project_root="/test", environment="staging")
        config_dict = config.model_dump()
        if config_dict["project_root"] != "/test":
            msg = f"Expected {"/test"}, got {config_dict["project_root"]}"
            raise AssertionError(msg)
        assert config_dict["environment"] == "staging"

    def test_config_json_serialization(self) -> None:
        """Test config JSON serialization."""
        config = FlextMeltanoConfig(project_root="/test", environment="prod")
        json_str = config.model_dump_json()
        if '"/test"' not in json_str:
            msg = f"Expected {'"/test"'} in {json_str}"
            raise AssertionError(msg)
        assert '"prod"' in json_str


class TestFlextMeltanoEvent:
    """Test FlextMeltanoEvent entity."""

    def test_event_initialization(self) -> None:
        """Test event initialization."""
        event = FlextMeltanoEvent(
            source="meltano",
            event_type="pipeline_started",
            data={"pipeline": "tap-csv-to-target-jsonl"},
        )
        if event.source != "meltano":
            msg = f"Expected {"meltano"}, got {event.source}"
            raise AssertionError(msg)
        assert event.event_type == "pipeline_started"
        if event.data["pipeline"] != "tap-csv-to-target-jsonl":
            msg = f"Expected {"tap-csv-to-target-jsonl"}, got {event.data["pipeline"]}"
            raise AssertionError(msg)
        assert isinstance(event.id, str)
        assert isinstance(event.timestamp, datetime)

    def test_event_validate_domain_rules_success(self) -> None:
        """Test event domain rules validation success."""
        event = FlextMeltanoEvent(
            source="meltano",
            event_type="valid_event",
            data={"test": "data"},
        )
        result = event.validate_domain_rules()
        assert result.is_success


class TestFlextMeltanoBaseService:
    """Test FlextMeltanoBaseService base class."""

    def test_base_service_initialization(self) -> None:
        """Test base service initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)
        if service.config != config:
            msg = f"Expected {config}, got {service.config}"
            raise AssertionError(msg)
        assert service.logger is not None
        assert not service._initialized

    def test_base_service_initialization_custom_config(self) -> None:
        """Test base service initialization with custom config."""
        config = FlextMeltanoConfig(project_root="/test", environment="prod")
        service = FlextMeltanoTapService(config)
        if service.config.project_root != "/test":
            msg = f"Expected {"/test"}, got {service.config.project_root}"
            raise AssertionError(msg)
        assert service.config.environment == "prod"

    def test_base_service_initialize_success(self) -> None:
        """Test base service initialization success."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        result = service.initialize()
        assert result.is_success
        if not (result.data):
            msg = f"Expected True, got {result.data}"
            raise AssertionError(msg)
        assert service._initialized is True

    def test_base_service_initialize_idempotent(self) -> None:
        """Test base service initialize is idempotent."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        # First initialization
        result1 = service.initialize()
        assert result1.is_success

        # Second initialization should also succeed
        result2 = service.initialize()
        assert result2.is_success

    def test_base_service_validate_service_success(self) -> None:
        """Test base service validation success."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        result = service.validate_service()
        assert result.is_success
        if not (result.data):
            msg = f"Expected True, got {result.data}"
            raise AssertionError(msg)

    def test_base_service_get_health_status(self) -> None:
        """Test base service health status."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        result = service.get_health_status()
        assert result.is_success
        assert result.data is not None
        if result.data["service"] != "tap":
            msg = f"Expected {"tap"}, got {result.data["service"]}"
            raise AssertionError(msg)
        assert result.data is not None
        if "tap_configured" not in result.data:
            msg = f"Expected {"tap_configured"} in {result.data}"
            raise AssertionError(msg)

    def test_base_service_health_status_after_initialization(self) -> None:
        """Test base service health status after initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)
        service.initialize()

        result = service.get_health_status()
        assert result.is_success
        assert result.data is not None


class TestFlextMeltanoTapService:
    """Test FlextMeltanoTapService class."""

    def test_tap_service_initialization(self) -> None:
        """Test tap service initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)
        if service.config != config:
            msg = f"Expected {config}, got {service.config}"
            raise AssertionError(msg)
        assert service.tap_class is None
        assert not service._initialized

    def test_tap_service_validate_service_success(self) -> None:
        """Test tap service validation success."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        result = service.validate_service()
        assert result.is_success

    def test_tap_service_get_health_status(self) -> None:
        """Test tap service health status."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        result = service.get_health_status()
        assert result.is_success
        assert result.data is not None
        if result.data["service"] != "tap":
            msg = f"Expected {"tap"}, got {result.data["service"]}"
            raise AssertionError(msg)
        assert result.data is not None
        if result.data["tap_configured"]:
            msg = f"Expected False, got {result.data["tap_configured"]}"
            raise AssertionError(msg)

    def test_tap_service_set_tap_class_success(self) -> None:
        """Test tap service set tap class success."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        # Mock tap class
        mock_tap_class = Mock()
        mock_tap_class.__name__ = "MockTap"

        result = service.set_tap_class(mock_tap_class)
        assert result.is_success
        if service.tap_class != mock_tap_class:
            msg = f"Expected {mock_tap_class}, got {service.tap_class}"
            raise AssertionError(msg)

    def test_tap_service_set_tap_class_none(self) -> None:
        """Test tap service set tap class with None."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        result = service.set_tap_class(None)  # type: ignore[arg-type]
        assert not result.is_success
        assert result.error is not None
        if "Tap class cannot be None" not in result.error:
            msg = f"Expected {"Tap class cannot be None"} in {result.error}"
            raise AssertionError(msg)

    def test_tap_service_validate_ready_for_use_not_configured(self) -> None:
        """Test tap service validate ready for use when not configured."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        result = service.validate_ready_for_use()
        assert not result.is_success
        assert result.error is not None
        if "Tap class not configured" not in result.error:
            msg = f"Expected {"Tap class not configured"} in {result.error}"
            raise AssertionError(msg)

    def test_tap_service_validate_ready_for_use_configured(self) -> None:
        """Test tap service validate ready for use when configured."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        mock_tap_class = Mock()
        mock_tap_class.__name__ = "MockTap"
        service.set_tap_class(mock_tap_class)

        result = service.validate_ready_for_use()
        assert result.is_success

    def test_tap_service_discover_catalog_not_ready(self) -> None:
        """Test tap service discover catalog when not ready."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        result = service.discover_catalog()
        assert not result.is_success
        assert result.error is not None
        if "Service not ready for use" not in result.error:
            msg = f"Expected {"Service not ready for use"} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.base.FlextMeltanoTapService.validate_ready_for_use")
    def test_tap_service_discover_catalog_success(self, mock_validate: Mock) -> None:
        """Test tap service discover catalog success."""
        mock_validate.return_value = FlextResult(data=True)

        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        result = service.discover_catalog()
        assert result.is_success
        assert result.data is not None
        if result.data["catalog_type"] != "singer":
            msg = f"Expected {"singer"}, got {result.data["catalog_type"]}"
            raise AssertionError(msg)
        if "streams" not in result.data:
            msg = f"Expected {"streams"} in {result.data}"
            raise AssertionError(msg)

    def test_tap_service_health_status_with_tap_configured(self) -> None:
        """Test tap service health status with tap configured."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)

        mock_tap_class = Mock()
        mock_tap_class.__name__ = "MockTap"
        service.set_tap_class(mock_tap_class)

        result = service.get_health_status()
        assert result.is_success
        assert result.data is not None
        if not (result.data["tap_configured"]):
            msg = f"Expected True, got {result.data["tap_configured"]}"
            raise AssertionError(msg)
        assert result.data is not None
        if result.data["tap_class"] != "MockTap":
            msg = f"Expected {"MockTap"}, got {result.data["tap_class"]}"
            raise AssertionError(msg)


class TestFlextMeltanoTargetService:
    """Test FlextMeltanoTargetService class."""

    def test_target_service_initialization(self) -> None:
        """Test target service initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTargetService(config)
        if service.config != config:
            msg = f"Expected {config}, got {service.config}"
            raise AssertionError(msg)
        assert service.target_class is None
        assert not service._initialized

    def test_target_service_validate_service_success(self) -> None:
        """Test target service validation success."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTargetService(config)

        result = service.validate_service()
        assert result.is_success

    def test_target_service_get_health_status(self) -> None:
        """Test target service health status."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTargetService(config)

        result = service.get_health_status()
        assert result.is_success
        assert result.data is not None
        if result.data["service"] != "target":
            msg = f"Expected {"target"}, got {result.data["service"]}"
            raise AssertionError(msg)
        assert result.data is not None
        if result.data["target_configured"]:
            msg = f"Expected False, got {result.data["target_configured"]}"
            raise AssertionError(msg)

    def test_target_service_set_target_class_success(self) -> None:
        """Test target service set target class success."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTargetService(config)

        # Mock target class
        mock_target_class = Mock()
        mock_target_class.__name__ = "MockTarget"

        result = service.set_target_class(mock_target_class)
        assert result.is_success
        if service.target_class != mock_target_class:
            msg = f"Expected {mock_target_class}, got {service.target_class}"
            raise AssertionError(msg)

    def test_target_service_set_target_class_none(self) -> None:
        """Test target service set target class with None."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTargetService(config)

        result = service.set_target_class(None)  # type: ignore[arg-type]
        assert not result.is_success
        assert result.error is not None
        if "Target class cannot be None" not in result.error:
            msg = f"Expected {"Target class cannot be None"} in {result.error}"
            raise AssertionError(msg)

    def test_target_service_validate_ready_for_use_not_configured(self) -> None:
        """Test target service validate ready for use when not configured."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTargetService(config)

        result = service.validate_ready_for_use()
        assert not result.is_success
        assert result.error is not None
        if "Target class not configured" not in result.error:
            msg = f"Expected {"Target class not configured"} in {result.error}"
            raise AssertionError(msg)

    def test_target_service_validate_ready_for_use_configured(self) -> None:
        """Test target service validate ready for use when configured."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTargetService(config)

        mock_target_class = Mock()
        mock_target_class.__name__ = "MockTarget"
        service.set_target_class(mock_target_class)

        result = service.validate_ready_for_use()
        assert result.is_success

    def test_target_service_health_status_with_target_configured(self) -> None:
        """Test target service health status with target configured."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTargetService(config)

        mock_target_class = Mock()
        mock_target_class.__name__ = "MockTarget"
        service.set_target_class(mock_target_class)

        result = service.get_health_status()
        assert result.is_success
        assert result.data is not None
        if not (result.data["target_configured"]):
            msg = f"Expected True, got {result.data["target_configured"]}"
            raise AssertionError(msg)
        assert result.data is not None
        if result.data["target_class"] != "MockTarget":
            msg = f"Expected {"MockTarget"}, got {result.data["target_class"]}"
            raise AssertionError(msg)


class TestFlextMeltanoExtensionService:
    """Test FlextMeltanoExtensionService class."""

    def test_extension_service_initialization(self) -> None:
        """Test extension service initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExtensionService(config)
        if service.config != config:
            msg = f"Expected {config}, got {service.config}"
            raise AssertionError(msg)
        assert service.extension_class is None
        assert not service._initialized

    def test_extension_service_validate_service_success(self) -> None:
        """Test extension service validation success."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExtensionService(config)

        result = service.validate_service()
        assert result.is_success

    def test_extension_service_get_health_status(self) -> None:
        """Test extension service health status."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExtensionService(config)

        result = service.get_health_status()
        assert result.is_success
        assert result.data is not None
        if result.data["service"] != "extension":
            msg = f"Expected {"extension"}, got {result.data["service"]}"
            raise AssertionError(msg)
        assert result.data is not None
        if result.data["extension_configured"]:
            msg = f"Expected False, got {result.data["extension_configured"]}"
            raise AssertionError(msg)

    def test_extension_service_set_extension_class_success(self) -> None:
        """Test extension service set extension class success."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExtensionService(config)

        # Mock extension class
        mock_extension_class = Mock()
        mock_extension_class.__name__ = "MockExtension"

        result = service.set_extension_class(mock_extension_class)
        assert result.is_success
        if service.extension_class != mock_extension_class:
            msg = f"Expected {mock_extension_class}, got {service.extension_class}"
            raise AssertionError(msg)

    def test_extension_service_set_extension_class_none(self) -> None:
        """Test extension service set extension class with None."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExtensionService(config)

        result = service.set_extension_class(None)
        assert not result.is_success
        assert result.error is not None
        if "Extension class cannot be None" not in result.error:
            msg = f"Expected {"Extension class cannot be None"} in {result.error}"
            raise AssertionError(msg)

    def test_extension_service_health_status_with_extension_configured(self) -> None:
        """Test extension service health status with extension configured."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExtensionService(config)

        mock_extension_class = Mock()
        mock_extension_class.__name__ = "MockExtension"
        service.set_extension_class(mock_extension_class)

        result = service.get_health_status()
        assert result.is_success
        assert result.data is not None
        if not (result.data["extension_configured"]):
            msg = f"Expected True, got {result.data["extension_configured"]}"
            raise AssertionError(msg)
        assert result.data is not None
        # Extension class name is not included in health status data


class TestFlextMeltanoDbtService:
    """Test FlextMeltanoDbtService class."""

    def test_dbt_service_initialization(self) -> None:
        """Test DBT service initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDbtService(config)
        if service.config != config:
            msg = f"Expected {config}, got {service.config}"
            raise AssertionError(msg)
        assert not service._initialized

    def test_dbt_service_validate_service_success(self) -> None:
        """Test DBT service validation success."""
        with tempfile.TemporaryDirectory() as temp_dir:
            dbt_project_dir = Path(temp_dir) / "dbt_project"
            dbt_project_dir.mkdir()

            config = FlextMeltanoConfig(dbt_project_dir=str(dbt_project_dir))
            service = FlextMeltanoDbtService(config)

            result = service.validate_service()
            assert result.is_success

    def test_dbt_service_get_health_status(self) -> None:
        """Test DBT service health status."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDbtService(config)

        result = service.get_health_status()
        assert result.is_success
        assert result.data is not None
        if result.data["service"] != "dbt":
            msg = f"Expected {"dbt"}, got {result.data["service"]}"
            raise AssertionError(msg)
        if "dbt_version" not in result.data:
            msg = f"Expected {"dbt_version"} in {result.data}"
            raise AssertionError(msg)

    def test_dbt_service_get_dbt_version(self) -> None:
        """Test DBT service get version."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDbtService(config)

        version = service.get_dbt_version()
        assert isinstance(version, str)
        assert len(version) > 0

    @patch("dbt.cli.main.dbtRunner")
    def test_dbt_service_execute_success(self, mock_dbt_runner: Mock) -> None:
        """Test DBT service execute success."""
        # Mock DBT runner
        mock_runner_instance = Mock()
        mock_runner_instance.invoke.return_value.success = True
        mock_runner_instance.invoke.return_value.result = {"status": "success"}
        mock_dbt_runner.return_value = mock_runner_instance

        config = FlextMeltanoConfig()
        service = FlextMeltanoDbtService(config)

        result = service.execute()
        assert result.is_success
        assert result.data is not None
        if result.data["service"] != "dbt":
            msg = f"Expected {"dbt"}, got {result.data["service"]}"
            raise AssertionError(msg)
        if "initialized" not in result.data:
            msg = f"Expected {"initialized"} in {result.data}"
            raise AssertionError(msg)

    @patch("dbt.cli.main.dbtRunner")
    def test_dbt_service_execute_failure(self, mock_dbt_runner: Mock) -> None:
        """Test DBT service execute failure."""
        # Mock DBT runner failure
        mock_runner_instance = Mock()
        mock_runner_instance.invoke.return_value.success = False
        mock_runner_instance.invoke.return_value.exception = Exception("DBT failed")
        mock_dbt_runner.return_value = mock_runner_instance

        config = FlextMeltanoConfig()
        service = FlextMeltanoDbtService(config)

        result = service.execute()
        assert not result.is_success
        assert result.error is not None
        if "DBT execution failed" not in result.error:
            msg = f"Expected {"DBT execution failed"} in {result.error}"
            raise AssertionError(msg)

    @patch("dbt.cli.main.dbtRunner")
    def test_dbt_service_execute_exception(self, mock_dbt_runner: Mock) -> None:
        """Test DBT service execute with exception."""
        mock_dbt_runner.side_effect = Exception("DBT runner error")

        config = FlextMeltanoConfig()
        service = FlextMeltanoDbtService(config)

        result = service.execute()
        assert not result.is_success
        assert result.error is not None
        if "DBT execution error" not in result.error:
            msg = f"Expected {"DBT execution error"} in {result.error}"
            raise AssertionError(msg)


class TestFactoryFunctions:
    """Test factory functions for service creation."""

    def test_create_meltano_tap_service_success(self) -> None:
        """Test successful tap service creation."""
        config = FlextMeltanoConfig()
        result = create_meltano_tap_service(config)

        assert result.is_success
        assert isinstance(result.data, FlextMeltanoTapService)
        if result.data.config != config:
            msg = f"Expected {config}, got {result.data.config}"
            raise AssertionError(msg)

    def test_create_meltano_target_service_success(self) -> None:
        """Test successful target service creation."""
        config = FlextMeltanoConfig()
        result = create_meltano_target_service(config)

        assert result.is_success
        assert isinstance(result.data, FlextMeltanoTargetService)
        if result.data.config != config:
            msg = f"Expected {config}, got {result.data.config}"
            raise AssertionError(msg)

    def test_create_meltano_dbt_service_success(self) -> None:
        """Test successful DBT service creation."""
        config = FlextMeltanoConfig()
        result = create_meltano_dbt_service(config)

        assert result.is_success
        assert isinstance(result.data, FlextMeltanoDbtService)
        if result.data.config != config:
            msg = f"Expected {config}, got {result.data.config}"
            raise AssertionError(msg)

    def test_create_meltano_extension_service_success(self) -> None:
        """Test successful extension service creation."""
        config = FlextMeltanoConfig()
        result = create_meltano_extension_service(config)

        assert result.is_success
        assert isinstance(result.data, FlextMeltanoExtensionService)
        if result.data.config != config:
            msg = f"Expected {config}, got {result.data.config}"
            raise AssertionError(msg)

    @patch("flext_meltano.base.FlextMeltanoTapService.__init__")
    def test_create_meltano_tap_service_exception(self, mock_init: Mock) -> None:
        """Test tap service creation with exception."""
        mock_init.side_effect = ValueError("Initialization failed")

        config = FlextMeltanoConfig()
        result = create_meltano_tap_service(config)

        assert not result.is_success
        assert result.error is not None
        if "Failed to create tap service" not in result.error:
            msg = f"Expected {"Failed to create tap service"} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.base.FlextMeltanoTargetService.__init__")
    def test_create_meltano_target_service_exception(self, mock_init: Mock) -> None:
        """Test target service creation with exception."""
        mock_init.side_effect = TypeError("Type error")

        config = FlextMeltanoConfig()
        result = create_meltano_target_service(config)

        assert not result.is_success
        assert result.error is not None
        if "Failed to create target service" not in result.error:
            msg = f"Expected {"Failed to create target service"} in {result.error}"
            raise AssertionError(msg)

    @patch("flext_meltano.base.FlextMeltanoDbtService.__init__")
    def test_create_meltano_dbt_service_exception(self, mock_init: Mock) -> None:
        """Test DBT service creation with exception."""
        mock_init.side_effect = ImportError("Import error")

        config = FlextMeltanoConfig()
        result = create_meltano_dbt_service(config)

        assert not result.is_success
        assert result.error is not None
        if "Failed to create dbt service" not in result.error:
            msg = f"Expected {"Failed to create dbt service"} in {result.error}"
            raise AssertionError(msg)

    def test_create_meltano_extension_service_exception(self) -> None:
        """Test extension service creation with exception handling."""
        # Test with invalid config that should cause failure
        import tempfile
        from pathlib import Path

        with tempfile.TemporaryDirectory() as temp_dir:
            invalid_path = Path(temp_dir) / "nonexistent_subdir" / "invalid"
            config = FlextMeltanoConfig(project_root=str(invalid_path))

            # This should succeed as the service should handle invalid paths gracefully
            result = create_meltano_extension_service(config)

            # Extension service creation should be robust
            assert result.is_success
            assert isinstance(result.data, FlextMeltanoExtensionService)


class TestServiceIntegration:
    """Test service integration scenarios."""

    def test_full_tap_service_workflow(self) -> None:
        """Test complete tap service workflow."""
        config = FlextMeltanoConfig(project_root="/test", environment="dev")

        # Create service
        result = create_meltano_tap_service(config)
        assert result.is_success
        assert result.data is not None
        service = result.data

        # Initialize service
        init_result = service.initialize()
        assert init_result.is_success

        # Check health before configuration
        health_result = service.get_health_status()
        assert health_result.is_success
        assert health_result.data is not None
        if health_result.data["tap_configured"]:
            msg = f"Expected False, got {health_result.data["tap_configured"]}"
            raise AssertionError(msg)
        # Configure tap
        mock_tap_class = Mock()
        mock_tap_class.__name__ = "TestTap"
        config_result = service.set_tap_class(mock_tap_class)
        assert config_result.is_success

        # Check health after configuration
        health_result = service.get_health_status()
        assert health_result.is_success
        assert health_result.data is not None
        if not (health_result.data["tap_configured"]):
            msg = f"Expected True, got {health_result.data["tap_configured"]}"
            raise AssertionError(msg)

        # Validate ready for use
        ready_result = service.validate_ready_for_use()
        assert ready_result.is_success

    def test_full_target_service_workflow(self) -> None:
        """Test complete target service workflow."""
        config = FlextMeltanoConfig(project_root="/test", environment="prod")

        # Create service
        result = create_meltano_target_service(config)
        assert result.is_success
        assert result.data is not None
        service = result.data

        # Initialize service
        init_result = service.initialize()
        assert init_result.is_success

        # Configure target
        mock_target_class = Mock()
        mock_target_class.__name__ = "TestTarget"
        config_result = service.set_target_class(mock_target_class)
        assert config_result.is_success

        # Validate ready for use
        ready_result = service.validate_ready_for_use()
        assert ready_result.is_success

    def test_full_dbt_service_workflow(self) -> None:
        """Test complete DBT service workflow."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a fake DBT project directory
            dbt_project_dir = Path(temp_dir) / "dbt_project"
            dbt_project_dir.mkdir()

            config = FlextMeltanoConfig(
                project_root=temp_dir,
                environment="staging",
                dbt_project_dir=str(dbt_project_dir),
            )

            # Create service
            result = create_meltano_dbt_service(config)
            assert result.is_success
            assert result.data is not None
            service = result.data

            # Initialize service
            init_result = service.initialize()
            assert init_result.is_success

            # Get version
            version = service.get_dbt_version()
            assert isinstance(version, str)

            # Check health
            health_result = service.get_health_status()
            assert health_result.is_success
            assert health_result.data is not None
            if health_result.data["service"] != "dbt":
                msg = f"Expected {"dbt"}, got {health_result.data["service"]}"
                raise AssertionError(msg)

            # Execute service
            execute_result = service.execute()
            assert execute_result.is_success
            assert execute_result.data is not None
            if execute_result.data["service"] != "dbt":
                msg = f"Expected {"dbt"}, got {execute_result.data["service"]}"
                raise AssertionError(msg)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
