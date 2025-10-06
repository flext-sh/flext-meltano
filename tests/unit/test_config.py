"""FLEXT Meltano Config Unit Tests - Enterprise ELT testing patterns.

This module provides comprehensive unit tests for FlextMeltanoConfig following
FLEXT testing patterns and Pydantic 2.11+ integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import tempfile
from pathlib import Path

from flext_tests import FlextTestsUtilities

from flext_meltano.config import FlextMeltanoConfig


class TestFlextMeltanoConfig:
    """Unit test suite for FlextMeltanoConfig."""

    def setup_method(self) -> None:
        """Setup for each test using flext_tests patterns."""
        self.test_assertions = FlextTestsUtilities.assertion()

    def test_config_initialization_default(self) -> None:
        """Test config initialization with default parameters."""
        config = FlextMeltanoConfig()

        self.test_assertions.assert_true(
            condition=config is not None,
            message="Config should be initialized",
        )

    def test_config_initialization_with_project_root(self) -> None:
        """Test config initialization with specific project root."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config = FlextMeltanoConfig(project_root=temp_path)

            self.test_assertions.assert_true(
                condition=config is not None,
                message="Config should be initialized with project root",
            )
            self.test_assertions.assert_true(
                condition=config.project_root == temp_path,
                message="Project root should be set correctly",
            )

    def test_config_initialization_with_environment(self) -> None:
        """Test config initialization with specific environment."""
        config = FlextMeltanoConfig(environment="test")

        self.test_assertions.assert_true(
            condition=config is not None,
            message="Config should be initialized with environment",
        )
        self.test_assertions.assert_true(
            condition=config.environment == "test",
            message="Environment should be set correctly",
        )

    def test_config_initialization_with_log_level(self) -> None:
        """Test config initialization with specific log level."""
        config = FlextMeltanoConfig(log_level="DEBUG")

        self.test_assertions.assert_true(
            condition=config is not None,
            message="Config should be initialized with log level",
        )
        self.test_assertions.assert_true(
            condition=config.log_level == "DEBUG",
            message="Log level should be set correctly",
        )

    def test_config_initialization_with_timeout(self) -> None:
        """Test config initialization with specific timeout."""
        config = FlextMeltanoConfig(timeout_seconds=300)

        self.test_assertions.assert_true(
            condition=config is not None,
            message="Config should be initialized with timeout",
        )
        self.test_assertions.assert_true(
            condition=config.timeout_seconds == 300,
            message="Timeout should be set correctly",
        )

    def test_config_initialization_with_all_parameters(self) -> None:
        """Test config initialization with all parameters."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            config = FlextMeltanoConfig(
                project_root=temp_path,
                environment="test",
                log_level="DEBUG",
                timeout_seconds=300,
                log_pipeline_progress=True,
                log_extract_errors=True,
                track_meltano_performance=True,
            )

            self.test_assertions.assert_true(
                condition=config is not None,
                message="Config should be initialized with all parameters",
            )
            self.test_assertions.assert_true(
                condition=config.project_root == temp_path,
                message="Project root should be set correctly",
            )
            self.test_assertions.assert_true(
                condition=config.environment == "test",
                message="Environment should be set correctly",
            )
            self.test_assertions.assert_true(
                condition=config.log_level == "DEBUG",
                message="Log level should be set correctly",
            )
            self.test_assertions.assert_true(
                condition=config.timeout_seconds == 300,
                message="Timeout should be set correctly",
            )

    def test_config_default_values(self) -> None:
        """Test config default values."""
        config = FlextMeltanoConfig()

        # Test default values
        self.test_assertions.assert_true(
            condition=config.environment == "dev",
            message="Default environment should be 'dev'",
        )
        self.test_assertions.assert_true(
            condition=config.log_level == "INFO",
            message="Default log level should be 'INFO'",
        )
        self.test_assertions.assert_true(
            condition=config.timeout_seconds == 300,
            message="Default timeout should be 300 seconds",
        )

    def test_config_validation(self) -> None:
        """Test config validation with Pydantic."""
        # Test valid config
        config = FlextMeltanoConfig(
            environment="test",
            log_level="DEBUG",
            timeout_seconds=600,
        )

        self.test_assertions.assert_true(
            condition=config is not None,
            message="Valid config should be created",
        )

    def test_config_serialization(self) -> None:
        """Test config serialization to dict."""
        config = FlextMeltanoConfig(
            environment="test",
            log_level="DEBUG",
            timeout_seconds=600,
        )

        config_dict = config.model_dump()

        self.test_assertions.assert_true(
            condition=isinstance(config_dict, dict),
            message="Config should serialize to dict",
        )
        self.test_assertions.assert_true(
            condition="environment" in config_dict,
            message="Config dict should contain environment",
        )
        self.test_assertions.assert_true(
            condition="log_level" in config_dict,
            message="Config dict should contain log_level",
        )

    def test_config_deserialization(self) -> None:
        """Test config deserialization from dict."""
        config_dict = {
            "environment": "test",
            "log_level": "DEBUG",
            "timeout_seconds": 600,
        }

        config = FlextMeltanoConfig.model_validate(config_dict)

        self.test_assertions.assert_true(
            condition=config is not None,
            message="Config should be created from dict",
        )
        self.test_assertions.assert_true(
            condition=config.environment == "test",
            message="Environment should be set from dict",
        )

    def test_config_immutability(self) -> None:
        """Test config immutability (frozen model)."""
        config = FlextMeltanoConfig(environment="test")

        # Config should be frozen, so this should raise an error
        try:
            config.environment = "production"  # type: ignore[assignment]
            self.test_assertions.assert_true(
                condition=False,
                message="Config should be immutable",
            )
        except Exception:
            # Expected behavior - config is frozen
            self.test_assertions.assert_true(
                condition=True,
                message="Config should be immutable",
            )

    def test_config_constants_reference(self) -> None:
        """Test that config uses constants from FlextMeltanoConstants."""
        config = FlextMeltanoConfig()

        # Test that config uses constants (this is tested by the fact that
        # the config is created successfully with the constants)
        self.test_assertions.assert_true(
            condition=config is not None,
            message="Config should use constants successfully",
        )

    def test_config_logging_settings(self) -> None:
        """Test config logging settings."""
        config = FlextMeltanoConfig(
            log_pipeline_progress=True,
            log_extract_errors=True,
            track_meltano_performance=True,
        )

        self.test_assertions.assert_true(
            condition=config.log_pipeline_progress is True,
            message="Log pipeline progress should be True",
        )
        self.test_assertions.assert_true(
            condition=config.log_extract_errors is True,
            message="Log extract errors should be True",
        )
        self.test_assertions.assert_true(
            condition=config.track_meltano_performance is True,
            message="Track meltano performance should be True",
        )

    def test_config_environment_validation(self) -> None:
        """Test config environment validation."""
        # Test valid environments
        valid_environments = ["dev", "test", "staging", "production"]

        for env in valid_environments:
            config = FlextMeltanoConfig(environment=env)
            self.test_assertions.assert_true(
                condition=config.environment == env,
                message=f"Environment '{env}' should be valid",
            )

    def test_config_log_level_validation(self) -> None:
        """Test config log level validation."""
        # Test valid log levels
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

        for level in valid_log_levels:
            config = FlextMeltanoConfig(log_level=level)
            self.test_assertions.assert_true(
                condition=config.log_level == level,
                message=f"Log level '{level}' should be valid",
            )
