# from flext-meltano_docs/guides/integration.md:376
from __future__ import annotations

from flext_meltano import FlextMeltanoTapAbstractions, m, p, r


def handle_discovery(name: str) -> p.Result[m.Meltano.DataSourceInstance]:
    """Consistent r patterns across all integrations."""
    abstractions = FlextMeltanoTapAbstractions()
    result = abstractions.create_tap_from_config(name, {})
    if result.failure:
        return r[m.Meltano.DataSourceInstance].fail(
            f"Integration failed: {result.error}"
        )
    return result```
### Quality Standards

**Integration Requirements**:

- Use only root-level imports from flext-meltano
- Follow r patterns for all operations
- Implement proper error handling and logging
- Maintain Singer protocol compliance
- Use FLEXT service architecture patterns

---

**Integration Guide v0.12.0-dev** - Comprehensive patterns for FLEXT ecosystem ELT integration with clear guidance on current capabilities and planned improvements.
