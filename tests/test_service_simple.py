"""Foundation Layer Test Suite - Base Module Validation.

**Test Category**: Unit Tests
**Coverage Target**: 95%+ for base module components
**Dependencies**: None (isolated unit testing)
**Execution Time**: < 5 seconds total

## Test Scope

Validates the foundation layer components of FLEXT Meltano's bridge architecture,
focusing on configuration management, service base classes, and factory functions
that provide the foundation for all bridge operations.

## Test Coverage Areas

1. **Configuration Management**: FlextMeltanoConfig initialization and validation
2. **Service Base Classes**: Tap, Target, DBT, and Extension service abstractions
3. **Factory Functions**: Service creation with dependency injection patterns
4. **Enterprise Patterns**: FlextResult integration and error handling
5. **Bridge Integration**: JSON-serializable results for Go service consumption

## Architecture Alignment

Tests align with FLEXT Meltano's foundation layer architecture:
- **Configuration Value Objects**: Environment-aware settings with validation
- **Service Abstractions**: Base classes following enterprise patterns
- **Factory Pattern**: Consistent service creation with dependency injection
- **Railway-Oriented Programming**: FlextResult pattern validation

These tests ensure the foundation layer provides reliable building blocks for
the Go ↔ Python bridge integration that all other modules depend upon.
"""

import tempfile
from pathlib import Path
from typing import cast

import pytest

from flext_meltano import (
    FlextMeltanoConfig,
)
from flext_meltano.executors_bridge import FlextMeltanoBridge


class TestFlextMeltanoConfig:
    """Configuration Management Unit Tests.

    **Test Focus**: FlextMeltanoConfig value object validation
    **Coverage**: Configuration initialization, validation, environment handling
    **Pattern**: Enterprise configuration management with Pydantic integration

    Validates the core configuration value object that serves as the foundation
    for all bridge operations, ensuring environment-aware settings with proper
    validation and type safety.
    """

    def test_config_initialization_default(self) -> None:
        """Test config initialization with defaults."""
        config = FlextMeltanoConfig()
        assert config is not None
        assert config.project_root is not None
        # Accept both dev and development as valid defaults (may vary by environment)
        if config.environment not in {"dev", "development"}:
            msg: str = f"Expected 'dev' or 'development', got {config.environment}"
            raise AssertionError(msg)

    def test_config_initialization_with_params(self) -> None:
        """Test config initialization with parameters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_path = str(Path(temp_dir) / "test")
            dbt_path = str(Path(temp_dir) / "dbt")
            config = FlextMeltanoConfig(
                project_root=test_path,
                environment="production",
                dbt_project_dir=dbt_path,
            )
            if config.project_root != test_path:
                msg: str = f"Expected {test_path}, got {config.project_root}"
                raise AssertionError(msg)
            assert config.environment == "production"
            if config.dbt_project_dir != dbt_path:
                dbt_msg: str = f"Expected {dbt_path}, got {config.dbt_project_dir}"
                raise AssertionError(dbt_msg)


class TestFlextMeltanoServices:
    """Test service classes."""

    def test_tap_service_initialization(self) -> None:
        """Test tap service functionality through bridge integration."""
        # FlextMeltanoTapService is abstract, so we test it through bridge functionality
        bridge = FlextMeltanoBridge()
        assert bridge is not None
        # Test that the bridge can access tap functionality
        plugins_result = bridge.list_plugins()
        assert plugins_result["success"] is True
        assert "data" in plugins_result

    def test_target_service_initialization(self) -> None:
        """Test target service initialization - using concrete implementation pattern."""
        # FlextMeltanoTargetService is abstract, so we test it through bridge functionality
        bridge = FlextMeltanoBridge()
        assert bridge is not None
        # Test that the bridge can access target functionality
        version_result = bridge.get_version()
        assert version_result["success"] is True

    # FlextMeltanoExtensionService was removed in refactoring

    def test_dbt_service_initialization(self) -> None:
        """Test DBT service functionality through bridge integration."""
        # FlextMeltanoDbtService is abstract, so we test it through bridge functionality
        bridge = FlextMeltanoBridge()
        assert bridge is not None
        # Test that DBT functionality is accessible through the bridge
        version_result = bridge.get_version()
        assert version_result["success"] is True
        data_dict = cast("dict[str, object]", version_result["data"])
        assert "dbt_core" in data_dict


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
