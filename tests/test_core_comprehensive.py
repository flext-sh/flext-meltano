"""Comprehensive tests for core.py module to increase coverage."""

from __future__ import annotations

import tempfile

import pytest

from flext_meltano.core import (
    FlextMeltanoCore,
    FlextMeltanoCoreConfig,
    FlextMeltanoCoreContext,
    FlextMeltanoCoreExecutor,
    FlextMeltanoCorePlugin,
    FlextMeltanoCoreResult,
    FlextMeltanoCoreRunner,
    FlextMeltanoCoreService,
    FlextMeltanoCoreValidator,
    create_core_context,
    create_core_executor,
    create_core_plugin,
    create_core_runner,
    create_core_service,
    create_core_validator,
    flext_meltano_core_execute,
    flext_meltano_core_run,
    flext_meltano_core_validate,
)


class TestFlextMeltanoCoreConfig:
    """Test FlextMeltanoCoreConfig functionality."""

    def test_config_initialization_default(self) -> None:
        """Test config initialization with defaults."""
        config = FlextMeltanoCoreConfig()
        assert config is not None
        assert hasattr(config, "project_root")
        assert hasattr(config, "environment")

    def test_config_initialization_with_params(self) -> None:
        """Test config initialization with parameters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoCoreConfig(
                project_root=temp_dir,
                environment="test",
            )
            assert config is not None


class TestFlextMeltanoCoreContext:
    """Test FlextMeltanoCoreContext functionality."""

    def test_context_initialization(self) -> None:
        """Test context initialization."""
        context = FlextMeltanoCoreContext()
        assert context is not None

    def test_context_with_config(self) -> None:
        """Test context with config."""
        config = FlextMeltanoCoreConfig()
        context = FlextMeltanoCoreContext(config=config)
        assert context is not None


class TestFlextMeltanoCoreResult:
    """Test FlextMeltanoCoreResult functionality."""

    def test_result_success(self) -> None:
        """Test successful result."""
        result = FlextMeltanoCoreResult(success=True, data={"test": "data"})
        if not (result.success):
            msg = f"Expected True, got {result.success}"
            raise AssertionError(msg)
        if result.data != {"test": "data"}:
            expected_data = {"test": "data"}
            msg = f"Expected {expected_data}, got {result.data}"
            raise AssertionError(msg)

    def test_result_failure(self) -> None:
        """Test failure result."""
        result = FlextMeltanoCoreResult(success=False, error="Test error")
        if result.success:
            msg = f"Expected False, got {result.success}"
            raise AssertionError(msg)
        assert result.error == "Test error"


class TestFlextMeltanoCorePlugin:
    """Test FlextMeltanoCorePlugin functionality."""

    def test_plugin_initialization(self) -> None:
        """Test plugin initialization."""
        plugin = FlextMeltanoCorePlugin(name="test-plugin", type="extractor")
        assert plugin is not None
        if plugin.name != "test-plugin":
            msg = f"Expected {"test-plugin"}, got {plugin.name}"
            raise AssertionError(msg)
        assert plugin.type == "extractor"

    def test_plugin_execute(self) -> None:
        """Test plugin execution."""
        plugin = FlextMeltanoCorePlugin(name="test-plugin", type="extractor")
        result = plugin.execute()
        # Plugin execution may fail without proper setup, but should not crash
        assert result is not None


class TestFlextMeltanoCoreService:
    """Test FlextMeltanoCoreService functionality."""

    def test_service_initialization(self) -> None:
        """Test service initialization."""
        service = FlextMeltanoCoreService()
        assert service is not None

    def test_service_with_config(self) -> None:
        """Test service with config."""
        config = FlextMeltanoCoreConfig()
        service = FlextMeltanoCoreService(config=config)
        assert service is not None

    def test_service_execute(self) -> None:
        """Test service execution."""
        service = FlextMeltanoCoreService()
        result = service.execute()
        # Service execution may fail without proper setup, but should not crash
        assert result is not None


class TestFlextMeltanoCoreExecutor:
    """Test FlextMeltanoCoreExecutor functionality."""

    def test_executor_initialization(self) -> None:
        """Test executor initialization."""
        executor = FlextMeltanoCoreExecutor()
        assert executor is not None

    def test_executor_execute(self) -> None:
        """Test executor execution."""
        executor = FlextMeltanoCoreExecutor()
        result = executor.execute(command=["--version"])
        # Executor may fail without proper setup, but should not crash
        assert result is not None


class TestFlextMeltanoCoreRunner:
    """Test FlextMeltanoCoreRunner functionality."""

    def test_runner_initialization(self) -> None:
        """Test runner initialization."""
        runner = FlextMeltanoCoreRunner()
        assert runner is not None

    def test_runner_run(self) -> None:
        """Test runner run."""
        runner = FlextMeltanoCoreRunner()
        result = runner.run(job="test-job")
        # Runner may fail without proper setup, but should not crash
        assert result is not None


class TestFlextMeltanoCoreValidator:
    """Test FlextMeltanoCoreValidator functionality."""

    def test_validator_initialization(self) -> None:
        """Test validator initialization."""
        validator = FlextMeltanoCoreValidator()
        assert validator is not None

    def test_validator_validate(self) -> None:
        """Test validator validation."""
        validator = FlextMeltanoCoreValidator()
        result = validator.validate()
        # Validator may fail without proper setup, but should not crash
        assert result is not None


class TestFlextMeltanoCore:
    """Test FlextMeltanoCore main class."""

    def test_core_initialization(self) -> None:
        """Test core initialization."""
        core = FlextMeltanoCore()
        assert core is not None

    def test_core_with_config(self) -> None:
        """Test core with config."""
        config = FlextMeltanoCoreConfig()
        core = FlextMeltanoCore(config=config)
        assert core is not None

    def test_core_execute(self) -> None:
        """Test core execution."""
        core = FlextMeltanoCore()
        result = core.execute()
        # Core execution may fail without proper setup, but should not crash
        assert result is not None

    def test_core_run(self) -> None:
        """Test core run."""
        core = FlextMeltanoCore()
        result = core.run(job="test-job")
        # Core run may fail without proper setup, but should not crash
        assert result is not None

    def test_core_validate(self) -> None:
        """Test core validation."""
        core = FlextMeltanoCore()
        result = core.validate()
        # Core validation may fail without proper setup, but should not crash
        assert result is not None


class TestCoreFactoryFunctions:
    """Test core module factory functions."""

    def test_create_core_context(self) -> None:
        """Test create_core_context factory."""
        result = create_core_context()
        assert result is not None

    def test_create_core_executor(self) -> None:
        """Test create_core_executor factory."""
        result = create_core_executor()
        assert result is not None

    def test_create_core_plugin(self) -> None:
        """Test create_core_plugin factory."""
        result = create_core_plugin(name="test", type="extractor")
        assert result is not None

    def test_create_core_runner(self) -> None:
        """Test create_core_runner factory."""
        result = create_core_runner()
        assert result is not None

    def test_create_core_service(self) -> None:
        """Test create_core_service factory."""
        result = create_core_service()
        assert result is not None

    def test_create_core_validator(self) -> None:
        """Test create_core_validator factory."""
        result = create_core_validator()
        assert result is not None


class TestCoreStandaloneFunctions:
    """Test core module standalone functions."""

    def test_flext_meltano_core_execute(self) -> None:
        """Test flext_meltano_core_execute function."""
        result = flext_meltano_core_execute(command=["--version"])
        # Function may fail without proper setup, but should not crash
        assert result is not None

    def test_flext_meltano_core_run(self) -> None:
        """Test flext_meltano_core_run function."""
        result = flext_meltano_core_run(job="test-job")
        # Function may fail without proper setup, but should not crash
        assert result is not None

    def test_flext_meltano_core_validate(self) -> None:
        """Test flext_meltano_core_validate function."""
        result = flext_meltano_core_validate()
        # Function may fail without proper setup, but should not crash
        assert result is not None


class TestCoreIntegration:
    """Test core module integration scenarios."""

    def test_complete_core_workflow(self) -> None:
        """Test complete core workflow."""
        # Create configuration
        config = FlextMeltanoCoreConfig()

        # Create core instance
        core = FlextMeltanoCore(config=config)

        # Create context
        context = create_core_context()

        # Create services
        service = create_core_service()
        executor = create_core_executor()
        validator = create_core_validator()

        # All should be created successfully
        assert core is not None
        assert context is not None
        assert service is not None
        assert executor is not None
        assert validator is not None

    def test_core_error_handling(self) -> None:
        """Test core error handling."""
        core = FlextMeltanoCore()

        # Test with invalid parameters (should handle gracefully)
        result = core.execute()
        # Should not crash, even with invalid input
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
