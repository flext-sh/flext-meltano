"""FLEXT Meltano Models - Modern Python 3.13 + flext-core patterns.

REFACTORED: Uses flext-core DomainValueObject and types.
Zero tolerance for duplication.

Pydantic models for representing the structure of a meltano.yml file.
These models provide strong typing and validation for the complex, nested
data within a Meltano project configuration.
"""

from __future__ import annotations

from typing import Any, ClassVar

from flext_core.domain.pydantic_base import DomainValueObject, Field


class MeltanoPlugin(DomainValueObject):
    """A Meltano plugin definition - REFACTORED to use flext-core patterns."""

    name: str = Field(description="Plugin name")
    namespace: str | None = Field(None, description="Plugin namespace")
    pip_url: str | None = Field(None, description="Python package URL")
    executable: str | None = Field(None, description="Executable command")
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Plugin configuration",
    )
    settings: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Plugin settings",
    )
    variant: str | None = Field(None, description="Plugin variant")
    docs: str | None = Field(None, description="Documentation URL")
    description: str | None = Field(None, description="Plugin description")


class MeltanoPlugins(DomainValueObject):
    """All plugins in a Meltano project organized by type - REFACTORED."""

    extractors: list[MeltanoPlugin] = Field(
        default_factory=list,
        description="Extractor plugins",
    )
    loaders: list[MeltanoPlugin] = Field(
        default_factory=list,
        description="Loader plugins",
    )
    transformers: list[MeltanoPlugin] = Field(
        default_factory=list,
        description="Transformer plugins",
    )
    files: list[MeltanoPlugin] = Field(default_factory=list, description="File plugins")
    utilities: list[MeltanoPlugin] = Field(
        default_factory=list,
        description="Utility plugins",
    )
    orchestrators: list[MeltanoPlugin] = Field(
        default_factory=list,
        description="Orchestrator plugins",
    )


class MeltanoJob(DomainValueObject):
    """A Meltano job definition for multi-step pipeline execution - REFACTORED."""

    job_name: str = Field(description="Job name")
    tasks: list[str] = Field(description="List of tasks to execute")
    description: str | None = Field(None, description="Job description")
    env: dict[str, Any] = Field(
        default_factory=dict,
        description="Environment variables",
    )


class MeltanoSchedule(DomainValueObject):
    """A Meltano schedule definition for automated execution - REFACTORED."""

    name: str = Field(description="Schedule name")
    job: str = Field(description="Job to execute")
    cron_interval: str = Field(description="Cron schedule expression")
    start_date: str | None = Field(None, description="Schedule start date")
    timezone: str = Field("UTC", description="Schedule timezone")
    enabled: bool = Field(True, description="Whether schedule is enabled")


class MeltanoEnvironment(DomainValueObject):
    """A Meltano environment definition for multi-stage deployment - REFACTORED."""

    name: str = Field(description="Environment name")
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Environment configuration",
    )
    env: dict[str, Any] = Field(
        default_factory=dict,
        description="Environment variables",
    )


class MeltanoProjectConfig(DomainValueObject):
    """The complete configuration of a meltano.yml file - REFACTORED to use flext-core.

    This model represents the entire structure of a meltano.yml configuration file.
    """

    version: int = Field(description="Meltano file version")
    send_anonymous_usage_stats: bool = Field(
        False,
        alias="send_anonymous_usage_stats",
        description="Send anonymous usage statistics",
    )
    project_id: str = Field(alias="project_id", description="Unique project identifier")
    plugins: MeltanoPlugins = Field(
        default_factory=MeltanoPlugins,
        description="Project plugins",
    )
    schedules: list[MeltanoSchedule] = Field(
        default_factory=list,
        description="Scheduled jobs",
    )
    jobs: list[MeltanoJob] = Field(default_factory=list, description="Job definitions")
    environments: list[MeltanoEnvironment] = Field(
        default_factory=list,
        description="Environment configurations",
    )
    default_environment: str | None = Field(
        None,
        description="Default environment name",
    )
    project_root: str | None = Field(None, description="Project root directory")

    model_config: ClassVar[dict[str, Any]] = {
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
