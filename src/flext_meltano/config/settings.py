"""FlextMeltano Platform Settings.

Unified configuration for entire Meltano ecosystem integration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from flext_core.constants import FlextConstants
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings


class FlextMeltanoMeltanoConfig(BaseModel):
    """Meltano-specific configuration."""

    project_root: Path = Field(
        default=Path.cwd(),
        description="Root directory for Meltano projects",
    )
    config_file: str = Field(
        default="meltano.yml",
        description="Meltano configuration file name",
    )
    environment: str = Field(
        default=FlextConstants.ENV_DEVELOPMENT.value,
        description="Default Meltano environment",
    )
    system_database_uri: str = Field(
        default="sqlite:///meltano.db",
        description="Meltano system database URI",
    )


class FlextMeltanoSingerConfig(BaseModel):
    """Singer SDK configuration."""

    tap_timeout: int = Field(
        default=3600,
        description="Tap execution timeout in seconds",
    )
    target_timeout: int = Field(
        default=3600,
        description="Target execution timeout in seconds",
    )
    batch_size: int = Field(
        default=10000,
        description="Default batch size for Singer streams",
    )
    buffer_size: int = Field(
        default=10485760,  # 10MB
        description="Stream buffer size in bytes",
    )


class FlextMeltanoDbtConfig(BaseModel):
    """dbt integration configuration."""

    project_dir: Path = Field(
        default=Path("transform"),
        description="dbt project directory",
    )
    profiles_dir: Path = Field(
        default=Path.home() / ".dbt",
        description="dbt profiles directory",
    )
    target: str = Field(
        default="dev",
        description="Default dbt target",
    )
    threads: int = Field(
        default=4,
        description="Number of threads for dbt execution",
    )


class FlextMeltanoEdkConfig(BaseModel):
    """Meltano EDK configuration."""

    extensions_dir: Path = Field(
        default=Path(".meltano/extensions"),
        description="Extensions installation directory",
    )
    python_version: str = Field(
        default="3.13",
        description="Python version for extensions",
    )
    auto_install: bool = Field(
        default=True,
        description="Automatically install missing extensions",
    )


class FlextMeltanoRuntimeConfig(BaseModel):
    """FlexCore Go runtime configuration."""

    host: str = Field(
        default="localhost",
        description="FlexCore runtime host",
    )
    port: int = Field(
        default=8080,
        description="FlexCore runtime port",
    )
    grpc_port: int = Field(
        default=50051,
        description="FlexCore gRPC port",
    )
    timeout: int = Field(
        default=30,
        description="Runtime connection timeout",
    )
    enabled: bool = Field(
        default=True,
        description="Enable FlexCore Go runtime integration",
    )


class FlextMeltanoObservabilityConfig(BaseModel):
    """Observability and monitoring configuration."""

    logging_level: str = Field(
        default=FlextConstants.LOG_INFO.value,
        description="Default logging level",
    )
    metrics_enabled: bool = Field(
        default=True,
        description="Enable metrics collection",
    )
    tracing_enabled: bool = Field(
        default=True,
        description="Enable distributed tracing",
    )
    prometheus_port: int = Field(
        default=9090,
        description="Prometheus metrics port",
    )


class FlextMeltanoSettings(BaseSettings):
    """Unified FLEXT Meltano platform settings."""

    # Core platform settings
    platform_name: str = Field(
        default="flext-meltano",
        description="Platform identifier",
    )
    version: str = Field(
        default="0.7.0",
        description="Platform version",
    )
    environment: str = Field(
        default=FlextConstants.ENV_DEVELOPMENT.value,
        description="Platform environment",
    )

    # Component configurations
    meltano: FlextMeltanoMeltanoConfig = Field(
        default_factory=FlextMeltanoMeltanoConfig,
        description="Meltano configuration",
    )
    singer: FlextMeltanoSingerConfig = Field(
        default_factory=FlextMeltanoSingerConfig,
        description="Singer SDK configuration",
    )
    dbt: FlextMeltanoDbtConfig = Field(
        default_factory=FlextMeltanoDbtConfig,
        description="dbt configuration",
    )
    edk: FlextMeltanoEdkConfig = Field(
        default_factory=FlextMeltanoEdkConfig,
        description="Meltano EDK configuration",
    )
    runtime: FlextMeltanoRuntimeConfig = Field(
        default_factory=FlextMeltanoRuntimeConfig,
        description="FlexCore runtime configuration",
    )
    observability: FlextMeltanoObservabilityConfig = Field(
        default_factory=FlextMeltanoObservabilityConfig,
        description="Observability configuration",
    )

    # Additional platform settings
    debug: bool = Field(
        default=False,
        description="Enable debug mode",
    )
    max_workers: int = Field(
        default=4,
        description="Maximum number of worker processes",
    )

    class Config:
        """Pydantic model configuration."""

        env_prefix = "FLEXT_MELTANO_"
        env_nested_delimiter = "__"
        case_sensitive = False
        validate_assignment = True
        extra = "forbid"

    def to_dict(self) -> dict[str, Any]:
        """Convert settings to dictionary.

        Returns:
            Dictionary representation of settings

        """
        return self.model_dump()

    @classmethod
    def from_file(cls, config_file: Path) -> FlextMeltanoSettings:
        """Load settings from configuration file.

        Args:
            config_file: Path to configuration file

        Returns:
            Loaded settings instance

        """
        import json
        import tomllib

        import yaml

        if not config_file.exists():
            msg = f"Configuration file not found: {config_file}"
            raise FileNotFoundError(msg)

        content = config_file.read_text(encoding="utf-8")

        if config_file.suffix == ".json":
            data = json.loads(content)
        elif config_file.suffix in {".yaml", ".yml"}:
            data = yaml.safe_load(content)
        elif config_file.suffix == ".toml":
            data = tomllib.loads(content)
        else:
            msg = f"Unsupported config file format: {config_file.suffix}"
            raise ValueError(msg)

        return cls(**data)

    def save_to_file(self, config_file: Path) -> None:
        """Save settings to configuration file.

        Args:
            config_file: Path to save configuration file

        """
        import json
        import tomllib

        import yaml

        data = self.to_dict()

        if config_file.suffix == ".json":
            content = json.dumps(data, indent=2, default=str)
        elif config_file.suffix in {".yaml", ".yml"}:
            content = yaml.dump(data, default_flow_style=False)
        elif config_file.suffix == ".toml":
            import tomli_w
            content = tomli_w.dumps(data)
        else:
            msg = f"Unsupported config file format: {config_file.suffix}"
            raise ValueError(msg)

        config_file.write_text(content, encoding="utf-8")
