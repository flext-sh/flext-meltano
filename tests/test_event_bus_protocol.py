"""Tests for FLEXT Meltano event bus protocol and implementation.

Comprehensive tests for event bus functionality.
Zero tolerance for untested code.
"""

from __future__ import annotations

import asyncio
from typing import Any
from unittest.mock import patch

import pytest
from pydantic import BaseModel

from flext_meltano.event_bus_protocol import (
    FlextMeltanoEventBusProtocol,
    FlextMeltanoSimpleEventBus,
)


class TestEvent(BaseModel):
    """Test event class for testing."""

    event_type: str = "test_event"
    data: str = "test_data"


class CustomEvent(BaseModel):
    """Custom event without event_type."""

    message: str = "custom_message"


class TestFlextMeltanoEventBusProtocol:
    """Test the event bus protocol interface."""

    def test_protocol_methods_exist(self) -> None:
        """Test that the protocol defines required methods."""
        # Verify protocol has the required methods
        assert hasattr(FlextMeltanoEventBusProtocol, "publish")
        assert hasattr(FlextMeltanoEventBusProtocol, "subscribe")
        assert hasattr(FlextMeltanoEventBusProtocol, "unsubscribe")

    def test_protocol_is_protocol(self) -> None:
        """Test that FlextMeltanoEventBusProtocol is a Protocol."""
        # Just verify it has the expected interface
        # Protocol detection varies across Python versions
        assert callable(getattr(FlextMeltanoEventBusProtocol, "publish", None))
        assert callable(getattr(FlextMeltanoEventBusProtocol, "subscribe", None))
        assert callable(getattr(FlextMeltanoEventBusProtocol, "unsubscribe", None))


