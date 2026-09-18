# from flext-meltano_docs/architecture/adr/002-clean-architecture-ddd.md:207
from __future__ import annotations


# Service initialization with dependencies
@dataclass
class FlextMeltanoService:
    config_validator: ConfigValidator
    meltano_adapter: MeltanoAdapter
    dbt_adapter: FlextMeltanoAdapter.Dbt

    def execute_pipeline(self, pipeline: Pipeline) -> p.Result[ExecutionResult]:
        # Use injected dependencies
        return (
            self.config_validator
            .validate(pipeline.settings)
            .flat_map(lambda _: self.meltano_adapter.run_pipeline(pipeline))
            .flat_map(lambda result: self.dbt_adapter.run_transformations(result))
        )```
## Related ADRs

- [ADR-001](001-railway-oriented-programming.md) - Error handling patterns
- [ADR-003](003-singer-protocol-abstraction.md) - Protocol abstraction layer

## Notes

**Evolution Considerations:**

- Start with basic layered structure
- Add complexity only when justified by use cases
- Monitor for over-engineering and simplify when possible
- Consider hexagonal architecture for future growth

**Performance Impact:**

- Minimal impact on normal operation paths
- Test performance improved due to isolation
- Development velocity improved due to clear boundaries

**Team Adoption:**

- Training provided on layered architecture concepts
- Code reviews enforce layer boundary rules
- Automated tools validate architectural compliance
