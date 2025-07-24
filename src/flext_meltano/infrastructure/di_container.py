"""🚨 ARCHITECTURAL COMPLIANCE: DI Container for flext-meltano."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


def get_service_result() -> Any:
    """Get FlextResult from flext-core (ONLY available export)."""
    try:
        from flext_core import FlextResult

        return FlextResult
    except ImportError as e:
        raise ImportError(f"Failed to load FlextResult: {e}") from e


def get_di_container() -> Any:
    """Get FlextContainer instance from flext-core."""
    try:
        from flext_core import FlextContainer

        return FlextContainer()
    except ImportError as e:
        raise ImportError(f"Failed to load FlextContainer: {e}") from e


def get_entity_id() -> Any:
    """Get FlextEntityId from flext-core (fallback to str if not available)."""
    try:
        from flext_core import FlextEntityId

        return FlextEntityId
    except ImportError:
        # Fallback to str type if FlextEntityId is not available
        return str


def get_container() -> Any:
    """Get container instance from flext-core."""
    try:
        from flext_core import get_flext_container

        return get_flext_container()
    except ImportError as e:
        raise ImportError(f"Failed to load get_container: {e}") from e


def injectable() -> Any:
    """Decorator to mark classes as injectable services.

    This decorator marks classes for dependency injection.
    Currently a no-op decorator for future DI framework integration.

    Returns:
        The original class unchanged

    """

    def decorator(cls: type) -> type:
        # Mark class as injectable for future DI integration
        cls._injectable = True  # type: ignore[attr-defined]
        return cls

    return decorator


# Local fallbacks for missing flext-core components
class FlextMeltanoDomainEntity(BaseModel):
    """Local domain entity replacement."""

    model_config = {"arbitrary_types_allowed": True}


class FlextMeltanoDomainEvent(BaseModel):
    """Local domain event replacement."""

    timestamp: str = ""


class FlextMeltanoAbstractService(ABC):
    """Local abstract service base class."""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize service."""


class FlextMeltanoAbstractEntity(FlextMeltanoDomainEntity):
    """Local abstract entity replacement."""


# Export compatibility functions
def get_domain_entity() -> type[FlextMeltanoDomainEntity]:
    """Get domain entity class (local fallback)."""
    return FlextMeltanoDomainEntity


def get_domain_event() -> type[FlextMeltanoDomainEvent]:
    """Get domain event class (local fallback)."""
    return FlextMeltanoDomainEvent


def get_field() -> Any:
    """Get Field function (Pydantic Field)."""
    try:
        from flext_core import FlextField
        return FlextField
    except ImportError:
        return Field


# Local ConfigDefaults implementation
class FlextMeltanoConfigDefaults:
    """Local config defaults fallback."""

    # Default configuration values
    ENVIRONMENT = "dev"
    PROJECT_ROOT = "/var/tmp/flext-meltano"  # noqa: S108
    LOG_LEVEL = "info"
    TIMEOUT_SECONDS = 30
    MAX_RETRIES = 3
    MAX_ENTITY_NAME_LENGTH = 255

    class FlextMeltanoBusiness:
        """Business logic defaults."""

        MINIMUM_MELTANO_COMMAND_COUNT = 2
        DEFAULT_CHUNK_SIZE = 1000
        MAX_CONCURRENT_JOBS = 5

    def __init__(self) -> None:
        self.business = self.FlextMeltanoBusiness()


def get_config_defaults() -> type[FlextMeltanoConfigDefaults]:
    """Get ConfigDefaults - local fallback implementation."""
    return FlextMeltanoConfigDefaults


# Local Environment implementation


class FlextMeltanoEnvironment(Enum):
    """Environment enum for different deployment environments."""

    DEV = "dev"
    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PROD = "prod"
    PRODUCTION = "production"


class FlextMeltanoExecutionStatus(Enum):
    """Execution status for jobs and tasks."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    COMPLETED = "completed"  # Alias for SUCCESS
    FAILED = "failed"
    CANCELLED = "cancelled"


# Direct exports for convenience - FLEXT naming conventions
FlextResult = get_service_result()
EntityId = get_entity_id()

# Legacy compatibility (deprecated)
ServiceResult = FlextResult  # For backward compatibility during migration

# Backward compatibility aliases for renamed classes
DomainEntity = FlextMeltanoDomainEntity
DomainEvent = FlextMeltanoDomainEvent
AbstractService = FlextMeltanoAbstractService
AbstractEntity = FlextMeltanoAbstractEntity
