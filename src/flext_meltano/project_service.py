"""FLEXT Meltano Project Service - Enterprise project management foundation.

Handles Meltano project lifecycle operations following FLEXT Clean Architecture
with railway-oriented programming and zero custom ELT implementations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import yaml
from flext_core import FlextCore

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.validators import FlextMeltanoValidators


class FlextMeltanoProjectService(
    FlextCore.Service[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]
):
    """Enterprise Meltano project service with railway-oriented programming.

    Manages complete Meltano project lifecycle using FLEXT ecosystem patterns:
    - Project creation and initialization with FlextCore.Result error handling
    - Railway-oriented validation chains for composable operations
    - Complete flext-core integration (Container, Logger, Utilities)
    - Zero try/except fallbacks - explicit FlextCore.Result error handling

    Extends flext-core foundation for enterprise ELT pipeline orchestration.
    """

    def __init__(self, config: FlextMeltanoConfig | None = None) -> None:
        """Initialize project service with complete FLEXT ecosystem integration."""
        super().__init__()
        self._config = config or FlextMeltanoConfig()
        self.logger: FlextCore.Logger = FlextCore.Logger(__name__)
        self._container = FlextCore.Container.get_global()
        self._utilities = FlextCore.Utilities()
        self._abstractions = FlextMeltanoAbstractions()

    def execute(
        self,
    ) -> FlextCore.Result[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict]:
        """Execute the Meltano project service.

        Returns:
            FlextCore.Result containing project service configuration and status.

        """
        try:
            config_data: FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict = {
                "service_type": "flext_meltano_project_service",
                "status": "ready",
                "config": self._config.model_dump()
                if hasattr(self._config, "model_dump")
                else {},
            }

            self.logger.info("FlextMeltanoProjectService executed successfully")
            return FlextCore.Result[FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict].ok(
                data=config_data
            )

        except Exception as e:
            error_msg = f"Project service execution failed: {e}"
            self.logger.exception(error_msg)
            return FlextCore.Result[
                FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict
            ].fail(error_msg)

    def create_temporary_project(
        self,
        project_id: str | None = None,
        prefix: str = "flext_meltano_",
    ) -> FlextCore.Result[FlextMeltanoTypes.Dbt.Project]:
        """Create temporary Meltano project with railway-oriented validation.

        Uses FlextCore.Result.flat_map chains for composable project creation
        with automatic error propagation and resource management.

        Args:
            project_id: Optional project identifier for uniqueness
            prefix: Temporary directory prefix for organization

        Returns:
            FlextCore.Result containing project dict[str, object] with standardized structure

        """
        return (
            self._validate_project_parameters(project_id, prefix)
            .flat_map(
                lambda params: self._create_temp_directory(params["prefix"]).flat_map(
                    lambda temp_path: self._generate_minimal_config(
                        temp_path, params["project_id"]
                    )
                )
            )
            .flat_map(
                lambda config_data: self._write_meltano_config(
                    config_data["path"], config_data["config"]
                )
            )
            .flat_map(self._initialize_project_instance)
            .flat_map(self._convert_to_project_dict)
        )

    def initialize_project(
        self,
        project_root: Path,
    ) -> FlextCore.Result[FlextMeltanoTypes.Dbt.Project]:
        """Initialize Meltano project using railway pattern validation chain.

        Chains initialization steps with automatic error handling:
        - Project root validation
        - Meltano.yml existence check
        - Project loading and conversion

        Args:
            project_root: Directory path containing meltano.yml

        Returns:
            FlextCore.Result containing initialized project dict[str, object] or validation error

        """
        return (
            self._validate_project_path(project_root)
            .flat_map(self._validate_meltano_config_exists)
            .flat_map(self._load_project_from_path)
            .flat_map(self._convert_to_project_dict)
        )

    def validate_project(self, project_path: Path) -> FlextCore.Result[bool]:
        """Validate Meltano project structure using dedicated validators.

        Delegates to FlextMeltanoValidators for consistent validation
        across the entire FLEXT ecosystem.

        Args:
            project_path: Path to potential Meltano project directory

        Returns:
            FlextCore.Result containing True if valid, False with error details if invalid

        """
        return FlextMeltanoValidators.validate_meltano_project_structure(project_path)

    def create_project(
        self,
        project_name: str,
        project_dir: Path,
    ) -> FlextCore.Result[FlextCore.Types.StringDict]:
        """Create new Meltano project using railway-oriented file operations.

        Validates project name, creates directory structure, and initializes
        meltano.yml using composable FlextCore.Result operations.

        Args:
            project_name: Name for the new Meltano project
            project_dir: Parent directory where project will be created

        Returns:
            FlextCore.Result containing project creation metadata or validation error

        """
        return (
            self._validate_project_creation_params(project_name, project_dir)
            .flat_map(
                lambda params: self._create_project_directory(
                    params["name"], params["parent_dir"]
                )
            )
            .flat_map(self._create_project_structure)
            .flat_map(
                lambda project_path: self._initialize_project_config(
                    project_path, project_name
                )
            )
            .flat_map(
                lambda project_path: self._build_creation_result(
                    project_name, project_path
                )
            )
        )

    # Railway-oriented helper methods

    def _validate_project_parameters(
        self, project_id: str | None, prefix: str
    ) -> FlextCore.Result[dict[str, str]]:
        """Validate temporary project creation parameters."""
        if not prefix or not prefix.strip():
            return FlextCore.Result[dict[str, str]].fail(
                "Project prefix cannot be empty"
            )

        return FlextCore.Result[dict[str, str]].ok({
            "project_id": project_id or "flext-meltano-project",
            "prefix": prefix.strip(),
        })

    def _create_temp_directory(self, prefix: str) -> FlextCore.Result[Path]:
        """Create temporary directory with FLEXT utilities."""
        try:
            temp_dir = tempfile.mkdtemp(prefix=prefix)
            return FlextCore.Result[Path].ok(Path(temp_dir))
        except Exception as e:
            return FlextCore.Result[Path].fail(f"Failed to create temp directory: {e}")

    def _generate_minimal_config(
        self, temp_path: Path, project_id: str
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
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
                        }
                    },
                }
            ],
        }
        return FlextCore.Result[FlextCore.Types.Dict].ok({
            "path": temp_path,
            "config": config,
        })

    def _write_meltano_config(
        self, project_path: Path, config: dict
    ) -> FlextCore.Result[Path]:
        """Write meltano.yml configuration file."""
        try:
            config_file = (
                project_path / FlextMeltanoConstants.Meltano.MELTANO_PROJECT_FILE
            )
            with config_file.open("w", encoding="utf-8") as f:
                yaml.safe_dump(config, f, default_flow_style=False)
            return FlextCore.Result[Path].ok(project_path)
        except Exception as e:
            return FlextCore.Result[Path].fail(f"Failed to write meltano.yml: {e}")

    def _initialize_project_instance(
        self, project_path: Path
    ) -> FlextCore.Result[object]:
        """Initialize Meltano project instance using abstractions."""
        project_result = self._abstractions.find_project(project_path)
        if project_result.is_failure:
            return FlextCore.Result[object].fail(
                project_result.error or "Failed to initialize project"
            )
        return project_result

    def _convert_to_project_dict(
        self, project: object
    ) -> FlextCore.Result[FlextMeltanoTypes.Dbt.Project]:
        """Convert Meltano project object to FLEXT dict[str, object] representation."""
        try:
            project_dict: FlextMeltanoTypes.Dbt.Project = {
                "name": str(getattr(project, "name", "meltano_project")),
                "root": str(getattr(project, "root", "unknown")),
                "settings": str(getattr(project, "settings", "")),
                "meltano_version": str(getattr(project, "meltano_version", "")),
            }
            return FlextCore.Result[FlextMeltanoTypes.Dbt.Project].ok(project_dict)
        except Exception as e:
            return FlextCore.Result[FlextMeltanoTypes.Dbt.Project].fail(
                f"Failed to convert project object: {e}"
            )

    def _validate_project_path(self, project_root: Path) -> FlextCore.Result[Path]:
        """Validate project directory exists."""
        if not project_root.exists():
            return FlextCore.Result[Path].fail(
                f"Project directory not found: {project_root}"
            )
        return FlextCore.Result[Path].ok(project_root)

    def _validate_meltano_config_exists(
        self, project_root: Path
    ) -> FlextCore.Result[Path]:
        """Validate meltano.yml exists in project directory."""
        meltano_yml = project_root / FlextMeltanoConstants.Meltano.MELTANO_PROJECT_FILE
        if not meltano_yml.exists():
            return FlextCore.Result[Path].fail(
                f"Not a Meltano project: meltano.yml not found in {project_root}"
            )
        return FlextCore.Result[Path].ok(project_root)

    def _load_project_from_path(self, project_root: Path) -> FlextCore.Result[object]:
        """Load Meltano project from validated path."""
        project_result = self._abstractions.find_project(project_root)
        if project_result.is_failure:
            return FlextCore.Result[object].fail(
                project_result.error or "Failed to load Meltano project"
            )
        return project_result

    def _validate_project_creation_params(
        self, project_name: str, project_dir: Path
    ) -> FlextCore.Result[FlextCore.Types.Dict]:
        """Validate parameters for project creation."""
        if not project_name or not project_name.strip():
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                "Project name cannot be empty"
            )

        if not project_dir.exists():
            return FlextCore.Result[FlextCore.Types.Dict].fail(
                f"Parent directory not found: {project_dir}"
            )

        return FlextCore.Result[FlextCore.Types.Dict].ok({
            "name": project_name.strip(),
            "parent_dir": project_dir,
        })

    def _create_project_directory(
        self, project_name: str, parent_dir: Path
    ) -> FlextCore.Result[Path]:
        """Create project directory structure."""
        try:
            project_path = parent_dir / project_name
            project_path.mkdir(parents=True, exist_ok=True)
            return FlextCore.Result[Path].ok(project_path)
        except Exception as e:
            return FlextCore.Result[Path].fail(
                f"Failed to create project directory: {e}"
            )

    def _create_project_structure(self, project_path: Path) -> FlextCore.Result[Path]:
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

            return FlextCore.Result[Path].ok(project_path)
        except Exception as e:
            return FlextCore.Result[Path].fail(
                f"Failed to create project structure: {e}"
            )

    def _initialize_project_config(
        self, project_path: Path, project_name: str
    ) -> FlextCore.Result[Path]:
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
            return FlextCore.Result[Path].ok(project_path)
        except Exception as e:
            return FlextCore.Result[Path].fail(f"Failed to initialize meltano.yml: {e}")

    def _build_creation_result(
        self, project_name: str, project_path: Path
    ) -> FlextCore.Result[FlextCore.Types.StringDict]:
        """Build successful project creation result."""
        try:
            result: FlextCore.Types.StringDict = {
                "success": "true",
                "project_name": project_name,
                "project_path": str(project_path),
                "creation_method": "manual_file_creation",
                "meltano_yml_exists": str(
                    (project_path / FlextMeltanoConstants.MELTANO_PROJECT_FILE).exists()
                ),
            }

            self.logger.info(
                "Meltano project created successfully",
                project_name=project_name,
                project_path=str(project_path),
            )

            return FlextCore.Result[FlextCore.Types.StringDict].ok(result)
        except Exception as e:
            return FlextCore.Result[FlextCore.Types.StringDict].fail(
                f"Failed to build creation result: {e}"
            )


__all__ = ["FlextMeltanoProjectService"]
