"""Meltano Project Domain Entity - NEW SEMANTIC ARCHITECTURE.

🚨 DEPRECATION WARNING: Direct imports from this file are deprecated.

❌ OLD: from flext_meltano.domain.entities.project import MeltanoProject
✅ NEW: from flext_meltano import MeltanoProject

MeltanoProject represents the core domain concept of a Meltano project
with all its business rules and invariants.
"""

from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any, ClassVar

from flext_core import DomainEntity
from flext_core.domain.shared_types import ServiceResult
from pydantic import Field, field_validator

if TYPE_CHECKING:
    from pathlib import Path


class MeltanoProject(DomainEntity):
    """Meltano project domain entity with business rules."""

    # Identity
    name: str = Field(..., description="Project name")
    directory: Path = Field(..., description="Project directory")

    # Configuration
    config_path: Path = Field(..., description="Path to meltano.yml")
    environment: str = Field(default="dev", description="Current environment")

    # Status
    status: str = Field(default="initialized", description="Project status")
    is_active: bool = Field(default=True, description="Whether project is active")

    # Metadata
    description: str | None = Field(default=None, description="Project description")
    version: str = Field(default="1", description="Meltano config version")

    # Business rules
    VALID_STATUSES: ClassVar[set[str]] = {
        "initialized",
        "configured",
        "running",
        "stopped",
        "error",
    }
    VALID_ENVIRONMENTS: ClassVar[set[str]] = {"dev", "staging", "prod", "test"}

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        """Validate project status."""
        if v not in cls.VALID_STATUSES:
            msg = f"Invalid status '{v}'. Must be one of: {cls.VALID_STATUSES}"
            raise ValueError(msg)
        return v

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment."""
        if v not in cls.VALID_ENVIRONMENTS:
            msg = f"Invalid environment '{v}'. Must be one of: {cls.VALID_ENVIRONMENTS}"
            raise ValueError(msg)
        return v

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate project name."""
        if not v or len(v.strip()) == 0:
            msg = "Project name cannot be empty"
            raise ValueError(msg)

        # Business rule: only alphanumeric, dash, underscore
        import re

        if not re.match(r"^[a-zA-Z0-9_-]+$", v):
            msg = "Project name must contain only alphanumeric characters, dashes, and underscores"
            raise ValueError(msg)

        return v.strip()

    def activate(self) -> ServiceResult[Any]:
        """Activate the project."""
        if self.is_active:
            return ServiceResult.fail("Project is already active")

        self.is_active = True
        return ServiceResult.ok(None)

    def deactivate(self) -> ServiceResult[Any]:
        """Deactivate the project."""
        if not self.is_active:
            return ServiceResult.fail("Project is already inactive")

        self.is_active = False
        self.status = "stopped"
        return ServiceResult.ok(None)

    def change_environment(self, new_environment: str) -> ServiceResult[Any]:
        """Change project environment."""
        if new_environment not in self.VALID_ENVIRONMENTS:
            return ServiceResult.fail(f"Invalid environment '{new_environment}'. "
                f"Must be one of: {self.VALID_ENVIRONMENTS}",
            )

        self.environment = new_environment

        # Emit domain event would go here
        return ServiceResult.ok(None)

    def update_status(self, new_status: str) -> ServiceResult[Any]:
        """Update project status with business rules."""
        if new_status not in self.VALID_STATUSES:
            return ServiceResult.fail(f"Invalid status '{new_status}'. Must be one of: {self.VALID_STATUSES}",
            )

        # Business rule: cannot go from error to running directly
        if self.status == "error" and new_status == "running":
            return ServiceResult.fail("Cannot start project in error state. Fix errors first.",
            )

        self.status = new_status
        return ServiceResult.ok(None)

    def is_ready_for_execution(self) -> bool:
        """Check if project is ready for pipeline execution."""
        return (
            self.is_active
            and self.status in {"configured", "running", "stopped"}
            and self.config_path.exists()
        )

    def get_config_file_path(self) -> Path:
        """Get the full path to meltano.yml."""
        return self.directory / "meltano.yml"


# Deprecation warning for direct imports
def __getattr__(name: str) -> Any:
    """Handle direct imports with deprecation warning."""
    if name == "MeltanoProject":
        warnings.warn(
            "🚨 DEPRECATED: Importing MeltanoProject from 'flext_meltano.domain.entities.project' is deprecated.\n"
            "✅ Use: from flext_meltano import MeltanoProject\n"
            "📖 This import will be removed in version 0.8.0.\n"
            "📚 Migration guide: https://docs.flext.dev/migration/meltano",
            DeprecationWarning,
            stacklevel=2,
        )
        return MeltanoProject
    msg = f"module 'flext_meltano.domain.entities.project' has no attribute '{name}'"
    raise AttributeError(
        msg,
    )
