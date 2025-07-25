"""FLEXT Meltano settings and configuration.

Settings model for configuring FLEXT Meltano projects.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pathlib import Path
    from typing import Any

from pydantic import BaseModel, Field


class FlextMeltanoProjectConfig(BaseModel):
    """Project configuration for FLEXT Meltano."""

    project_root: Path = Field(description="Root directory of the project")
    default_environment: str = Field(default="dev", description="Default environment")


class FlextMeltanoSettings(BaseModel):
    """FLEXT Meltano settings configuration."""

    environment: str = Field(default="dev", description="Current environment")
    project: FlextMeltanoProjectConfig | None = Field(default=None, description="Project configuration")

    # Execution settings
    execution: dict[str, Any] = Field(default_factory=dict, description="Execution configuration")
    state: dict[str, Any] = Field(default_factory=dict, description="State configuration")
    debug: bool = Field(default=False, description="Debug mode enabled")

    # Plugin settings
    plugins: dict[str, Any] = Field(default_factory=dict, description="Plugin configuration")
    auto_install: bool = Field(default=True, description="Auto-install plugins")

    # Project settings
    project_name: str = Field(default="flext-meltano", description="Project name")
    project_root: str = Field(default=".", description="Project root directory")
    project_version: str = Field(default="1.0.0", description="Project version")
    default_environment: str = Field(default="dev", description="Default environment")

    # Database settings
    database_uri: str | None = Field(default=None, description="Database connection URI")

    # Job settings
    job_timeout: int = Field(default=3600, description="Job timeout in seconds")
    max_concurrent_jobs: int = Field(default=4, description="Maximum concurrent jobs")

    # State backend settings
    state_backend: str = Field(default="filesystem", description="State backend type")

    # Configuration management
    configure_dependencies: bool = Field(default=True, description="Configure dependencies automatically")
    backup_enabled: bool = Field(default=False, description="Backup enabled")

    def __init__(self, **data: Any) -> None:  # noqa: ANN401
        """Initialize settings with proper project config handling."""
        # Handle case where project_root is passed directly
        if "project_root" in data and "project" not in data:
            project_root = data.pop("project_root")
            environment = data.get("environment", "dev")
            data["project"] = FlextMeltanoProjectConfig(
                project_root=project_root,
                default_environment=environment,
            )
        super().__init__(**data)
