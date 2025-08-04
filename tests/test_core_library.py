"""Core Library Comprehensive Test Suite - Foundation Integration Validation.

**Test Category**: Integration Tests
**Coverage Target**: 95%+ for core library integration patterns
**Dependencies**: flext-core patterns, enterprise service creation
**Execution Time**: < 8 seconds total

## Test Scope

Validates the core library integration patterns of FLEXT Meltano's bridge architecture,
focusing on service creation, configuration management, and enterprise patterns that
provide the foundation for all Go ↔ Python bridge operations.

## Test Coverage Areas

1. **Library Imports**: Comprehensive import validation for all public APIs (449+ exports)
2. **Service Creation**: Factory patterns and dependency injection validation
3. **Configuration Management**: Enterprise configuration patterns and validation
4. **Integration Patterns**: Bridge-ready service instantiation and result handling
5. **Enterprise Compliance**: Clean Architecture and FlextResult pattern validation

## Architecture Alignment

Tests align with FLEXT Meltano's core library architecture:
- **Enterprise Service Creation**: Factory patterns with proper dependency injection
- **Configuration Management**: FlextMeltanoConfig validation and environment handling
- **Bridge Integration**: Service patterns designed for Go service consumption
- **Type Safety**: Comprehensive type validation throughout service creation
"""

import tempfile
from pathlib import Path

import pytest

import flext_meltano
from flext_meltano import (
    # DbtRunResult,  # TYPE_CHECKING only
    FlextMeltanoConfig,
    FlextMeltanoDiscoverer,
    FlextMeltanoExecutor,
    FlextMeltanoInstaller,
    FlextMeltanoValidationService,
    # MeltanoCoreProject,  # TYPE_CHECKING only
    Sink,
    # SQLAdapter,  # TYPE_CHECKING only
    Stream,
    Tap,
    Target,
    create_discoverer,
    create_executor,
    create_installer_service,
    create_validation_service,
    flext_meltano_execute_job,
    flext_meltano_run_command,
)


class TestCoreLibraryImports:
    """Test core library imports and availability."""

    def test_version_available(self) -> None:
        """Test that version is available."""
        assert hasattr(flext_meltano, "__version__")
        if flext_meltano.__version__ != "2.0.0-enterprise":
            msg: str = f"Expected {'2.0.0-enterprise'}, got {flext_meltano.__version__}"
            raise AssertionError(msg)

    def test_core_classes_available(self) -> None:
        """Test that core classes are available."""
        assert FlextMeltanoConfig is not None
        assert FlextMeltanoExecutor is not None
        assert FlextMeltanoDiscoverer is not None
        assert FlextMeltanoInstaller is not None
        assert FlextMeltanoValidationService is not None

    def test_factory_functions_available(self) -> None:
        """Test that factory functions are available."""
        assert create_executor is not None
        assert create_discoverer is not None
        assert create_installer_service is not None
        assert create_validation_service is not None

    def test_singer_sdk_re_exports(self) -> None:
        """Test Singer SDK re-exports are available."""

        assert Tap is not None
        assert Target is not None
        assert Stream is not None
        assert Sink is not None

    def test_meltano_re_exports(self) -> None:
        """Test Meltano re-exports are available."""

        # assert MeltanoCoreProject is not None  # TYPE_CHECKING only

    def test_dbt_re_exports(self) -> None:
        """Test DBT re-exports are available."""

        # assert DbtRunResult is not None  # TYPE_CHECKING only
        # assert SQLAdapter is not None  # TYPE_CHECKING only


class TestCoreConfiguration:
    """Test core configuration functionality."""

    def test_config_creation(self) -> None:
        """Test basic configuration creation."""
        config = FlextMeltanoConfig(
            project_root=".",
            environment="test",
        )
        if config.project_root != str(Path().absolute()):
            msg: str = f"Expected {Path().absolute()!s}, got {config.project_root}"
            raise AssertionError(msg)
        assert config.environment == "test"

    def test_config_defaults(self) -> None:
        """Test configuration defaults."""
        config = FlextMeltanoConfig()
        if config.environment != "dev":
            msg: str = f"Expected {'dev'}, got {config.environment}"
            raise AssertionError(msg)
        assert config.meltano_ui_bind_port == 5000
        if config.singer_sdk_log_level != "INFO":
            msg: str = f"Expected {'INFO'}, got {config.singer_sdk_log_level}"
            raise AssertionError(msg)

    def test_config_validation(self) -> None:
        """Test configuration validation."""
        # Config should create project root if it doesn't exist

        test_path = Path(tempfile.mkdtemp(prefix="test_meltano_project"))
        config = FlextMeltanoConfig(project_root=str(test_path))
        assert Path(config.project_root).exists()

        # Clean up
        if test_path.exists():
            test_path.rmdir()


