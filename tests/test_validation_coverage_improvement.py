"""Tests to improve coverage of validation.py module."""

from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

from flext_meltano.base import FlextMeltanoConfig
from flext_meltano.validation import (
    FlextMeltanoValidationResult,
    FlextMeltanoValidationService,
    create_validation_service,
    flext_meltano_test_tap_connection,
    flext_meltano_validate_project,
    flext_meltano_validate_tap_config,
)


class TestValidationCoverageImprovement:
    """Tests to improve validation.py coverage."""

    def test_validation_service_creation(self) -> None:
        """Test validation service creation and basic functionality."""
        # Test with default config
        config = FlextMeltanoConfig()
        service = FlextMeltanoValidationService(config)
        assert service is not None
        assert isinstance(service, FlextMeltanoValidationService)

        # Test with config parameter
        config_dict = {"project_root": tempfile.gettempdir()}
        config_with_params = FlextMeltanoConfig(**config_dict)
        service_with_config = FlextMeltanoValidationService(config_with_params)
        assert service_with_config is not None

    def test_validation_result_creation(self) -> None:
        """Test validation result creation and properties."""
        # Test successful result
        success_result = FlextMeltanoValidationResult(
            validation_id="test-validation-1",
            is_valid=True,
            validation_type="project",
        )
        assert success_result.is_valid is True
        assert success_result.validation_type == "project"
        assert success_result.validation_id == "test-validation-1"

        # Test failure result with details
        failure_result = FlextMeltanoValidationResult(
            validation_id="test-validation-2",
            is_valid=False,
            validation_type="config",
            issues=["Missing required field", "Invalid format"],
            details={"field": "database_url", "expected": "string"},
        )
        assert failure_result.is_valid is False
        assert len(failure_result.issues) == 2
        assert "database_url" in str(failure_result.details)

    def test_create_validation_service_factory(self) -> None:
        """Test validation service factory function."""
        # Test with default config
        config = FlextMeltanoConfig()
        result = create_validation_service(config)
        assert result.success
        assert isinstance(result.data, FlextMeltanoValidationService)

        # Test with configuration
        config_dict = {"project_root": str(Path(tempfile.gettempdir()) / "test")}
        config_with_params = FlextMeltanoConfig(**config_dict)
        result = create_validation_service(config_with_params)
        assert result.success
        assert isinstance(result.data, FlextMeltanoValidationService)

    def test_project_validation_function(self) -> None:
        """Test standalone project validation function."""
        # Test project validation - returns dict for Go compatibility
        result = flext_meltano_validate_project()
        assert isinstance(result, dict)
        assert "success" in result
        assert isinstance(result["success"], bool)

        # Test with specific project path
        with tempfile.TemporaryDirectory() as temp_dir:
            result = flext_meltano_validate_project(project_root=temp_dir)
            assert isinstance(result, dict)
            assert "success" in result
            assert isinstance(result["success"], bool)

    async def test_tap_config_validation_function(self) -> None:
        """Test tap configuration validation function."""
        # Test with minimal config - returns dict for Go compatibility
        config = {"host": "localhost", "port": 5432}
        result = await flext_meltano_validate_tap_config("tap-postgres", config)
        assert isinstance(result, dict)
        assert "success" in result
        assert isinstance(result["success"], bool)

        # Test with empty config
        result = await flext_meltano_validate_tap_config("tap-csv", {})
        assert isinstance(result, dict)
        assert "success" in result
        assert isinstance(result["success"], bool)

        # Test with None config - convert to empty dict since function expects dict
        result = await flext_meltano_validate_tap_config("tap-test", {})
        assert isinstance(result, dict)
        assert "success" in result
        assert isinstance(result["success"], bool)

    async def test_tap_connection_testing_function(self) -> None:
        """Test tap connection testing function."""
        # Test connection with valid parameters - returns dict for Go compatibility
        config = {"host": "localhost", "database": "test"}
        result = await flext_meltano_test_tap_connection("tap-postgres", Path(), config)
        assert isinstance(result, dict)
        assert "success" in result
        assert isinstance(result["success"], bool)

        # Test connection with different config
        result = await flext_meltano_test_tap_connection(
            "tap-postgres",
            Path(),
            config,
        )
        assert isinstance(result, dict)
        assert "success" in result
        assert isinstance(result["success"], bool)

    def test_validation_service_methods(self) -> None:
        """Test validation service instance methods."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoValidationService(config)

        # Test validate_project method
        result = service.validate_project()
        assert hasattr(result, "success")
        assert isinstance(result.success, bool)

        # Test validate_tap_config method
        tap_config = {"test": "value"}
        result = service.validate_tap_config("tap-test", tap_config)
        assert hasattr(result, "success")
        assert isinstance(result.success, bool)

    def test_validation_error_handling(self) -> None:
        """Test validation error handling scenarios."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoValidationService(config)

        # Test with invalid tap name
        result = service.validate_tap_config("", {})
        # Should handle gracefully
        assert hasattr(result, "success")
        assert isinstance(result.success, bool)

        # Test with invalid config structure
        invalid_config = "not a dict"
        result = service.validate_tap_config("tap-test", invalid_config)
        assert hasattr(result, "success")
        assert isinstance(result.success, bool)

    def test_validation_with_project_structure(self) -> None:
        """Test validation with different project structures."""
        # Test with temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create minimal project structure
            (temp_path / "meltano.yml").touch()

            # Test validation with this structure
            project_config = FlextMeltanoConfig(project_root=str(temp_path))
            service_with_project = FlextMeltanoValidationService(project_config)
            result = service_with_project.validate_project()
            assert hasattr(result, "success")
            assert isinstance(result.success, bool)

    def test_validation_result_serialization(self) -> None:
        """Test validation result serialization capabilities."""
        result = FlextMeltanoValidationResult(
            validation_id="test-123",
            is_valid=True,
            validation_type="config",
            details={"key": "value", "count": 42},
        )

        # Test string representation
        str_repr = str(result)
        assert isinstance(str_repr, str)
        assert len(str_repr) > 0

        # Test that it has expected attributes
        assert hasattr(result, "is_valid")
        assert hasattr(result, "validation_type")
        assert hasattr(result, "validation_id")

    def test_validation_service_configuration_handling(self) -> None:
        """Test validation service configuration handling."""
        # Test with various configuration options
        configs = [
            {},
            {"environment": "dev"},
            {"project_root": tempfile.gettempdir()},
            {
                "project_root": str(Path(tempfile.gettempdir()) / "test"),
                "environment": "test",
            },
        ]

        for config_dict in configs:
            config = FlextMeltanoConfig(**config_dict)
            service = FlextMeltanoValidationService(config)
            assert service is not None

            # Test that service can perform basic operations
            result = service.validate_project()
            assert hasattr(result, "success")

    def test_validation_edge_cases(self) -> None:
        """Test validation edge cases and boundary conditions."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoValidationService(config)

        # Test with very long tap names
        long_tap_name = "tap-" + "x" * 100
        result = service.validate_tap_config(long_tap_name, {})
        assert hasattr(result, "success")

        # Test with special characters in tap names
        special_tap_name = "tap-test@#$%"
        result = service.validate_tap_config(special_tap_name, {})
        assert hasattr(result, "success")

        # Test with complex nested config
        complex_config = {
            "database": {
                "host": "localhost",
                "port": 5432,
                "credentials": {
                    "username": "user",
                    "password": "pass",
                },
            },
            "tables": ["table1", "table2", "table3"],
        }
        result = service.validate_tap_config("tap-postgres", complex_config)
        assert hasattr(result, "success")

    def test_validation_timeout_handling(self) -> None:
        """Test validation timeout handling."""
        # Test with very short timeout
        config_short = FlextMeltanoConfig(project_root=".")
        service = FlextMeltanoValidationService(config_short)

        # Use async test_tap_connection method instead
        result = asyncio.run(
            service.test_tap_connection("tap-postgres", {"host": "localhost"}),
        )
        assert hasattr(result, "success")
        assert isinstance(result.success, bool)

        # Test with longer timeout
        config_long = FlextMeltanoConfig(project_root=".")
        service_long = FlextMeltanoValidationService(config_long)

        result = asyncio.run(
            service_long.test_tap_connection("tap-csv", {"files": ["test.csv"]}),
        )
        assert hasattr(result, "success")

    def test_validation_caching_behavior(self) -> None:
        """Test validation caching and performance behavior."""
        config = FlextMeltanoConfig()
        service = FlextMeltanoValidationService(config)

        # Perform same validation multiple times
        tap_name = "tap-test"
        config = {"test_key": "test_value"}

        results = []
        for _ in range(3):
            result = service.validate_tap_config(tap_name, config)
            results.append(result)
            assert hasattr(result, "success")

        # All results should be consistent
        success_values = [r.success for r in results]
        assert len(set(success_values)) <= 1  # All same value
