"""Common configuration classes for FLEXT Meltano taps and targets.

This module consolidates configuration patterns that were duplicated across
multiple tap and target projects, eliminating code duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings


class FlextMeltanoBaseConfig(BaseSettings):
    """Base configuration class for all FLEXT Meltano taps and targets.

    Provides common patterns and validation that were duplicated across projects.
    """

    # Performance settings (common to all taps/targets)
    batch_size: int = Field(
        default=1000,
        description="Batch size for processing records",
        gt=0,
        le=10000,
    )
    timeout: int = Field(
        default=30,
        description="Request timeout in seconds",
        gt=0,
        le=300,
    )
    max_retries: int = Field(
        default=3,
        description="Maximum retry attempts",
        ge=0,
        le=10,
    )

    # Logging configuration (common pattern)
    log_level: str = Field(
        default="INFO",
        description="Logging level",
    )

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level is acceptable."""
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if v.upper() not in allowed:
            msg = f"Invalid log_level: {v}. Must be one of {allowed}"
            raise ValueError(msg)
        return v.upper()


class FlextMeltanoConnectionConfig(BaseModel):
    """Common connection configuration patterns.

    Consolidates connection patterns that were duplicated across Oracle WMS,
    Oracle OIC, LDAP, and other tap/target projects.
    """

    host: str = Field(..., description="Server hostname or IP address")
    port: int = Field(description="Server port")
    timeout: int = Field(
        default=30,
        description="Connection timeout in seconds",
        gt=0,
        le=300,
    )
    use_ssl: bool = Field(
        default=False,
        description="Use SSL/TLS for connection",
    )

    # Connection pooling (common to Oracle connections)
    max_connections: int = Field(
        default=10,
        description="Maximum number of connections in pool",
        gt=0,
        le=100,
    )

    # Retry configuration (common pattern)
    max_retries: int = Field(
        default=3,
        description="Maximum retry attempts for connections",
        ge=0,
        le=10,
    )
    retry_delay: int = Field(
        default=1,
        description="Delay between retries in seconds",
        ge=0,
        le=60,
    )


class FlextMeltanoAuthConfig(BaseModel):
    """Common authentication configuration patterns.

    Consolidates auth patterns from Oracle WMS, Oracle OIC, LDAP projects.
    """

    username: str = Field(..., description="Authentication username")
    password: str = Field(
        ...,
        description="Authentication password",
        json_schema_extra={"secret": True},
    )
    auth_method: str = Field(
        default="basic",
        description="Authentication method",
    )

    @field_validator("auth_method")
    @classmethod
    def validate_auth_method(cls, v: str) -> str:
        """Validate authentication method."""
        allowed = {"basic", "token", "oauth", "bearer", "certificate"}
        if v.lower() not in allowed:
            msg = f"Invalid auth_method: {v}. Must be one of {allowed}"
            raise ValueError(msg)
        return v.lower()


class FlextMeltanoStreamConfig(BaseModel):
    """Common stream configuration patterns.

    Consolidates stream configuration that was duplicated across tap projects.
    """

    name: str = Field(..., description="Stream name")
    primary_keys: list[str] | None = Field(
        default=None,
        description="Primary key fields",
    )
    replication_key: str | None = Field(
        default=None,
        description="Replication key field",
    )
    replication_method: str = Field(
        default="FULL_TABLE",
        description="Replication method",
    )

    # Performance configuration (common to all streams)
    batch_size: int = Field(
        default=1000,
        description="Batch size for stream processing",
        gt=0,
        le=10000,
    )

    # Schema configuration
    json_schema: dict[str, Any] | None = Field(
        default=None,
        description="JSON schema for the stream",
    )

    @field_validator("replication_method")
    @classmethod
    def validate_replication_method(cls, v: str) -> str:
        """Validate replication method."""
        allowed = {"FULL_TABLE", "INCREMENTAL", "LOG_BASED"}
        if v.upper() not in allowed:
            msg = f"Invalid replication_method: {v}. Must be one of {allowed}"
            raise ValueError(msg)
        return v.upper()


class FlextMeltanoValidationConfig(BaseModel):
    """Common validation configuration patterns.

    Consolidates validation patterns from target projects.
    """

    # Error handling configuration
    ignore_errors: bool = Field(
        default=True,
        description="Continue processing on validation errors",
    )
    max_errors: int = Field(
        default=100,
        description="Maximum number of errors before stopping",
        gt=0,
    )

    # Validation strictness
    strict_mode: bool = Field(
        default=False,
        description="Enable strict validation mode",
    )
    validate_schema: bool = Field(
        default=True,
        description="Validate records against schema",
    )

    # Data quality settings
    allow_null_values: bool = Field(
        default=True,
        description="Allow null values in non-required fields",
    )
    trim_whitespace: bool = Field(
        default=True,
        description="Trim whitespace from string values",
    )


class FlextMeltanoLDAPConnectionConfig(FlextMeltanoConnectionConfig):
    """LDAP connection configuration consolidating tap-ldap and target-ldap patterns.

    Eliminates 100+ lines of duplicated LDAP configuration between projects.
    """

    host: str = Field(..., description="LDAP server hostname or IP address")
    port: int = Field(default=389, description="LDAP server port (389 for LDAP, 636 for LDAPS)")
    bind_dn: str | None = Field(None, description="Distinguished name for binding to LDAP")
    bind_password: str | None = Field(None, description="Password for LDAP authentication")
    base_dn: str = Field(..., description="Base DN for LDAP searches")
    use_ssl: bool = Field(default=False, description="Use SSL/TLS for LDAP connection")
    use_tls: bool = Field(default=False, description="Use StartTLS after plain connection")
    connect_timeout: int = Field(default=10, description="Connection timeout in seconds", gt=0)
    receive_timeout: int = Field(default=30, description="Receive timeout in seconds", gt=0)
    page_size: int = Field(default=1000, description="Page size for paged results", gt=0)
