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
# All adapter functionality consolidated in adapters.py

# =============================================================================
# EXECUTION LAYER - Command processing and execution
# =============================================================================

from flext_meltano.executors import *
from flext_meltano.executors_bridge import *

# =============================================================================
# INTEGRATION LAYER - External library integrations
# =============================================================================


# =============================================================================
# COMPLETE ABSTRACTION LAYER - Zero dependency on singer_sdk/meltano/dbt
# =============================================================================

from flext_meltano.singer_types import *
from flext_meltano.tap_abstractions import *
from flext_meltano.target_abstractions import *

# =============================================================================
# SUPPORT LAYER - Utilities, config, validation
# =============================================================================

from flext_meltano.config import *
from flext_meltano.utilities import *
from flext_meltano.validators import *
from flext_meltano.file_managers import *
from flext_meltano.config_builders import *

# =============================================================================
# CONSOLIDATED EXPORTS - Combine all __all__ from modules
# =============================================================================

# Import all modules for __all__ aggregation
import flext_meltano.constants as _constants
import flext_meltano.typings as _typings
import flext_meltano.exceptions as _exceptions
import flext_meltano.adapters as _adapters
import flext_meltano.services as _services
import flext_meltano.executors as _executors
import flext_meltano.executors_bridge as _executors_bridge
import flext_meltano.singer_types as _singer_types
import flext_meltano.tap_abstractions as _tap_abstractions
import flext_meltano.target_abstractions as _target_abstractions
import flext_meltano.config as _config
import flext_meltano.utilities as _utilities
import flext_meltano.validators as _validators
import flext_meltano.file_managers as _file_managers
import flext_meltano.config_builders as _config_builders

# Collect all __all__ exports from imported modules
_temp_exports: list[str] = []

for module in [
    _constants,
    _typings,
    _exceptions,
    _adapters,
    _services,
    _executors,
    _executors_bridge,
    _singer_types,
    _tap_abstractions,
    _target_abstractions,
    _config,
    _utilities,
    _validators,
    _file_managers,
    _config_builders,
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
__all__: list[str] = _final_exports  # noqa: PLE0605 # type: ignore[reportUnsupportedDunderAll]

# =============================================================================
# COMPLETE MODULE AGGREGATION - All exports collected dynamically
# =============================================================================
