"""FLEXT Meltano settings — namespaced under ``settings.Meltano``.

Strict, dependency-free leaf: stdlib + pydantic + pydantic-settings + the public
``FlextSettings`` base. Universal fields come via MRO; all project fields live in
the ``Meltano`` namespace group with simple scalar types (env-settable).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Annotated

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import SettingsConfigDict

from flext_core import FlextSettings

_ENV_ALIAS: dict[str, str] = {
    "dev": "development",
    "test": "testing",
    "prod": "production",
}
_ENV_ALLOWED: frozenset[str] = frozenset({"development", "testing", "production"})


class FlextMeltanoSettings(FlextSettings):
    """Runtime settings for Meltano orchestration; fields under ``settings.Meltano.*``."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_MELTANO_",
        env_nested_delimiter="__",
        extra="ignore",
    )

    class _Meltano(BaseModel):
        """Namespaced Meltano orchestration settings."""

        project_root: Annotated[
            str,
            Field(
                default="",
                validation_alias="MELTANO_PROJECT_ROOT",
                description="Root directory of the Meltano project",
            ),
        ]
        config_dir: Annotated[
            str,
            Field(default=".meltano", description="Meltano configuration directory"),
        ]
        logs_dir: Annotated[
            str, Field(default="logs", description="Meltano logs directory")
        ]
        environment: Annotated[
            str,
            Field(
                default="development",
                validation_alias="MELTANO_ENVIRONMENT",
                description="Active Meltano runtime environment",
            ),
        ]
        log_level: Annotated[
            str, Field(default="INFO", description="Meltano runtime log level")
        ]
        meltano_version: Annotated[
            str,
            Field(default="3.9.1", description="Required Meltano version"),
        ]
        singer_sdk_version: Annotated[
            str,
            Field(default="0.48.0", description="Required Singer SDK version"),
        ]
        dbt_version: Annotated[
            str,
            Field(default="1.10.5", description="Required dbt version"),
        ]
        pipelines_dir: Annotated[
            str,
            Field(
                default="",
                validation_alias="FLEXT_MELTANO_PIPELINES_DIR",
                description="Root directory for pipeline configurations",
            ),
        ]

        @field_validator("pipelines_dir", mode="before")
        @classmethod
        def _coerce_pipelines_dir(cls, value: str | None) -> str:
            text = value.strip() if value is not None else ""
            if text:
                return str(Path(text).expanduser().resolve())
            return str((Path.cwd() / ".flext-meltano" / "pipelines").resolve())

        @field_validator("project_root", mode="before")
        @classmethod
        def _coerce_project_root(cls, value: str | None) -> str:
            return str(Path(value).resolve()) if value else ""

        @field_validator("config_dir", "logs_dir", mode="before")
        @classmethod
        def _coerce_path(cls, value: str | None) -> str:
            return value or ""

        @field_validator("environment")
        @classmethod
        def _validate_environment(cls, value: str) -> str:
            normalized = value.strip().lower()
            normalized = _ENV_ALIAS.get(normalized, normalized)
            if normalized not in _ENV_ALLOWED:
                msg = "Environment must be one of: development, testing, production"
                raise ValueError(msg)
            return normalized

    if TYPE_CHECKING:
        Meltano: _Meltano
    else:
        Meltano: _Meltano = Field(
            default_factory=_Meltano,
            description="Namespaced Meltano settings.",
        )


settings: FlextMeltanoSettings = FlextMeltanoSettings.fetch_global()
"""Pre-instantiated project settings singleton — ``from flext_meltano import settings``."""

__all__: list[str] = ["FlextMeltanoSettings", "settings"]
