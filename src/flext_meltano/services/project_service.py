"""FLEXT Pipeline Project Service - Enterprise project management foundation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import override

from flext_core import r
from flext_meltano import (
    FlextMeltanoAbstractions,
    FlextMeltanoServiceBase,
    FlextMeltanoSettings,
    FlextMeltanoValidators,
    c,
    m,
    t,
    u,
)


class FlextMeltanoProjectService(FlextMeltanoServiceBase):
    """Enterprise pipeline project service with railway-oriented programming."""

    @property
    def _abstractions(self) -> FlextMeltanoAbstractions:
        """Lazy-initialize abstractions service."""
        return FlextMeltanoAbstractions()

    @staticmethod
    def _validate_project_creation_params(
        project_name: str,
        project_dir: Path,
    ) -> r[t.FlatContainerMapping]:
        """Validate parameters for project creation."""
        if not project_name or not project_name.strip():
            return r[t.FlatContainerMapping].fail("Project name cannot be empty")
        if not project_dir.exists():
            return r[t.FlatContainerMapping].fail(
                f"Parent directory not found: {project_dir}"
            )
        return r[t.FlatContainerMapping].ok({
            "name": project_name.strip(),
            "parent_dir": project_dir,
        })

    @staticmethod
    def _validate_project_parameters(
        project_id: str | None, prefix: str
    ) -> r[t.StrMapping]:
        """Validate temporary project creation parameters."""
        if not prefix or not prefix.strip():
            return r[t.StrMapping].fail("Project prefix cannot be empty")
        return r[t.StrMapping].ok({
            "project_id": project_id or "flext-meltano-project",
            "prefix": prefix.strip(),
        })

    @staticmethod
    def _validate_project_path(project_root: Path) -> r[Path]:
        """Validate project directory exists."""
        if not project_root.exists():
            return r[Path].fail(f"Project directory not found: {project_root}")
        return r[Path].ok(project_root)

    @staticmethod
    def validate_project(project_path: Path) -> r[bool]:
        """Validate Meltano project structure using dedicated validators."""
        return FlextMeltanoValidators.validate_pipeline_project_structure(project_path)

    def create_project(self, project_name: str, project_dir: Path) -> r[t.StrMapping]:
        """Create new Meltano project using railway-oriented file operations."""
        params_r: r[t.FlatContainerMapping] = self._validate_project_creation_params(
            project_name,
            project_dir,
        )
        dir_r: r[Path] = params_r.flat_map(
            lambda params: u.Meltano.create_project_directory(
                str(params["name"]),
                m.Meltano.PathPayload(value=Path(str(params["parent_dir"]))).value,
            ),
        )
        struct_r: r[Path] = dir_r.flat_map(u.Meltano.create_project_structure)
        init_r: r[Path] = struct_r.flat_map(
            lambda project_path: u.Meltano.initialize_project_config(
                project_path, project_name
            ),
        )
        return init_r.flat_map(
            lambda project_path: self._build_creation_result(project_name, project_path)
        )

    def create_temporary_project(
        self,
        project_id: str | None = None,
        prefix: str = "flext_meltano_",
    ) -> r[t.Meltano.DbtProject]:
        """Create temporary Meltano project with railway-oriented validation."""
        params_r2: r[t.StrMapping] = self._validate_project_parameters(
            project_id, prefix
        )
        config_r: r[t.ContainerMapping] = params_r2.flat_map(
            lambda params: u.Meltano.create_temp_directory(params["prefix"]).flat_map(
                lambda temp_path: u.Meltano.generate_minimal_config(
                    temp_path, params["project_id"]
                ),
            ),
        )
        path_r: r[Path] = config_r.flat_map(u.Meltano.extract_and_write_config)
        inst_r: r[Path] = path_r.flat_map(self._initialize_project_instance)
        return inst_r.flat_map(u.Meltano.convert_to_project_dict)

    @staticmethod
    def build_service_execution_payload(
        service_type: str,
        meltano_config: FlextMeltanoSettings,
    ) -> r[t.ContainerMapping]:
        """Build normalized execution payload for service health responses."""
        payload: t.ContainerMapping = u.Meltano.build_status_payload(
            c.Meltano.OperationStatus.READY,
            extra_fields={"service_type": service_type},
            config=meltano_config,
            config_field="config",
        )
        return r[t.ContainerMapping].ok(payload)

    @override
    def execute(self) -> r[t.ContainerMapping]:
        """Execute the pipeline project service."""
        result = self.build_service_execution_payload(
            "flext_meltano_project_service", self.settings
        )
        if result.is_success:
            self.logger.info("FlextMeltanoProjectService executed successfully")
            return result
        error_msg = result.error or "Project service execution failed"
        self.logger.error(error_msg)
        return r[t.ContainerMapping].fail(error_msg)

    def initialize_project(self, project_root: Path) -> r[t.Meltano.DbtProject]:
        """Initialize Meltano project using railway pattern validation chain."""
        vpath_r: r[Path] = self._validate_project_path(project_root)
        vcfg_r: r[Path] = vpath_r.flat_map(u.Meltano.validate_meltano_config_exists)
        loaded_r: r[Path] = vcfg_r.flat_map(self._load_project_from_path)
        return loaded_r.flat_map(u.Meltano.convert_to_project_dict)

    def _build_creation_result(
        self, project_name: str, project_path: Path
    ) -> r[t.StrMapping]:
        """Build successful project creation result."""
        result = u.Meltano.build_project_creation_result(
            project_name,
            project_path,
        )
        self.logger.info(
            "Meltano project created successfully",
            project_name=project_name,
            project_path=str(project_path),
        )
        return r[t.StrMapping].ok(result)

    def _initialize_project_instance(self, project_path: Path) -> r[Path]:
        """Initialize Meltano project instance using abstractions."""
        project_result = self._abstractions.find_project(project_path)
        if project_result.is_failure:
            return r[Path].fail(project_result.error or "Failed to initialize project")
        return project_result

    def _load_project_from_path(self, project_root: Path) -> r[Path]:
        """Load Meltano project from validated path."""
        project_result = self._abstractions.find_project(project_root)
        if project_result.is_failure:
            return r[Path].fail(
                project_result.error or "Failed to load Meltano project"
            )
        return project_result


__all__ = ["FlextMeltanoProjectService"]
