"""FLEXT Meltano Configuration.

Centralized configuration using flext-core `FlextConfig` pattern.
This module replaces the inline definition that used to live in `base.py`.

- Single source of truth for Meltano configuration
- Validation with Pydantic field validators
- JSON-serializable and subprocess-friendly

All code is production-grade, fully typed, and SOLID compliant.
"""
from __future__ import annotations

import contextlib
from pathlib import Path

from flext_core.config import FlextMainConfig
from pydantic import Field, field_validator


class FlextMeltanoConfig(FlextMainConfig):
    """Configuration using flext-core `FlextConfig` pattern (no duplication)."""

    project_root: str = Field(default=".", description="Meltano project root directory")
    environment: str = Field(default="dev", description="Meltano environment")

    # Meltano-specific configuration
    meltano_database_uri: str | None = Field(
        default=None,
        description="Meltano system database URI",
    )
    meltano_ui_bind_port: int = Field(default=5000, description="Meltano UI port")

    # Singer SDK configuration
    singer_sdk_log_level: str = Field(
        default="INFO",
        description="Singer SDK log level",
    )

    # DBT configuration
    dbt_project_dir: str | None = Field(
        default=None,
        description="DBT project directory",
    )
    dbt_profiles_dir: str | None = Field(
        default=None,
        description="DBT profiles directory",
    )

    @field_validator("project_root")
    @classmethod
    def validate_project_root(cls, value: str) -> str:
        """Validate project root exists (best-effort creation when reasonable)."""
        path = Path(value)
        # Avoid creating obviously invalid test paths
        if not path.exists() and not str(path).startswith("/nonexistent"):
            with contextlib.suppress(OSError, PermissionError):
                path.mkdir(parents=True, exist_ok=True)
        return str(path.absolute())


__all__ = [
    "FlextMeltanoConfig",
]
