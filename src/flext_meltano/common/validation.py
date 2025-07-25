"""Common validation functions for FLEXT Meltano taps and targets.

This module consolidates validation patterns that were duplicated across
multiple tap and target projects, providing centralized validation logic.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import ValidationError

from flext_meltano.common.config import (
    FlextMeltanoAuthConfig,
    FlextMeltanoConnectionConfig,
    FlextMeltanoStreamConfig,
)
from flext_meltano.exceptions import (
    FlextMeltanoValidationError,
)


def validate_connection_config(config: dict[str, Any]) -> dict[str, Any]:
    """Validate connection configuration using common patterns.

    Consolidates connection validation from Oracle WMS, Oracle OIC, LDAP projects.

    Args:
        config: Configuration dictionary to validate

    Returns:
        Validated configuration dictionary

    Raises:
        FlextMeltanoValidationError: If validation fails
    """
    try:
        connection_config = FlextMeltanoConnectionConfig(**config)
        return connection_config.model_dump()
    except ValidationError as e:
        msg = f"Connection configuration validation failed: {e}"
        raise FlextMeltanoValidationError(msg) from e


def validate_auth_config(config: dict[str, Any]) -> dict[str, Any]:
    """Validate authentication configuration using common patterns.

    Consolidates auth validation from multiple projects.

    Args:
        config: Authentication configuration to validate

    Returns:
        Validated authentication configuration

    Raises:
        FlextMeltanoValidationError: If validation fails
    """
    try:
        auth_config = FlextMeltanoAuthConfig(**config)
        return auth_config.model_dump()
    except ValidationError as e:
        msg = f"Authentication configuration validation failed: {e}"
        raise FlextMeltanoValidationError(msg) from e


def validate_stream_config(config: dict[str, Any]) -> dict[str, Any]:
    """Validate stream configuration using common patterns.

    Consolidates stream validation from tap projects.

    Args:
        config: Stream configuration to validate

    Returns:
        Validated stream configuration

    Raises:
        FlextMeltanoValidationError: If validation fails
    """
    try:
        stream_config = FlextMeltanoStreamConfig(**config)
        return stream_config.model_dump()
    except ValidationError as e:
        msg = f"Stream configuration validation failed: {e}"
        raise FlextMeltanoValidationError(msg) from e


class FlextMeltanoConfigValidator:
    """Common configuration validator for taps and targets.

    Consolidates validation logic that was duplicated across projects,
    providing a centralized validation interface.
    """

    def __init__(self, *, strict_mode: bool = False) -> None:
        """Initialize validator.

        Args:
            strict_mode: Enable strict validation mode
        """
        self.strict_mode = strict_mode
        self.errors: list[str] = []

    def validate_config(self, config: dict[str, Any]) -> bool:
        """Validate complete configuration.

        Args:
            config: Configuration dictionary to validate

        Returns:
            True if validation passes, False otherwise
        """
        self.errors = []

        # Validate required sections
        required_sections = ["connection", "auth"]
        for section in required_sections:
            if section not in config:
                self.errors.append(f"Missing required configuration section: {section}")

        # Validate connection configuration
        if "connection" in config:
            try:
                validate_connection_config(config["connection"])
            except FlextMeltanoValidationError as e:
                self.errors.append(str(e))

        # Validate authentication configuration
        if "auth" in config:
            try:
                validate_auth_config(config["auth"])
            except FlextMeltanoValidationError as e:
                self.errors.append(str(e))

        # Validate streams configuration (for taps)
        if "streams" in config:
            for i, stream_config in enumerate(config["streams"]):
                try:
                    validate_stream_config(stream_config)
                except FlextMeltanoValidationError as e:
                    self.errors.append(f"Stream {i} validation failed: {e}")

        return len(self.errors) == 0

    def get_errors(self) -> list[str]:
        """Get validation errors.

        Returns:
            List of validation error messages
        """
        return self.errors.copy()

    def validate_record(self, record: dict[str, Any]) -> list[str]:
        """Validate individual record.

        Consolidates record validation patterns from target projects.

        Args:
            record: Record to validate

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Basic record structure validation
        if not isinstance(record, dict):
            errors.append("Record must be a dictionary")
            return errors

        # Check for required fields (common pattern)
        if not record:
            errors.append("Record cannot be empty")

        # Validate field types (common patterns)
        for field_name, field_value in record.items():
            if field_name.startswith("_"):
                # Skip internal fields
                continue

            # Check for null values in required fields
            if field_value is None and self.strict_mode:
                errors.append(f"Field '{field_name}' cannot be null in strict mode")

        return errors

    def validate_batch(self, records: list[dict[str, Any]]) -> dict[str, Any]:
        """Validate batch of records.

        Consolidates batch validation patterns from target projects.

        Args:
            records: List of records to validate

        Returns:
            Validation results dictionary with statistics
        """
        if not records:
            return {
                "total_records": 0,
                "valid_records": 0,
                "invalid_records": 0,
                "errors": ["Batch cannot be empty"],
            }

        total_records = len(records)
        valid_records = 0
        invalid_records = 0
        batch_errors = []

        for i, record in enumerate(records):
            record_errors = self.validate_record(record)
            if record_errors:
                invalid_records += 1
                batch_errors.extend([f"Record {i}: {error}" for error in record_errors])
            else:
                valid_records += 1

        return {
            "total_records": total_records,
            "valid_records": valid_records,
            "invalid_records": invalid_records,
            "errors": batch_errors,
        }


