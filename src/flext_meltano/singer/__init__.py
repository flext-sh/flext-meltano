"""FlextMeltano Singer SDK Integration Module.

Singer protocol implementation for taps and targets following Clean
Architecture patterns.
"""

from flext_meltano.singer.catalog import FlextMeltanoCatalog
from flext_meltano.singer.stream import FlextMeltanoStream
from flext_meltano.singer.tap import FlextMeltanoTap
from flext_meltano.singer.target import FlextMeltanoTarget

__all__ = [
    "FlextMeltanoCatalog",
    "FlextMeltanoStream",
    "FlextMeltanoTap",
    "FlextMeltanoTarget",
]
