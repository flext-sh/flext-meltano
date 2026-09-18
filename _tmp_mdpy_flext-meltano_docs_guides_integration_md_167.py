# from flext-meltano_docs/guides/integration.md:167
from __future__ import annotations

from flext_meltano import (
    FlextMeltanoAdapter,
    FlextMeltanoDbtServiceBase,
    FlextMeltanoService,
    m,
    p,
    r,
    t,
)


class EnterpriseELTService(FlextMeltanoService):
    """Complete ELT pipeline for enterprise applications."""

    def __init__(self):
        super().__init__()
        self._meltano_service = FlextMeltanoService()
        self._adapter = FlextMeltanoAdapter()

    def execute_elt_pipeline(
        self, tap_name: str, target_name: str, dbt_models: t.StrSequence | None = None
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Execute complete ELT pipeline."""
        pipeline_result = self._adapter.execute()
        if pipeline_result.failure:
            return pipeline_result

        if dbt_models:
            transform_result = self._run_dbt_models(dbt_models)
            if transform_result.failure:
                return transform_result

        return r[m.Meltano.CommandExecutionResult].ok({
            "pipeline": pipeline_result.unwrap(),
            "models_executed": dbt_models or [],
        })

    def _run_dbt_models(
        self, models: t.StrSequence
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Run dbt models."""
        dbt_service = FlextMeltanoDbtServiceBase()
        return dbt_service.run_models(models)```
---

## 🔗 Bridge Communication Patterns

### Go ↔ Python Integration

**Bridge command patterns for ecosystem integration**:

