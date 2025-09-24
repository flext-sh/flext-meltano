"""FLEXT Meltano Config Singleton Pattern Tests - Singleton testing patterns.

This module provides tests for FlextMeltanoConfig singleton pattern using
comprehensive testing patterns and singleton validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_meltano import FlextMeltanoConfig


class TestFlextMeltanoConfigSingletonPattern:
    """Test singleton pattern with parameter overrides."""

    def setup_method(self) -> None:
        """Clear global instance before each test."""
        FlextMeltanoConfig.clear_global_instance()

    def teardown_method(self) -> None:
        """Clear global instance after each test."""
        FlextMeltanoConfig.clear_global_instance()

    def test_get_global_instance_with_overrides(self) -> None:
        """Test get_global_instance with parameter overrides."""
        # Get instance with overrides
        config = FlextMeltanoConfig.get_global_instance(
            project_root="/custom/project",
            environment="production",
            log_level="ERROR",
        )

        # project_root gets resolved by validator
        assert config.project_root.is_absolute()
        assert config.environment == "production"
        assert config.log_level == "ERROR"

    def test_create_with_overrides(self) -> None:
        """Test create_for_environment method with overrides."""
        result = FlextMeltanoConfig.create_for_environment(
            environment="staging",
            project_root="/test/project",
            meltano_version="3.10.0",
        )

        config = result
        # project_root gets resolved by validator, check if it contains expected path
        assert config.project_root.is_absolute()
        assert config.environment == "staging"
        assert config.meltano_version == "3.10.0"

    def test_create_for_environment_with_overrides(self) -> None:
        """Test create_for_environment method with overrides."""
        result = FlextMeltanoConfig.create_for_environment(
            environment="production",
            project_root="/prod/project",
            log_level="WARNING",
            max_concurrent_jobs=8,
        )

        config = result
        assert config.environment == "production"
        # project_root gets resolved by validator
        assert config.project_root.is_absolute()
        assert config.log_level == "WARNING"
        assert config.max_concurrent_jobs == 8  # Override value

    def test_apply_overrides_to_instance(self) -> None:
        """Test apply_overrides method on existing instance."""
        config = FlextMeltanoConfig()
        config.project_root = Path("/initial/project")

        # Apply overrides
        result = config.apply_overrides(
            environment="test",
            log_level="DEBUG",
            meltano_version="3.11.0",
        )

        assert result.is_success
        assert config.environment == "test"
        assert config.log_level == "DEBUG"
        assert config.meltano_version == "3.11.0"

    def test_apply_overrides_sealed_config(self) -> None:
        """Test apply_overrides fails on sealed configuration."""
        config = FlextMeltanoConfig()
        config.project_root = Path("/test")
        config.seal()

        result = config.apply_overrides(environment="production")

        assert result.is_failure
        assert result.error is not None
        assert "sealed" in result.error.lower()

    def test_get_meltano_environment_variables(self) -> None:
        """Test get_meltano_environment_variables includes both base and Meltano vars."""
        config = FlextMeltanoConfig()
        config.project_root = Path("/test/project")
        config.environment = "development"
        config.log_level = "INFO"

        env_vars = config.get_meltano_environment_variables()

        # Check Meltano-specific variables
        assert env_vars["MELTANO_PROJECT_ROOT"] == "/test/project"
        assert env_vars["MELTANO_ENVIRONMENT"] == "development"
        assert env_vars["MELTANO_LOG_LEVEL"] == "INFO"

        # Check that base FlextConfig variables are also included
        assert "FLEXT_APP_NAME" in env_vars or "app_name" in env_vars

    def test_singleton_consistency_with_overrides(self) -> None:
        """Test that singleton pattern maintains consistency with overrides."""
        # Get first instance
        config1 = FlextMeltanoConfig.get_global_instance(environment="development")

        # Get second instance with different overrides
        config2 = FlextMeltanoConfig.get_global_instance(environment="production")

        # Both should be different instances but use same base config
        assert config1.environment == "development"
        assert config2.environment == "production"

        # Both should have same base configuration from FlextConfig
        assert config1.app_name == config2.app_name
        assert config1.version == config2.version

    def test_error_handling_invalid_environment(self) -> None:
        """Test error handling for invalid environment."""
        # Should raise ValueError for invalid environment
        with pytest.raises(ValueError, match="Invalid environment"):
            FlextMeltanoConfig.create_for_environment(
                environment="invalid_env",
                project_root="/test",
            )

    def test_error_handling_invalid_overrides(self) -> None:
        """Test error handling for invalid override values."""
        result = FlextMeltanoConfig.create_for_environment(
            environment="development",
            project_root="/test",
            invalid_field="invalid_value",
        )

        # Should succeed but ignore invalid fields
        config = result
        assert not hasattr(config, "invalid_field")

    def test_metadata_tracking_overrides(self) -> None:
        """Test that metadata tracks applied overrides."""
        config = FlextMeltanoConfig(project_root=Path("/test"))

        # Apply overrides
        config.apply_overrides(environment="production", log_level="ERROR")

        metadata = config.get_metadata()
        assert metadata["overrides_applied"] == "true"
        assert metadata["override_count"] == "2"
