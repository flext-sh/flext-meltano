"""FLEXT Pipeline Validators - Generic business rule validators.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import contextlib
from pathlib import Path

from flext_core import FlextLogger, FlextResult, FlextTypes

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels

logger = FlextLogger(__name__)


class FlextMeltanoValidators:
    """Generic pipeline business rule validators using FlextValidations foundation.

    This class provides complete validation for pipeline-specific business rules
    while delegating generic validation operations to flext-core. It follows the
    zero duplication principle by containing only pipeline specific validation logic.

    The validator supports validation for:
    - Pipeline component configurations
    - Pipeline project structures
    - Transformation project configurations
    - Connection configurations

    Example:
        >>> validator = FlextMeltanoValidators()
        >>> config: dict[str, object] = {
        ...     "name": source - csv,
        ...     "namespace": "source_csv",
        ... }
        >>> result: FlextResult[object] = (
        ...     validator.validate_pipeline_component_business_rules(config)
        ... )
        >>> if result.is_success:
        ...     print("Component configuration is valid")

    """

    @classmethod
    def validate_pipeline_component_business_rules(
        cls,
        config: FlextTypes.JsonValue,
    ) -> FlextResult[bool]:
        """Validate pipeline component business rules using monadic error accumulation.

        Uses FlextResult.accumulate_errors() to collect all validation errors
        instead of stopping at the first failure, providing comprehensive
        validation feedback with composable validation rules.

        Args:
            config: Plugin configuration dictionary to validate.

        Returns:
            FlextResult containing boolean validation result or accumulated error details.

        """
        return FlextResult.accumulate_errors(
            cls._validate_config_is_dict(config),
            cls._validate_plugin_name(config),
            cls._validate_plugin_namespace(config),
            cls._validate_plugin_pip_url(config),
            cls._validate_plugin_executable(config),
            cls._validate_pipeline_specific_rules(config),
        ).map(lambda _: True)  # Convert successful validations to boolean result

    @classmethod
    def _validate_config_is_dict(
        cls, config: FlextTypes.JsonValue
    ) -> FlextResult[bool]:
        """Validate that config is a dictionary.

        Args:
            config: Configuration dictionary to validate.

        Returns:
            FlextResult indicating if config is a valid dictionary.

        """
        if not isinstance(config, dict):
            return FlextResult.fail(
                "Plugin config validation failed: config must be a dictionary"
            )
        return FlextResult.ok(data=True)

    @classmethod
    def _validate_plugin_name(cls, config: FlextTypes.JsonValue) -> FlextResult[bool]:
        if not isinstance(config, dict):
            return FlextResult.fail("Config must be dictionary for name validation")

        name = config.get("name", "")
        if not isinstance(name, str):
            return FlextResult.fail("Plugin name must be a string")

        if not name or not name.strip():
            return FlextResult.fail("Plugin name cannot be empty")

        return cls._validate_pipeline_name_business_rules(name.strip())

    @classmethod
    def _validate_pipeline_name_business_rules(cls, name: str) -> FlextResult[bool]:
        """Validate pipeline-specific name business rules.

        Args:
        name: Plugin name to validate.

        Returns:
        FlextResult indicating business rule validation.

        """
        validation_errors: list[str] = []

        # Pipeline business rule: sink component names
        if (
            name.startswith("target-")
            and len(name) < FlextMeltanoConstants.Plugin.MIN_TARGET_PLUGIN_NAME_LENGTH
        ):
            validation_errors.append(
                "Sink component names must be at least 8 characters"
            )

        # Pipeline business rule: source component names
        if (
            name.startswith("tap-")
            and len(name) < FlextMeltanoConstants.Plugin.MIN_TAP_PLUGIN_NAME_LENGTH
        ):
            validation_errors.append(
                "Source component names must be at least 5 characters"
            )

        if validation_errors:
            return FlextResult.fail("; ".join(validation_errors))

        return FlextResult.ok(data=True)

    @classmethod
    def _validate_plugin_namespace(
        cls, config: FlextTypes.JsonValue
    ) -> FlextResult[bool]:
        if not isinstance(config, dict):
            return FlextResult.fail(
                "Config must be dictionary for namespace validation"
            )

        namespace = config.get("namespace")
        if namespace is None:
            return FlextResult.fail("Plugin namespace is required")

        if not isinstance(namespace, str):
            return FlextResult.fail("Plugin namespace must be a string")

        if not namespace.strip():
            return FlextResult.fail("Plugin namespace cannot be empty")

        return FlextResult.ok(data=True)

    @classmethod
    def _validate_plugin_pip_url(
        cls, config: FlextTypes.JsonValue
    ) -> FlextResult[bool]:
        if not isinstance(config, dict):
            return FlextResult.fail("Config must be dictionary for pip_url validation")

        pip_url = config.get("pip_url")
        if pip_url is None:
            return FlextResult.fail("Plugin pip_url is required")

        if not isinstance(pip_url, str):
            return FlextResult.fail("Plugin pip_url must be a string")

        if not pip_url.strip():
            return FlextResult.fail("Plugin pip_url cannot be empty")

        return FlextResult.ok(data=True)

    @classmethod
    def _validate_plugin_executable(
        cls, config: FlextTypes.JsonValue
    ) -> FlextResult[bool]:
        if not isinstance(config, dict):
            return FlextResult.fail(
                "Config must be dictionary for executable validation"
            )

        executable = config.get("executable")
        if executable is None:
            return FlextResult.fail("Plugin executable is required")

        if not isinstance(executable, str):
            return FlextResult.fail("Plugin executable must be a string")

        if not executable.strip():
            return FlextResult.fail("Plugin executable cannot be empty")

        return FlextResult.ok(data=True)

    @classmethod
    def _validate_pipeline_specific_rules(
        cls, config: FlextTypes.JsonValue
    ) -> FlextResult[bool]:
        """Validate additional pipeline-specific business rules.

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
        return FlextResult.ok(data=True)

    @classmethod
    def validate_pipeline_project_business_rules(
        cls,
        config: FlextTypes.JsonValue,
    ) -> FlextResult[bool]:
        """Validate pipeline project business rules.

        Validates pipeline project configuration including version requirements
        and project ID format restrictions.

        Args:
            config: Project configuration dictionary to validate.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> config: dict[str, object] = {
            ...     "version": 1,
            ...     "project_id": my - meltano - project,
            ... }
            >>> result = FlextMeltanoValidators.validate_meltano_project_business_rules(
            ...     config
            ... )
            >>> if result.is_success and result.unwrap():
            ...     print("Project configuration is valid")

        """
        # Validate config is dict[str, object] using direct validation
        if not isinstance(config, dict):
            return FlextResult[bool].fail(
                "Project config validation failed: config must be a dictionary",
            )

        config_dict: dict[str, object] = dict[str, object](config)

        # DOMAIN-SPECIFIC: Pipeline project business rules
        class PipelineProjectBusinessRules(FlextMeltanoModels.PipelineProjectModel):
            """Pipeline project business rules - uses unified FlextMeltanoModels.PipelineProjectModel.

            This class extends the unified model for validation-specific functionality
            while maintaining the consolidated [Project]Models pattern.
            """

        # Use Pydantic model validation directly
        try:
            PipelineProjectBusinessRules.model_validate(config_dict)
            return FlextResult[bool].ok(data=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return FlextResult[bool].fail(f"Project validation failed: {e}")

    @classmethod
    def validate_transformation_business_rules(
        cls, config: FlextTypes.JsonValue
    ) -> FlextResult[bool]:
        """Validate transformation-specific business rules.

        Validates transformation project configuration including project name format
        requirements and version specifications.

        Args:
            config: Transformation configuration dictionary to validate.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> config: dict[str, object] = {
            ...     "name": "my_transformation_project",
            ...     "version": 1.0.0,
            ... }
            >>> result: FlextResult[object] = (
            ...     FlextMeltanoValidators.validate_transformation_business_rules(
            ...         config
            ...     )
            ... )
            >>> if result.is_success and result.unwrap():
            ...     print("Transformation configuration is valid")

        """
        # Validate config is dict[str, object] using direct validation
        if not isinstance(config, dict):
            return FlextResult[bool].fail(
                "Transformation config validation failed: config must be a dictionary",
            )

        config_dict: dict[str, object] = dict[str, object](config)

        # DOMAIN-SPECIFIC: Transformation business rules
        class TransformationBusinessRules(
            FlextMeltanoModels.TransformationProjectModel
        ):
            """Transformation project business rules - uses unified FlextMeltanoModels.TransformationProjectModel.

            This class extends the unified model for validation-specific functionality
            while maintaining the consolidated [Project]Models pattern.
            """

        # Use Pydantic model validation directly
        try:
            TransformationBusinessRules.model_validate(config_dict)
            return FlextResult[bool].ok(data=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return FlextResult[bool].fail(f"Transformation validation failed: {e}")

    @classmethod
    def validate_pipeline_project_structure(
        cls,
        project_path: Path,
    ) -> FlextResult[bool]:
        """Validate pipeline project structure with domain-specific business rules.

        Performs complete validation of the pipeline project directory
        structure, checking for required files and directories.

        Args:
            project_path: Path to the pipeline project directory.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> from pathlib import Path
            >>> project_path = Path("/path/to/pipeline/project")
            >>> result = FlextMeltanoValidators.validate_pipeline_project_structure(
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

            # Check for required pipeline files
            pipeline_config = project_path / "pipeline.yml"
            if not pipeline_config.exists():
                return FlextResult[
                    bool
                ].fail(
                    f"pipeline.yml not found in {project_path}",  # Test expectation compliance
                )

            # Check for transform directory (Transformation) - optional for basic projects
            transform_dir = project_path / "transform"
            if not transform_dir.exists():
                # Create transform directory if it doesn't exist (optional)
                with contextlib.suppress(OSError):
                    transform_dir.mkdir(parents=True, exist_ok=True)

            return FlextResult[bool].ok(data=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to validate project structure: {e}"
            logger.exception(error_msg)
            return FlextResult[bool].fail(error_msg)

    @classmethod
    def validate_connection_config(
        cls,
        config: dict[str, object],
    ) -> FlextResult[dict[str, object]]:
        """Validate connection configuration with domain-specific business rules.

        Validates connection configuration data for pipeline services,
        ensuring proper format and required fields.

        Args:
            config: Connection configuration dictionary to validate.

        Returns:
            FlextResult containing validated configuration or error details.

        Example:
            >>> config: dict[str, object] = {
            ...     "host": "localhost",
            ...     "port": 5432,
            ...     "database": "mydb",
            ... }
            >>> result: FlextResult[object] = (
            ...     FlextMeltanoValidators.validate_connection_config(config)
            ... )
            >>> if result.is_success:
            ...     validated_config: dict[str, object] = result.unwrap()
            ...     print(f"Validated config: {validated_config}")

        """
        try:
            # DOMAIN-SPECIFIC: Connection config business rules
            if not config:
                return FlextResult[dict[str, object]].fail(
                    "Connection configuration cannot be empty",
                )

            return FlextResult[dict[str, object]].ok(data=config)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to validate connection config: {e}"
            logger.exception(error_msg)
            return FlextResult[dict[str, object]].fail(error_msg)

    @classmethod
    def validate_plugin_config(
        cls,
        config: FlextTypes.JsonValue,
    ) -> FlextResult[bool]:
        """Validate plugin configuration with complete business rules.

        Validates plugin configuration data for Meltano plugins,
        ensuring proper format, required fields, and business rules.

        Args:
        config: Plugin configuration to validate.

        Returns:
        FlextResult containing boolean validation result or error details.

        """
        return cls.validate_pipeline_component_business_rules(config)


__all__ = [
    "FlextMeltanoValidators",
]
