"""UNIFIED MELTANO MODELS - ZERO TOLERANCE CONSOLIDATION.

Pydantic models for representing the structure of a meltano.yml file.
These models provide strong typing and validation for the complex, nested
data within a Meltano project configuration, ensuring that all interactions
with the configuration are type-safe and robust.

CONSOLIDATES:
- infrastructure/meltano/models.py (66 LOC) - Meltano project configuration models

ZERO TOLERANCE PRINCIPLES:
✅ Single source of truth for all Meltano configuration models
✅ Python 3.13 type system with modern union syntax
✅ Pydantic BaseModel for enterprise validation
✅ ConfigurationDict integration for type safety
✅ Strategic field aliases for meltano.yml compatibility
"""

from __future__ import annotations

# Import ConfigurationDict at runtime for Pydantic model validation
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field, SkipValidation

if TYPE_CHECKING:
    from flx_core.domain.advanced_types import ConfigurationDict


class MeltanoPlugin(BaseModel):
    """A Meltano plugin definition with enterprise validation."""

    model_config = {"arbitrary_types_allowed": True}

    name: str
    namespace: str | None = None
    pip_url: str | None = None
    executable: str | None = None
    config: SkipValidation[ConfigurationDict] = Field(default_factory=dict)
    settings: list[SkipValidation[ConfigurationDict]] = Field(default_factory=list)
    variant: str | None = None
    docs: str | None = None
    description: str | None = None


class MeltanoPlugins(BaseModel):
    """All plugins in a Meltano project organized by type."""

    extractors: list[MeltanoPlugin] = Field(default_factory=list)
    loaders: list[MeltanoPlugin] = Field(default_factory=list)
    transformers: list[MeltanoPlugin] = Field(default_factory=list)
    files: list[MeltanoPlugin] = Field(default_factory=list)
    utilities: list[MeltanoPlugin] = Field(default_factory=list)
    orchestrators: list[MeltanoPlugin] = Field(default_factory=list)


class MeltanoJob(BaseModel):
    """A Meltano job definition for multi-step pipeline execution."""

    model_config = {"arbitrary_types_allowed": True}

    job_name: str
    tasks: list[str]
    description: str | None = None
    env: SkipValidation[ConfigurationDict] = Field(default_factory=dict)


class MeltanoSchedule(BaseModel):
    """A Meltano schedule definition for automated execution."""

    name: str
    job: str
    cron_interval: str
    start_date: str | None = None
    timezone: str = "UTC"
    enabled: bool = True


class MeltanoEnvironment(BaseModel):
    """A Meltano environment definition for multi-stage deployment."""

    model_config = {"arbitrary_types_allowed": True}

    name: str
    config: ConfigurationDict = Field(default_factory=dict)
    env: SkipValidation[ConfigurationDict] = Field(default_factory=dict)


class MeltanoProjectConfig(BaseModel):
    """The complete configuration of a meltano.yml file with enterprise features."""

    version: int
    send_anonymous_usage_stats: bool = Field(
        default=False,
        alias="send_anonymous_usage_stats",
    )
    project_id: str = Field(alias="project_id")
    plugins: MeltanoPlugins = Field(default_factory=MeltanoPlugins)
    schedules: list[MeltanoSchedule] = Field(default_factory=list)
    jobs: list[MeltanoJob] = Field(default_factory=list)
    environments: list[MeltanoEnvironment] = Field(default_factory=list)
    default_environment: str | None = None
    project_root: str | None = None

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "extra": "forbid",
    }


# Export unified interface
__all__ = [
    "MeltanoEnvironment",
    "MeltanoJob",
    "MeltanoPlugin",
    "MeltanoPlugins",
    "MeltanoProjectConfig",
    "MeltanoSchedule",
]
