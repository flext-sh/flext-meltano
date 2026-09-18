# from flext-meltano/docs/architecture/adr/003-singer-protocol-abstraction.md:197
from __future__ import annotations


class FlextMeltanoStream:
    def get_records(self, context: Optional[dict]) -> Iterator[dict]:
        """Get records with FLEXT state management."""
        try:
            # Singer SDK record retrieval
            for record in super().get_records(context):
                # FLEXT state updates
                self.update_bookmark(record)
                yield record
        except Exception as e:
            # FLEXT error handling
            logger.error(f"Record retrieval failed: {e}")
            raise SingerStreamError(f"Stream {self.name} failed: {e}")```
## Related ADRs

- [ADR-001](001-railway-oriented-programming.md) - Error handling patterns
- [ADR-002](002-clean-architecture-ddd.md) - Architecture layering
- [ADR-004](004-type-safety-first.md) - Type safety requirements

## Notes

**SDK Compatibility:**

- Tested with Singer SDK v0.44.0
- Compatibility layer for major version changes
- Automated testing against multiple SDK versions

**Performance Considerations:**

- Minimal overhead for normal operations
- Error paths optimized for fast failure
- Memory usage within acceptable limits

**Migration Path:**

- Existing direct SDK usage migrated incrementally
- New implementations use abstraction layer exclusively
- Legacy code wrapped with compatibility adapters
