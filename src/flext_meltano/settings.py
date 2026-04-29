"""FLEXT Meltano configuration model and helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated, ClassVar, Self

from flext_cli import r, u

from flext_core import FlextSettings
from flext_meltano import c, m, p, t


@FlextSettings.auto_register("meltano")
class FlextMeltanoSettings(FlextSettings):
    """Runtime settings for Meltano orchestration services."""

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_MELTANO_",
        extra="ignore",
    )

    project_root: Annotated[
        Path,
        u.Field(
            default=Path(),
            validation_alias=c.Meltano.ENV_VAR_PROJECT_ROOT,
            description="Root directory of the Meltano project",
        ),
    ]
    config_dir: Annotated[
        Path,
        u.Field(
            default=Path(c.Meltano.PATH_CONFIG_DIR),
            description="Meltano configuration directory",
        ),
    ]
    logs_dir: Annotated[
        Path,
        u.Field(
            default=Path(c.Meltano.PATH_LOGS_DIR),
            description="Meltano logs directory",
        ),
    ]
    environment: Annotated[
        str,
        u.Field(
            default=c.Meltano.SETTINGS_ENVIRONMENTS[0],
            validation_alias=c.Meltano.ENV_VAR_ENVIRONMENT,
            description="Active Meltano runtime environment",
        ),
    ]
    log_level: Annotated[
        c.LogLevel,
        u.Field(
            default=c.LogLevel.INFO,
            validation_alias=c.Meltano.ENV_VAR_LOG_LEVEL,
            description="Meltano logging level",
        ),
    ] = c.LogLevel.INFO
    meltano_version: Annotated[
        str,
        u.Field(
            default=c.Meltano.VERSION_MELTANO_REQUIRED,
            description="Required Meltano version",
        ),
    ]
    singer_sdk_version: Annotated[
        str,
        u.Field(
            default=c.Meltano.VERSION_SINGER_SDK_REQUIRED,
            description="Required Singer SDK version",
        ),
    ]
    dbt_version: Annotated[
        str,
        u.Field(
            default=c.Meltano.VERSION_DBT_REQUIRED,
            description="Required dbt version",
        ),
    ]
    pipelines_dir: Annotated[
        Path,
        u.Field(
            default=Path(),
            validation_alias=c.Meltano.CLI_DEFAULT_PIPELINES_ROOT_ENV,
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
        normalized = str(c.Meltano.ENVIRONMENT_ALIASES.get(normalized, normalized))
        if normalized not in c.Meltano.SETTINGS_ENVIRONMENTS:
            msg = "Environment must be one of: development, testing, production"
            raise ValueError(msg)
        return normalized

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
        return r[Path].ok(self.project_root / c.Meltano.PATH_MELTANO_PROJECT_FILE)

    def get_absolute_config_dir(self) -> p.Result[Path]:
        """Return absolute Meltano settings directory path."""
        return r[Path].ok((self.project_root / self.config_dir).resolve())

    def get_absolute_logs_dir(self) -> p.Result[Path]:
        """Return absolute logs directory path."""
        return r[Path].ok((self.project_root / self.logs_dir).resolve())

    def get_absolute_venv_dir(self) -> Path:
        """Return absolute Meltano virtualenv directory."""
        return (self.project_root / Path(c.Meltano.PATH_VENV_DIR)).resolve()

    def validate_project_structure(self) -> p.Result[bool]:
        """Validate required project structure artifacts."""
        if not self.project_root.exists() or not self.project_root.is_dir():
            return r[bool].fail(f"Project path {self.project_root} does not exist")
        if not (self.project_root / c.Meltano.PATH_MELTANO_PROJECT_FILE).exists():
            return r[bool].fail(
                "Project path "
                f"{self.project_root} does not contain "
                f"{c.Meltano.PATH_MELTANO_PROJECT_FILE}"
            )
        return r[bool].ok(value=True)

    def get_environment_variables(self) -> t.StrMapping:
        """Build runtime environment variables for Meltano commands."""
        return {
            c.Meltano.ENV_VAR_PROJECT_ROOT: str(self.project_root),
            c.Meltano.ENV_VAR_ENVIRONMENT: self.environment,
            c.Meltano.ENV_VAR_LOG_LEVEL: self.log_level.value,
        }

    @classmethod
    def fetch_version(cls) -> str:
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
        return list(c.Meltano.SUPPORTED_PLUGIN_TYPES)

    @classmethod
    def get_supported_environments(cls) -> t.StrSequence:
        """Return list of valid deployment environment names."""
        return list(c.Meltano.SETTINGS_ENVIRONMENTS)

    @classmethod
    def get_supported_log_levels(cls) -> t.StrSequence:
        """Return supported logging levels."""
        return [level.value for level in c.Meltano.SUPPORTED_LOG_LEVELS]

    @classmethod
    def create_from_project_root(cls, project_root: Path) -> p.Result[Self]:
        """Create settings from a project root path."""
        try:
            instance: Self = cls(project_root=Path(project_root))
            ok_result: p.Result[Self] = r.ok(instance)
            return ok_result
        except ValueError as error:
            failure: p.Result[Self] = r[Self].fail(str(error))
            return failure

    @classmethod
    def create_for_environment(cls, env_type: t.Meltano.EnvironmentInput) -> Self:
        """Create settings for a named runtime environment."""
        normalized = env_type.strip().lower()
        normalized = str(c.Meltano.ENVIRONMENT_ALIASES.get(normalized, normalized))
        if normalized not in c.Meltano.SETTINGS_ENVIRONMENTS:
            msg = "Environment must be one of: development, testing, production"
            raise ValueError(msg)
        return cls(environment=normalized)


__all__: list[str] = ["FlextMeltanoSettings"]
