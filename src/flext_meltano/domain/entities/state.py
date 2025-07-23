from flext_core import ServiceResult

"""Meltano State Domain Entity - NEW SEMANTIC ARCHITECTURE.

🚨 DEPRECATION WARNING: Direct imports from this file are deprecated.

❌ OLD: from flext_meltano.domain.entities.state import MeltanoState
✅ NEW: from flext_meltano import MeltanoState

MeltanoState represents the state of a Meltano pipeline execution
for incremental data processing.
"""

from __future__ import annotations

import warnings
from datetime import UTC, datetime
from typing import Any, ClassVar

from pydantic import BaseModel, Field, field_validator

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container
from flext_meltano.infrastructure.di_container import get_service_result

# Define DomainEntity as BaseModel for now
DomainEntity = BaseModel


# Initialize types via DI container
class MeltanoState(DomainEntity):
    """Meltano state domain entity for incremental processing."""

    # Identity
    state_id: str = Field(..., description="Unique state identifier")
    job_id: str = Field(..., description="Associated job ID")

    # State data
    state_data: dict[str, Any] | None = Field(
        default_factory=dict,
        description="State payload",
    )

    # Metadata
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="State creation time",
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="State last update time",
    )

    # Versioning
    version: int = Field(default=1, description="State version")
    previous_state_id: str | None = Field(default=None, description="Previous state ID")

    # Validation
    is_valid: bool = Field(default=True, description="Whether state is valid")
    validation_errors: list[str] = Field(
        default_factory=list,
        description="Validation errors",
    )

    # Processing metadata
    streams_processed: list[str] = Field(
        default_factory=list,
        description="Processed streams",
    )
    records_count: int = Field(default=0, description="Total records processed")

    # Business rules
    MAX_STATE_SIZE_MB: ClassVar[int] = 10  # Maximum state size in MB

    @field_validator("state_id")
    @classmethod
    def validate_state_id(cls, v: str) -> str:
        """Validate state ID."""
        if not v or len(v.strip()) == 0:
            msg = "State ID cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, v: str) -> str:
        """Validate job ID."""
        if not v or len(v.strip()) == 0:
            msg = "Job ID cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("version")
    @classmethod
    def validate_version(cls, v: int) -> int:
        """Validate state version."""
        if v < 1:
            msg = "State version must be positive"
            raise ValueError(msg)
        return v

    def update_state(self, new_state_data: dict[str, Any]) -> ServiceResult[Any]:
        """Update the state data."""
        if not self.is_valid:
            return ServiceResult.fail("Cannot update invalid state")

        # Business rule: validate state size
        import json

        state_size_mb = len(json.dumps(new_state_data).encode()) / (1024 * 1024)
        if state_size_mb > self.MAX_STATE_SIZE_MB:
            return ServiceResult.fail(
                f"State size ({state_size_mb:.2f}MB) exceeds maximum allowed "
                f"({self.MAX_STATE_SIZE_MB}MB)",
            )

        self.state_data = new_state_data
        self.updated_at = datetime.now(UTC)
        self.version += 1

        return ServiceResult.ok(None)

    def add_stream_state(
        self,
        stream_name: str,
        stream_state: dict[str, Any],
    ) -> ServiceResult[Any]:
        """Add or update state for a specific stream."""
        if not stream_name or not stream_name.strip():
            return ServiceResult.fail("Stream name cannot be empty")

        # Ensure state_data is initialized
        if self.state_data is None:
            self.state_data = {}

        if "streams" not in self.state_data:
            self.state_data["streams"] = {}

        self.state_data["streams"][stream_name] = stream_state

        if stream_name not in self.streams_processed:
            self.streams_processed.append(stream_name)

        self.updated_at = datetime.now(UTC)
        return ServiceResult.ok(None)

    def get_stream_state(self, stream_name: str) -> dict[str, Any] | None:
        """Get state for a specific stream."""
        if self.state_data is None or "streams" not in self.state_data:
            return None

        stream_state = self.state_data["streams"].get(stream_name)
        return stream_state if isinstance(stream_state, dict) else None

    def invalidate(self, errors: list[str]) -> ServiceResult[Any]:
        """Mark state as invalid with errors."""
        if not errors:
            return ServiceResult.fail("Must provide validation errors")

        self.is_valid = False
        self.validation_errors = errors
        self.updated_at = datetime.now(UTC)

        return ServiceResult.ok(None)

    def validate_and_fix(self) -> ServiceResult[Any]:
        """Validate and attempt to fix the state."""
        errors = []

        # Validate state structure - fix if None or non-dict
        if self.state_data is None:
            # Fix by initializing empty dict
            self.state_data = {}

        # Check type after potential None fix
        if not isinstance(self.state_data, dict):
            # Cannot fix non-dict state_data
            # state_data could be string, int, list, etc. after model validation
            self.is_valid = False
            self.validation_errors = ["State data must be a dictionary"]
            return ServiceResult.fail(
                "State validation failed: State data must be a dictionary",
            )

        # At this point, state_data is guaranteed to be a dict
        # Type narrowing for MyPy - state_data is Dict after validation above

        # Validate streams structure
        if "streams" in self.state_data and not isinstance(
            self.state_data["streams"],
            dict,
        ):
            errors.append("Streams must be a dictionary")

        # Check for required fields in stream states
        if "streams" in self.state_data:
            streams = self.state_data["streams"]
            if isinstance(streams, dict):
                for stream_name, stream_state in streams.items():
                    if not isinstance(stream_state, dict):
                        errors.append(
                            f"Stream '{stream_name}' state must be a dictionary",
                        )
                    elif "replication_key_value" not in stream_state:
                        # Auto-fix: add default replication key
                        stream_state["replication_key_value"] = None

        if errors:
            self.is_valid = False
            self.validation_errors = errors
            return ServiceResult.fail(f"State validation failed: {'; '.join(errors)}")

        self.is_valid = True
        self.validation_errors = []
        return ServiceResult.ok(None)

    def get_bookmarks(self) -> dict[str, Any]:
        """Get bookmarks from state data."""
        if self.state_data is None:
            return {}
        bookmarks = self.state_data.get("bookmarks", {})
        return bookmarks if isinstance(bookmarks, dict) else {}

    def set_bookmarks(self, bookmarks: dict[str, Any]) -> ServiceResult[Any]:
        """Set bookmarks in state data."""
        if self.state_data is None:
            self.state_data = {}

        self.state_data["bookmarks"] = bookmarks
        self.updated_at = datetime.now(UTC)
        return ServiceResult.ok(None)

    def increment_records_count(self, count: int) -> None:
        """Increment the processed records count."""
        if count > 0:
            self.records_count += count
            self.updated_at = datetime.now(UTC)

    def get_age_hours(self) -> float:
        """Get state age in hours."""
        return (datetime.now(UTC) - self.created_at).total_seconds() / 3600

    def is_stale(self, max_age_hours: float = 24.0) -> bool:
        """Check if state is stale."""
        return self.get_age_hours() > max_age_hours


# Deprecation warning for direct imports
def __getattr__(name: str) -> Any:
    """Handle direct imports with deprecation warning."""
    if name == "MeltanoState":
        warnings.warn(
            "🚨 DEPRECATED: Importing MeltanoState from 'flext_meltano.domain.entities.state' is deprecated.\n"
            "✅ Use: from flext_meltano import MeltanoState\n"
            "📖 This import will be removed in version 0.8.0.\n"
            "📚 Migration guide: https://docs.flext.dev/migration/meltano",
            DeprecationWarning,
            stacklevel=2,
        )
        return MeltanoState
    msg = f"module 'flext_meltano.domain.entities.state' has no attribute '{name}'"
    raise AttributeError(
        msg,
    )
