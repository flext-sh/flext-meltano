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
# FOUNDATION LAYER - Import first, no dependencies on other modules
# =============================================================================

from flext_meltano.constants import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_meltano.typings import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_meltano.exceptions import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403

# =============================================================================
# SERVICE LAYER - Core business logic and integrations
# =============================================================================

from flext_meltano.adapters import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_meltano.services import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_meltano.wrappers import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403

# =============================================================================
# EXECUTION LAYER - Command processing and execution
# =============================================================================

from flext_meltano.executors import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_meltano.executors_bridge import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403

# =============================================================================
# INTEGRATION LAYER - External library integrations
# =============================================================================

from flext_meltano.singer_adapters import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403

# =============================================================================
# SUPPORT LAYER - Utilities, config, validation
# =============================================================================

from flext_meltano.config import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_meltano.utilities import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403
from flext_meltano.validators import *  # type: ignore[unused-ignore,reportWildcardImport,assignment] # noqa: F403

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

# Collect all __all__ exports from imported modules
_temp_exports: list[str] = []

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
        _temp_exports.extend(module.__all__)

# Remove duplicates and sort for consistent exports - build complete list first
_seen: set[str] = set()
_final_exports: list[str] = []
for item in _temp_exports:
    if item not in _seen:
        _seen.add(item)
        _final_exports.append(item)
_final_exports.sort()

# Define __all__ as literal list for linter compatibility
# This dynamic assignment is necessary for aggregating module exports
__all__: list[str] = _final_exports  # pyright: ignore[reportUnsupportedDunderAll] # noqa: PLE0605

# =============================================================================
# BACKWARD COMPATIBILITY ALIASES
# =============================================================================

# Legacy validation function alias
from flext_meltano.validators import validate_config_value_simple as validate_config_value  # noqa: E402

# Legacy bridge aliases
from flext_meltano.executors_bridge import FlextMeltanoBridge as MeltanoBridge  # noqa: E402

# Legacy wrapper aliases
from flext_meltano.wrappers import FlextMeltanoWrapper  # noqa: E402
MeltanoDbtWrapper = FlextMeltanoWrapper.DbtWrapper

# Legacy service implementation aliases
from flext_meltano.service_implementations import (  # noqa: E402
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
    FlextMeltanoDbtService,
)

# Singer SDK re-exports for backward compatibility
from singer_sdk import Stream, Tap, Target  # noqa: E402
from singer_sdk.sinks import Sink  # noqa: E402
from singer_sdk.typing import PropertiesList, Property  # noqa: E402
import singer_sdk.typing as singer_typing  # noqa: E402


# Legacy factory functions for backward compatibility
def get_tap_test_class(tap_name: str, config: dict[str, object] | None = None) -> type[Tap]:  # noqa: E402
    """Legacy factory function for tap test classes."""
    class TestTap(Tap):
        name = tap_name
        config = config or {}
    return TestTap


# Add to exports dynamically (use += for type checker compatibility)
__all__ += [
    "validate_config_value",
    "MeltanoBridge",
    "MeltanoDbtWrapper",
    "FlextMeltanoTapService",
    "FlextMeltanoTargetService",
    "FlextMeltanoDbtService",
    # Singer SDK re-exports
    "Stream",
    "Tap",
    "Target",
    "Sink",
    "PropertiesList",
    "Property",
    "singer_typing",
    "get_tap_test_class",
]
