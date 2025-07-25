"""Simple API for FLEXT Oracle OIC Extension setup and configuration.

Copyright (c) 2025 Flext. All rights reserved.
SPDX-License-Identifier: MIT

This module provides a simple API for setting up Oracle Integration Cloud extensions.
It uses flext-core patterns for configuration and error handling.
"""

from __future__ import annotations

import logging
import os
from typing import TYPE_CHECKING, Any, cast

from flext_core import FlextLogLevel, setup_logging
from flext_oracle_oic_ext.config import (
    OICExtensionConnectionConfig,
    OICExtensionExtractionConfig,
    OICExtensionLifecycleConfig,
    OICExtensionMonitoringConfig,
    OICExtensionPerformanceConfig,
    OracleOICExtensionSettings,
)

from flext_meltano.helpers.execution import FlextMeltanoResult

if TYPE_CHECKING:
    from flext_meltano.simple_api import EnvironmentLiteral

# Type alias for log levels
LogLevelLiteral = FlextLogLevel

# Simple replacement for FlextLoggingConfig
FlextLoggingConfig = dict


def get_logger(name: str) -> logging.Logger:
    """Get logger for module."""
    return logging.getLogger(name)


logger = get_logger(__name__)


def setup_oic_extension(
    settings: OracleOICExtensionSettings | None = None,
) -> FlextMeltanoResult[Any]:
    """Set up Oracle OIC extension with logging and configuration validation."""
    try:
        if settings is None:
            # Create minimal settings for testing - requires connection to be provided externally
            # NOTE: This is for development/testing. Use environment variables
            # in production.

            connection = OICExtensionConnectionConfig(
                base_url=os.getenv(
                    "OIC_BASE_URL",
                    "https://example.integration.ocp.oraclecloud.com",
                ),
                oauth_client_id=os.getenv("OIC_CLIENT_ID", "client_id"),
                oauth_client_secret=os.getenv("OIC_CLIENT_SECRET", "client_secret"),
                # nosec: default for dev/test
                oauth_token_url=os.getenv(
                    "OIC_TOKEN_URL",
                    "https://idcs.identity.oraclecloud.com/oauth2/v1/token",
                ),  # nosec: default for dev/test
                oauth_scope=None,
            )
            settings = OracleOICExtensionSettings(
                connection=connection,
                instance_id=None,
                region=None,
            )

        # Setup logging using flext-infrastructure.monitoring.flext-observability
        # Convert string log level to LogLevel enum
        log_level = (
            FlextLogLevel(settings.log_level.lower())
            if isinstance(settings.log_level, str)
            else settings.log_level
        )
        logging_config = FlextLoggingConfig(log_level=log_level, json_logs=True)
        setup_logging(logging_config)

        return FlextMeltanoResult.ok(settings)

    except (ValueError, TypeError, ImportError, OSError) as e:
        return FlextMeltanoResult.ok(error=f"Failed to setup OIC extension: {e}")


def create_development_oic_config(
    base_url: str | None = None,
    oauth_client_id: str | None = None,
    oauth_client_secret: str | None = None,
    oauth_token_url: str | None = None,
    **overrides: Any,  # noqa: ANN401
) -> OracleOICExtensionSettings:
    """Create development configuration with conservative settings.

    All credentials should be provided via environment variables or parameters.
    This function no longer contains hardcoded default values for security reasons.
    """
    # Get values from environment variables or parameters, with safe defaults
    final_base_url = (
        base_url
        or os.getenv("OIC_DEV_BASE_URL")
        or "https://CONFIGURE-DEV-INSTANCE.integration.ocp.oraclecloud.com"
    )
    final_oauth_client_id = (
        oauth_client_id or os.getenv("OIC_DEV_CLIENT_ID") or "CONFIGURE_DEV_CLIENT_ID"
    )
    final_oauth_client_secret = (
        oauth_client_secret
        or os.getenv("OIC_DEV_CLIENT_SECRET")
        or "CONFIGURE_DEV_CLIENT_SECRET"
    )
    final_oauth_token_url = (
        oauth_token_url
        or os.getenv("OIC_DEV_TOKEN_URL")
        or "https://CONFIGURE-IDCS-DEV.identity.oraclecloud.com/oauth2/v1/token"
    )

    config = {
        "connection": {
            "base_url": final_base_url,
            "oauth_client_id": final_oauth_client_id,
            "oauth_client_secret": final_oauth_client_secret,
            "oauth_token_url": final_oauth_token_url,
        },
        "lifecycle": {
            "auto_activate": False,
            "health_check_interval": 300,
            "activation_timeout": 60,
            "validate_before_activate": True,
            "rollback_on_failure": True,
        },
        "monitoring": {
            "enable_monitoring": True,
            "monitoring_interval": 60,
            "alert_threshold": 80,
            "error_window_hours": 12,
            "performance_window_hours": 3,
        },
        "performance": {
            "request_timeout": 30,
            "max_retries": 3,
            "retry_delay": 1.0,
            "batch_size": 50,
            "max_concurrent_requests": 3,
        },
        "extraction": {
            "extract_artifacts": True,
            "extract_logs": True,
            "extract_metadata": True,
            "artifact_directory": "./dev_artifacts",
            "log_window_hours": 12,
        },
        "environment": "dev",
        "log_level": "DEBUG",
        "debug": True,
    }

    # Override with provided values
    for key, value in overrides.items():
        if isinstance(value, dict) and key in config:
            current_value = config[key]
            if isinstance(current_value, dict):
                current_value.update(value)
            else:
                config[key] = value
        else:
            config[key] = value

    return OracleOICExtensionSettings(
        connection=OICExtensionConnectionConfig(
            **cast("dict[str, Any]", config["connection"]),
        ),
        lifecycle=OICExtensionLifecycleConfig(
            **cast("dict[str, Any]", config["lifecycle"]),
        ),
        monitoring=OICExtensionMonitoringConfig(
            **cast("dict[str, Any]", config["monitoring"]),
        ),
        performance=OICExtensionPerformanceConfig(
            **cast("dict[str, Any]", config["performance"]),
        ),
        extraction=OICExtensionExtractionConfig(
            **cast("dict[str, Any]", config["extraction"]),
        ),
        environment=cast("EnvironmentLiteral", config["environment"]),
        log_level=cast("LogLevelLiteral", config["log_level"]),
        debug=cast("bool", config["debug"]),
        instance_id=None,
        region=None,
    )


