# from flext-meltano_docs/architecture/system-context.md:878
from __future__ import annotations
class MessageQueueIntegration:
    """Message queue integration for reliable asynchronous communication."""

    def __init__(self, queue_client, dead_letter_queue):
        self.queue_client = queue_client
        self.dead_letter_queue = dead_letter_queue
        self.max_retries = 3

    def send_message(self, message: QueueMessage) -> p.Result[bool]:
        """Send message to queue with reliability guarantees."""

        try:
            # Add message metadata
            enriched_message = self.enrich_message(message)

            # Send with delivery confirmation
            message_id = self.queue_client.send_message(
                queue_url=self.queue_url,
                message_body=json.dumps(enriched_message),
                message_attributes=self.get_message_attributes(enriched_message)
            )

            self.logger.info(f"Sent message: {message_id}")
            return r.| ok(value=True)

        except Exception as e:
            return r.fail(QueueError(f"Failed to send message: {e}"))

    def receive_and_process_messages(self, message_processor: Callable) -> None:
        """Receive and process messages from queue."""

        while True:
            try:
                # Receive messages
                messages = self.queue_client.receive_messages(
                    queue_url=self.queue_url,
                    max_messages=10,
                    wait_time_seconds=20
                )

                for message in messages:
                    try:
                        # Process message
                        payload = json.loads(message.body)
                        result = message_processor(payload)

                        if result.success:
                            # Delete processed message
                            self.queue_client.delete_message(
                                queue_url=self.queue_url,
                                receipt_handle=message.receipt_handle
                            )
                        else:
                            # Handle processing failure
                            self.handle_processing_failure(message, result.error)

                    except Exception as e:
                        self.handle_processing_failure(message, e)

            except Exception as e:
                self.logger.error(f"Message processing error: {e}")
                time.sleep(self.error_backoff_seconds)

    def handle_processing_failure(self, message, error) -> None:
        """Handle message processing failure with retry logic."""

        retry_count = message.attributes.get('retry_count', 0)

        if retry_count < self.max_retries:
            # Retry with backoff
            retry_count += 1
            delay_seconds = 2 ** retry_count  # Exponential backoff

            # Update message for retry
            message.attributes['retry_count'] = retry_count
            message.attributes['next_retry_time'] = datetime.utcnow().timestamp() + delay_seconds

            # Re-queue message
            self.queue_client.send_message(
                queue_url=self.queue_url,
                message_body=message.body,
                message_attributes=message.attributes,
                delay_seconds=delay_seconds
            )
        else:
            # Move to dead letter queue
            self.dead_letter_queue.send_message(
                queue_url=self.dead_letter_queue_url,
                message_body=message.body,
                message_attributes={
                    **message.attributes,
                    'final_error': str(error),
                    'failed_at': datetime.utcnow().isoformat()
                }
            )

        # Delete original message
        self.queue_client.delete_message(
            queue_url=self.queue_url,
            receipt_handle=message.receipt_handle
        )```
______________________________________________________________________

## 🚀 Deployment Contexts

### Development Context

