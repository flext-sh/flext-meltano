"""FLEXT Pipeline Project Service - Enterprise project management foundation.

Handles pipeline project lifecycle operations following FLEXT Clean Architecture
with railway-oriented programming and zero custom pipeline implementations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path
from typing import override

from flext_meltano import (
    FlextMeltanoAbstractions,
    FlextMeltanoServiceBase,
    FlextMeltanoSettings,
    FlextMeltanoValidators,
    c,
    m,
    r,
    t,
    u,
)


class FlextMeltanoProjectService(FlextMeltanoServiceBase):
    """Enterprise pipeline project service with railway-oriented programming.

    Manages complete pipeline project lifecycle using FLEXT ecosystem patterns:
    - Project creation and initialization with r error handling
    - Railway-oriented validation chains for composable operations
    - Complete flext-core integration (Container, Logger, Utilities)
    - Zero try/except fallbacks - explicit r error handling

    Extends flext-core foundation for enterprise data pipeline orchestration.
    """

    @property
    def _abstractions(self) -> FlextMeltanoAbstractions:
        """Lazy-initialize abstractions service."""
        return FlextMeltanoAbstractions()

    @staticmethod
    def _validate_project_creation_params(
        project_name: str,
        project_dir: Path,
    ) -> r[Mapping[str, str | Path]]:
        """Validate parameters for project creation."""
        if not project_name or not project_name.strip():
            return r[Mapping[str, str | Path]].fail("Project name cannot be empty")
        if not project_dir.exists():
            return r[Mapping[str, str | Path]].fail(
                f"Parent directory not found: {project_dir}",
            )
        return r[Mapping[str, str | Path]].ok({
            "name": project_name.strip(),
            "parent_dir": project_dir,
        })

    @staticmethod
    def _validate_project_parameters(
        project_id: str | None,
        prefix: str,
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
        """Validate Meltano project structure using dedicated validators.

        Delegates to FlextMeltanoValidators for consistent validation
        across the entire FLEXT ecosystem.

        Args:
        project_path: Path to potential Meltano project directory

        Returns:
        r containing True if valid, False with error details if invalid

        """
        return FlextMeltanoValidators.validate_pipeline_project_structure(project_path)

    def create_project(
        self,
        project_name: str,
        project_dir: Path,
    ) -> r[t.StrMapping]:
        """Create new Meltano project using railway-oriented file operations.

        Validates project name, creates directory structure, and initializes
        meltano.yml using composable r operations.

        Args:
        project_name: Name for the new Meltano project
        project_dir: Parent directory where project will be created

        Returns:
        r containing project creation metadata or validation error

        """
        params_r: r[Mapping[str, str | Path]] = self._validate_project_creation_params(
            project_name, project_dir
        )
        dir_r: r[Path] = params_r.flat_map(
            lambda params: u.Meltano.create_project_directory(
                str(params["name"]),
                m.Meltano.PathPayload(value=Path(str(params["parent_dir"]))).value,
            )
        )
        struct_r: r[Path] = dir_r.flat_map(u.Meltano.create_project_structure)
        init_r: r[Path] = struct_r.flat_map(
            lambda project_path: u.Meltano.initialize_project_config(
                project_path, project_name
            )
        )
        return init_r.flat_map(
            lambda project_path: self._build_creation_result(project_name, project_path)
        )

    def create_temporary_project(
        self,
        project_id: str | None = None,
        prefix: str = "flext_meltano_",
    ) -> r[t.Meltano.Dbt.Project]:
        """Create temporary Meltano project with railway-oriented validation.

        Uses r.flat_map chains for composable project creation
        with automatic error propagation and resource management.

        Args:
        project_id: Optional project identifier for uniqueness
        prefix: Temporary directory prefix for organization

        Returns:
        r containing project t.ContainerMapping with standardized structure

        """
        params_r2: r[t.StrMapping] = self._validate_project_parameters(
            project_id, prefix
        )
        config_r: r[t.ContainerMapping] = params_r2.flat_map(
            lambda params: u.Meltano.create_temp_directory(params["prefix"]).flat_map(
                lambda temp_path: u.Meltano.generate_minimal_config(
                    temp_path, params["project_id"]
                )
            )
        )
        path_r: r[Path] = config_r.flat_map(u.Meltano.extract_and_write_config)
        inst_r: r[Path] = path_r.flat_map(self._initialize_project_instance)
        return inst_r.flat_map(u.Meltano.convert_to_project_dict)

    @staticmethod
    def build_service_execution_payload(
        service_type: str,
        meltano_config: FlextMeltanoSettings,
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Build normalized execution payload for service health responses."""
        try:
            return r[t.Meltano.MeltanoConfigDict].ok({
                "service_type": service_type,
                "status": c.Meltano.Enums.OperationStatus.READY,
                "config": meltano_config.model_dump()
                if u.is_pydantic_model(meltano_config)
                else {},
            })
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.Meltano.MeltanoConfigDict].fail(f"Service execution failed: {e}")

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute the pipeline project service.

        Returns:
        r containing project service configuration and status.

        """
        result = self.build_service_execution_payload(
            "flext_meltano_project_service",
            self.settings,
        )
        if result.is_success:
            self.logger.info("FlextMeltanoProjectService executed successfully")
            return result
        error_msg = result.error or "Project service execution failed"
        self.logger.error(error_msg)
        return r[t.Meltano.MeltanoConfigDict].fail(error_msg)

    def initialize_project(self, project_root: Path) -> r[t.Meltano.Dbt.Project]:
        """Initialize Meltano project using railway pattern validation chain.

        Chains initialization steps with automatic error handling:
        - Project root validation
        - Meltano.yml existence check
        - Project loading and conversion

        Args:
        project_root: Directory path containing meltano.yml

        Returns:
        r containing initialized project t.ContainerMapping or validation error

        """
        vpath_r: r[Path] = self._validate_project_path(project_root)
        vcfg_r: r[Path] = vpath_r.flat_map(u.Meltano.validate_meltano_config_exists)
        loaded_r: r[Path] = vcfg_r.flat_map(self._load_project_from_path)
        return loaded_r.flat_map(u.Meltano.convert_to_project_dict)

    def _build_creation_result(
        self,
        project_name: str,
        project_path: Path,
    ) -> r[t.StrMapping]:
        """Build successful project creation result."""
        try:
            result: t.StrMapping = {
                "success": "true",
                "project_name": project_name,
                "project_path": str(project_path),
                "creation_method": "manual_file_creation",
                "meltano_yml_exists": str(
                    (project_path / c.Meltano.Paths.MELTANO_PROJECT_FILE).exists(),
                ),
            }
            self.logger.info(
                "Meltano project created successfully",
                project_name=project_name,
                project_path=str(project_path),
            )
            return r[t.StrMapping].ok(result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.StrMapping].fail(f"Failed to build creation result: {e}")

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
                project_result.error or "Failed to load Meltano project",
            )
        return project_result


__all__ = ["FlextMeltanoProjectService"]