# URL validation (consolidates 60+ lines of duplication)
def validate_base_url(url: str) -> str:
    """Validate base URL format - consolidates duplicated validation across projects.

    Eliminates duplication from:
    - flext-tap-oracle-wms/config.py
    - flext-oracle-oic-ext/config.py
    - flext-tap-oracle-oic/config.py

    Args:
        url: URL to validate

    Returns:
        Normalized URL (trailing slash removed)

    Raises:
        ValueError: If URL format is invalid
    """
    if not url.startswith(("http://", "https://")):
        msg = f"Invalid base_url: {url}. Must start with http:// or https://"
        raise ValueError(msg)
    return url.rstrip("/")


def validate_log_level(level: str) -> str:
    """Validate log level - consolidates duplicated validation across projects.

    Eliminates duplication from:
    - flext-tap-oracle-wms/config.py
    - flext-meltano/common/config.py
    - Other tap/target projects

    Args:
        level: Log level to validate

    Returns:
        Normalized log level (uppercase)

    Raises:
        ValueError: If log level is invalid
    """
    allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    if level.upper() not in allowed:
        msg = f"Invalid log_level: {level}. Must be one of {allowed}"
        raise ValueError(msg)
    return level.upper()


# File path validation (consolidates 60+ lines of LDIF duplication)
def validate_file_path(path: str | None) -> str | None:
    """Validate file path exists - consolidates LDIF validation patterns.

    Eliminates duplication from:
    - flext-tap-ldif/config.py
    - flext-target-ldif/config.py

    Args:
        path: File path to validate

    Returns:
        Original path if valid or None

    Raises:
        ValueError: If path doesn't exist or isn't a file
    """
    if path is None:
        return None

    file_path = Path(path)

    if not file_path.exists():
        msg = f"File path does not exist: {path}"
        raise ValueError(msg)
    if not file_path.is_file():
        msg = f"Path is not a file: {path}"
        raise ValueError(msg)
    return path


def validate_directory_path(path: str | None) -> str | None:
    """Validate directory path exists - consolidates LDIF validation patterns.

    Args:
        path: Directory path to validate

    Returns:
        Original path if valid or None

    Raises:
        ValueError: If path doesn't exist or isn't a directory
    """
    if path is None:
        return None

    dir_path = Path(path)

    if not dir_path.exists():
        msg = f"Directory path does not exist: {path}"
        raise ValueError(msg)
    if not dir_path.is_dir():
        msg = f"Path is not a directory: {path}"
        raise ValueError(msg)
    return path
# Oracle validation (consolidates Oracle validation patterns)
def validate_oracle_host_for_database(host: str | None, connection_type: str | None) -> str | None:
    """Validate Oracle host for database connections."""
    if connection_type in {"database", "hybrid"} and not host:
        msg = "Host is required for database connections"
        raise ValueError(msg)
    return host

def validate_oracle_service_name_for_database(service_name: str | None, connection_type: str | None) -> str | None:
    """Validate Oracle service name for database connections."""
    if connection_type in {"database", "hybrid"} and not service_name:
        msg = "Service name is required for database connections"
        raise ValueError(msg)
    return service_name
