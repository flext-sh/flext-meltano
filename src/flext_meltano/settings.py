"""FLEXT Meltano configuration model and helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, ClassVar

from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings, r
from flext_meltano import c, t, u


@FlextSettings.auto_register("meltano")
class FlextMeltanoSettings(FlextSettings):
    """Runtime settings for Meltano orchestration services."""

    model_config: ClassVar[SettingsConfigDict] = SettingsConfigDict(extra="ignore")

    MELTANO_VERSION: ClassVar[str] = c.Meltano.Versions.MELTANO_REQUIRED
    SINGER_SDK_VERSION: ClassVar[str] = c.Meltano.Versions.SINGER_SDK_REQUIRED
    DBT_VERSION: ClassVar[str] = c.Meltano.Versions.DBT_REQUIRED
    PROJECT_FILE: ClassVar[str] = c.Meltano.Paths.MELTANO_PROJECT_FILE
    STATE_DIR: ClassVar[str] = c.Meltano.Paths.STATE_DIR
    VENV_DIR: ClassVar[str] = c.Meltano.Paths.VENV_DIR
    MELTANO_PROJECT_ROOT_ENV: ClassVar[str] = (
        c.Meltano.EnvironmentVariables.PROJECT_ROOT
    )
    MELTANO_ENVIRONMENT_ENV: ClassVar[str] = c.Meltano.EnvironmentVariables.ENVIRONMENT
    MELTANO_LOG_LEVEL_ENV: ClassVar[str] = c.Meltano.EnvironmentVariables.LOG_LEVEL

    project_root: Annotated[
        Path,
        Field(default=Path(), validation_alias=MELTANO_PROJECT_ROOT_ENV),
    ]
    config_dir: Annotated[Path, Field(default=Path(".meltano"))]
    logs_dir: Annotated[Path, Field(default=Path("logs"))]
    environment: Annotated[
        str,
        Field(default="development", validation_alias=MELTANO_ENVIRONMENT_ENV),
    ]
    log_level: Annotated[
        c.LogLevel,
        Field(default=c.LogLevel.INFO, validation_alias=MELTANO_LOG_LEVEL_ENV),
    ]
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
        aliases = {
            "dev": c.Meltano.Enums.Environment.DEVELOPMENT,
            "test": c.Meltano.Enums.Environment.TESTING,
            "prod": c.Meltano.Enums.Environment.PRODUCTION,
        }
        normalized = aliases.get(normalized, normalized)
        if normalized not in {
            c.Meltano.Enums.Environment.DEVELOPMENT,
            c.Meltano.Enums.Environment.TESTING,
            c.Meltano.Enums.Environment.PRODUCTION,
        }:
            msg = "Environment must be one of: development, testing, production"
            raise ValueError(msg)
        return str(normalized)

    @field_validator("log_level")
    @classmethod
    def _validate_log_level(cls, value: c.LogLevel | str) -> c.LogLevel:
        normalized = str(value).strip().upper()
        if normalized not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            msg = "Invalid log_level"
            raise ValueError(msg)
        return c.LogLevel(normalized)

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
        return (self.project_root / Path(self.VENV_DIR)).resolve()

    def validate_project_structure(self) -> r[bool]:
        """Validate required project structure artifacts."""
        return u.Meltano.validate_project_structure(self.project_root)

    def get_environment_variables(self) -> t.StrMapping:
        """Build runtime environment variables for Meltano commands."""
        return {
            self.MELTANO_PROJECT_ROOT_ENV: str(self.project_root),
            self.MELTANO_ENVIRONMENT_ENV: self.environment,
            self.MELTANO_LOG_LEVEL_ENV: self.log_level.value,
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
    def get_supported_plugin_types(cls) -> t.StrSequence:
        """Return supported Meltano plugin categories."""
        return [
            c.Meltano.Enums.PluginType.EXTRACTORS,
            c.Meltano.Enums.PluginType.LOADERS,
            c.Meltano.Enums.PluginType.TRANSFORMS,
        ]

    @classmethod
    def get_supported_environments(cls) -> t.StrSequence:
        """Return list of valid deployment environment names."""
        return [
            c.Meltano.Enums.Environment.DEVELOPMENT,
            c.Meltano.Enums.Environment.TESTING,
            c.Meltano.Enums.Environment.PRODUCTION,
        ]

    @classmethod
    def get_supported_log_levels(cls) -> t.StrSequence:
        """Return supported logging levels."""
        return ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    @classmethod
    def create_from_project_root(cls, project_root: Path) -> r[FlextMeltanoSettings]:
        """Create settings from a project root path."""
        try:
            return r[FlextMeltanoSettings].ok(
                FlextMeltanoSettings(project_root=project_root),
            )
        except ValueError as error:
            return r[FlextMeltanoSettings].fail(str(error))

    @classmethod
    def create_for_environment(cls, env_type: str) -> FlextMeltanoSettings:
        """Create settings for a named runtime environment."""
        normalized = env_type.strip().lower()
        aliases = {
            "dev": c.Meltano.Enums.Environment.DEVELOPMENT,
            "test": c.Meltano.Enums.Environment.TESTING,
            "prod": c.Meltano.Enums.Environment.PRODUCTION,
        }
        normalized = aliases.get(normalized, normalized)
        if normalized not in {
            c.Meltano.Enums.Environment.DEVELOPMENT,
            c.Meltano.Enums.Environment.TESTING,
            c.Meltano.Enums.Environment.PRODUCTION,
        }:
            msg = "Environment must be one of: development, testing, production"
            raise ValueError(msg)
        return cls(environment=str(normalized))


__all__ = ["FlextMeltanoSettings"]
