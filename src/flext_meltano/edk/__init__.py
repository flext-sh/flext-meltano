"""FlextMeltano EDK Integration Module.

Meltano EDK extension development and management following Clean
Architecture patterns.
"""

from flext_meltano.edk.extension import FlextMeltanoExtension
from flext_meltano.edk.manager import FlextMeltanoExtensionManager

__all__ = [
    "FlextMeltanoExtension",
    "FlextMeltanoExtensionManager",
]
