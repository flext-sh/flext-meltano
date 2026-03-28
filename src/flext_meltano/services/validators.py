"""FLEXT Pipeline Validators - Generic business rule validators.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import contextlib
from pathlib import Path
from typing import override

from flext_core import FlextLogger, r
from pydantic import ValidationError

from flext_meltano import FlextMeltanoServiceBase, m, t


class FlextMeltanoValidators(FlextMeltanoServiceBase):
    """Generic pipeline business rule validators using foundation."""

    @classmethod
    def validate_connection_config(
        cls,
        config: t.ConfigurationMapping,
    ) -> r[t.ConfigurationMapping]:
        """Validate connection configuration with domain-specific business rules."""
        try:
            if not config:
                return r[t.ScalarMapping].fail(
                    "Connection configuration cannot be empty"
                )
            return r[t.ScalarMapping].ok(config)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Failed to validate connection config: {e}"
            FlextLogger(__name__).exception(error_msg)
            return r[t.ScalarMapping].fail(error_msg)

    @classmethod
    def validate_component_rules(cls, config: t.ConfigurationMapping) -> r[bool]:
        """Validate pipeline component business rules with model validation."""
        try:
            m.Meltano.PluginComponentConfig.model_validate(config)
            return r[bool].ok(value=True)
        except ValidationError as error:
            return r[bool].fail(f"Plugin config validation failed: {error}")

    @classmethod
    def validate_pipeline_project_business_rules(
        cls,
        config: t.ConfigurationMapping,
    ) -> r[bool]:
        """Validate pipeline project business rules."""
        try:
            m.Meltano.PipelineProjectModel.model_validate(config)
            return r[bool].ok(value=True)
        except ValidationError as error:
            return r[bool].fail(f"Project validation failed: {error}")

    @classmethod
    def validate_pipeline_project_structure(cls, project_path: Path) -> r[bool]:
        """Validate pipeline project structure with domain-specific business rules."""
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
            FlextLogger(__name__).exception(error_msg)
            return r[bool].fail(error_msg)

    @classmethod
    def validate_plugin_config(cls, config: t.ConfigurationMapping) -> r[bool]:
        """Validate plugin configuration with complete business rules."""
        return cls.validate_component_rules(config)

    @classmethod
    def validate_transformation_business_rules(
        cls,
        config: t.ConfigurationMapping,
    ) -> r[bool]:
        """Validate transformation-specific business rules."""
        try:
            m.Meltano.TransformationProjectModel.model_validate(config)
            return r[bool].ok(value=True)
        except ValidationError as error:
            return r[bool].fail(f"Transformation validation failed: {error}")

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute validators service — returns current settings."""
        return r[t.Meltano.MeltanoConfigDict].ok(self.settings.model_dump())


__all__ = ["FlextMeltanoValidators"]
