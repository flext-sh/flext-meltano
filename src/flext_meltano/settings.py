"""FLEXT Meltano configuration model and helpers."""

from __future__ import annotations

from pathlib import Path

from flext_core import FlextSettings, c, r, t
from pydantic import Field, field_validator


class FlextMeltanoSettings(FlextSettings):
    """Runtime settings for Meltano orchestration services."""

    project_root: t.Scalar = Field(default=".")
    config_dir: str = Field(default=".meltano")
    logs_dir: str = Field(default="logs")
    environment: str = Field(default="development")
    log_level: c.Settings.LogLevel = Field(default=c.Settings.LogLevel.INFO)
    meltano_version: str = Field(default="3.9.1")
    singer_sdk_version: str = Field(default="0.48.0")
    dbt_version: str = Field(default="1.10.5")

    @field_validator("project_root", mode="before")
    @classmethod
    def _coerce_project_root(cls, value: t.Scalar) -> str:
        return str(Path(str(value)).resolve())

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
        return r[Path].ok(Path(str(self.project_root)) / "pipeline.yml")

    def get_absolute_config_dir(self) -> r[Path]:
        """Return absolute Meltano config directory path."""
        return r[Path].ok((Path(str(self.project_root)) / self.config_dir).resolve())

    def get_absolute_logs_dir(self) -> r[Path]:
        """Return absolute logs directory path."""
        return r[Path].ok((Path(str(self.project_root)) / self.logs_dir).resolve())

    def get_absolute_venv_dir(self) -> Path:
        """Return absolute Meltano virtualenv directory."""
        return (Path(str(self.project_root)) / ".meltano" / "python").resolve()

    def validate_project_structure(self) -> r[bool]:
        """Validate required project structure artifacts."""
        pipeline_file = Path(str(self.project_root)) / "pipeline.yml"
        if not pipeline_file.exists():
            return r[bool].fail(f"pipeline.yml not found in {self.project_root}")
        return r[bool].ok(True)

    def get_environment_variables(self) -> dict[str, str]:
        """Build runtime environment variables for Meltano commands."""
        return {
            "MELTANO_PROJECT_ROOT": str(self.project_root),
            "MELTANO_ENVIRONMENT": self.environment,
            "MELTANO_LOG_LEVEL": self.log_level,
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
    def get_supported_log_levels(cls) -> list[str]:
        """Return supported logging levels."""
        return ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    @classmethod
    def create_from_project_root(cls, project_root: Path) -> r[FlextMeltanoSettings]:
        """Create settings from a project root path."""
        try:
            return r[FlextMeltanoSettings].ok(cls(project_root=str(project_root)))
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