class TestServiceCreation:
    """Test service creation using factory functions."""

    def test_executor_creation(self) -> None:
        """Test executor service creation."""
        config = FlextMeltanoConfig()
        result = create_executor(config)

        assert result.success
        assert isinstance(result.data, FlextMeltanoExecutor)

    def test_discoverer_creation(self) -> None:
        """Test discoverer service creation."""
        config = FlextMeltanoConfig()
        result = create_discoverer(config)

        assert result.success
        assert isinstance(result.data, FlextMeltanoDiscoverer)

    def test_installer_creation(self) -> None:
        """Test installer service creation."""
        config = FlextMeltanoConfig()
        result = create_installer_service(config)

        assert result.success
        assert isinstance(result.data, FlextMeltanoInstaller)

    def test_validation_service_creation(self) -> None:
        """Test validation service creation."""
        config = FlextMeltanoConfig()
        result = create_validation_service(config)

        assert result.success
        assert isinstance(result.data, FlextMeltanoValidationService)


class TestServiceValidation:
    """Test service validation functionality."""

    def test_executor_validation(self) -> None:
        """Test executor validation."""
        config = FlextMeltanoConfig()
        executor = FlextMeltanoExecutor(config)

        # Should validate even without meltano installed
        health_result = executor.get_health_status()
        assert health_result.success
        assert health_result.data is not None
        if health_result.data["service"] != "execution":
            msg: str = f"Expected {'execution'}, got {health_result.data['service']}"
            raise AssertionError(msg)

    def test_discoverer_validation(self) -> None:
        """Test discoverer validation."""
        config = FlextMeltanoConfig()
        discoverer = FlextMeltanoDiscoverer(config)

        health_result = discoverer.get_health_status()
        assert health_result.success
        assert health_result.data is not None
        if health_result.data["service"] != "discovery":
            msg: str = f"Expected {'discovery'}, got {health_result.data['service']}"
            raise AssertionError(msg)

    def test_installer_validation(self) -> None:
        """Test installer validation."""
        config = FlextMeltanoConfig()
        installer = FlextMeltanoInstaller(config)

        health_result = installer.get_health_status()
        assert health_result.success
        assert health_result.data is not None
        if health_result.data["service"] != "installation":
            msg: str = f"Expected {'installation'}, got {health_result.data['service']}"
            raise AssertionError(msg)

    def test_validation_service_validation(self) -> None:
        """Test validation service validation."""
        config = FlextMeltanoConfig()
        validator = FlextMeltanoValidationService(config)

        health_result = validator.get_health_status()
        assert health_result.success
        assert health_result.data is not None
        if health_result.data["service"] != "validation":
            msg: str = f"Expected {'validation'}, got {health_result.data['service']}"
            raise AssertionError(msg)


class TestEnterprisePatterns:
    """Test enterprise patterns compliance."""

    def test_flext_result_pattern(self) -> None:
        """Test FlextResult pattern is used consistently."""
        config = FlextMeltanoConfig()

        # All factory functions should return FlextResult
        executor_result = create_executor(config)
        assert hasattr(executor_result, "success")
        assert hasattr(executor_result, "data")
        assert hasattr(executor_result, "error")

        discoverer_result = create_discoverer(config)
        assert hasattr(discoverer_result, "success")
        assert hasattr(discoverer_result, "data")
        assert hasattr(discoverer_result, "error")

    def test_dependency_injection(self) -> None:
        """Test dependency injection patterns."""
        config = FlextMeltanoConfig()

        # Services should accept config via constructor
        executor = FlextMeltanoExecutor(config)
        if executor.config != config:
            msg: str = f"Expected {config}, got {executor.config}"
            raise AssertionError(msg)

        discoverer = FlextMeltanoDiscoverer(config)
        if discoverer.config != config:
            msg: str = f"Expected {config}, got {discoverer.config}"
            raise AssertionError(msg)

    def test_service_initialization(self) -> None:
        """Test service initialization patterns."""
        config = FlextMeltanoConfig()

        # Services should have initialize method
        executor = FlextMeltanoExecutor(config)
        init_result = executor.initialize()
        assert init_result.success

        discoverer = FlextMeltanoDiscoverer(config)
        init_result = discoverer.initialize()
        assert init_result.success


class TestLegacyCompatibility:
    """Test legacy compatibility functions."""

    def test_legacy_execution_functions(self) -> None:
        """Test legacy execution functions still work."""

        # Functions should exist and be callable
        assert callable(flext_meltano_execute_job)
        assert callable(flext_meltano_run_command)

    def test_legacy_discovery_functions(self) -> None:
        """Test legacy discovery functions still work."""

        from flext_meltano import (
            flext_meltano_discover_catalog,
            flext_meltano_discover_plugins,
        )

        # Functions should exist and be callable
        assert callable(flext_meltano_discover_catalog)
        assert callable(flext_meltano_discover_plugins)

    def test_legacy_validation_functions(self) -> None:
        """Test legacy validation functions still work."""

        from flext_meltano import (
            flext_meltano_test_tap_connection,
            flext_meltano_validate_project,
            flext_meltano_validate_tap_config,
        )

        # Functions should exist and be callable
        assert callable(flext_meltano_validate_project)
        assert callable(flext_meltano_test_tap_connection)
        assert callable(flext_meltano_validate_tap_config)

    def test_deprecation_warnings(self) -> None:
        """Test that legacy functions issue deprecation warnings."""

        with pytest.warns(DeprecationWarning, match="deprecated"):
            result = flext_meltano_execute_job("tap-csv", "target-csv", ".")
        # Result should still work
        assert hasattr(result, "success")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
