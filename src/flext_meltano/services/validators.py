"""FLEXT Pipeline Validators - Generic business rule validators.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_meltano import FlextMeltanoServiceBase, c, m, r, t, u


class FlextMeltanoValidators(FlextMeltanoServiceBase):
    """Generic pipeline business rule validators using foundation."""

    @classmethod
    def validate_component_rules(cls, settings: t.ConfigurationMapping) -> r[bool]:
        """Validate pipeline component business rules with model validation."""
        try:
            m.Meltano.PluginComponentConfig.model_validate(settings)
            return r[bool].ok(value=True)
        except c.ValidationError as error:
            return r[bool].fail(f"Plugin settings validation failed: {error}")

    @classmethod
    def validate_pipeline_project_business_rules(
        cls,
        settings: t.ConfigurationMapping,
    ) -> r[bool]:
        """Validate pipeline project business rules."""
        try:
            m.Meltano.PipelineProjectModel.model_validate(settings)
            return r[bool].ok(value=True)
        except c.ValidationError as error:
            return r[bool].fail(f"Project validation failed: {error}")

    @classmethod
    def validate_pipeline_project_structure(cls, project_path: Path) -> r[bool]:
        """Validate pipeline project structure with domain-specific business rules."""
        if not project_path.exists() or not project_path.is_dir():
            error_msg = (
                f"Project path {project_path} does not exist or is not a directory"
            )
            u.fetch_logger(__name__).exception(error_msg)
            return r[bool].fail(error_msg)

        meltano_yml = project_path / c.Meltano.PATH_MELTANO_PROJECT_FILE
        if not meltano_yml.exists():
            error_msg = f"Project path {project_path} does not contain {c.Meltano.PATH_MELTANO_PROJECT_FILE}"
            u.fetch_logger(__name__).exception(error_msg)
            return r[bool].fail(error_msg)

        transform_dir = project_path / c.Meltano.PATH_TRANSFORM_DIR
        try:
            transform_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            error_msg = f"Failed to prepare transform directory: {e}"
            u.fetch_logger(__name__).exception(error_msg)
            return r[bool].fail(error_msg)

        return r[bool].ok(value=True)

    @classmethod
    def validate_plugin_config(cls, settings: t.ConfigurationMapping) -> r[bool]:
        """Validate plugin configuration with complete business rules."""
        return cls.validate_component_rules(settings)

    @classmethod
    def validate_transformation_business_rules(
        cls,
        settings: t.ConfigurationMapping,
    ) -> r[bool]:
        """Validate transformation-specific business rules."""
        try:
            m.Meltano.TransformationProjectModel.model_validate(settings)
            return r[bool].ok(value=True)
        except c.ValidationError as error:
            return r[bool].fail(f"Transformation validation failed: {error}")

    @override
    def execute(self) -> r[t.ContainerMapping]:
        """Execute validators service — returns current settings."""
        return r[t.ContainerMapping].ok(self.settings.model_dump())


__all__: list[str] = ["FlextMeltanoValidators"]
