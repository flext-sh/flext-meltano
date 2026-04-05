"""FLEXT Meltano Utilities - Project structure and file operations."""

from __future__ import annotations

import tempfile
from collections.abc import Mapping
from pathlib import Path

from flext_cli import FlextCliUtilities, r

from flext_core import u
from flext_meltano import c, m, p, t


class FlextMeltanoUtilitiesProject:
    """Project directory creation, validation, and config initialization."""

    @staticmethod
    def ensure_directory(
        directory_path: Path,
        *,
        exist_ok: bool = True,
    ) -> r[Path]:
        """Ensure a directory exists and return its normalized path."""

        def _ensure() -> Path:
            directory_path.mkdir(parents=True, exist_ok=exist_ok)
            return directory_path

        return u.try_(
            _ensure,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(lambda e: f"Failed to ensure directory exists: {e}")

    @staticmethod
    def ensure_project_subdirectory(
        project_path: Path,
        directory_name: str,
    ) -> r[Path]:
        """Ensure a named Meltano project subdirectory exists."""
        return FlextMeltanoUtilitiesProject.ensure_directory(
            project_path / directory_name,
            exist_ok=True,
        )

    @staticmethod
    def build_project_metadata(
        project_root: Path,
        *,
        state: str | None = None,
    ) -> t.Meltano.OptionalScalarMap:
        """Build canonical project metadata mapping from a project root."""
        metadata: dict[str, t.Scalar | None] = {
            "root": str(project_root),
            "name": str(project_root.name),
        }
        if state is not None:
            metadata["state"] = state
        return metadata

    @staticmethod
    def build_project_creation_result(
        project_name: str,
        project_path: Path,
        *,
        creation_method: str = "manual_file_creation",
        success: bool = True,
    ) -> t.StrMapping:
        """Build canonical project creation response payload."""
        return {
            "success": "true" if success else "false",
            "project_name": project_name,
            "project_path": str(project_path),
            "creation_method": creation_method,
            "meltano_yml_exists": str(
                (project_path / c.Meltano.PATH_MELTANO_PROJECT_FILE).exists()
            ),
        }

    @staticmethod
    def create_project_file(
        file_path: Path,
        content: str | t.ContainerMapping,
    ) -> r[Path]:
        """Create a project file with content."""
        if not isinstance(content, (str, dict)):
            return r[Path].fail("Invalid content type: must be string or dict")
        guard: str | t.ContainerMapping = content

        def _create() -> Path:
            ensured_parent = FlextMeltanoUtilitiesProject.ensure_directory(
                file_path.parent,
                exist_ok=True,
            )
            if ensured_parent.is_failure:
                raise OSError(
                    ensured_parent.error or "Failed to prepare parent directory"
                )
            text = m.Meltano.FileContentPayload.model_validate({
                "content": guard
            }).content
            u.write_file(file_path, text)
            return file_path

        return u.try_(_create, catch=(OSError, ValueError)).map_error(
            lambda e: f"Failed to create project file: {e}"
        )

    @staticmethod
    def directory_exists(path: Path) -> r[bool]:
        """Check if directory exists."""
        return u.try_(
            lambda: path.exists() and path.is_dir(),
            catch=(OSError, ValueError),
        ).map_error(lambda exc: f"Failed to check directory existence: {exc}")

    @staticmethod
    def validate_project_structure(project_path: Path) -> r[bool]:
        """Validate Meltano project structure."""

        def _validate() -> bool:
            if not project_path.exists():
                msg = f"Project path does not exist: {project_path}"
                raise ValueError(msg)
            meltano_file = project_path / c.Meltano.PATH_MELTANO_PROJECT_FILE
            if meltano_file.exists():
                return True
            msg = f"Meltano config file not found: {meltano_file}"
            raise ValueError(msg)

        return u.try_(
            _validate,
            catch=(OSError, ValueError),
        ).map_error(lambda err: f"Failed to validate project structure: {err}")

    @staticmethod
    def convert_to_project_dict(
        project: (
            p.Meltano.Project
            | t.Meltano.DbtProject
            | Mapping[str, t.ContainerMapping | None]
            | Path
            | t.ContainerMapping
            | None
        ),
    ) -> r[t.Meltano.DbtProject]:
        """Convert Meltano project value to FLEXT ContainerMapping representation."""

        def _convert() -> t.Meltano.DbtProject:
            if isinstance(project, Mapping):
                return {
                    "name": str(project.get("name", "meltano_project")),
                    "root": str(project.get("root", c.IDENTIFIER_UNKNOWN)),
                    "settings": str(project.get("settings", "")),
                    "meltano_version": str(project.get("meltano_version", "")),
                }
            return {
                "name": "meltano_project",
                "root": c.IDENTIFIER_UNKNOWN,
                "settings": "",
                "meltano_version": "",
            }

        return u.try_(
            _convert,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(lambda e: f"Failed to convert project: {e}")

    @staticmethod
    def create_project_directory(project_name: str, parent_dir: Path) -> r[Path]:
        """Create project directory structure."""
        return FlextMeltanoUtilitiesProject.ensure_directory(
            parent_dir / project_name,
            exist_ok=True,
        ).map_error(lambda e: f"Failed to create project directory: {e}")

    @staticmethod
    def create_project_structure(project_path: Path) -> r[Path]:
        """Create standard Meltano project directory structure."""

        def _create() -> Path:
            for d in [*c.Meltano.FILE_PATH_STANDARD_DIRS, c.Meltano.PATH_OUTPUT_DIR]:
                (project_path / d).mkdir(exist_ok=True)
                (project_path / d / ".gitkeep").touch()
            return project_path

        return u.try_(
            _create,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(lambda e: f"Failed to create project structure: {e}")

    @staticmethod
    def create_temp_directory(prefix: str) -> r[Path]:
        """Create temporary directory with FLEXT utilities."""
        return u.try_(
            lambda: Path(tempfile.mkdtemp(prefix=prefix)),
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(lambda e: f"Failed to create temp directory: {e}")

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
            "version": c.Meltano.PLUGIN_CONFIG_VERSION,
            "default_environment": c.Meltano.METADATA_DEFAULT_ENVIRONMENTS[0],
            "project_id": project_id,
            "environments": [
                {
                    "name": c.Meltano.METADATA_DEFAULT_ENVIRONMENTS[0],
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

        def _initialize() -> Path:
            environments = c.Meltano.METADATA_DEFAULT_ENVIRONMENTS
            config_content = (
                f"version: {c.Meltano.PLUGIN_CONFIG_VERSION}\n"
                f"default_environment: {environments[0]}\n"
                f"project_id: {project_name}\n"
                "environments:\n"
                f"- name: {environments[0]}\n"
                f"- name: {environments[1]}\n"
                f"- name: {environments[2]}\n"
            )
            config_file = project_path / c.Meltano.PATH_MELTANO_PROJECT_FILE
            u.write_file(config_file, config_content)
            return project_path

        return u.try_(
            _initialize,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(
            lambda e: (
                f"Failed to initialize {c.Meltano.PATH_MELTANO_PROJECT_FILE}: {e}"
            ),
        )

    @staticmethod
    def validate_meltano_config_exists(project_root: Path) -> r[Path]:
        """Validate meltano.yml exists in project directory."""
        meltano_yml = project_root / c.Meltano.PATH_MELTANO_PROJECT_FILE
        if not meltano_yml.exists():
            return r[Path].fail(
                "Not a Meltano project: "
                f"{c.Meltano.PATH_MELTANO_PROJECT_FILE} "
                f"not found in {project_root}",
            )
        return r[Path].ok(project_root)

    @staticmethod
    def write_meltano_config(
        project_path: Path,
        config: t.ContainerMapping,
    ) -> r[Path]:
        """Write meltano.yml configuration file."""
        config_file = project_path / c.Meltano.PATH_MELTANO_PROJECT_FILE
        dump_result = FlextCliUtilities.Cli.yaml_dump(config_file, config)
        if dump_result.is_failure:
            return r[Path].fail(
                f"Failed to write {c.Meltano.PATH_MELTANO_PROJECT_FILE}: "
                f"{dump_result.error}",
            )
        return r[Path].ok(project_path)
