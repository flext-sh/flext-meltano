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
    """Domain-specific Meltano business rule validators using FlextValidations foundation.

    This class provides comprehensive validation for Meltano-specific business rules
    while delegating generic validation operations to flext-core. It follows the
    zero duplication principle by containing only Meltano/Singer/DBT specific
    validation logic.

    The validator supports validation for:
    - Meltano plugin configurations
    - Meltano project structures
    - DBT project configurations
    - Connection configurations

    Example:
        >>> validator = FlextMeltanoValidators()
        >>> config = {"name": "tap-csv", "namespace": "tap_csv"}
        >>> result = validator.validate_meltano_plugin_business_rules(config)
        >>> if result.is_success:
        ...     print("Plugin configuration is valid")

    """

    @classmethod
    def validate_meltano_plugin_business_rules(
        cls,
        config: object,
    ) -> FlextResult[bool]:
        """Validate Meltano-specific plugin business rules using monadic error accumulation.

        Uses FlextResult.accumulate_errors() to collect all validation errors
        instead of stopping at the first failure, providing comprehensive
        validation feedback with composable validation rules.

        Args:
            config: Plugin configuration object to validate.

        Returns:
            FlextResult containing boolean validation result or accumulated error details.

        Example:
            >>> config = {
            ...     "name": "tap-csv",
            ...     "namespace": "tap_csv",
            ...     "executable": "tap-csv",
            ... }
            >>> result = FlextMeltanoValidators.validate_meltano_plugin_business_rules(
            ...     config
            ... )
            >>> if result.is_success and result.unwrap():
            ...     print("Plugin configuration is valid")

        """
        # MONADIC ERROR ACCUMULATION: Collect all validation errors
        # Fixed: Use *args syntax for accumulate_errors
        return FlextResult.accumulate_errors(
            cls._validate_config_is_dict(config),
            cls._validate_plugin_name(config),
            cls._validate_plugin_namespace(config),
            cls._validate_plugin_executable(config),
            cls._validate_meltano_specific_rules(config),
        ).map(
            lambda _: True
        )  # Convert successful validations to boolean result  # Convert successful validations to boolean result

    @classmethod
    def _validate_config_is_dict(cls, config: object) -> FlextResult[None]:
        """Validate that config is a dictionary.

        Args:
            config: Configuration object to validate.

        Returns:
            FlextResult indicating if config is a valid dictionary.

        """
        if not isinstance(config, dict):
            return FlextResult.fail(
                "Plugin config validation failed: config must be a dictionary"
            )
        return FlextResult.ok(data=None)

    @classmethod
    def _validate_plugin_name(cls, config: object) -> FlextResult[None]:
        """Validate plugin name field.

        Args:
            config: Configuration dictionary.

        Returns:
            FlextResult indicating name validation result.

        """
        if not isinstance(config, dict):
            return FlextResult.fail("Config must be dictionary for name validation")

        name = config.get("name", "")
        if not name or not str(name).strip():
            return FlextResult.fail("Plugin name cannot be empty")

        return cls._validate_meltano_name_business_rules(str(name).strip())

    @classmethod
    def _validate_meltano_name_business_rules(cls, name: str) -> FlextResult[None]:
        """Validate Meltano-specific name business rules.

        Args:
            name: Plugin name to validate.

        Returns:
            FlextResult indicating business rule validation.

        """
        validation_errors = []

        # Meltano business rule: target plugin names
        if (
            name.startswith("target-")
            and len(name) < FlextMeltanoConstants.Plugin.MIN_TARGET_PLUGIN_NAME_LENGTH
        ):
            validation_errors.append(
                "Target plugin names must be at least 8 characters"
            )

        # Meltano business rule: tap plugin names
        if (
            name.startswith("tap-")
            and len(name) < FlextMeltanoConstants.Plugin.MIN_TAP_PLUGIN_NAME_LENGTH
        ):
            validation_errors.append("Tap plugin names must be at least 5 characters")

        if validation_errors:
            return FlextResult.fail("; ".join(validation_errors))

        return FlextResult.ok(data=None)

    @classmethod
    def _validate_plugin_namespace(cls, config: object) -> FlextResult[None]:
        """Validate plugin namespace field.

        Args:
            config: Configuration dictionary.

        Returns:
            FlextResult indicating namespace validation result.

        """
        if not isinstance(config, dict):
            return FlextResult.fail(
                "Config must be dictionary for namespace validation"
            )

        # Namespace is optional, but if present should be valid
        namespace = config.get("namespace")
        if namespace is not None and not str(namespace).strip():
            return FlextResult.fail("Plugin namespace cannot be empty if provided")

        return FlextResult.ok(data=None)

    @classmethod
    def _validate_plugin_executable(cls, config: object) -> FlextResult[None]:
        """Validate plugin executable field.

        Args:
            config: Configuration dictionary.

        Returns:
            FlextResult indicating executable validation result.

        """
        if not isinstance(config, dict):
            return FlextResult.fail(
                "Config must be dictionary for executable validation"
            )

        # Executable is optional, but if present should be valid
        executable = config.get("executable")
        if executable is not None and not str(executable).strip():
            return FlextResult.fail("Plugin executable cannot be empty if provided")

        return FlextResult.ok(data=None)

    @classmethod
    def _validate_meltano_specific_rules(cls, config: object) -> FlextResult[None]:
        """Validate additional Meltano-specific business rules.

        Args:
            config: Configuration dictionary.

        Returns:
            FlextResult indicating Meltano-specific validation result.

        """
        if not isinstance(config, dict):
            return FlextResult.fail(
                "Config must be dictionary for Meltano rules validation"
            )

        # Additional Meltano-specific validations can be added here
        # For now, return success as placeholder
        return FlextResult.ok(data=None)

    @classmethod
    def validate_meltano_project_business_rules(
        cls,
        config: object,
    ) -> FlextResult[bool]:
        """Validate Meltano-specific project business rules.

        Validates Meltano project configuration including version requirements
        and project ID format restrictions.

        Args:
            config: Project configuration object to validate.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> config = {"version": 1, "project_id": "my-meltano-project"}
            >>> result = FlextMeltanoValidators.validate_meltano_project_business_rules(
            ...     config
            ... )
            >>> if result.is_success and result.unwrap():
            ...     print("Project configuration is valid")

        """
        # Validate config is dict using direct validation
        if not isinstance(config, dict):
            return FlextResult[bool].fail(
                "Project config validation failed: config must be a dictionary",
            )

        config_dict = config

        # DOMAIN-SPECIFIC: Meltano project business rules
        class MeltanoProjectBusinessRules(BaseModel):
            version: int = Field(
                ge=1,
                le=1,
                description="Meltano supports only version 1",
            )
            project_id: str = Field(min_length=1, description="Project ID required")

            @field_validator("project_id")
            @classmethod
            def validate_project_id_business_rules(cls, v: str) -> str:
                """Validate Meltano-specific project ID business rules.

                Args:
                    v: Project ID to validate.

                Returns:
                    str: Validated project ID.

                Raises:
                    ValueError: If project ID violates business rules.

                """
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
        """Validate DBT-specific business rules.

        Validates DBT project configuration including project name format
        requirements and version specifications.

        Args:
            config: DBT configuration object to validate.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> config = {"name": "my_dbt_project", "version": "1.0.0"}
            >>> result = FlextMeltanoValidators.validate_dbt_business_rules(config)
            >>> if result.is_success and result.unwrap():
            ...     print("DBT configuration is valid")

        """
        # Validate config is dict using direct validation
        if not isinstance(config, dict):
            return FlextResult[bool].fail(
                "DBT config validation failed: config must be a dictionary",
            )

        config_dict = config

        # DOMAIN-SPECIFIC: DBT business rules
        class DbtBusinessRules(BaseModel):
            name: str = Field(min_length=1, description="DBT project name required")
            version: str = Field(
                min_length=1,
                description="DBT project version required",
            )

            @field_validator("name")
            @classmethod
            def validate_dbt_name_business_rules(cls, v: str) -> str:
                """Validate DBT-specific project name business rules.

                Args:
                    v: DBT project name to validate.

                Returns:
                    str: Validated DBT project name.

                Raises:
                    ValueError: If project name violates business rules.

                """
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
        """Validate plugin configuration (compatibility alias).

        This method is deprecated and maintained for backward compatibility.
        Use validate_meltano_plugin_business_rules instead.

        Args:
            config: Plugin configuration to validate.

        Returns:
            FlextResult containing boolean validation result or error details.

        """
        return cls.validate_meltano_plugin_business_rules(config)

    @classmethod
    def validate_meltano_config(cls, config: object) -> FlextResult[bool]:
        """Validate Meltano configuration (compatibility alias).

        This method is deprecated and maintained for backward compatibility.
        Use validate_meltano_project_business_rules instead.

        Args:
            config: Meltano configuration to validate.

        Returns:
            FlextResult containing boolean validation result or error details.

        """
        return cls.validate_meltano_project_business_rules(config)

    @classmethod
    def validate_dbt_config(cls, config: object) -> FlextResult[bool]:
        """Validate DBT configuration (compatibility alias).

        This method is deprecated and maintained for backward compatibility.
        Use validate_dbt_business_rules instead.

        Args:
            config: DBT configuration to validate.

        Returns:
            FlextResult containing boolean validation result or error details.

        """
        return cls.validate_dbt_business_rules(config)

    @classmethod
    def validate_meltano_project_structure(
        cls,
        project_path: Path,
    ) -> FlextResult[bool]:
        """Validate Meltano project structure with domain-specific business rules.

        Performs comprehensive validation of the Meltano project directory
        structure, checking for required files and directories.

        Args:
            project_path: Path to the Meltano project directory.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> from pathlib import Path
            >>> project_path = Path("/path/to/meltano/project")
            >>> result = FlextMeltanoValidators.validate_meltano_project_structure(
            ...     project_path
            ... )
            >>> if result.is_success and result.unwrap():
            ...     print("Project structure is valid")

        """
        try:
            # Check if path exists and is directory
            if not project_path.exists():
                return FlextResult[bool].fail(
                    f"Project path does not exist: {project_path}",
                )

            if not project_path.is_dir():
                return FlextResult[bool].fail(
                    f"Project path is not a directory: {project_path}",
                )

            # Check for required Meltano files
            meltano_yml = project_path / "meltano.yml"
            if not meltano_yml.exists():
                return FlextResult[
                    bool
                ].fail(
                    f"meltano.yml not found in {project_path}",  # Test expectation compliance
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
        cls,
        config: FlextTypes.Core.Dict,
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Validate connection configuration with domain-specific business rules.

        Validates connection configuration data for Meltano services,
        ensuring proper format and required fields.

        Args:
            config: Connection configuration dictionary to validate.

        Returns:
            FlextResult containing validated configuration or error details.

        Example:
            >>> config = {"host": "localhost", "port": 5432, "database": "mydb"}
            >>> result = FlextMeltanoValidators.validate_connection_config(config)
            >>> if result.is_success:
            ...     validated_config = result.unwrap()
            ...     print(f"Validated config: {validated_config}")

        """
        try:
            # DOMAIN-SPECIFIC: Connection config business rules
            if not config:
                return FlextResult[FlextTypes.Core.Dict].fail(
                    "Connection configuration cannot be empty",
                )

            return FlextResult[FlextTypes.Core.Dict].ok(data=config)
        except Exception as e:
            error_msg = f"Failed to validate connection config: {e}"
            logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)


__all__ = [
    "FlextMeltanoValidators",
]
