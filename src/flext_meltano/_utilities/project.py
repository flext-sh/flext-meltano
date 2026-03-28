"""FLEXT Meltano Utilities - Project structure and file operations."""

from __future__ import annotations

import tempfile
from collections.abc import Mapping
from pathlib import Path

import yaml
from flext_cli import FlextCliUtilities, r

from flext_meltano import c, m, p, t


class FlextMeltanoUtilitiesProject:
    """Project directory creation, validation, and config initialization."""

    @staticmethod
    def create_project_file(
        file_path: Path,
        content: str | t.Meltano.MeltanoConfigDict,
    ) -> r[Path]:
        """Create a project file with content."""
        if not isinstance(content, (str, dict)):
            return r[Path].fail("Invalid content type: must be string or dict")
        guard: str | t.Meltano.MeltanoConfigDict = content

        def _create() -> Path:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            text = m.Meltano.FileContentPayload.model_validate({
                "content": guard
            }).content
            file_path.write_text(text, encoding="utf-8")
            return file_path

        return FlextCliUtilities.try_(
            _create, catch=(OSError, ValueError, yaml.YAMLError)
        ).map_error(lambda e: f"Failed to create project file: {e}")

    @staticmethod
    def directory_exists(path: Path) -> r[bool]:
        """Check if directory exists."""
        try:
            return r[bool].ok(path.exists() and path.is_dir())
        except (OSError, ValueError) as exc:
            return r[bool].fail(f"Failed to check directory existence: {exc}")

    @staticmethod
    def validate_project_structure(project_path: Path) -> r[bool]:
        """Validate Meltano project structure."""
        try:
            if not project_path.exists():
                return r[bool].fail(f"Project path does not exist: {project_path}")
            meltano_file = project_path / c.Meltano.Paths.MELTANO_PROJECT_FILE
            fallback = project_path / "meltano.yml"
            if meltano_file.exists() or fallback.exists():
                return r[bool].ok(True)
            return r[bool].fail(f"Meltano config file not found: {meltano_file}")
        except (OSError, ValueError) as err:
            return r[bool].fail(f"Failed to validate project structure: {err}")

    @staticmethod
    def convert_to_project_dict(
        project: (
            p.Meltano.Project
            | t.Meltano.Dbt.Project
            | Mapping[str, t.ContainerMapping | None]
            | Path
            | t.ContainerMapping
            | None
        ),
    ) -> r[t.Meltano.Dbt.Project]:
        """Convert Meltano project value to FLEXT ContainerMapping representation."""
        try:
            project_dict: t.Meltano.Dbt.Project = {
                "name": str(a)
                if (a := getattr(project, "name", None))
                else "meltano_project",
                "root": str(a)
                if (a := getattr(project, "root", None))
                else c.IDENTIFIER_UNKNOWN,
                "settings": str(a) if (a := getattr(project, "settings", None)) else "",
                "meltano_version": str(a)
                if (a := getattr(project, "meltano_version", None))
                else "",
            }
            return r[t.Meltano.Dbt.Project].ok(project_dict)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.Meltano.Dbt.Project].fail(f"Failed to convert project: {e}")

    @staticmethod
    def create_project_directory(project_name: str, parent_dir: Path) -> r[Path]:
        """Create project directory structure."""
        try:
            project_path = parent_dir / project_name
            project_path.mkdir(parents=True, exist_ok=True)
            return r[Path].ok(project_path)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to create project directory: {e}")

    @staticmethod
    def create_project_structure(project_path: Path) -> r[Path]:
        """Create standard Meltano project directory structure."""
        try:
            for d in [*c.Meltano.FilePaths.STANDARD_DIRS, c.Meltano.Paths.OUTPUT_DIR]:
                (project_path / d).mkdir(exist_ok=True)
                (project_path / d / ".gitkeep").touch()
            return r[Path].ok(project_path)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to create project structure: {e}")

    @staticmethod
    def create_temp_directory(prefix: str) -> r[Path]:
        """Create temporary directory with FLEXT utilities."""
        try:
            temp_dir = tempfile.mkdtemp(prefix=prefix)
            return r[Path].ok(Path(temp_dir))
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to create temp directory: {e}")

    @staticmethod
    def extract_and_write_config(config_data: t.ContainerMapping) -> r[Path]:
        """Extract and validate path and config from generated config data."""
        path_obj = config_data.get("path")
        config_obj = config_data.get("config")
        payload = m.Meltano.ConfigMappingPayload.model_validate({
            "values": config_obj
        }).values
        config_dict: t.ContainerMapping = (
            t.Meltano.CONTAINER_MAP_ADAPTER.validate_python(payload)
        )
        normalized_path = m.Meltano.PathPayload(value=Path(str(path_obj))).value
        return FlextMeltanoUtilitiesProject.write_meltano_config(
            normalized_path, config_dict
        )

    @staticmethod
    def generate_minimal_config(
        temp_path: Path,
        project_id: str,
    ) -> r[t.ContainerMapping]:
        """Generate minimal meltano.yml configuration."""
        config: t.ContainerMapping = {
            "version": 1,
            "default_environment": "dev",
            "project_id": project_id,
            "environments": [
                {
                    "name": "dev",
                    "config": {
                        "plugins": {
                            "extractors": list[t.ContainerMapping](),
                            "loaders": list[t.ContainerMapping](),
                            "transformers": list[t.ContainerMapping](),
                        },
                    },
                },
            ],
        }
        return r[t.ContainerMapping].ok({"path": str(temp_path), "config": config})

    @staticmethod
    def initialize_project_config(project_path: Path, project_name: str) -> r[Path]:
        """Initialize meltano.yml configuration file."""
        try:
            config_content = f"version: 1\ndefault_environment: dev\nproject_id: {project_name}\nenvironments:\n- name: dev\n- name: staging\n- name: prod\n"
            config_file = project_path / "meltano.yml"
            config_file.write_text(config_content, encoding="utf-8")
            return r[Path].ok(project_path)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[Path].fail(f"Failed to initialize meltano.yml: {e}")

    @staticmethod
    def validate_meltano_config_exists(project_root: Path) -> r[Path]:
        """Validate meltano.yml exists in project directory."""
        meltano_yml = project_root / c.Meltano.Paths.MELTANO_PROJECT_FILE
        if not meltano_yml.exists():
            return r[Path].fail(
                f"Not a Meltano project: meltano.yml not found in {project_root}",
            )
        return r[Path].ok(project_root)

    @staticmethod
    def write_meltano_config(
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
