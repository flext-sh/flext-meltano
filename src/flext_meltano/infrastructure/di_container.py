"""🚨 ARCHITECTURAL COMPLIANCE: DI Container for flext-meltano."""

from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


def get_service_result() -> Any:
    """Get ServiceResult from flext-core (ONLY available export)."""
    try:
        from flext_core import ServiceResult

        return ServiceResult
    except ImportError as e:
        raise ImportError(f"Failed to load ServiceResult: {e}") from e


def get_di_container() -> Any:
    """Get DIContainer from flext-core."""
    try:
        from flext_core import DIContainer

        return DIContainer
    except ImportError as e:
        raise ImportError(f"Failed to load DIContainer: {e}") from e


def get_entity_id() -> Any:
    """Get EntityId from flext-core."""
    try:
        from flext_core import EntityId

        return EntityId
    except ImportError as e:
        raise ImportError(f"Failed to load EntityId: {e}") from e


def get_container() -> Any:
    """Get container instance from flext-core."""
    try:
        from flext_core import get_container

        return get_container()
    except ImportError as e:
        raise ImportError(f"Failed to load get_container: {e}") from e


# Local fallbacks for missing flext-core components
class DomainEntity(BaseModel):
    """Local domain entity replacement."""

    model_config = {"arbitrary_types_allowed": True}


class DomainEvent(BaseModel):
    """Local domain event replacement."""

    timestamp: str = ""


class AbstractService(ABC):
    """Local abstract service base class."""

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize service."""


class AbstractEntity(DomainEntity):
    """Local abstract entity replacement."""


# Export compatibility functions
def get_domain_entity() -> type[DomainEntity]:
    """Get domain entity class (local fallback)."""
    return DomainEntity


def get_domain_event() -> type[DomainEvent]:
    """Get domain event class (local fallback)."""
    return DomainEvent


def get_field() -> Any:
    """Get Field function (Pydantic Field)."""
    return Field


def get_config_defaults() -> Any:
    """Get ConfigDefaults - local fallback implementation."""

    class ConfigDefaults:
        """Local config defaults fallback."""

        # Default configuration values
        ENVIRONMENT = "dev"
        PROJECT_ROOT = "/var/tmp/flext-meltano"  # noqa: S108
        LOG_LEVEL = "info"
        TIMEOUT_SECONDS = 30
        MAX_RETRIES = 3
        MAX_ENTITY_NAME_LENGTH = 255

        class Business:
            """Business logic defaults."""

            MINIMUM_MELTANO_COMMAND_COUNT = 2
            DEFAULT_CHUNK_SIZE = 1000
            MAX_CONCURRENT_JOBS = 5

        def __init__(self) -> None:
            self.business = self.Business()

    return ConfigDefaults


# Local Environment implementation


class Environment(Enum):
    """Environment enum for different deployment environments."""

    DEV = "dev"
    DEVELOPMENT = "development"
    TEST = "test"
    STAGING = "staging"
    PROD = "prod"
    PRODUCTION = "production"


# Direct exports for convenience

EntityId = get_entity_id()
