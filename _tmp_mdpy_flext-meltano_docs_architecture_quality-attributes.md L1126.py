# from flext-meltano/docs/architecture/quality-attributes.md:1126
from __future__ import annotations


class RailwayExecutor:
    """Railway-oriented execution with comprehensive error handling."""

    def execute_with_railway(self, operation: Operation) -> p.Result[OperationResult]:
        """Execute operation using railway pattern with full error handling."""
        return (
            self
            .validate_operation(operation)
            .flat_map(lambda op: self.check_permissions(op))
            .flat_map(lambda op: self.reserve_resources(op))
            .flat_map(lambda op: self.execute_operation(op))
            .flat_map(lambda result: self.validate_result(result))
            .flat_map(lambda result: self.persist_result(result))
            .map(lambda result: OperationResult.from_success(result))
        )

    def validate_operation(self, operation: Operation) -> p.Result[ValidatedOperation]:
        """Validate operation parameters and constraints."""
        # Schema validation
        schema_result = self.schema_validator.validate(operation.payload)
        if schema_result.failure:
            return r.fail(
                ValidationError(f"Schema validation failed: {schema_result.error}")
            )

        # Business rule validation
        business_result = self.business_validator.validate(operation)
        if business_result.failure:
            return r.fail(
                BusinessRuleViolation(
                    f"Business rule violation: {business_result.error}"
                )
            )

        # Resource availability check
        resource_result = self.resource_checker.check_availability(operation)
        if resource_result.failure:
            return r.fail(
                ResourceUnavailableError(
                    f"Resources unavailable: {resource_result.error}"
                )
            )

        return r.ok(ValidatedOperation(operation, schema_result.unwrap()))

    def execute_operation(
        self, operation: ValidatedOperation
    ) -> p.Result[ExecutionResult]:
        """Execute operation with comprehensive error handling."""
        try:
            # Set execution timeout
            with self.timeout_context(operation.timeout_seconds):
                # Execute with circuit breaker
                if not self.circuit_breaker.allow_request():
                    return r.fail(
                        CircuitBreakerOpenError(
                            "Circuit breaker is open - service temporarily unavailable"
                        )
                    )

                # Execute operation
                result = operation.execute()

                # Record success
                self.circuit_breaker.record_success()

                return r.ok(result)

        except TimeoutError:
            self.circuit_breaker.record_failure()
            return r.fail(
                OperationTimeoutError(
                    f"Operation timed out after {operation.timeout_seconds} seconds"
                )
            )

        except ExternalServiceError as e:
            self.circuit_breaker.record_failure()
            return r.fail(ExternalServiceError(f"External service error: {e.message}"))

        except Exception as e:
            # Record failure for circuit breaker
            self.circuit_breaker.record_failure()

            # Log error with context
            self.logger.error(
                f"Operation execution failed: {e}",
                extra={
                    "operation_id": operation.id,
                    "operation_type": operation.type,
                    "error_type": type(e).__name__,
                    "stack_trace": traceback.format_exc(),
                },
            )

            return r.fail(
                OperationExecutionError(f"Operation execution failed: {e!s}")
            )```
#### 2. Circuit Breaker Pattern

