"""FLEXT Meltano configuration model and helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, ClassVar, Self

from flext_core import FlextSettings, r
from flext_meltano import c, t, u


@FlextSettings.auto_register("meltano")
class FlextMeltanoSettings(FlextSettings):
    """Runtime settings for Meltano orchestration services."""

    model_config: ClassVar[c.SettingsConfigDict] = c.SettingsConfigDict(
        env_prefix="FLEXT_MELTANO_",
        extra="ignore",
    )

    MELTANO_VERSION: ClassVar[str] = c.Meltano.VERSION_MELTANO_REQUIRED
    SINGER_SDK_VERSION: ClassVar[str] = c.Meltano.VERSION_SINGER_SDK_REQUIRED
    DBT_VERSION: ClassVar[str] = c.Meltano.VERSION_DBT_REQUIRED
    PROJECT_FILE: ClassVar[str] = c.Meltano.PATH_MELTANO_PROJECT_FILE
    STATE_DIR: ClassVar[str] = c.Meltano.PATH_STATE_DIR
    VENV_DIR: ClassVar[str] = c.Meltano.PATH_VENV_DIR
    MELTANO_PROJECT_ROOT_ENV: ClassVar[str] = c.Meltano.ENV_VAR_PROJECT_ROOT
    MELTANO_ENVIRONMENT_ENV: ClassVar[str] = c.Meltano.ENV_VAR_ENVIRONMENT
    MELTANO_LOG_LEVEL_ENV: ClassVar[str] = c.Meltano.ENV_VAR_LOG_LEVEL
    PIPELINES_DIR_ENV: ClassVar[str] = c.Meltano.CLI_DEFAULT_PIPELINES_ROOT_ENV

    project_root: Annotated[
        Path,
        u.Field(
            default=Path(),
            validation_alias=MELTANO_PROJECT_ROOT_ENV,
            description="Root directory of the Meltano project",
        ),
    ]
    config_dir: Annotated[
        Path,
        u.Field(
            default=Path(".meltano"), description="Meltano configuration directory"
        ),
    ]
    logs_dir: Annotated[
        Path, u.Field(default=Path("logs"), description="Meltano logs directory")
    ]
    environment: Annotated[
        str,
        u.Field(
            default="development",
            validation_alias=MELTANO_ENVIRONMENT_ENV,
            description="Active Meltano runtime environment",
        ),
    ]
    log_level: Annotated[
        c.LogLevel,
        u.Field(
            default=c.LogLevel.INFO,
            validation_alias=MELTANO_LOG_LEVEL_ENV,
            description="Meltano logging level",
        ),
    ]
    meltano_version: Annotated[
        str,
        u.Field(default=MELTANO_VERSION, description="Required Meltano version"),
    ]
    singer_sdk_version: Annotated[
        str,
        u.Field(default=SINGER_SDK_VERSION, description="Required Singer SDK version"),
    ]
    dbt_version: Annotated[
        str, u.Field(default=DBT_VERSION, description="Required dbt version")
    ]
    pipelines_dir: Annotated[
        Path,
        u.Field(
            default=Path(),
            validation_alias=PIPELINES_DIR_ENV,
            description="Root directory for pipeline configurations",
        ),
    ]

    @u.field_validator("pipelines_dir", mode="before")
    @classmethod
    def _coerce_pipelines_dir(cls, value: t.Scalar) -> Path:
        text = str(value).strip()
        if text:
            return Path(text).expanduser().resolve()
        return (Path.cwd() / ".flext-meltano" / "pipelines").resolve()

    @u.field_validator("project_root", mode="before")
    @classmethod
    def _coerce_project_root(cls, value: t.Scalar) -> Path:
        return Path(str(value)).resolve()

    @u.field_validator("config_dir", "logs_dir", mode="before")
    @classmethod
    def _coerce_path(cls, value: t.Scalar) -> Path:
        return Path(str(value))

    @u.field_validator("environment")
    @classmethod
    def _validate_environment(cls, value: str) -> str:
        normalized = value.strip().lower()
        aliases = {
            "dev": c.Meltano.Environment.DEVELOPMENT,
            "test": c.Meltano.Environment.TESTING,
            "prod": c.Meltano.Environment.PRODUCTION,
        }
        normalized = aliases.get(normalized, normalized)
        if normalized not in {
            c.Meltano.Environment.DEVELOPMENT,
            c.Meltano.Environment.TESTING,
            c.Meltano.Environment.PRODUCTION,
        }:
            msg = "Environment must be one of: development, testing, production"
            raise ValueError(msg)
        return str(normalized)

    @u.field_validator("log_level")
    @classmethod
    def _validate_log_level(cls, value: c.LogLevel | str) -> c.LogLevel:
        normalized = str(value).strip().upper()
        if normalized not in {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}:
            msg = "Invalid log_level"
            raise ValueError(msg)
        return c.LogLevel(normalized)

    def get_project_file(self) -> p.Result[Path]:
        """Return the canonical pipeline file path."""
        return r[Path].ok(self.project_root / self.PROJECT_FILE)

    def get_absolute_config_dir(self) -> p.Result[Path]:
        """Return absolute Meltano settings directory path."""
        return r[Path].ok((self.project_root / self.config_dir).resolve())

    def get_absolute_logs_dir(self) -> p.Result[Path]:
        """Return absolute logs directory path."""
        return r[Path].ok((self.project_root / self.logs_dir).resolve())

    def get_absolute_venv_dir(self) -> Path:
        """Return absolute Meltano virtualenv directory."""
        return (self.project_root / Path(self.VENV_DIR)).resolve()

    def validate_project_structure(self) -> p.Result[bool]:
        """Validate required project structure artifacts."""
        if not self.project_root.exists() or not self.project_root.is_dir():
            return r[bool].fail(f"Project path {self.project_root} does not exist")
        if not (self.project_root / self.PROJECT_FILE).exists():
            return r[bool].fail(
                f"Project path {self.project_root} does not contain {self.PROJECT_FILE}"
            )
        return r[bool].ok(value=True)

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
        return c.Meltano.FLEXT_MELTANO_VERSION

    @classmethod
    def get_name(cls) -> str:
        """Return package distribution name."""
        return c.Meltano.PROJECT_PREFIX

    @classmethod
    def get_default_timeout(cls) -> int:
        """Return default command timeout in seconds."""
        return c.Meltano.NETWORK_DEFAULT_TIMEOUT

    @classmethod
    def get_default_batch_size(cls) -> int:
        """Return default batch size for operations."""
        return c.Meltano.BATCH_DEFAULT_DEFAULT_BATCH_SIZE

    @classmethod
    def get_supported_plugin_types(cls) -> t.StrSequence:
        """Return supported Meltano plugin categories."""
        return [
            c.Meltano.PluginType.EXTRACTORS,
            c.Meltano.PluginType.LOADERS,
            c.Meltano.PluginType.TRANSFORMS,
        ]

    @classmethod
    def get_supported_environments(cls) -> t.StrSequence:
        """Return list of valid deployment environment names."""
        return [
            c.Meltano.Environment.DEVELOPMENT,
            c.Meltano.Environment.TESTING,
            c.Meltano.Environment.PRODUCTION,
        ]

    @classmethod
    def get_supported_log_levels(cls) -> t.StrSequence:
        """Return supported logging levels."""
        return ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    @classmethod
    def create_from_project_root(cls, project_root: Path) -> p.Result[Self]:
        """Create settings from a project root path."""
        try:
            instance: Self = cls(project_root=project_root)
            success: r[Self] = r[Self](value=instance, success=True)
            return success
        except ValueError as error:
            failure: r[Self] = r[Self].fail(str(error))
            return failure

    @classmethod
    def create_for_environment(cls, env_type: str) -> Self:
        """Create settings for a named runtime environment."""
        normalized = env_type.strip().lower()
        aliases = {
            "dev": c.Meltano.Environment.DEVELOPMENT,
            "test": c.Meltano.Environment.TESTING,
            "prod": c.Meltano.Environment.PRODUCTION,
        }
        normalized = aliases.get(normalized, normalized)
        if normalized not in {
            c.Meltano.Environment.DEVELOPMENT,
            c.Meltano.Environment.TESTING,
            c.Meltano.Environment.PRODUCTION,
        }:
            msg = "Environment must be one of: development, testing, production"
            raise ValueError(msg)
        return cls(environment=str(normalized))


__all__: list[str] = ["FlextMeltanoSettings"]
