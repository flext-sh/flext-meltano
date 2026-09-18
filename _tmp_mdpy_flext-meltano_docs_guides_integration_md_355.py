# from flext-meltano_docs/guides/integration.md:355
from __future__ import annotations

from flext_core import FlextContainer
from flext_meltano import FlextMeltanoTapAbstractions, FlextMeltanoTargetAbstractions

# Register services for ecosystem consumption
container = FlextContainer.shared()
container.bind("tap_abstractions", FlextMeltanoTapAbstractions)
container.bind("target_abstractions", FlextMeltanoTargetAbstractions)```
**2. Configuration Management**:

