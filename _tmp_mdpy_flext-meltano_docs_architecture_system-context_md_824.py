# from flext-meltano_docs/architecture/system-context.md:824
from __future__ import annotations
class EventDrivenIntegration:
    """Event-driven integration for asynchronous operations."""

    def __init__(self, event_queue, event_handlers: Dict[str, Callable]):
        self.event_queue = event_queue
        self.event_handlers = event_handlers

    def publish_event(self, event: IntegrationEvent) -> p.Result[bool]:
        """Publish integration event to queue."""

        try:
            # Validate event
            validation_result = self.validate_event(event)
            if validation_result.failure:
                return validation_result

            # Publish to queue
            self.event_queue.publish(event.event_type, event.payload)

            # Log event
            self.logger.info(f"Published event: {event.event_type}")

            return r.| ok(value=True)

        except Exception as e:
            return r.fail(EventPublishingError(f"Failed to publish event: {e}"))

    def process_events(self) -> None:
        """Process incoming integration events."""

        while True:
            try:
                # Get next event
                event = self.event_queue.get_next_event()

                if event:
                    # Route to appropriate handler
                    handler = self.event_handlers.get(event.event_type)
                    if handler:
                        result = handler(event.payload)
                        if result.success:
                            self.event_queue.mark_processed(event)
                        else:
                            self.handle_processing_error(event, result.error)
                    else:
                        self.logger.warning(f"No handler for event type: {event.event_type}")

            except Exception as e:
                self.logger.error(f"Event processing error: {e}")
                time.sleep(self.error_backoff_seconds)```
#### Message Queue Integration