def create_production_oic_config(
    base_url: str,
    oauth_client_id: str,
    oauth_client_secret: str,
    oauth_token_url: str,
    **overrides: Any,  # noqa: ANN401
) -> OracleOICExtensionSettings:
    """Create production configuration with performance optimizations."""
    config = {
        "connection": {
            "base_url": base_url,
            "oauth_client_id": oauth_client_id,
            "oauth_client_secret": oauth_client_secret,
            "oauth_token_url": oauth_token_url,
        },
        "lifecycle": {
            "auto_activate": True,
            "health_check_interval": 600,
            "activation_timeout": 120,
            "validate_before_activate": True,
            "rollback_on_failure": True,
        },
        "monitoring": {
            "enable_monitoring": True,
            "monitoring_interval": 300,
            "alert_threshold": 95,
            "error_window_hours": 24,
            "performance_window_hours": 6,
        },
        "performance": {
            "request_timeout": 60,
            "max_retries": 5,
            "retry_delay": 2.0,
            "batch_size": 100,
            "max_concurrent_requests": 10,
        },
        "extraction": {
            "extract_artifacts": True,
            "extract_logs": True,
            "extract_metadata": True,
            "artifact_directory": "/opt/oic/artifacts",
            "log_window_hours": 24,
        },
        "environment": "prod",
        "log_level": "INFO",
        "debug": False,
    }

    # Override with provided values
    for key, value in overrides.items():
        if isinstance(value, dict) and key in config:
            current_value = config[key]
            if isinstance(current_value, dict):
                current_value.update(value)
            else:
                config[key] = value
        else:
            config[key] = value

    return OracleOICExtensionSettings(
        connection=OICExtensionConnectionConfig(
            **cast("dict[str, Any]", config["connection"]),
        ),
        lifecycle=OICExtensionLifecycleConfig(
            **cast("dict[str, Any]", config["lifecycle"]),
        ),
        monitoring=OICExtensionMonitoringConfig(
            **cast("dict[str, Any]", config["monitoring"]),
        ),
        performance=OICExtensionPerformanceConfig(
            **cast("dict[str, Any]", config["performance"]),
        ),
        extraction=OICExtensionExtractionConfig(
            **cast("dict[str, Any]", config["extraction"]),
        ),
        environment=cast("EnvironmentLiteral", config["environment"]),
        log_level=cast("LogLevelLiteral", config["log_level"]),
        debug=cast("bool", config["debug"]),
        instance_id=None,
        region=None,
    )


