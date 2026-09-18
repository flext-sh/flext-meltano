# from flext-meltano_docs/architecture/system-context.md:734
from __future__ import annotations


class SynchronousIntegration:
    """Synchronous request-response integration pattern."""

    def execute_sync_operation(
        self, request: OperationRequest
    ) -> p.Result[OperationResponse]:
        """Execute synchronous operation with timeout and error handling."""
        # Validate request
        validation_result = self.validate_request(request)
        if validation_result.failure:
            return validation_result

        # Execute operation with timeout
        try:
            with self.timeout_context(self.operation_timeout):
                response = self.external_system.execute_operation(request)
                return r.ok(self.adapt_response(response))

        except TimeoutError:
            return r.fail(
                IntegrationTimeoutError(
                    f"Operation timed out after {self.operation_timeout}s"
                )
            )

        except ExternalSystemError as e:
            return r.fail(IntegrationError(f"External system error: {e.message}"))```
#### Circuit Breaker Pattern

