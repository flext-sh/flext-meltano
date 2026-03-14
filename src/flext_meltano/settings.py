"""FLEXT Meltano configuration model and helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, ClassVar

from flext_core import FlextSettings, c, r, t
from pydantic import Field, field_validator


class FlextMeltanoSettings(FlextSettings):
    """Runtime settings for Meltano orchestration services."""

    MELTANO_VERSION: ClassVar[str] = "3.9.1"
    SINGER_SDK_VERSION: ClassVar[str] = "0.48.0"
    DBT_VERSION: ClassVar[str] = "1.10.5"
    PROJECT_FILE: ClassVar[str] = "pipeline.yml"
    STATE_DIR: ClassVar[str] = ".pipeline"
    VENV_DIR: ClassVar[str] = ".meltano/python"
    MELTANO_PROJECT_ROOT_ENV: ClassVar[str] = "MELTANO_PROJECT_ROOT"
    MELTANO_ENVIRONMENT_ENV: ClassVar[str] = "MELTANO_ENVIRONMENT"
    MELTANO_LOG_LEVEL_ENV: ClassVar[str] = "MELTANO_LOG_LEVEL"

    class ConfigBuilders:
        """Namespace for configuration builder utilities."""

    project_root: Annotated[Path, Field(default=Path())]
    config_dir: Annotated[Path, Field(default=Path(".meltano"))]
    logs_dir: Annotated[Path, Field(default=Path("logs"))]
    environment: Annotated[str, Field(default="development")]
    log_level: Annotated[c.Settings.LogLevel, Field(default=c.Settings.LogLevel.INFO)]
    meltano_version: Annotated[str, Field(default=MELTANO_VERSION)]
    singer_sdk_version: Annotated[str, Field(default=SINGER_SDK_VERSION)]
    dbt_version: Annotated[str, Field(default=DBT_VERSION)]

    @field_validator("project_root", mode="before")
    @classmethod
    def _coerce_project_root(cls, value: t.Scalar) -> Path:
        return Path(str(value)).resolve()

    @field_validator("config_dir", "logs_dir", mode="before")
    @classmethod
    def _coerce_path(cls, value: t.Scalar) -> Path:
        return Path(str(value))

    @field_validator("environment")
    @classmethod
    def _validate_environment(cls, value: str) -> str:
        normalized = value.strip().lower()
        if normalized not in {"development", "testing", "production"}:
            msg = "Environment must be one of: development, testing, production"
            raise ValueError(msg)
        return normalized

    @field_validator("log_level")
    @classmethod
    def _validate_log_level(cls, value: str) -> str:
        normalized = value.strip().upper()
        if normalized not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            msg = "Invalid log_level"
            raise ValueError(msg)
        return normalized

    def get_project_file(self) -> r[Path]:
        """Return the canonical pipeline file path."""
        return r[Path].ok(self.project_root / self.PROJECT_FILE)

    def get_absolute_config_dir(self) -> r[Path]:
        """Return absolute Meltano config directory path."""
        return r[Path].ok((self.project_root / self.config_dir).resolve())

    def get_absolute_logs_dir(self) -> r[Path]:
        """Return absolute logs directory path."""
        return r[Path].ok((self.project_root / self.logs_dir).resolve())

    def get_absolute_venv_dir(self) -> Path:
        """Return absolute Meltano virtualenv directory."""
        return (self.project_root / ".meltano" / "python").resolve()

    def validate_project_structure(self) -> r[bool]:
        """Validate required project structure artifacts."""
        pipeline_file = self.project_root / self.PROJECT_FILE
        if not pipeline_file.exists():
            return r[bool].fail(f"{self.PROJECT_FILE} not found in {self.project_root}")
        return r[bool].ok(True)

    def get_environment_variables(self) -> dict[str, str]:
        """Build runtime environment variables for Meltano commands."""
        return {
            self.MELTANO_PROJECT_ROOT_ENV: str(self.project_root),
            self.MELTANO_ENVIRONMENT_ENV: self.environment,
            self.MELTANO_LOG_LEVEL_ENV: self.log_level,
        }

    @classmethod
    def get_version(cls) -> str:
        """Return package semantic version."""
        return "0.9.0"

    @classmethod
    def get_name(cls) -> str:
        """Return package distribution name."""
        return "flext-meltano"

    @classmethod
    def get_default_timeout(cls) -> int:
        """Return default command timeout in seconds."""
        return 30

    @classmethod
    def get_default_batch_size(cls) -> int:
        """Return default batch size for operations."""
        return 1000

    @classmethod
    def get_supported_plugin_types(cls) -> list[str]:
        """Return supported Meltano plugin categories."""
        return ["extractors", "loaders", "transforms"]

    @classmethod
    def get_supported_environments(cls) -> list[str]:
        """Return list of valid deployment environment names."""
        return ["development", "testing", "production"]

    @classmethod
    def get_supported_log_levels(cls) -> list[str]:
        """Return supported logging levels."""
        return ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    @classmethod
    def create_from_project_root(cls, project_root: Path) -> r[FlextMeltanoSettings]:
        """Create settings from a project root path."""
        try:
            return r[FlextMeltanoSettings].ok(
                FlextMeltanoSettings(project_root=project_root)
            )
        except ValueError as error:
            return r[FlextMeltanoSettings].fail(str(error))

    @classmethod
    def create_for_environment(cls, env_type: str) -> FlextMeltanoSettings:
        """Create settings for a named runtime environment."""
        normalized = env_type.strip().lower()
        if normalized not in {"development", "testing", "production"}:
            msg = "Environment must be one of: development, testing, production"
            raise ValueError(msg)
        return cls(environment=normalized)


__all__ = ["FlextMeltanoSettings"]
