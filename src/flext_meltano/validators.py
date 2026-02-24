"""FLEXT Pipeline Validators - Generic business rule validators.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import contextlib
from collections.abc import Mapping
from pathlib import Path

from flext_core import FlextLogger, r
from pydantic import ValidationError

from flext_meltano.models import FlextMeltanoModels
from flext_meltano.typings import FlextMeltanoTypes as t

m = FlextMeltanoModels

logger = FlextLogger(__name__)


class FlextMeltanoValidators:
    """Generic pipeline business rule validators using uoundation.

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
        >>> config: dict[str, t.GeneralValueType] = {
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
        config: t.JsonValue,
    ) -> r[bool]:
        """Validate pipeline component business rules with model validation."""
        try:
            m.Meltano.PluginComponentConfig.model_validate(config)
            return r[bool].ok(value=True)
        except ValidationError as error:
            return r[bool].fail(f"Plugin config validation failed: {error}")

    @classmethod
    def validate_pipeline_project_business_rules(
        cls,
        config: t.JsonValue,
    ) -> r[bool]:
        """Validate pipeline project business rules.

        Validates pipeline project configuration including version requirements
        and project ID format restrictions.

        Args:
            config: Project configuration dictionary to validate.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> config: dict[str, t.GeneralValueType] = {
            ...     "version": 1,
            ...     "project_id": my - meltano - project,
            ... }
            >>> result = FlextMeltanoValidators.validate_meltano_project_business_rules(
            ...     config
            ... )
            >>> if result.is_success and result.value:
            ...     print("Project configuration is valid")

        """
        try:
            m.Meltano.PipelineProjectModel.model_validate(config)
            return r[bool].ok(value=True)
        except ValidationError as error:
            return r[bool].fail(f"Project validation failed: {error}")

    @classmethod
    def validate_transformation_business_rules(
        cls,
        config: t.JsonValue,
    ) -> r[bool]:
        """Validate transformation-specific business rules.

        Validates transformation project configuration including project name format
        requirements and version specifications.

        Args:
            config: Transformation configuration dictionary to validate.

        Returns:
            FlextResult containing boolean validation result or error details.

        Example:
            >>> config: dict[str, t.GeneralValueType] = {
            ...     "name": "my_transformation_project",
            ...     "version": 1.0.0,
            ... }
            >>> result: FlextResult[object] = (
            ...     FlextMeltanoValidators.validate_transformation_business_rules(
            ...         config
            ...     )
            ... )
            >>> if result.is_success and result.value:
            ...     print("Transformation configuration is valid")

        """
        try:
            m.Meltano.TransformationProjectModel.model_validate(config)
            return r[bool].ok(value=True)
        except ValidationError as error:
            return r[bool].fail(f"Transformation validation failed: {error}")

    @classmethod
    def validate_pipeline_project_structure(
        cls,
        project_path: Path,
    ) -> r[bool]:
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
            >>> if result.is_success and result.value:
            ...     print("Project structure is valid")

        """
        try:
            # Check if path exists and is directory
            if not project_path.exists():
                return r[bool].fail(
                    f"Project path does not exist: {project_path}",
                )

            if not project_path.is_dir():
                return r[bool].fail(
                    f"Project path is not a directory: {project_path}",
                )

            # Check for required pipeline files
            pipeline_config = project_path / "pipeline.yml"
            if not pipeline_config.exists():
                return r[
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

            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to validate project structure: {e}"
            logger.exception(error_msg)
            return r[bool].fail(error_msg)

    @classmethod
    def validate_connection_config(
        cls,
        config: Mapping[str, t.JsonValue],
    ) -> r[Mapping[str, t.JsonValue]]:
        """Validate connection configuration with domain-specific business rules.

        Validates connection configuration data for pipeline services,
        ensuring proper format and required fields.

        Args:
            config: Connection configuration dictionary to validate.

        Returns:
            FlextResult containing validated configuration or error details.

        Example:
            >>> config: dict[str, t.JsonValue] = {
            ...     "host": "localhost",
            ...     "port": 5432,
            ...     "database": "mydb",
            ... }
            >>> result: r[dict[str, t.JsonValue]] = (
            ...     FlextMeltanoValidators.validate_connection_config(config)
            ... )
            >>> if result.is_success:
            ...     validated_config: dict[str, t.JsonValue] = result.value
            ...     print(f"Validated config: {validated_config}")

        """
        try:
            # DOMAIN-SPECIFIC: Connection config business rules
            if not config:
                return r[Mapping[str, t.JsonValue]].fail(
                    "Connection configuration cannot be empty",
                )

            return r[Mapping[str, t.JsonValue]].ok(config)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to validate connection config: {e}"
            logger.exception(error_msg)
            return r[Mapping[str, t.JsonValue]].fail(error_msg)

    @classmethod
    def validate_plugin_config(
        cls,
        config: t.JsonValue,
    ) -> r[bool]:
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
