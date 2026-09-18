# from flext-meltano/docs/architecture/adr/001-railway-oriented-programming.md:189
from __future__ import annotations


def test_pipeline_failure_handling():
    # Given
    invalid_config = PipelineConfig(invalid_param="test")

    # When
    result = service.create_pipeline(invalid_config)

    # Then
    assert result.failure
    assert isinstance(result.error_value, ConfigurationError)
    assert "invalid_param" in str(result.error_value)```
## Related ADRs

- [ADR-002](002-clean-architecture-ddd.md) - Clean Architecture patterns
- [ADR-008](008-error-handling-strategy.md) - Detailed error handling strategy
- [ADR-010](010-testing-strategy.md) - Testing strategy for error scenarios

## Notes

**Migration Plan:**

1. Phase 1: Core services (Completed)
1. Phase 2: Adapter layer (Completed)
1. Phase 3: API layer (Completed)
1. Phase 4: Legacy code cleanup (In Progress)

**Performance Impact:**

- Minimal overhead for success paths
- Error path performance acceptable for enterprise use cases
- Memory usage within acceptable limits

**Monitoring:**

- Error rates tracked via application metrics
- Common error patterns identified for improvement
- Error context preserved for debugging
