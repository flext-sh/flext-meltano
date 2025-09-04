"""FLEXT Meltano Validators - Extending FlextUtilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TypeVar

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextUtilities,
)
from pydantic import BaseModel, Field, field_validator

# Type variables
T = TypeVar("T")

logger = FlextLogger(__name__)

# Constants to avoid FBT003 violations

# =============================================================================
# FLEXT MELTANO VALIDATORS - EXTENDING FlextUtilities (ZERO DUPLICATION)
# =============================================================================


class FlextMeltanoValidators(FlextUtilities):
    """FLEXT Meltano Validators extending FlextUtilities with Meltano-specific validation."""

    # =================================================================
    # MELTANO-SPECIFIC VALIDATORS (Only what's NOT in FlextUtilities)
    # =================================================================

    @classmethod
    def validate_plugin_config(cls, config: object) -> FlextResult[bool]:
        """Valida plugin config usando Pydantic validation."""
        try:

            class PluginConfigSchema(BaseModel):
                name: str = Field(min_length=1)
                namespace: str = Field(min_length=1)
                pip_url: str = Field(min_length=1)
                executable: str = Field(min_length=1)

            # Validate using Pydantic - automatic type and constraint validation
            if isinstance(config, dict):
                PluginConfigSchema(**config)
                return FlextResult[bool].ok(data=True)
            return FlextResult[bool].fail("Config must be a dictionary")
        except Exception as e:
            return FlextResult[bool].fail(f"Plugin config validation failed: {e}")

    @classmethod
    def validate_meltano_config(cls, config: object) -> FlextResult[bool]:
        """Valida Meltano config usando Pydantic validation."""
        try:

            class MeltanoConfigSchema(BaseModel):
                version: int = Field(ge=1, le=1)  # Must be exactly version 1
                project_id: str = Field(min_length=1)

                @field_validator("project_id")
                @classmethod
                def validate_project_id(cls, v: str) -> str:
                    if not v.strip():
                        msg = "Project ID cannot be empty or whitespace"
                        raise ValueError(msg)
                    return v

            # Validate using Pydantic
            if isinstance(config, dict):
                MeltanoConfigSchema(**config)
                return FlextResult[bool].ok(data=True)
            return FlextResult[bool].fail("Config must be a dictionary")
        except Exception as e:
            return FlextResult[bool].fail(f"Meltano config validation failed: {e}")

    @classmethod
    def validate_dbt_config(cls, config: object) -> FlextResult[bool]:
        """Valida DBT config usando Pydantic validation."""
        try:

            class DbtConfigSchema(BaseModel):
                name: str = Field(min_length=1)
                version: str = Field(min_length=1)

            # Validate using Pydantic
            if isinstance(config, dict):
                DbtConfigSchema(**config)
                return FlextResult[bool].ok(data=True)
            return FlextResult[bool].fail("Config must be a dictionary")
        except Exception as e:
            return FlextResult[bool].fail(f"DBT config validation failed: {e}")

    # =================================================================
    # PATH VALIDATION (Meltano-specific extensions of FlextUtilities)
    # =================================================================

    @classmethod
    def validate_directory_path(cls, path: str | Path | None) -> str | None:
        """Valida diretório usando validação real de sistema de arquivos."""
        if path is None:
            return None

        try:
            path_obj = Path(path)
            # Validate that path exists and is a directory
            if path_obj.exists() and path_obj.is_dir():
                return str(path_obj.absolute())
            return None
        except Exception:
            return None

    @classmethod
    def validate_file_path(cls, path: str | Path | None) -> str | None:
        """Valida arquivo usando validação real de sistema de arquivos."""
        if path is None:
            return None

        try:
            path_obj = Path(path)
            # Validate that path exists and is a file
            if path_obj.exists() and path_obj.is_file():
                return str(path_obj.absolute())
            return None
        except Exception:
            return None

    @classmethod
    def validate_config_value_simple(
        cls, value: object, expected_type: type[T], *, required: bool = True
    ) -> FlextResult[T | None]:
        """Valida config usando type conversion real."""
        try:
            if value is None:
                return (
                    FlextResult[T | None].ok(None)
                    if not required
                    else FlextResult[T | None].fail("Required value is None")
                )

            # Attempt type conversion with proper casting
            if expected_type is bool and isinstance(value, str):
                # Handle string to bool conversion
                converted_value = value.lower() in {"true", "1", "yes", "on"}
                return FlextResult[T | None].ok(converted_value)
            # Standard type conversion
            converted_value = expected_type(value)
            return FlextResult[T | None].ok(converted_value)
        except Exception as e:
            return FlextResult[T | None].fail(f"Type conversion failed: {e}")


__all__ = [
    # Main class only - no helper functions
    "FlextMeltanoValidators",
]
