# from flext-meltano_docs/architecture/adr/003-singer-protocol-abstraction.md:150
from __future__ import annotations


# Base abstractions
class FlextMeltanoSingerBase:
    """Base class for all Singer operations with FLEXT patterns."""


class FlextMeltanoTap(FlextMeltanoSingerBase, SingerTap):
    """FLEXT tap abstraction with railway-oriented error handling."""


class FlextMeltanoTarget(FlextMeltanoSingerBase, SingerTarget):
    """FLEXT target abstraction with railway-oriented error handling."""


class FlextMeltanoStream(FlextMeltanoSingerBase):
    """Stream abstraction with FLEXT state management."""```
### Error Handling Integration

