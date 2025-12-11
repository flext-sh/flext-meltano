"""FLEXT Pipeline Project Service - Enterprise project management foundation.

Handles pipeline project lifecycle operations following FLEXT Clean Architecture
with railway-oriented programming and zero custom pipeline implementations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import cast

import yaml
from flext_core import (
    FlextContainer,
    FlextLogger,
    FlextResult,
    FlextService,
    u,
)

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.settings import FlextMeltanoSettings
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.validators import FlextMeltanoValidators

# Import aliases for concise usage
r = FlextResult
s = FlextService
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels


class FlextMeltanoProjectService(s[t.MeltanoCore.MeltanoConfigDict]):
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
        self._config = config or FlextMeltanoSettings()
        self.logger: FlextLogger = FlextLogger(__name__)
        self._container = FlextContainer.get_global()
        self._abstractions = FlextMeltanoAbstractions()

    def execute(
        self,
    ) -> r[t.MeltanoCore.MeltanoConfigDict]:
        """Execute the pipeline project service.

        Returns:
        r containing project service configuration and status.

        """
        try:
            config_data: t.MeltanoCore.MeltanoConfigDict = {
                "service_type": "flext_meltano_project_service",
                "status": "ready",
                "config": self._config.model_dump()
                if hasattr(self._config, "model_dump")
                else {},
            }

            self.logger.info("FlextMeltanoProjectService executed successfully")
            return r[t.MeltanoCore.MeltanoConfigDict].ok(data=config_data)

        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            error_msg = f"Project service execution failed: {e}"
            self.logger.exception(error_msg)
            return r[t.MeltanoCore.MeltanoConfigDict].fail(error_msg)

    def create_temporary_project(
        self,
        project_id: str | None = None,
        prefix: str = "flext_meltano_",
    ) -> r[t.Dbt.Project]:
        """Create temporary Meltano project with railway-oriented validation.

        Uses r.flat_map chains for composable project creation
        with automatic error propagation and resource management.

        Args:
        project_id: Optional project identifier for uniqueness
        prefix: Temporary directory prefix for organization

        Returns:
        r containing project dict[str, object] with standardized structure

        """
        return (
            self._validate_project_parameters(project_id, prefix)
            .flat_map(
                lambda params: self._create_temp_directory(params["prefix"]).flat_map(
                    lambda temp_path: self._generate_minimal_config(
                        temp_path,
                        params["project_id"],
                    ),
                ),
            )
            .flat_map(
                lambda config_data: self._write_meltano_config(
                    cast("Path", config_data["path"]),
                    cast("dict[str, object]", config_data["config"]),
                ),
            )
            .flat_map(self._initialize_project_instance)
            .flat_map(self._convert_to_project_dict)
        )

    def initialize_project(
        self,
        project_root: Path,
    ) -> r[t.Dbt.Project]:
        """Initialize Meltano project using railway pattern validation chain.

        Chains initialization steps with automatic error handling:
        - Project root validation
        - Meltano.yml existence check
        - Project loading and conversion

        Args:
        project_root: Directory path containing meltano.yml

        Returns:
        r containing initialized project dict[str, object] or validation error

        """
        return (
            self._validate_project_path(project_root)
            .flat_map(self._validate_meltano_config_exists)
            .flat_map(self._load_project_from_path)
            .flat_map(self._convert_to_project_dict)
        )

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
    ) -> r[dict[str, str]]:
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
            self._validate_project_creation_params(project_name, project_dir)
            .flat_map(
                lambda params: self._create_project_directory(
                    cast("str", params["name"]),
                    cast("Path", params["parent_dir"]),
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

    # Railway-oriented helper methods

    @staticmethod
    def _validate_project_parameters(
        project_id: str | None,
        prefix: str,
    ) -> r[dict[str, str]]:
        """Validate temporary project creation parameters."""
        if not prefix or not prefix.strip():
            return r[dict[str, str]].fail("Project prefix cannot be empty")

        return r[dict[str, str]].ok({
            "project_id": project_id or "flext-meltano-project",
            "prefix": prefix.strip(),
        })

    @staticmethod
    def _create_temp_directory(prefix: str) -> r[Path]:
        """Create temporary directory with FLEXT utilities."""
        try:
            temp_dir = tempfile.mkdtemp(prefix=prefix)
            return r[Path].ok(Path(temp_dir))
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to create temp directory: {e}")

    @staticmethod
    def _generate_minimal_config(
        temp_path: Path,
        project_id: str,
    ) -> r[dict[str, object]]:
        """Generate minimal meltano.yml configuration."""
        config = {
            "version": 1,
            "default_environment": "dev",
            "project_id": project_id,
            "environments": [
                {
                    "name": "dev",
                    "config": {
                        "plugins": {
                            "extractors": [],
                            "loaders": [],
                            "transformers": [],
                        },
                    },
                },
            ],
        }
        return r[dict[str, object]].ok({
            "path": temp_path,
            "config": config,
        })

    @staticmethod
    def _write_meltano_config(project_path: Path, config: dict[str, object]) -> r[Path]:
        """Write meltano.yml configuration file."""
        try:
            config_file = project_path / c.Paths.MELTANO_PROJECT_FILE
            with config_file.open("w", encoding="utf-8") as f:
                yaml.safe_dump(config, f, default_flow_style=False)
            return r[Path].ok(project_path)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to write meltano.yml: {e}")

    def _initialize_project_instance(self, project_path: Path) -> r[object]:
        """Initialize Meltano project instance using abstractions."""
        project_result = self._abstractions.find_project(project_path)
        if project_result.is_failure:
            return r[object].fail(
                project_result.error or "Failed to initialize project",
            )
        return cast("r[object]", project_result)

    @staticmethod
    def _convert_to_project_dict(project: object) -> r[t.Dbt.Project]:
        """Convert Meltano project object to FLEXT dict[str, object] representation."""
        try:
            project_dict: t.Dbt.Project = {
                "name": u.get(project, "name", default="meltano_project"),
                "root": u.get(project, "root", default="unknown"),
                "settings": u.get(project, "settings", default=""),
                "meltano_version": u.get(project, "meltano_version", default=""),
            }
            return r[t.Dbt.Project].ok(project_dict)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.Dbt.Project].fail(f"Failed to convert project object: {e}")

    @staticmethod
    def _validate_project_path(project_root: Path) -> r[Path]:
        """Validate project directory exists."""
        if not project_root.exists():
            return r[Path].fail(f"Project directory not found: {project_root}")
        return r[Path].ok(project_root)

    @staticmethod
    def _validate_meltano_config_exists(project_root: Path) -> r[Path]:
        """Validate meltano.yml exists in project directory."""
        meltano_yml = project_root / c.Paths.MELTANO_PROJECT_FILE
        if not meltano_yml.exists():
            return r[Path].fail(
                f"Not a Meltano project: meltano.yml not found in {project_root}",
            )
        return r[Path].ok(project_root)

    def _load_project_from_path(self, project_root: Path) -> r[object]:
        """Load Meltano project from validated path."""
        project_result = self._abstractions.find_project(project_root)
        if project_result.is_failure:
            return r[object].fail(
                project_result.error or "Failed to load Meltano project",
            )
        return cast("r[object]", project_result)

    @staticmethod
    def _validate_project_creation_params(
        project_name: str,
        project_dir: Path,
    ) -> r[dict[str, object]]:
        """Validate parameters for project creation."""
        if not project_name or not project_name.strip():
            return r[dict[str, object]].fail("Project name cannot be empty")

        if not project_dir.exists():
            return r[dict[str, object]].fail(
                f"Parent directory not found: {project_dir}",
            )

        return r[dict[str, object]].ok({
            "name": project_name.strip(),
            "parent_dir": project_dir,
        })

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
    def _initialize_project_config(project_path: Path, project_name: str) -> r[Path]:
        """Initialize meltano.yml configuration file."""
        try:
            config_content = f"""version: 1
default_environment: dev
project_id: {project_name}
environments:
- name: dev
- name: staging
- name: prod
"""

            config_file = project_path / "meltano.yml"
            config_file.write_text(config_content, encoding="utf-8")
            return r[Path].ok(project_path)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to initialize meltano.yml: {e}")

    def _build_creation_result(
        self,
        project_name: str,
        project_path: Path,
    ) -> r[dict[str, str]]:
        """Build successful project creation result."""
        try:
            result: dict[str, str] = {
                "success": "true",
                "project_name": project_name,
                "project_path": str(project_path),
                "creation_method": "manual_file_creation",
                "meltano_yml_exists": str(
                    (project_path / c.Paths.MELTANO_PROJECT_FILE).exists(),
                ),
            }

            self.logger.info(
                "Meltano project created successfully",
                project_name=project_name,
                project_path=str(project_path),
            )

            return r[dict[str, str]].ok(result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[dict[str, str]].fail(f"Failed to build creation result: {e}")


__all__ = ["FlextMeltanoProjectService"]
