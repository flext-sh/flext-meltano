"""FLEXT Pipeline Project Service - Enterprise project management foundation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import override

from flext_meltano import (
    FlextMeltanoAbstractions,
    FlextMeltanoServiceBase,
    FlextMeltanoValidators,
    c,
    p,
    r,
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
    ) -> p.Result[t.JsonMapping]:
        """Validate parameters for project creation."""
        if not project_name or not project_name.strip():
            return r[t.JsonMapping].fail("Project name cannot be empty")
        if not project_dir.exists():
            return r[t.JsonMapping].fail(f"Parent directory not found: {project_dir}")
        validation_payload: dict[str, t.JsonValue] = {
            "name": project_name.strip(),
            "parent_dir": str(project_dir),
        }
        return r[t.JsonMapping].ok(validation_payload)

    @staticmethod
    def _validate_project_parameters(
        project_id: str | None, prefix: str
    ) -> p.Result[t.StrMapping]:
        """Validate temporary project creation parameters."""
        if not prefix or not prefix.strip():
            return r[t.StrMapping].fail("Project prefix cannot be empty")
        return r[t.StrMapping].ok({
            "project_id": project_id or "flext-meltano-project",
            "prefix": prefix.strip(),
        })

    @staticmethod
    def _validate_project_path(project_root: Path) -> p.Result[Path]:
        """Validate project directory exists."""
        if not project_root.exists():
            return r[Path].fail(f"Project directory not found: {project_root}")
        return r[Path].ok(project_root)

    @staticmethod
    def validate_project(project_path: Path) -> p.Result[bool]:
        """Validate Meltano project structure using dedicated validators."""
        return FlextMeltanoValidators.validate_pipeline_project_structure(project_path)

    def create_project(
        self, project_name: str, project_dir: Path
    ) -> p.Result[t.StrMapping]:
        """Create new Meltano project using railway-oriented file operations."""
        params_r = self._validate_project_creation_params(project_name, project_dir)
        if params_r.failure:
            return r[t.StrMapping].fail(params_r.error or "Validation failed")

        name = str(params_r.value["name"])
        parent = Path(str(params_r.value["parent_dir"]))
        project_path = parent / name

        try:
            project_path.mkdir(parents=True, exist_ok=True)
            for d in [*c.Meltano.FILE_PATH_STANDARD_DIRS, c.Meltano.PATH_OUTPUT_DIR]:
                (project_path / d).mkdir(parents=True, exist_ok=True)
                (project_path / d / ".gitkeep").touch()

            environments = c.Meltano.METADATA_DEFAULT_ENVIRONMENTS
            config_content = (
                f"version: {c.Meltano.PLUGIN_CONFIG_VERSION}\n"
                f"default_environment: {environments[0]}\n"
                f"project_id: {name}\n"
                "environments:\n"
                f"- name: {environments[0]}\n"
                f"- name: {environments[1]}\n"
                f"- name: {environments[2]}\n"
            )
            config_file = project_path / c.Meltano.PATH_MELTANO_PROJECT_FILE
            u.write_file(config_file, config_content)
        except OSError as e:
            return r[t.StrMapping].fail(f"Failed to create project files: {e}")

        return self._build_creation_result(project_name, project_path)

    def create_temporary_project(
        self,
        project_id: str | None = None,
        prefix: str = "flext_meltano_",
    ) -> p.Result[t.Meltano.DbtProject]:
        """Create temporary Meltano project with railway-oriented validation."""
        params_r = self._validate_project_parameters(project_id, prefix)
        if params_r.failure:
            return r[t.Meltano.DbtProject].fail(params_r.error or "Validation failed")

        params = params_r.value
        try:
            temp_path = Path(tempfile.mkdtemp(prefix=params["prefix"]))
            settings: t.JsonMapping = {
                "version": c.Meltano.PLUGIN_CONFIG_VERSION,
                "default_environment": c.Meltano.METADATA_DEFAULT_ENVIRONMENTS[0],
                "project_id": params["project_id"],
                "environments": [
                    {
                        "name": c.Meltano.METADATA_DEFAULT_ENVIRONMENTS[0],
                        "settings": {
                            "plugins": {
                                "extractors": list[t.JsonValue](),
                                "loaders": list[t.JsonValue](),
                                "transformers": list[t.JsonValue](),
                            },
                        },
                    },
                ],
            }
            config_file = temp_path / c.Meltano.PATH_MELTANO_PROJECT_FILE
            dump_result = u.Cli.yaml_dump(config_file, settings)
            if dump_result.failure:
                return r[t.Meltano.DbtProject].fail(
                    dump_result.error or "YAML dump failed"
                )
        except OSError as e:
            return r[t.Meltano.DbtProject].fail(f"Temp project creation failed: {e}")

        inst_r = self._initialize_project_instance(temp_path)
        if inst_r.failure:
            return r[t.Meltano.DbtProject].fail(inst_r.error or "Init failed")

        return r[t.Meltano.DbtProject].ok({
            "name": "meltano_project",
            "root": c.IDENTIFIER_UNKNOWN,
            "settings": "",
            "meltano_version": "",
        })

    @staticmethod
    def build_service_execution_payload(
        service_type: str,
        meltano_config: p.Settings,
    ) -> p.Result[t.JsonMapping]:
        """Build normalized execution payload for service health responses."""
        settings_payload = t.Cli.JSON_MAPPING_ADAPTER.validate_python(
            meltano_config.model_dump(),
        )
        payload: dict[str, t.JsonValue] = {
            "status": c.Meltano.OperationStatus.READY,
            "service_type": service_type,
            "settings": dict(settings_payload.items()),
        }
        return r[t.JsonMapping].ok(payload)

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute the pipeline project service."""
        result = self.build_service_execution_payload(
            "flext_meltano_project_service", self.settings
        )
        if result.success:
            self.logger.info("FlextMeltanoProjectService executed successfully")
            return result
        error_msg = result.error or "Project service execution failed"
        self.logger.error(error_msg)
        return r[t.JsonMapping].fail(error_msg)

    def initialize_project(self, project_root: Path) -> p.Result[t.Meltano.DbtProject]:
        """Initialize Meltano project using railway pattern validation chain."""
        vpath_r = self._validate_project_path(project_root)
        if vpath_r.failure:
            return r[t.Meltano.DbtProject].fail(vpath_r.error or "Path missing")

        meltano_yml = project_root / c.Meltano.PATH_MELTANO_PROJECT_FILE
        if not meltano_yml.exists():
            return r[t.Meltano.DbtProject].fail(f"Not a Meltano project: {meltano_yml}")

        loaded_r = self._load_project_from_path(project_root)
        if loaded_r.failure:
            return r[t.Meltano.DbtProject].fail(loaded_r.error or "Load failed")

        return r[t.Meltano.DbtProject].ok({
            "name": "meltano_project",
            "root": c.IDENTIFIER_UNKNOWN,
            "settings": "",
            "meltano_version": "",
        })

    def _build_creation_result(
        self, project_name: str, project_path: Path
    ) -> p.Result[t.StrMapping]:
        """Build successful project creation result."""
        result: t.StrMapping = {
            "success": "true",
            "project_name": project_name,
            "project_path": str(project_path),
            "creation_method": "manual_file_creation",
            "meltano_yml_exists": str(
                (project_path / c.Meltano.PATH_MELTANO_PROJECT_FILE).exists()
            ),
        }
        self.logger.info(
            "Meltano project created successfully",
            project_name=project_name,
            project_path=str(project_path),
        )
        return r[t.StrMapping].ok(result)

    def _initialize_project_instance(self, project_path: Path) -> p.Result[Path]:
        """Initialize Meltano project instance using abstractions."""
        project_result = self._abstractions.find_project(project_path)
        if project_result.failure:
            return r[Path].fail(project_result.error or "Failed to initialize project")
        return project_result

    def _load_project_from_path(self, project_root: Path) -> p.Result[Path]:
        """Load Meltano project from validated path."""
        project_result = self._abstractions.find_project(project_root)
        if project_result.failure:
            return r[Path].fail(
                project_result.error or "Failed to load Meltano project"
            )
        return project_result


__all__: list[str] = ["FlextMeltanoProjectService"]