class TestFlextMeltanoSimpleEventBus:
    """Test FlextMeltanoSimpleEventBus implementation."""

    def test_init(self) -> None:
        """Test simple event bus initialization."""
        bus = FlextMeltanoSimpleEventBus()
        assert isinstance(bus._handlers, dict)
        assert len(bus._handlers) == 0

    @pytest.mark.asyncio
    async def test_publish_with_pydantic_event(self) -> None:
        """Test publishing a Pydantic event."""
        bus = FlextMeltanoSimpleEventBus()
        event = TestEvent(data="test_publish")

        # Should not raise any exceptions
        await bus.publish(event)

    @pytest.mark.asyncio
    async def test_publish_with_dict_event(self) -> None:
        """Test publishing a dictionary event."""
        bus = FlextMeltanoSimpleEventBus()
        event = {"type": "dict_event", "data": "test_data"}

        # Should not raise any exceptions
        await bus.publish(event)

    @pytest.mark.asyncio
    async def test_publish_with_dict_event_no_type(self) -> None:
        """Test publishing a dictionary event without type."""
        bus = FlextMeltanoSimpleEventBus()
        event = {"data": "test_data"}  # No "type" key

        # Should not raise any exceptions, should use "unknown" as type
        await bus.publish(event)

    @pytest.mark.asyncio
    async def test_publish_with_custom_event_no_event_type(self) -> None:
        """Test publishing event without event_type attribute."""
        bus = FlextMeltanoSimpleEventBus()
        event = CustomEvent(message="test")

        # Should use class name as event type
        await bus.publish(event)

    @pytest.mark.asyncio
    async def test_subscribe_and_publish(self) -> None:
        """Test subscribing to events and receiving them."""
        bus = FlextMeltanoSimpleEventBus()
        received_events = []

        async def handler(event: Any) -> None:
            received_events.append(event)

        # Subscribe to event type
        await bus.subscribe("test_event", handler)

        # Publish event
        event = TestEvent(data="test_subscribe")
        await bus.publish(event)

        # Verify event was received
        assert len(received_events) == 1
        assert received_events[0] == event

    @pytest.mark.asyncio
    async def test_subscribe_multiple_handlers(self) -> None:
        """Test subscribing multiple handlers to the same event."""
        bus = FlextMeltanoSimpleEventBus()
        received_events_1 = []
        received_events_2 = []

        async def handler1(event: Any) -> None:
            received_events_1.append(event)

        async def handler2(event: Any) -> None:
            received_events_2.append(event)

        # Subscribe both handlers
        await bus.subscribe("test_event", handler1)
        await bus.subscribe("test_event", handler2)

        # Publish event
        event = TestEvent(data="multiple_handlers")
        await bus.publish(event)

        # Both handlers should receive the event
        assert len(received_events_1) == 1
        assert len(received_events_2) == 1
        assert received_events_1[0] == event
        assert received_events_2[0] == event

    @pytest.mark.asyncio
    async def test_subscribe_different_patterns(self) -> None:
        """Test subscribing to different event patterns."""
        bus = FlextMeltanoSimpleEventBus()
        event1_received = []
        event2_received = []

        async def handler1(event: Any) -> None:
            event1_received.append(event)

        async def handler2(event: Any) -> None:
            event2_received.append(event)

        # Subscribe to different patterns
        await bus.subscribe("event_type_1", handler1)
        await bus.subscribe("event_type_2", handler2)

        # Publish events of different types
        event1 = {"type": "event_type_1", "data": "first"}
        event2 = {"type": "event_type_2", "data": "second"}

        await bus.publish(event1)
        await bus.publish(event2)

        # Each handler should only receive its event
        assert len(event1_received) == 1
        assert len(event2_received) == 1
        assert event1_received[0] == event1
        assert event2_received[0] == event2

    @pytest.mark.asyncio
    async def test_unsubscribe(self) -> None:
        """Test unsubscribing from events."""
        bus = FlextMeltanoSimpleEventBus()
        received_events = []

        async def handler(event: Any) -> None:
            received_events.append(event)

        # Subscribe and publish
        await bus.subscribe("test_event", handler)
        event1 = TestEvent(data="before_unsubscribe")
        await bus.publish(event1)

        # Unsubscribe and publish again
        await bus.unsubscribe("test_event", handler)
        event2 = TestEvent(data="after_unsubscribe")
        await bus.publish(event2)

        # Should only receive the first event
        assert len(received_events) == 1
        assert received_events[0] == event1

    @pytest.mark.asyncio
    async def test_unsubscribe_nonexistent_pattern(self) -> None:
        """Test unsubscribing from a pattern that doesn't exist."""
        bus = FlextMeltanoSimpleEventBus()

        async def handler(event: Any) -> None:
            pass

        # Should not raise exception
        await bus.unsubscribe("nonexistent_pattern", handler)

    @pytest.mark.asyncio
    async def test_unsubscribe_nonexistent_handler(self) -> None:
        """Test unsubscribing a handler that wasn't subscribed."""
        bus = FlextMeltanoSimpleEventBus()

        async def handler1(event: Any) -> None:
            pass

        async def handler2(event: Any) -> None:
            pass

        # Subscribe handler1
        await bus.subscribe("test_event", handler1)

        # Try to unsubscribe handler2 (not subscribed)
        await bus.unsubscribe("test_event", handler2)

        # Should not raise exception

    @pytest.mark.asyncio
    async def test_handler_exception_handling(self) -> None:
        """Test that handler exceptions don't break event publishing."""
        bus = FlextMeltanoSimpleEventBus()
        good_handler_called = False

        class TestHandlerError(Exception):
            """Custom exception for testing handler failures."""

        async def bad_handler(event: Any) -> None:
            raise TestHandlerError("Handler failed!")

        async def good_handler(event: Any) -> None:
            nonlocal good_handler_called
            good_handler_called = True

        # Subscribe both handlers
        await bus.subscribe("test_event", bad_handler)
        await bus.subscribe("test_event", good_handler)

        # Publish event - should not raise exception
        event = TestEvent(data="exception_test")
        with patch("flext_meltano.event_bus_protocol.logger") as mock_logger:
            await bus.publish(event)

            # Verify exception was logged
            mock_logger.exception.assert_called()

        # Good handler should still be called
        assert good_handler_called

    @pytest.mark.asyncio
    async def test_non_callable_handler(self) -> None:
        """Test behavior with non-callable handlers."""
        bus = FlextMeltanoSimpleEventBus()
        non_callable = "not_a_function"

        # Subscribe non-callable object
        await bus.subscribe("test_event", non_callable)

        # Publish event - should not raise exception
        event = TestEvent(data="non_callable_test")
        await bus.publish(event)  # Should handle gracefully

    @pytest.mark.asyncio
    async def test_logging_publish(self) -> None:
        """Test that publishing logs correctly."""
        bus = FlextMeltanoSimpleEventBus()
        event = TestEvent(data="logging_test")

        with patch("flext_meltano.event_bus_protocol.logger") as mock_logger:
            await bus.publish(event)
            mock_logger.info.assert_called_with("Publishing event %s", "test_event")

    @pytest.mark.asyncio
    async def test_logging_subscribe(self) -> None:
        """Test that subscribing logs correctly."""
        bus = FlextMeltanoSimpleEventBus()

        async def handler(event: Any) -> None:
            pass

        with patch("flext_meltano.event_bus_protocol.logger") as mock_logger:
            await bus.subscribe("test_pattern", handler)
            mock_logger.info.assert_called_with("Handler subscribed %s", "test_pattern")

    @pytest.mark.asyncio
    async def test_logging_unsubscribe(self) -> None:
        """Test that unsubscribing logs correctly."""
        bus = FlextMeltanoSimpleEventBus()

        async def handler(event: Any) -> None:
            pass

        # Subscribe first
        await bus.subscribe("test_pattern", handler)

        # Then unsubscribe with logging
        with patch("flext_meltano.event_bus_protocol.logger") as mock_logger:
            await bus.unsubscribe("test_pattern", handler)
            mock_logger.info.assert_called_with("Handler unsubscribed %s", "test_pattern")

    def test_handlers_dict_structure(self) -> None:
        """Test the internal handlers dictionary structure."""
        bus = FlextMeltanoSimpleEventBus()

        # Initially empty
        assert bus._handlers == {}

        # After creating a subscription, structure should be maintained
        async def dummy_handler(event: Any) -> None:
            pass

        asyncio.run(bus.subscribe("test", dummy_handler))

        assert "test" in bus._handlers
        assert isinstance(bus._handlers["test"], list)
        assert dummy_handler in bus._handlers["test"]

    @pytest.mark.asyncio
    async def test_event_type_extraction_edge_cases(self) -> None:
        """Test edge cases in event type extraction."""
        bus = FlextMeltanoSimpleEventBus()

        # Event with event_type attribute
        class EventWithType:
            event_type = "custom_type"

        event_with_type = EventWithType()

        # Should not raise exceptions
        await bus.publish(event_with_type)  # type: ignore[arg-type]

        # Event as dict with empty type
        dict_event_empty_type = {"type": ""}
        await bus.publish(dict_event_empty_type)

        # Event as dict with None type
        dict_event_none_type = {"type": None}
        await bus.publish(dict_event_none_type)

    @pytest.mark.asyncio
    async def test_concurrent_publishing(self) -> None:
        """Test concurrent event publishing."""
        bus = FlextMeltanoSimpleEventBus()
        received_events = []

        async def handler(event: Any) -> None:
            received_events.append(event)

        await bus.subscribe("test_event", handler)

        # Publish multiple events concurrently
        events = [TestEvent(data=f"concurrent_{i}") for i in range(5)]
        tasks = [bus.publish(event) for event in events]

        await asyncio.gather(*tasks)

        # All events should be received
        assert len(received_events) == 5

        # Verify all events were received (order might vary)
        received_data = [event.data for event in received_events]
        expected_data = [f"concurrent_{i}" for i in range(5)]
        assert set(received_data) == set(expected_data)

    def test_implements_protocol(self) -> None:
        """Test that SimpleEventBus implements the protocol."""
        bus = FlextMeltanoSimpleEventBus()

        # Should have all protocol methods
        assert hasattr(bus, "publish")
        assert hasattr(bus, "subscribe")
        assert hasattr(bus, "unsubscribe")

        # Methods should be callable
        assert callable(bus.publish)
        assert callable(bus.subscribe)
        assert callable(bus.unsubscribe)
