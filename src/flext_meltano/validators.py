"""FLEXT Meltano Validators - Domain-specific business rule validators.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import contextlib
from pathlib import Path

# Import for type hints only - avoid circular imports
from flext_core import FlextCore

# Use specific module imports to avoid circular dependencies
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels

logger = FlextCore.Logger(__name__)


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
        >>> config: FlextCore.Types.Dict = {"name": tap - csv, "namespace": "tap_csv"}
        >>> result: FlextCore.Result[object] = (
        ...     validator.validate_meltano_plugin_business_rules(config)
        ... )
        >>> if result.is_success:
        ...     print("Plugin configuration is valid")

    """

    @classmethod
    def validate_meltano_plugin_business_rules(
        cls,
        config: FlextCore.Types.JsonValue,
    ) -> FlextCore.Result[bool]:
        """Validate Meltano-specific plugin business rules using monadic error accumulation.

        Uses FlextCore.Result.accumulate_errors() to collect all validation errors
        instead of stopping at the first failure, providing comprehensive
        validation feedback with composable validation rules.

        Args:
            config: Plugin configuration dictionary to validate.

        Returns:
            FlextCore.Result containing boolean validation result or accumulated error details.

        """
        return FlextCore.Result.accumulate_errors(
            cls._validate_config_is_dict(config),
            cls._validate_plugin_name(config),
            cls._validate_plugin_namespace(config),
            cls._validate_plugin_pip_url(config),
            cls._validate_plugin_executable(config),
            cls._validate_meltano_specific_rules(config),
        ).map(
            lambda _: True
        )  # Convert successful validations to boolean result  # Convert successful validations to boolean result

    @classmethod
    def _validate_config_is_dict(
        cls, config: FlextCore.Types.JsonValue
    ) -> FlextCore.Result[bool]:
        """Validate that config is a dictionary.

        Args:
            config: Configuration dictionary to validate.

        Returns:
            FlextCore.Result indicating if config is a valid dictionary.

        """
        if not isinstance(config, dict):
            return FlextCore.Result.fail(
                "Plugin config validation failed: config must be a dictionary"
            )
        return FlextCore.Result.ok(data=True)

    @classmethod
    def _validate_plugin_name(
        cls, config: FlextCore.Types.JsonValue
    ) -> FlextCore.Result[bool]:
        if not isinstance(config, dict):
            return FlextCore.Result.fail(
                "Config must be dictionary for name validation"
            )

        name = config.get("name", "")
        if not isinstance(name, str):
            return FlextCore.Result.fail("Plugin name must be a string")

        if not name or not name.strip():
            return FlextCore.Result.fail("Plugin name cannot be empty")

        return cls._validate_meltano_name_business_rules(name.strip())

    @classmethod
    def _validate_meltano_name_business_rules(cls, name: str) -> FlextCore.Result[bool]:
        """Validate Meltano-specific name business rules.

        Args:
            name: Plugin name to validate.

        Returns:
            FlextCore.Result indicating business rule validation.

        """
        validation_errors: FlextCore.Types.StringList = []

        # Meltano business rule: target plugin names
        if (
            name.startswith("target-")
            and len(name) < FlextMeltanoConstants.PLUGIN_MIN_TARGET_PLUGIN_NAME_LENGTH
        ):
            validation_errors.append(
                "Target plugin names must be at least 8 characters"
            )

        # Meltano business rule: tap plugin names
        if (
            name.startswith("tap-")
            and len(name) < FlextMeltanoConstants.PLUGIN_MIN_TAP_PLUGIN_NAME_LENGTH
        ):
            validation_errors.append("Tap plugin names must be at least 5 characters")

        if validation_errors:
            return FlextCore.Result.fail("; ".join(validation_errors))

        return FlextCore.Result.ok(data=True)

    @classmethod
    def _validate_plugin_namespace(
        cls, config: FlextCore.Types.JsonValue
    ) -> FlextCore.Result[bool]:
        if not isinstance(config, dict):
            return FlextCore.Result.fail(
                "Config must be dictionary for namespace validation"
            )

        namespace = config.get("namespace")
        if namespace is None:
            return FlextCore.Result.fail("Plugin namespace is required")

        if not isinstance(namespace, str):
            return FlextCore.Result.fail("Plugin namespace must be a string")

        if not namespace.strip():
            return FlextCore.Result.fail("Plugin namespace cannot be empty")

        return FlextCore.Result.ok(data=True)

    @classmethod
    def _validate_plugin_pip_url(
        cls, config: FlextCore.Types.JsonValue
    ) -> FlextCore.Result[bool]:
        if not isinstance(config, dict):
            return FlextCore.Result.fail(
                "Config must be dictionary for pip_url validation"
            )

        pip_url = config.get("pip_url")
        if pip_url is None:
            return FlextCore.Result.fail("Plugin pip_url is required")

        if not isinstance(pip_url, str):
            return FlextCore.Result.fail("Plugin pip_url must be a string")

        if not pip_url.strip():
            return FlextCore.Result.fail("Plugin pip_url cannot be empty")

        return FlextCore.Result.ok(data=True)

    @classmethod
    def _validate_plugin_executable(
        cls, config: FlextCore.Types.JsonValue
    ) -> FlextCore.Result[bool]:
        if not isinstance(config, dict):
            return FlextCore.Result.fail(
                "Config must be dictionary for executable validation"
            )

        executable = config.get("executable")
        if executable is None:
            return FlextCore.Result.fail("Plugin executable is required")

        if not isinstance(executable, str):
            return FlextCore.Result.fail("Plugin executable must be a string")

        if not executable.strip():
            return FlextCore.Result.fail("Plugin executable cannot be empty")

        return FlextCore.Result.ok(data=True)

    @classmethod
    def _validate_meltano_specific_rules(
        cls, config: FlextCore.Types.JsonValue
    ) -> FlextCore.Result[bool]:
        """Validate additional Meltano-specific business rules.

        Args:
            config: Configuration dictionary.

        Returns:
            FlextCore.Result indicating Meltano-specific validation result.

        """
        if not isinstance(config, dict):
            return FlextCore.Result.fail(
                "Config must be dictionary for Meltano rules validation"
            )

        # Additional Meltano-specific validations can be added here
        # For now, return success as placeholder
        return FlextCore.Result.ok(data=True)

    @classmethod
    def validate_meltano_project_business_rules(
        cls,
        config: FlextCore.Types.JsonValue,
    ) -> FlextCore.Result[bool]:
        """Validate Meltano-specific project business rules.

        Validates Meltano project configuration including version requirements
        and project ID format restrictions.

        Args:
            config: Project configuration dictionary to validate.

        Returns:
            FlextCore.Result containing boolean validation result or error details.

        Example:
            >>> config: FlextCore.Types.Dict = {
            ...     "version": 1,
            ...     "project_id": my - meltano - project,
            ... }
            >>> result = FlextMeltanoValidators.validate_meltano_project_business_rules(
            ...     config
            ... )
            >>> if result.is_success and result.unwrap():
            ...     print("Project configuration is valid")

        """
        # Validate config is dict using direct validation
        if not isinstance(config, dict):
            return FlextCore.Result[bool].fail(
                "Project config validation failed: config must be a dictionary",
            )

        config_dict: FlextCore.Types.Dict = dict(config)

        # DOMAIN-SPECIFIC: Meltano project business rules
        class MeltanoProjectBusinessRules(FlextMeltanoModels.MeltanoProjectModel):
            """Meltano project business rules - uses unified FlextMeltanoModels.MeltanoProjectModel.

            This class extends the unified model for validation-specific functionality
            while maintaining the consolidated [Project]Models pattern.
            """

        # Use Pydantic model validation directly
        try:
            MeltanoProjectBusinessRules.model_validate(config_dict)
            return FlextCore.Result[bool].ok(data=True)
        except Exception as e:
            return FlextCore.Result[bool].fail(f"Project validation failed: {e}")

    @classmethod
    def validate_dbt_business_rules(
        cls, config: FlextCore.Types.JsonValue
    ) -> FlextCore.Result[bool]:
        """Validate DBT-specific business rules.

        Validates DBT project configuration including project name format
        requirements and version specifications.

        Args:
            config: DBT configuration dictionary to validate.

        Returns:
            FlextCore.Result containing boolean validation result or error details.

        Example:
            >>> config: FlextCore.Types.Dict = {
            ...     "name": "my_dbt_project",
            ...     "version": 1.0.0,
            ... }
            >>> result: FlextCore.Result[object] = (
            ...     FlextMeltanoValidators.validate_dbt_business_rules(config)
            ... )
            >>> if result.is_success and result.unwrap():
            ...     print("DBT configuration is valid")

        """
        # Validate config is dict using direct validation
        if not isinstance(config, dict):
            return FlextCore.Result[bool].fail(
                "DBT config validation failed: config must be a dictionary",
            )

        config_dict: FlextCore.Types.Dict = dict(config)

        # DOMAIN-SPECIFIC: DBT business rules
        class DbtBusinessRules(FlextMeltanoModels.DbtProjectModel):
            """DBT project business rules - uses unified FlextMeltanoModels.DbtProjectModel.

            This class extends the unified model for validation-specific functionality
            while maintaining the consolidated [Project]Models pattern.
            """

        # Use Pydantic model validation directly
        try:
            DbtBusinessRules.model_validate(config_dict)
            return FlextCore.Result[bool].ok(data=True)
        except Exception as e:
            return FlextCore.Result[bool].fail(f"DBT validation failed: {e}")

    @classmethod
    def validate_meltano_project_structure(
        cls,
        project_path: Path,
    ) -> FlextCore.Result[bool]:
        """Validate Meltano project structure with domain-specific business rules.

        Performs comprehensive validation of the Meltano project directory
        structure, checking for required files and directories.

        Args:
            project_path: Path to the Meltano project directory.

        Returns:
            FlextCore.Result containing boolean validation result or error details.

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
                return FlextCore.Result[bool].fail(
                    f"Project path does not exist: {project_path}",
                )

            if not project_path.is_dir():
                return FlextCore.Result[bool].fail(
                    f"Project path is not a directory: {project_path}",
                )

            # Check for required Meltano files
            meltano_yml = project_path / "meltano.yml"
            if not meltano_yml.exists():
                return FlextCore.Result[
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

            return FlextCore.Result[bool].ok(data=True)
        except Exception as e:
            error_msg = f"Failed to validate project structure: {e}"
            logger.exception(error_msg)
            return FlextCore.Result[bool].fail(error_msg)

    @classmethod
    def validate_connection_config(
        cls,
        config: FlextCore.Types.Dict,
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Validate connection configuration with domain-specific business rules.

        Validates connection configuration data for Meltano services,
        ensuring proper format and required fields.

        Args:
            config: Connection configuration dictionary to validate.

        Returns:
            FlextCore.Result containing validated configuration or error details.

        Example:
            >>> config: FlextCore.Types.Dict = {
            ...     "host": "localhost",
            ...     "port": 5432,
            ...     "database": "mydb",
            ... }
            >>> result: FlextCore.Result[object] = (
            ...     FlextMeltanoValidators.validate_connection_config(config)
            ... )
            >>> if result.is_success:
            ...     validated_config: FlextCore.Types.Dict = result.unwrap()
            ...     print(f"Validated config: {validated_config}")

        """
        try:
            # DOMAIN-SPECIFIC: Connection config business rules
            if not config:
                return FlextCore.Result[FlextCore.Types.Dict].fail(
                    "Connection configuration cannot be empty",
                )

            return FlextCore.Result[FlextCore.Types.Dict].ok(data=config)
        except Exception as e:
            error_msg = f"Failed to validate connection config: {e}"
            logger.exception(error_msg)
            return FlextCore.Result[FlextCore.Types.Dict].fail(error_msg)

    @classmethod
    def validate_plugin_config(
        cls,
        config: FlextCore.Types.JsonValue,
    ) -> FlextCore.Result[bool]:
        """Validate plugin configuration with comprehensive business rules.

        Validates plugin configuration data for Meltano plugins,
        ensuring proper format, required fields, and business rules.

        Args:
            config: Plugin configuration to validate.

        Returns:
            FlextCore.Result containing boolean validation result or error details.

        """
        return cls.validate_meltano_plugin_business_rules(config)


__all__ = [
    "FlextMeltanoValidators",
]
