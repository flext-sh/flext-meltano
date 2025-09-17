"""FLEXT Meltano Validators - Domain-specific business rule validators.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import contextlib
from pathlib import Path

from pydantic import BaseModel, Field, field_validator

from flext_core import FlextLogger, FlextResult, FlextTypes
from flext_meltano.constants import FlextMeltanoConstants

logger = FlextLogger(__name__)


class FlextMeltanoValidators:
    """DOMAIN-SPECIFIC Meltano business rule validators using FlextValidations foundation.

    ZERO DUPLICATION PRINCIPLE:
    - Uses FlextValidations.Core for ALL generic validation operations
    - Contains ONLY Meltano/Singer/DBT business rule validations
    - NO generic validation logic - delegate to flext-core
    """

    @classmethod
    def validate_meltano_plugin_business_rules(
        cls, config: object
    ) -> FlextResult[bool]:
        """Validate MELTANO-SPECIFIC plugin business rules."""
        # Validate config is dict using direct validation
        if not isinstance(config, dict):
            return FlextResult[bool].fail(
                "Plugin config validation failed: config must be a dictionary"
            )

        config_dict = config

        # DOMAIN-SPECIFIC: Meltano plugin business rules
        class MeltanoPluginBusinessRules(BaseModel):
            name: str = Field(min_length=1, description="Plugin name required")
            namespace: str = Field(description="Plugin namespace (optional)")
            pip_url: str = Field(description="Plugin pip URL (optional)")
            executable: str = Field(description="Plugin executable (optional)")

            @field_validator("name")
            @classmethod
            def validate_plugin_name_business_rules(cls, v: str) -> str:
                """MELTANO-SPECIFIC: Plugin name business rules."""
                if not v or not v.strip():
                    msg = "Plugin name cannot be empty"
                    raise ValueError(msg)
                # Meltano business rule: names with special prefixes
                if (
                    v.startswith("target-")
                    and len(v)
                    < FlextMeltanoConstants.Plugin.MIN_TARGET_PLUGIN_NAME_LENGTH
                ):
                    msg = "Target plugin names must be at least 8 characters"
                    raise ValueError(msg)
                if (
                    v.startswith("tap-")
                    and len(v) < FlextMeltanoConstants.Plugin.MIN_TAP_PLUGIN_NAME_LENGTH
                ):
                    msg = "Tap plugin names must be at least 5 characters"
                    raise ValueError(msg)
                return v

        # Use Pydantic model validation directly
        try:
            MeltanoPluginBusinessRules.model_validate(config_dict)
            return FlextResult[bool].ok(data=True)
        except Exception as e:
            return FlextResult[bool].fail(f"Plugin validation failed: {e}")

    @classmethod
    def validate_meltano_project_business_rules(
        cls, config: object
    ) -> FlextResult[bool]:
        """Validate MELTANO-SPECIFIC project business rules."""
        # Validate config is dict using direct validation
        if not isinstance(config, dict):
            return FlextResult[bool].fail(
                "Project config validation failed: config must be a dictionary"
            )

        config_dict = config

        # DOMAIN-SPECIFIC: Meltano project business rules
        class MeltanoProjectBusinessRules(BaseModel):
            version: int = Field(
                ge=1, le=1, description="Meltano supports only version 1"
            )
            project_id: str = Field(min_length=1, description="Project ID required")

            @field_validator("project_id")
            @classmethod
            def validate_project_id_business_rules(cls, v: str) -> str:
                """MELTANO-SPECIFIC: Project ID business rules."""
                if not v.strip():
                    msg = "Project ID cannot be empty or whitespace"
                    raise ValueError(msg)
                # Meltano business rule: project ID format restrictions
                if " " in v:
                    msg = "Project ID cannot contain spaces"
                    raise ValueError(msg)
                if not v.replace("-", "").replace("_", "").isalnum():
                    msg = "Project ID can only contain letters, numbers, hyphens, and underscores"
                    raise ValueError(msg)
                return v

        # Use Pydantic model validation directly
        try:
            MeltanoProjectBusinessRules.model_validate(config_dict)
            return FlextResult[bool].ok(data=True)
        except Exception as e:
            return FlextResult[bool].fail(f"Project validation failed: {e}")

    @classmethod
    def validate_dbt_business_rules(cls, config: object) -> FlextResult[bool]:
        """Validate DBT-SPECIFIC business rules."""
        # Validate config is dict using direct validation
        if not isinstance(config, dict):
            return FlextResult[bool].fail(
                "DBT config validation failed: config must be a dictionary"
            )

        config_dict = config

        # DOMAIN-SPECIFIC: DBT business rules
        class DbtBusinessRules(BaseModel):
            name: str = Field(min_length=1, description="DBT project name required")
            version: str = Field(
                min_length=1, description="DBT project version required"
            )

            @field_validator("name")
            @classmethod
            def validate_dbt_name_business_rules(cls, v: str) -> str:
                """DBT-SPECIFIC: DBT project name business rules."""
                if not v or not v.strip():
                    msg = "DBT project name cannot be empty"
                    raise ValueError(msg)
                # DBT business rule: no spaces in project names
                if " " in v:
                    msg = "DBT project names cannot contain spaces"
                    raise ValueError(msg)
                return v

        # Use Pydantic model validation directly
        try:
            DbtBusinessRules.model_validate(config_dict)
            return FlextResult[bool].ok(data=True)
        except Exception as e:
            return FlextResult[bool].fail(f"DBT validation failed: {e}")

    # =================================================================
    # COMPATIBILITY ALIASES - For existing tests ONLY
    # =================================================================

    @classmethod
    def validate_plugin_config(cls, config: object) -> FlextResult[bool]:
        """DEPRECATED: Use validate_meltano_plugin_business_rules instead."""
        return cls.validate_meltano_plugin_business_rules(config)

    @classmethod
    def validate_meltano_config(cls, config: object) -> FlextResult[bool]:
        """DEPRECATED: Use validate_meltano_project_business_rules instead."""
        return cls.validate_meltano_project_business_rules(config)

    @classmethod
    def validate_dbt_config(cls, config: object) -> FlextResult[bool]:
        """DEPRECATED: Use validate_dbt_business_rules instead."""
        return cls.validate_dbt_business_rules(config)

    @classmethod
    def validate_meltano_project_structure(
        cls, project_path: Path
    ) -> FlextResult[bool]:
        """Validate Meltano project structure - DOMAIN-SPECIFIC business rules."""
        try:
            # Check if path exists and is directory
            if not project_path.exists():
                return FlextResult[bool].fail(
                    f"Project path does not exist: {project_path}"
                )

            if not project_path.is_dir():
                return FlextResult[bool].fail(
                    f"Project path is not a directory: {project_path}"
                )

            # Check for required Meltano files
            meltano_yml = project_path / "meltano.yml"
            if not meltano_yml.exists():
                return FlextResult[
                    bool
                ].fail(
                    f"meltano.yml not found in {project_path}"  # Test expectation compliance
                )

            # Check for transform directory (DBT) - optional for basic projects
            transform_dir = project_path / "transform"
            if not transform_dir.exists():
                # Create transform directory if it doesn't exist (optional)
                with contextlib.suppress(OSError):
                    transform_dir.mkdir(parents=True, exist_ok=True)

            return FlextResult[bool].ok(data=True)
        except Exception as e:
            error_msg = f"Failed to validate project structure: {e}"
            logger.exception(error_msg)
            return FlextResult[bool].fail(error_msg)

    @classmethod
    def validate_connection_config(
        cls, config: FlextTypes.Core.Dict
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Validate connection configuration - DOMAIN-SPECIFIC business rules."""
        try:
            # DOMAIN-SPECIFIC: Connection config business rules
            if not config:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    "Connection configuration cannot be empty"
                )

            return FlextResult[FlextTypes.Core.Dict].ok(config)
        except Exception as e:
            error_msg = f"Failed to validate connection config: {e}"
            logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)


__all__ = [
    "FlextMeltanoValidators",
]
