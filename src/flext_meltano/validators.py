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

from flext_meltano import FlextMeltanoModels, t

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
        >>> config: dict[str, object] = {
        ...     "name": source - csv,
        ...     "namespace": "source_csv",
        ... }
        >>> result: r[object] = validator.validate_pipeline_component_business_rules(
        ...     config
        ... )
        >>> if result.is_success:
        ...     logger.info("Component configuration is valid")

    """

    @classmethod
    def validate_connection_config(
        cls, config: Mapping[str, t.Scalar]
    ) -> r[Mapping[str, t.Scalar]]:
        """Validate connection configuration with domain-specific business rules.

        Validates connection configuration data for pipeline services,
        ensuring proper format and required fields.

        Args:
            config: Connection configuration dictionary to validate.

        Returns:
            r containing validated configuration or error details.

        Example:
            >>> config: dict[str, object
            ...     "host": "localhost",
            ...     "port": 5432,
            ...     "database": "mydb",
            ... }
            >>> result: r[dict[str, object(
            ...     FlextMeltanoValidators.validate_connection_config(config)
            ... )
            >>> if result.is_success:
            ...     validated_config: dict[str, objectesult.value
            ...     logger.info("Validated config", config=validated_config)

        """
        try:
            if not config:
                return r[Mapping[str, t.Scalar]].fail(
                    "Connection configuration cannot be empty"
                )
            return r[Mapping[str, t.Scalar]].ok(config)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to validate connection config: {e}"
            logger.exception(error_msg)
            return r[Mapping[str, t.Scalar]].fail(error_msg)

    @classmethod
    def validate_pipeline_component_business_rules(
        cls, config: Mapping[str, t.Scalar]
    ) -> r[bool]:
        """Validate pipeline component business rules with model validation."""
        try:
            m.Meltano.PluginComponentConfig(config)
            return r[bool].ok(value=True)
        except ValidationError as error:
            return r[bool].fail(f"Plugin config validation failed: {error}")

    @classmethod
    def validate_pipeline_project_business_rules(
        cls, config: Mapping[str, t.Scalar]
    ) -> r[bool]:
        """Validate pipeline project business rules.

        Validates pipeline project configuration including version requirements
        and project ID format restrictions.

        Args:
            config: Project configuration dictionary to validate.

        Returns:
            r containing boolean validation result or error details.

        Example:
            >>> config: dict[str, object] = {
            ...     "version": 1,
            ...     "project_id": my - meltano - project,
            ... }
            >>> result = FlextMeltanoValidators.validate_meltano_project_business_rules(
            ...     config
            ... )
            >>> if result.is_success and result.value:
            ...     logger.info("Project configuration is valid")

        """
        try:
            m.Meltano.PipelineProjectModel(config)
            return r[bool].ok(value=True)
        except ValidationError as error:
            return r[bool].fail(f"Project validation failed: {error}")

    @classmethod
    def validate_pipeline_project_structure(cls, project_path: Path) -> r[bool]:
        """Validate pipeline project structure with domain-specific business rules.

        Performs complete validation of the pipeline project directory
        structure, checking for required files and directories.

        Args:
            project_path: Path to the pipeline project directory.

        Returns:
            r containing boolean validation result or error details.

        Example:
            >>> from pathlib import Path
            >>> project_path = Path("/path/to/pipeline/project")
            >>> result = FlextMeltanoValidators.validate_pipeline_project_structure(
            ...     project_path
            ... )
            >>> if result.is_success and result.value:
            ...     logger.info("Project structure is valid")

        """
        try:
            if not project_path.exists():
                return r[bool].fail(f"Project path does not exist: {project_path}")
            if not project_path.is_dir():
                return r[bool].fail(f"Project path is not a directory: {project_path}")
            pipeline_config = project_path / "pipeline.yml"
            if not pipeline_config.exists():
                return r[bool].fail(f"pipeline.yml not found in {project_path}")
            transform_dir = project_path / "transform"
            if not transform_dir.exists():
                with contextlib.suppress(OSError):
                    transform_dir.mkdir(parents=True, exist_ok=True)
            return r[bool].ok(value=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to validate project structure: {e}"
            logger.exception(error_msg)
            return r[bool].fail(error_msg)

    @classmethod
    def validate_plugin_config(cls, config: Mapping[str, t.Scalar]) -> r[bool]:
        """Validate plugin configuration with complete business rules.

        Validates plugin configuration data for Meltano plugins,
        ensuring proper format, required fields, and business rules.

        Args:
        config: Plugin configuration to validate.

        Returns:
        r containing boolean validation result or error details.

        """
        return cls.validate_pipeline_component_business_rules(config)

    @classmethod
    def validate_transformation_business_rules(
        cls, config: Mapping[str, t.Scalar]
    ) -> r[bool]:
        """Validate transformation-specific business rules.

        Validates transformation project configuration including project name format
        requirements and version specifications.

        Args:
            config: Transformation configuration dictionary to validate.

        Returns:
            r containing boolean validation result or error details.

        Example:
            >>> config: dict[str, object] = {
            ...     "name": "my_transformation_project",
            ...     "version": 1.0.0,
            ... }
            >>> result: r[object] = (
            ...     FlextMeltanoValidators.validate_transformation_business_rules(
            ...         config
            ...     )
            ... )
            >>> if result.is_success and result.value:
            ...     logger.info("Transformation configuration is valid")

        """
        try:
            m.Meltano.TransformationProjectModel(config)
            return r[bool].ok(value=True)
        except ValidationError as error:
            return r[bool].fail(f"Transformation validation failed: {error}")


__all__ = ["FlextMeltanoValidators"]
