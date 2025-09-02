"""FLEXT Meltano - Enterprise Meltano/Singer SDK/DBT integration library.

This module provides enterprise-grade integration with Meltano Core, Singer SDK, and DBT Core
using FLEXT patterns and FlextResult error handling. All operations return FlextResult[T]
for composable and type-safe error handling following railway-oriented programming patterns.

Architecture:
    Foundation Layer: FlextMeltanoConstants, FlextMeltanoTypes, exceptions
    Service Layer: FlextMeltanoService, FlextMeltanoAdapter, FlextMeltanoWrapper
    Execution Layer: FlextMeltanoExecutor for CLI and command processing
    Integration Layer: Singer SDK and DBT Core native API integration

Core Components:
    FlextMeltanoAdapter: Meltano Core integration with project management and plugin operations
    FlextMeltanoService: Service layer for tap/target/DBT service implementations
    FlextMeltanoExecutor: CLI executor for command processing and bridge coordination
    FlextMeltanoWrapper: Unified wrapper for DBT/Singer/Meltano Core operations
    FlextMeltanoConstants: Meltano-specific constants extending FlextConstants
    FlextMeltanoTypes: Meltano-specific types extending FlextTypes

Examples:
    Basic adapter usage:
        >>> from flext_meltano import FlextMeltanoAdapter
        >>> adapter = FlextMeltanoAdapter()
        >>> result = adapter.get_version()
        >>> if result.success:
        ...     print(f"Meltano version: {result.value['version']}")

    Service usage:
        >>> from flext_meltano import FlextMeltanoService
        >>> service = FlextMeltanoService()
        >>> tap_service = service.TapService("tap-csv")
        >>> result = tap_service.process(config)

    Executor usage:
        >>> from flext_meltano import FlextMeltanoExecutor
        >>> executor = FlextMeltanoExecutor()
        >>> result = executor.execute_command(["discover", "plugins"])

Notes:
    - All business operations return FlextResult[T] for composability
    - Native API integration without subprocess calls
    - Enterprise-grade error handling and logging
    - Type-safe operations with proper generic parameters
    - Clean Architecture patterns with layered imports

"""

from __future__ import annotations

# =============================================================================
# VERSION DEFINITION
# =============================================================================

__version__ = "2.0.0-enterprise"

# =============================================================================
# FOUNDATION LAYER - Import first, no dependencies on other modules
# =============================================================================

from flext_meltano.constants import *
from flext_meltano.typings import *
from flext_meltano.exceptions import *

# =============================================================================
# SERVICE LAYER - Core business logic and integrations
# =============================================================================

from flext_meltano.adapters import *
from flext_meltano.services import *
from flext_meltano.wrappers import *

# =============================================================================
# EXECUTION LAYER - Command processing and execution
# =============================================================================

from flext_meltano.executors import *
from flext_meltano.executors_bridge import *

# Import bridge class specifically for export
from flext_meltano.executors_bridge import FlextMeltanoBridge

# Create MeltanoBridge alias for backward compatibility
MeltanoBridge = FlextMeltanoBridge

# =============================================================================
# INTEGRATION LAYER - External library integrations
# =============================================================================

from flext_meltano.singer_adapters import *

# =============================================================================
# SUPPORT LAYER - Utilities, config, validation
# =============================================================================

from flext_meltano.config import *
from flext_meltano.utilities import *
from flext_meltano.validators import *

# =============================================================================
# CONSOLIDATED EXPORTS - Combine all __all__ from modules
# =============================================================================

# Combine all __all__ exports from imported modules
import flext_meltano.constants as _constants
import flext_meltano.typings as _typings
import flext_meltano.exceptions as _exceptions
import flext_meltano.adapters as _adapters
import flext_meltano.services as _services
import flext_meltano.wrappers as _wrappers
import flext_meltano.executors as _executors
import flext_meltano.executors_bridge as _executors_bridge
import flext_meltano.singer_adapters as _singer_adapters
import flext_meltano.config as _config
import flext_meltano.utilities as _utilities
import flext_meltano.validators as _validators


# Collect all __all__ exports from imported modules with explicit type safety
def _collect_module_exports() -> list[str]:
    """Collect and deduplicate exports from all modules."""
    temp_exports: list[str] = []

    for module in [
        _constants,
        _typings,
        _exceptions,
        _adapters,
        _services,
        _wrappers,
        _executors,
        _executors_bridge,
        _singer_adapters,
        _config,
        _utilities,
        _validators,
    ]:
        if hasattr(module, "__all__"):
            module_exports = getattr(module, "__all__", [])
            if isinstance(module_exports, list):
                temp_exports.extend(module_exports)

    # Remove duplicates and sort
    seen: set[str] = set()
    final_exports: list[str] = []
    for item in temp_exports:
        if item not in seen and isinstance(item, str):
            seen.add(item)
            final_exports.append(item)

    final_exports.sort()
    return final_exports


# Define __all__ with explicit type safety - no ignore needed
# Note: __all__ must be static for Ruff compliance, using dynamic collection at runtime
__all__ = [
    # This will be populated by the module initialization
]

# Populate __all__ dynamically at import time
_dynamic_exports = _collect_module_exports()
__all__ += _dynamic_exports

# =============================================================================
# NO LEGACY COMPATIBILITY - CLASS-BASED API ONLY
# =============================================================================
