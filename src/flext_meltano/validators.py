"""FLEXT Meltano Validators - DOMAIN-SPECIFIC Meltano business rules using flext-core.

This module provides ONLY Meltano/Singer/DBT-specific business rule validations that cannot
be generalized to flext-core. ALL generic validation operations MUST use FlextValidations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextLogger, FlextResult, FlextValidations
from pydantic import BaseModel, Field, field_validator

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
        # Delegate generic dict validation to flext-core
        dict_result = FlextValidations.Core.TypeValidators.validate_dict(config)
        if dict_result.is_failure:
            return FlextResult[bool].fail(
                f"Plugin config validation failed: {dict_result.error}"
            )

        config_dict = dict_result.unwrap()

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

        # Delegate Pydantic validation to flext-core
        return FlextValidations.Core.validate_with_pydantic_schema(
            config_dict, MeltanoPluginBusinessRules
        ).map(lambda _: True)

    @classmethod
    def validate_meltano_project_business_rules(
        cls, config: object
    ) -> FlextResult[bool]:
        """Validate MELTANO-SPECIFIC project business rules."""
        # Delegate generic dict validation to flext-core
        dict_result = FlextValidations.Core.TypeValidators.validate_dict(config)
        if dict_result.is_failure:
            return FlextResult[bool].fail(
                f"Project config validation failed: {dict_result.error}"
            )

        config_dict = dict_result.unwrap()

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

        # Delegate Pydantic validation to flext-core
        return FlextValidations.Core.validate_with_pydantic_schema(
            config_dict, MeltanoProjectBusinessRules
        ).map(lambda _: True)

    @classmethod
    def validate_dbt_business_rules(cls, config: object) -> FlextResult[bool]:
        """Validate DBT-SPECIFIC business rules."""
        # Delegate generic dict validation to flext-core
        dict_result = FlextValidations.Core.TypeValidators.validate_dict(config)
        if dict_result.is_failure:
            return FlextResult[bool].fail(
                f"DBT config validation failed: {dict_result.error}"
            )

        config_dict = dict_result.unwrap()

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

        # Delegate Pydantic validation to flext-core
        return FlextValidations.Core.validate_with_pydantic_schema(
            config_dict, DbtBusinessRules
        ).map(lambda _: True)

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


__all__ = [
    "FlextMeltanoValidators",
]
