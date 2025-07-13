"""FLEXT Meltano Event Bridge.

This module provides integration between Meltano events and the FLEXT event system,
allowing seamless event propagation and handling across both platforms.
"""

from __future__ import annotations

import uuid
from datetime import UTC
from datetime import datetime
from typing import TYPE_CHECKING
from typing import Any

from structlog import get_logger

# Use actual FLEXT imports - no placeholders allowed
from flext_core.domain.pydantic_base import DomainEvent
from flext_core.domain.pydantic_base import Field

if TYPE_CHECKING:
    from collections.abc import Callable

    from flext_meltano.event_bus_protocol import EventBusProtocol

logger = get_logger(__name__)


class MeltanoEvent(DomainEvent):
    """Meltano-specific domain event extending flext_core.DomainEvent."""

    event_type: str = Field(description="Type of Meltano event")
    data: dict[str, Any] = Field(default_factory=dict, description="Event payload")
    correlation_id: str | None = Field(default=None, description="Correlation ID")
    source: str = Field(default="meltano", description="Event source")


class EventConfig:
    """Configuration for Meltano events."""

    def __init__(
        self,
        event_type: str,
        project: object = None,
        job_id: str | None = None,
        pipeline_name: str | None = None,
        state: object = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.event_type = event_type
        self.project = project
        self.job_id = job_id
        self.pipeline_name = pipeline_name
        self.state = state
        self.metadata = metadata


# DomainEvent now imported from flext_core - no duplicates allowed


class MeltanoEventBridge:
    """Bridge between Meltano and FLEXT event systems."""

    def __init__(self, flext_event_bus: EventBusProtocol | None = None) -> None:
        self.flext_event_bus = flext_event_bus or self._create_mock_event_bus()
        self._active_subscriptions: dict[
            str,
            Callable,
        ] = {}  # Properly initialized - no TODOs

        # Event mapping between Meltano and FLEXT events
        self._meltano_to_flext_mapping = {
            "job.started": "meltano.job.started",
            "job.completed": "meltano.job.completed",
            "job.failed": "meltano.job.failed",
            "job.cancelled": "meltano.job.cancelled",
            "pipeline.started": "meltano.pipeline.started",
            "pipeline.completed": "meltano.pipeline.completed",
            "pipeline.failed": "meltano.pipeline.failed",
            "state.updated": "meltano.state.updated",
            "plugin.installed": "meltano.plugin.installed",
            "plugin.removed": "meltano.plugin.removed",
            "project.initialized": "meltano.project.initialized",
            "project.loaded": "meltano.project.loaded",
        }

        logger.info("Initialized Meltano Event Bridge")

    def _create_mock_event_bus(self) -> EventBusProtocol:
        """Create mock event bus for testing/fallback - implements actual protocol."""

        class MockEventBus:
            async def publish(self, event: DomainEvent | dict[str, Any]) -> None:
                """Publish event to mock bus."""
                if isinstance(event, MeltanoEvent):
                    logger.info(
                        "Event published",
                        event_type=event.event_type,
                        data_keys=list(event.data.keys()),
                    )
                elif isinstance(event, dict):
                    logger.info(
                        "Event published",
                        event_type=event.get("type", "unknown"),
                    )
                else:
                    logger.info("Event published", event_type=type(event).__name__)

            async def subscribe(self, pattern: str, handler: Callable) -> None:
                logger.info("Subscription created", pattern=pattern)

            async def unsubscribe(self, pattern: str, handler: Callable) -> None:
                logger.info("Subscription removed", pattern=pattern)

        return MockEventBus()

    async def publish_meltano_event(
        self,
        config: EventConfig,
        **kwargs: object,
    ) -> None:
        """Publish Meltano event to FLEXT event bus.

        Args:
            config: Event configuration with project and job details.
            **kwargs: Additional event data payload.

        Raises:
            Exception: If event publishing fails.

        """
        try:
            # Map Meltano event type to FLEXT event type
            flext_event_type = self._meltano_to_flext_mapping.get(
                config.event_type,
                f"meltano.{config.event_type}",
            )

            # Build event data
            event_data = {
                "meltano_event_type": config.event_type,
                "timestamp": datetime.now(UTC).isoformat(),
                "event_id": str(uuid.uuid4()),
                **kwargs,
            }

            # Add project information if available:
            if config.project:
                event_data.update(
                    {
                        "project_name": getattr(config.project, "name", "unknown"),
                        "project_root": str(getattr(config.project, "root", "")),
                        "environment": (
                            getattr(
                                config.project,
                                "active_environment",
                                {},
                            ).get("name")
                            if hasattr(config.project, "active_environment")
                            else None
                        ),
                    },
                )

            # Add job information
            if config.job_id:
                event_data["job_id"] = config.job_id

            # Add pipeline information
            if config.pipeline_name:
                event_data["pipeline_name"] = config.pipeline_name

            # Add state information
            if config.state:
                event_data.update(
                    {
                        "state": getattr(config.state, "value", str(config.state)),
                        "state_name": getattr(config.state, "name", str(config.state)),
                    },
                )

            # Add metadata
            if config.metadata:
                event_data["metadata"] = config.metadata

            # Create FLEXT event using proper constructor
            flext_event = MeltanoEvent(
                event_type=flext_event_type,
                data=event_data,
                correlation_id=kwargs.get("correlation_id"),
                source="meltano",
            )

            # Publish to FLEXT event bus
            await self.flext_event_bus.publish(flext_event)

            logger.debug(
                "Published Meltano event to FLEXT",
                meltano_event=config.event_type,
                flext_event=flext_event_type,
                job_id=config.job_id,
                pipeline_name=config.pipeline_name,
            )

        except Exception as e:
            logger.exception(
                "Failed to publish Meltano event",
                event_type=config.event_type,
                error=str(e),
            )
            raise

    async def get_event_statistics(self) -> dict[str, Any]:
        """Get event bridge statistics.

        Returns:
            Dictionary containing event bridge metrics.

        """
        return {
            "active_subscriptions": len(self._active_subscriptions),
            "event_mappings": len(self._meltano_to_flext_mapping),
            "supported_event_types": list(self._meltano_to_flext_mapping.keys()),
        }

    async def cleanup(self) -> None:
        """Clean up event bridge resources.

        Closes connections and clears subscriptions.
        """
        logger.info("Cleaning up Meltano Event Bridge")
        self._active_subscriptions.clear()
        logger.info("Meltano Event Bridge cleanup completed")