def create_test_oic_config(
    **overrides: str | int | bool | dict[str, Any],
) -> OracleOICExtensionSettings:
    """Create test configuration with minimal resource usage."""
    config = {
        "connection": {
            "base_url": "https://test-instance.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client_id",
            "oauth_client_secret": "test_client_secret",
            "oauth_token_url": "https://idcs-test.identity.oraclecloud.com/oauth2/v1/token",
        },
        "lifecycle": {
            "auto_activate": False,
            "health_check_interval": 3600,
            "activation_timeout": 30,
            "validate_before_activate": False,
            "rollback_on_failure": False,
        },
        "monitoring": {
            "enable_monitoring": False,
            "monitoring_interval": 3600,
            "alert_threshold": 50,
            "error_window_hours": 1,
            "performance_window_hours": 1,
        },
        "performance": {
            "request_timeout": 10,
            "max_retries": 1,
            "retry_delay": 0.5,
            "batch_size": 10,
            "max_concurrent_requests": 1,
        },
        "extraction": {
            "extract_artifacts": False,
            "extract_logs": False,
            "extract_metadata": True,
            "artifact_directory": "./test_artifacts",
            "log_window_hours": 1,
        },
        "environment": "test",
        "log_level": "WARNING",
        "debug": False,
    }

    # Override with provided values
    for key, value in overrides.items():
        if isinstance(value, dict) and key in config:
            current_value = config[key]
            if isinstance(current_value, dict):
                current_value.update(value)
            else:
                config[key] = value
        else:
            config[key] = value

    return OracleOICExtensionSettings(
        connection=OICExtensionConnectionConfig(
            **cast("dict[str, Any]", config["connection"]),
        ),
        lifecycle=OICExtensionLifecycleConfig(
            **cast("dict[str, Any]", config["lifecycle"]),
        ),
        monitoring=OICExtensionMonitoringConfig(
            **cast("dict[str, Any]", config["monitoring"]),
        ),
        performance=OICExtensionPerformanceConfig(
            **cast("dict[str, Any]", config["performance"]),
        ),
        extraction=OICExtensionExtractionConfig(
            **cast("dict[str, Any]", config["extraction"]),
        ),
        environment=cast("EnvironmentLiteral", config["environment"]),
        log_level=cast("LogLevelLiteral", config["log_level"]),
        debug=cast("bool", config["debug"]),
        instance_id=None,
        region=None,
    )


def create_sandbox_oic_config(
    **overrides: str | int | bool | dict[str, Any],
) -> OracleOICExtensionSettings:
    """Create sandbox configuration for experimentation and learning."""
    config = {
        "connection": {
            "base_url": "https://sandbox.integration.ocp.oraclecloud.com",
            "oauth_client_id": "sandbox_client",
            "oauth_client_secret": "sandbox_secret",
            "oauth_token_url": "https://idcs-sandbox.identity.oraclecloud.com/oauth2/v1/token",
        },
        "lifecycle": {
            "auto_activate": False,
            "health_check_interval": 60,
            "activation_timeout": 30,
            "validate_before_activate": False,
            "rollback_on_failure": False,
        },
        "monitoring": {
            "enable_monitoring": True,
            "monitoring_interval": 30,
            "alert_threshold": 70,
            "error_window_hours": 2,
            "performance_window_hours": 1,
        },
        "performance": {
            "request_timeout": 20,
            "max_retries": 2,
            "retry_delay": 0.5,
            "batch_size": 25,
            "max_concurrent_requests": 2,
        },
        "extraction": {
            "extract_artifacts": True,
            "extract_logs": True,
            "extract_metadata": True,
            "artifact_directory": "./sandbox_artifacts",
            "log_window_hours": 4,
        },
        "environment": "dev",  # Sandbox uses dev environment
        "log_level": "DEBUG",
        "debug": True,
    }

    # Override with provided values
    for key, value in overrides.items():
        if isinstance(value, dict) and key in config:
            current_value = config[key]
            if isinstance(current_value, dict):
                current_value.update(value)
            else:
                config[key] = value
        else:
            config[key] = value

    return OracleOICExtensionSettings(
        connection=OICExtensionConnectionConfig(
            **cast("dict[str, Any]", config["connection"]),
        ),
        lifecycle=OICExtensionLifecycleConfig(
            **cast("dict[str, Any]", config["lifecycle"]),
        ),
        monitoring=OICExtensionMonitoringConfig(
            **cast("dict[str, Any]", config["monitoring"]),
        ),
        performance=OICExtensionPerformanceConfig(
            **cast("dict[str, Any]", config["performance"]),
        ),
        extraction=OICExtensionExtractionConfig(
            **cast("dict[str, Any]", config["extraction"]),
        ),
        environment=cast("EnvironmentLiteral", config["environment"]),
        log_level=cast("LogLevelLiteral", config["log_level"]),
        debug=cast("bool", config["debug"]),
        instance_id=None,
        region=None,
    )


def configure_for_meltano(
    config_dict: dict[str, Any],
) -> FlextMeltanoResult[Any]:
    """Configure Oracle OIC extension from Meltano configuration dictionary."""
    try:
        settings = OracleOICExtensionSettings.from_dict(config_dict)
        return FlextMeltanoResult.ok(settings)
    except (ValueError, TypeError, AttributeError, KeyError) as e:
        return FlextMeltanoResult.ok(error=f"Failed to configure from Meltano: {e}")


# Export convenience functions
__all__ = [
    "configure_for_meltano",
    "create_development_oic_config",
    "create_production_oic_config",
    "create_sandbox_oic_config",
    "create_test_oic_config",
    "setup_oic_extension",
]
