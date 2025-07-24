"""FlextMeltano Core Module.

Core platform components following Clean Architecture patterns.
"""

from flext_meltano.core.platform import FlextMeltanoPlatform
from flext_meltano.core.runtime import FlextMeltanoRuntime

# FlextMeltano prefixed classes
from .config import FlextMeltanoConfig
from .executor import FlextMeltanoExecutor

__all__ = [
    "FlextMeltanoConfig",
    "FlextMeltanoExecutor",
    "FlextMeltanoPlatform",
    "FlextMeltanoRuntime",
]
