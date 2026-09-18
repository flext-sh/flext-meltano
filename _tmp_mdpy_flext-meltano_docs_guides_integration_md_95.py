# from flext-meltano_docs/guides/integration.md:95
from __future__ import annotations

from typing import Annotated

from flext_meltano import (
    FlextMeltanoTargetAbstractions,
    FlextMeltanoTargetServiceBase,
    m,
    p,
    t,
    u,
)


class FlextOracleTargetService(FlextMeltanoTargetServiceBase):
    """Oracle target using flext-meltano Singer abstractions."""

    target_name: Annotated[
        t.NonEmptyStr, u.Field(description="Canonical target name (e.g. target-oracle)")
    ] = "target-oracle"

    def create_sink(
        self, stream_name: str, schema: t.JsonMapping
    ) -> p.Meltano.SingerDrainSink:
        """Create an Oracle sink for a Singer stream."""
        raise NotImplementedError

    def load_to_oracle(
        self, records: list, settings: dict
    ) -> p.Result[m.Meltano.DataSinkInstance]:
        """Load records to Oracle using flext-meltano abstractions."""
        abstractions = FlextMeltanoTargetAbstractions()
        return abstractions.create_flext_target({
            "sink_type": "target-oracle",
            "connection_config": settings,
        })```
---

## 🛠️ dbt Integration Patterns

### dbt Project Foundation

\__Standard pattern for flext-dbt-_ projects\_\*:

