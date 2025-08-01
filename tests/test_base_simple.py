"""Simple test for base module bypassing __init__.py import issues."""

import sys
import tempfile
from pathlib import Path

# Add src to path directly
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import pytest

# Import directly from base module, bypassing __init__.py
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
    """Test FlextMeltanoConfig functionality."""

    def test_config_initialization_default(self) -> None:
        """Test config initialization with defaults."""
        config = FlextMeltanoConfig()
        assert config is not None
        assert config.project_root is not None
        if config.environment != "dev":
            msg = f"Expected {'dev'}, got {config.environment}"
            raise AssertionError(msg)

    def test_config_initialization_with_params(self) -> None:
        """Test config initialization with parameters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = str(Path(temp_dir) / "test")
            dbt_path = str(Path(temp_dir) / "dbt")
            config = FlextMeltanoConfig(
                project_root=test_path,
                environment="prod",
                dbt_project_dir=dbt_path,
            )
            if config.project_root != test_path:
                msg = f"Expected {test_path}, got {config.project_root}"
                raise AssertionError(msg)
            assert config.environment == "prod"
            if config.dbt_project_dir != dbt_path:
                msg = f"Expected {dbt_path}, got {config.dbt_project_dir}"
                raise AssertionError(msg)


class TestFlextMeltanoEvent:
    """Test FlextMeltanoEvent functionality."""

    def test_event_initialization(self) -> None:
        """Test event initialization."""
        event = FlextMeltanoEvent(
            event_type="test_event",
            source="test_source",
            data={"key": "value"},
        )
        assert event is not None
        if event.event_type != "test_event":
            msg = f"Expected {'test_event'}, got {event.event_type}"
            raise AssertionError(msg)
        assert event.source == "test_source"
        if event.data != {"key": "value"}:
            expected_data = {"key": "value"}
            msg = f"Expected {expected_data}, got {event.data}"
            raise AssertionError(msg)


class TestFlextMeltanoServices:
    """Test service classes."""

    def test_tap_service_initialization(self) -> None:
        """Test tap service initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTapService(config)
        assert service is not None
        assert service.config is not None

    def test_target_service_initialization(self) -> None:
        """Test target service initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoTargetService(config)
        assert service is not None
        assert service.config is not None

    def test_extension_service_initialization(self) -> None:
        """Test extension service initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoExtensionService(config)
        assert service is not None
        assert service.config is not None

    def test_dbt_service_initialization(self) -> None:
        """Test DBT service initialization."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoDbtService(config)
        assert service is not None
        assert service.config is not None


class TestFactoryFunctions:
    """Test factory functions."""

    def test_create_meltano_tap_service(self) -> None:
        """Test create tap service factory function."""
        config = FlextMeltanoConfig()
        result = create_meltano_tap_service(config)
        # Tap service requires tap_class to be set for full initialization
        # This is expected behavior - service is created but validation fails
        assert not result.is_success
        assert "Tap class not configured" in result.error

    def test_create_meltano_target_service(self) -> None:
        """Test create target service factory function."""
        config = FlextMeltanoConfig()
        result = create_meltano_target_service(config)
        # Target service requires target_class to be set for full initialization
        # This is expected behavior - service is created but validation fails
        assert not result.is_success
        assert "Target class not configured" in result.error

    def test_create_meltano_dbt_service(self) -> None:
        """Test create DBT service factory function."""

        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(dbt_project_dir=temp_dir)
            result = create_meltano_dbt_service(config)
            assert result.is_success
            assert isinstance(result.data, FlextMeltanoDbtService)

    def test_create_meltano_extension_service(self) -> None:
        """Test create extension service factory function."""
        config = FlextMeltanoConfig()
        result = create_meltano_extension_service(config)
        assert result.is_success
        assert isinstance(result.data, FlextMeltanoExtensionService)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
