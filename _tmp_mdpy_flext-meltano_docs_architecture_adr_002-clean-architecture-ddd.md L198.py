# from flext-meltano/docs/architecture/adr/002-clean-architecture-ddd.md:198
from __future__ import annotations


# services.py
def execute_pipeline(self, pipeline: Pipeline) -> p.Result[ExecutionResult]:
    return self.meltano_adapter.run_pipeline(pipeline)```
### Dependency Injection

