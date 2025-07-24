"""FlextMeltano Project Models - Domain Entities.

Project domain models following Clean Architecture and DDD patterns.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any
from uuid import uuid4

from flext_core import FlextResult
from pydantic import BaseModel, Field, model_validator

from flext_meltano.constants import (
    FlextMeltanoConstants,
    FlextMeltanoEnvironmentType,
)

if TYPE_CHECKING:
    from pathlib import Path


def _get_current_timestamp() -> str:
    """Get current timestamp in ISO format.

    Returns:
        Current timestamp in ISO format with UTC timezone

    """
    return datetime.now(UTC).isoformat()


class FlextMeltanoProject(BaseModel):
    """Meltano project domain entity.

    Represents a Meltano project with business rules and validation.
    """

    # Core identification
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique project identifier",
    )
    name: str = Field(
        ...,
        description="Project name",
        min_length=1,
        max_length=100,
    )

    # File system paths
    directory: Path = Field(
        ...,
        description="Project root directory",
    )
    config_path: Path = Field(
        ...,
        description="Path to meltano.yml configuration file",
    )

    # Project metadata
    description: str | None = Field(
        default=None,
        description="Optional project description",
        max_length=500,
    )
    version: str = Field(
        default="1.0.0",
        description="Project version",
    )

    # Environment configuration
    current_environment: FlextMeltanoEnvironmentType = Field(
        default=FlextMeltanoConstants.DEFAULT_ENVIRONMENT,
        description="Current active environment",
    )
    available_environments: list[FlextMeltanoEnvironmentType] = Field(
        default_factory=lambda: [FlextMeltanoConstants.DEFAULT_ENVIRONMENT],
        description="Available environments for this project",
    )

    # Project state
    is_active: bool = Field(
        default=False,
        description="Whether project is currently active",
    )
    is_initialized: bool = Field(
        default=False,
        description="Whether project has been initialized",
    )

    # Timestamps
    created_at: str = Field(
        default_factory=lambda: _get_current_timestamp(),
        description="Project creation timestamp",
    )
    updated_at: str = Field(
        default_factory=lambda: _get_current_timestamp(),
        description="Last update timestamp",
    )

    class Config:
        """Pydantic model configuration."""

        frozen = False  # Allow updates for state changes
        validate_assignment = True
        extra = "forbid"
        use_enum_values = True

    @model_validator(mode="after")
    def validate_project_structure(self) -> FlextMeltanoProject:
        """Validate project structure and paths.

        Returns:
            Validated project instance

        Raises:
            ValueError: If validation fails

        """
        # Validate project name
        if not FlextMeltanoConstants.is_valid_plugin_name(self.name):
            msg = f"Invalid project name: {self.name}"
            raise ValueError(msg)

        # Validate config path points to meltano.yml
        if self.config_path.name != "meltano.yml":
            msg = "Config path must point to meltano.yml file"
            raise ValueError(msg)

        # Ensure config path is within project directory
        try:
            self.config_path.resolve().relative_to(self.directory.resolve())
        except ValueError as e:
            msg = "Config path must be within project directory"
            raise ValueError(msg) from e

        return self

    def activate(self) -> FlextResult[None]:
        """Activate this project.

        Business rule: Only initialized projects can be activated.

        Returns:
            FlextResult indicating success or failure

        """
        if not self.is_initialized:
            return FlextResult.fail("Cannot activate uninitialized project")

        self.is_active = True
        self.updated_at = _get_current_timestamp()

        return FlextResult.ok(None)

    def deactivate(self) -> FlextResult[None]:
        """Deactivate this project.

        Returns:
            FlextResult indicating success or failure

        """
        self.is_active = False
        self.updated_at = _get_current_timestamp()

        return FlextResult.ok(None)

    def change_environment(
        self,
        environment: FlextMeltanoEnvironmentType,
    ) -> FlextResult[None]:
        """Change current environment.

        Business rule: Environment must be in available environments.

        Args:
            environment: New environment to activate

        Returns:
            FlextResult indicating success or failure

        """
        if environment not in self.available_environments:
            return FlextResult.fail(
                f"Environment '{environment}' not available for project",
            )

        self.current_environment = environment
        self.updated_at = _get_current_timestamp()

        return FlextResult.ok(None)

    def add_environment(
        self,
        environment: FlextMeltanoEnvironmentType,
    ) -> FlextResult[None]:
        """Add new environment to project.

        Args:
            environment: Environment to add

        Returns:
            FlextResult indicating success or failure

        """
        if environment in self.available_environments:
            return FlextResult.fail(f"Environment '{environment}' already exists")

        self.available_environments.append(environment)
        self.updated_at = _get_current_timestamp()

        return FlextResult.ok(None)

    def remove_environment(
        self,
        environment: FlextMeltanoEnvironmentType,
    ) -> FlextResult[None]:
        """Remove environment from project.

        Business rule: Cannot remove current environment.
        Business rule: Must have at least one environment.

        Args:
            environment: Environment to remove

        Returns:
            FlextResult indicating success or failure

        """
        if environment == self.current_environment:
            return FlextResult.fail("Cannot remove current active environment")

        if len(self.available_environments) <= 1:
            return FlextResult.fail("Project must have at least one environment")

        if environment not in self.available_environments:
            return FlextResult.fail(f"Environment '{environment}' not found")

        self.available_environments.remove(environment)
        self.updated_at = _get_current_timestamp()

        return FlextResult.ok(None)

    def mark_initialized(self) -> FlextResult[None]:
        """Mark project as initialized.

        Returns:
            FlextResult indicating success or failure

        """
        if self.is_initialized:
            return FlextResult.fail("Project already initialized")

        self.is_initialized = True
        self.updated_at = _get_current_timestamp()

        return FlextResult.ok(None)

    def update_metadata(
        self,
        description: str | None = None,
        version: str | None = None,
    ) -> FlextResult[None]:
        """Update project metadata.

        Args:
            description: New description
            version: New version

        Returns:
            FlextResult indicating success or failure

        """
        if description is not None:
            if len(description) > 500:
                return FlextResult.fail("Description must be 500 characters or less")
            self.description = description

        if version is not None:
            if not version.strip():
                return FlextResult.fail("Version cannot be empty")
            self.version = version

        self.updated_at = _get_current_timestamp()

        return FlextResult.ok(None)

    def to_dict(self) -> dict[str, Any]:
        """Convert project to dictionary representation.

        Returns:
            Dictionary representation of the project

        """
        return {
            "id": self.id,
            "name": self.name,
            "directory": str(self.directory),
            "config_path": str(self.config_path),
            "description": self.description,
            "version": self.version,
            "current_environment": self.current_environment.value,
            "available_environments": [
                env.value for env in self.available_environments
            ],
            "is_active": self.is_active,
            "is_initialized": self.is_initialized,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
