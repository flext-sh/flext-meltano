"""FLEXT Pipeline Project Service - Enterprise project management foundation.

Handles pipeline project lifecycle operations following FLEXT Clean Architecture
with railway-oriented programming and zero custom pipeline implementations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import override

import yaml
from pydantic import TypeAdapter

from flext_meltano import (
    FlextMeltanoAbstractions,
    FlextMeltanoSettings,
    FlextMeltanoValidators,
    c,
    m,
    p,
    r,
    s,
    t,
    u,
)


class FlextMeltanoProjectService(s[t.Meltano.MeltanoConfigDict]):
    """Enterprise pipeline project service with railway-oriented programming.

    Manages complete pipeline project lifecycle using FLEXT ecosystem patterns:
    - Project creation and initialization with r error handling
    - Railway-oriented validation chains for composable operations
    - Complete flext-core integration (Container, Logger, Utilities)
    - Zero try/except fallbacks - explicit r error handling

    Extends flext-core foundation for enterprise data pipeline orchestration.
    """

    def __init__(self, config: FlextMeltanoSettings | None = None) -> None:
        """Initialize project service with complete FLEXT ecosystem integration."""
        super().__init__()
        self._meltano_config: FlextMeltanoSettings = (
            config if config is not None else FlextMeltanoSettings.model_validate({})
        )
        self._abstractions = FlextMeltanoAbstractions()

    @staticmethod
    def _convert_to_project_dict(
        project: p.Meltano.Project
        | t.Meltano.Dbt.Project
        | Mapping[str, t.ContainerMapping | None]
        | Path
        | t.ContainerMapping
        | None,
    ) -> r[t.Meltano.Dbt.Project]:
        """Convert Meltano project t.NormalizedValue to FLEXT t.ContainerMapping representation."""
        try:
            name_attr = getattr(project, "name", None)
            root_attr = getattr(project, "root", None)
            settings_attr = getattr(project, "settings", None)
            version_attr = getattr(project, "meltano_version", None)
            project_dict: t.Meltano.Dbt.Project = {
                "name": str(name_attr) if name_attr else "meltano_project",
                "root": (str(root_attr) if root_attr else c.IDENTIFIER_UNKNOWN),
                "settings": str(settings_attr) if settings_attr else "",
                "meltano_version": str(version_attr) if version_attr else "",
            }
            return r[t.Meltano.Dbt.Project].ok(project_dict)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.Meltano.Dbt.Project].fail(
                f"Failed to convert project t.NormalizedValue: {e}",
            )

    @staticmethod
    def _create_project_directory(project_name: str, parent_dir: Path) -> r[Path]:
        """Create project directory structure."""
        try:
            project_path = parent_dir / project_name
            project_path.mkdir(parents=True, exist_ok=True)
            return r[Path].ok(project_path)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to create project directory: {e}")

    @staticmethod
    def _create_project_structure(project_path: Path) -> r[Path]:
        """Create standard Meltano project directory structure."""
        try:
            directories = [
                "extract",
                "load",
                "transform",
                "analyze",
                "notebook",
                "orchestrate",
                "output",
            ]
            for directory in directories:
                (project_path / directory).mkdir(exist_ok=True)
                (project_path / directory / ".gitkeep").touch()
            return r[Path].ok(project_path)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to create project structure: {e}")

    @staticmethod
    def _create_temp_directory(prefix: str) -> r[Path]:
        """Create temporary directory with FLEXT utilities."""
        try:
            temp_dir = tempfile.mkdtemp(prefix=prefix)
            return r[Path].ok(Path(temp_dir))
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to create temp directory: {e}")

    @staticmethod
    def _extract_and_write_config(
        config_data: t.ContainerMapping,
    ) -> r[Path]:
        """Extract and validate path and config from generated config data.

        Args:
            config_data: Dictionary containing 'path' and 'config' keys

        Returns:
            r containing project path after writing config

        """
        path_obj = config_data.get("path")
        config_obj = config_data.get("config")
        config_payload = m.Meltano.ConfigMappingPayload.model_validate({
            "values": config_obj,
        }).values
        adapter: TypeAdapter[t.ContainerMapping] = TypeAdapter(t.ContainerMapping)
        config_dict: t.ContainerMapping = adapter.validate_python(config_payload)
        normalized_path = m.Meltano.PathPayload(value=Path(str(path_obj))).value
        return FlextMeltanoProjectService._write_meltano_config(
            normalized_path,
            config_dict,
        )

    @staticmethod
    def _generate_minimal_config(
        temp_path: Path,
        project_id: str,
    ) -> r[t.ContainerMapping]:
        """Generate minimal meltano.yml configuration."""
        extractors: Sequence[t.Dict] = []
        loaders: Sequence[t.Dict] = []
        transformers: Sequence[t.Dict] = []
        config = {
            "version": 1,
            "default_environment": "dev",
            "project_id": project_id,
            "environments": [
                {
                    "name": "dev",
                    "config": {
                        "plugins": {
                            "extractors": extractors,
                            "loaders": loaders,
                            "transformers": transformers,
                        },
                    },
                },
            ],
        }
        return r.ok({"path": temp_path, "config": config})

    @staticmethod
    def _initialize_project_config(project_path: Path, project_name: str) -> r[Path]:
        """Initialize meltano.yml configuration file."""
        try:
            config_content = f"version: 1\ndefault_environment: dev\nproject_id: {project_name}\nenvironments:\n- name: dev\n- name: staging\n- name: prod\n"
            config_file = project_path / "meltano.yml"
            config_file.write_text(config_content, encoding="utf-8")
            return r[Path].ok(project_path)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to initialize meltano.yml: {e}")

    @staticmethod
    def _validate_meltano_config_exists(project_root: Path) -> r[Path]:
        """Validate meltano.yml exists in project directory."""
        meltano_yml = project_root / c.Meltano.Paths.MELTANO_PROJECT_FILE
        if not meltano_yml.exists():
            return r[Path].fail(
                f"Not a Meltano project: meltano.yml not found in {project_root}",
            )
        return r[Path].ok(project_root)

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
    def _write_meltano_config(
        project_path: Path,
        config: t.ContainerMapping,
    ) -> r[Path]:
        """Write meltano.yml configuration file."""
        try:
            config_file = project_path / c.Meltano.Paths.MELTANO_PROJECT_FILE
            with config_file.open("w", encoding="utf-8") as f:
                yaml.safe_dump(config, f, default_flow_style=False)
            return r[Path].ok(project_path)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to write meltano.yml: {e}")

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
        return (
            self
            ._validate_project_creation_params(project_name, project_dir)
            .flat_map(
                lambda params: self._create_project_directory(
                    str(params["name"]),
                    m.Meltano.PathPayload(value=Path(str(params["parent_dir"]))).value,
                ),
            )
            .flat_map(self._create_project_structure)
            .flat_map(
                lambda project_path: self._initialize_project_config(
                    project_path,
                    project_name,
                ),
            )
            .flat_map(
                lambda project_path: self._build_creation_result(
                    project_name,
                    project_path,
                ),
            )
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
        return (
            self
            ._validate_project_parameters(project_id, prefix)
            .flat_map(
                lambda params: self._create_temp_directory(params["prefix"]).flat_map(
                    lambda temp_path: self._generate_minimal_config(
                        temp_path,
                        params["project_id"],
                    ),
                ),
            )
            .flat_map(self._extract_and_write_config)
            .flat_map(self._initialize_project_instance)
            .flat_map(self._convert_to_project_dict)
        )

    @staticmethod
    def build_service_execution_payload(
        service_type: str,
        meltano_config: FlextMeltanoSettings,
    ) -> r[t.Meltano.MeltanoConfigDict]:
        """Build normalized execution payload for service health responses."""
        try:
            return r[t.Meltano.MeltanoConfigDict].ok({
                "service_type": service_type,
                "status": "ready",
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
            self._meltano_config,
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
        return (
            self
            ._validate_project_path(project_root)
            .flat_map(self._validate_meltano_config_exists)
            .flat_map(self._load_project_from_path)
            .flat_map(self._convert_to_project_dict)
        )

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
