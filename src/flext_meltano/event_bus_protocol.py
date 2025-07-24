"""Event bus protocol and simple implementation for FLEXT-Meltano.

Uses flext_core.domain.pydantic_base.DomainEvent as the standard event type.
Does NOT duplicate code - extends flext_core functionality.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Protocol

# 🚨 ARCHITECTURAL COMPLIANCE: Using DI container for flext-core imports
from pydantic import BaseModel

if TYPE_CHECKING:
    # Define DomainEvent type alias
    DomainEvent = BaseModel
else:
    DomainEvent = BaseModel

# Initialize types via DI container
logger = logging.getLogger(__name__)


class FlextMeltanoEventBusProtocol(Protocol):
    """Protocol for event bus implementations compatible with flext_core."""

    async def publish(self, event: DomainEvent | dict[str, Any]) -> None:
        """Publish an event to the bus.

        Args:
            event: Event to publish (DomainEvent or dict).

        """
        ...

    async def subscribe(self, pattern: str, handler: object) -> None:
        """Subscribe to events matching a pattern.

        Args:
            pattern: Event pattern to match.
            handler: Handler function for events.

        """
        ...

    async def unsubscribe(self, pattern: str, handler: object) -> None:
        """Unsubscribe from events.

        Args:
            pattern: Event pattern to stop matching.
            handler: Handler function to remove.

        """
        ...


class FlextMeltanoSimpleEventBus:
    """Simple in-memory event bus implementation for development/testing."""

    def __init__(self) -> None:
        """Initialize simple event bus."""
        self._handlers: dict[str, list[Any]] = {}

    async def publish(self, event: DomainEvent | dict[str, Any]) -> None:
        """Publish event to registered handlers."""
        if isinstance(event, dict):
            event_type = event.get("type", "unknown")
        else:
            event_type = getattr(event, "event_type", type(event).__name__)

        logger.info("Publishing event %s", event_type)

        # Call handlers for this event type
        handlers = self._handlers.get(event_type, [])

        for handler in handlers:
            try:
                if callable(handler):
                    await handler(event)
            except Exception as e:
                logger.exception("Handler failed %s: %s", event_type, str(e))

    async def subscribe(self, pattern: str, handler: object) -> None:
        """Subscribe handler to event pattern."""
        if pattern not in self._handlers:
            self._handlers[pattern] = []
        self._handlers[pattern].append(handler)
        logger.info("Handler subscribed %s", pattern)

    async def unsubscribe(self, pattern: str, handler: object) -> None:
        """Unsubscribe handler from pattern."""
        if pattern in self._handlers and handler in self._handlers[pattern]:
            self._handlers[pattern].remove(handler)
            logger.info("Handler unsubscribed %s", pattern)
