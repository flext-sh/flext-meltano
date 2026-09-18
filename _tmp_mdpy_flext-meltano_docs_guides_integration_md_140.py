# from flext-meltano_docs/guides/integration.md:140
from __future__ import annotations

from flext_meltano import FlextMeltanoDbtServiceBase, p, t


class FlextOracleDbtService(FlextMeltanoDbtServiceBase):
    """Oracle dbt transformations using flext-meltano."""

    @property
    def connection_profile(self) -> p.Meltano.DbtConnectionProfile:
        """Oracle dbt connection profile."""
        raise NotImplementedError

    def run_oracle_models(self, models: t.StrSequence) -> p.Result[t.JsonMapping]:
        """Execute Oracle-specific dbt models."""
        return self.run_models(models)```
**Current Limitation**: dbt integration is placeholder implementation requiring dbt programmatic API integration.

---

## 🚀 Complete ELT Pipeline Integration

### Enterprise Pipeline Pattern

**Full ELT workflow using flext-meltano foundation**:

