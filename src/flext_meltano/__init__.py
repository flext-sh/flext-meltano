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
# FOUNDATION LAYER - Import using modern aggregation pattern
# =============================================================================

# Import specific classes to avoid F405 errors
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.exceptions import FlextMeltanoExceptions

# =============================================================================
# SERVICE LAYER - Core business logic and integrations
# =============================================================================

from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.services import FlextMeltanoService
from flext_meltano.wrappers import FlextMeltanoWrapper

# =============================================================================
# EXECUTION LAYER - Command processing and execution
# =============================================================================

from flext_meltano.executors import FlextMeltanoExecutor
from flext_meltano.executors_bridge import FlextMeltanoBridge

# Import bridge class specifically for export

# Create MeltanoBridge alias for backward compatibility
MeltanoBridge = FlextMeltanoBridge

# =============================================================================
# INTEGRATION LAYER - External library integrations
# =============================================================================

from flext_meltano.singer_adapters import FlextMeltanoAdapters
from flext_meltano.flext_type_adapters import (
    FlextMeltanoTypeAdapters,
    FlextTap,
    FlextTarget,
    FlextSingerStream,
    FlextMeltanoProject,
    FlextDbt,
)

# =============================================================================
# COMPLETE ABSTRACTION LAYER - Zero dependency on singer_sdk/meltano/dbt
# =============================================================================

from flext_meltano.flext_singer_types import (
    FlextSingerTypes,
    StringType,
    IntegerType,
    NumberType,
    BooleanType,
    DateTimeType,
    ArrayType,
    ObjectType,
    FlextSingerSchema,
    FlextSingerRecord,
    FlextSingerState,
    FlextPropertiesList,
)

from flext_meltano.flext_tap_abstractions import (
    FlextTap as FlextTapAbstract,
    FlextTapConfig,
    FlextTapStream,
    create_flext_tap_config,
)

from flext_meltano.flext_target_abstractions import (
    FlextTarget as FlextTargetAbstract, 
    FlextTargetConfig,
    FlextTargetStream,
    create_flext_target_config,
)

# =============================================================================
# SUPPORT LAYER - Utilities, config, validation
# =============================================================================

from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.utilities import FlextMeltanoUtilities
from flext_meltano.validators import FlextMeltanoValidators
from flext_meltano.file_managers import FlextMeltanoFileManagers
from flext_meltano.config_builders import FlextMeltanoConfigBuilders

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


# Define __all__ with static exports - Ruff compliance
__all__ = [
    # Foundation Layer exports - REAL CLASSES
    "FlextMeltanoConstants",
    "FlextMeltanoTypes",
    "FlextMeltanoExceptions",  # This is the real class name

    # Service Layer exports - REAL CLASSES
    "FlextMeltanoAdapter",
    "FlextMeltanoService",
    "FlextMeltanoWrapper",

    # Execution Layer exports - REAL CLASSES
    "FlextMeltanoExecutor",
    "FlextMeltanoBridge",
    "MeltanoBridge",  # Backward compatibility alias

    # Integration Layer exports - REAL CLASSES
    "FlextMeltanoAdapters",  # This is the real class name from singer_adapters

    # Modern Type Adapters exports - REAL CLASSES
    "FlextMeltanoTypeAdapters",
    "FlextTap",
    "FlextTarget",
    "FlextSingerStream",
    "FlextMeltanoProject",
    "FlextDbt",

    # Complete Abstraction Layer - ZERO DEPENDENCY on singer_sdk/meltano/dbt
    "FlextSingerTypes",
    "StringType",
    "IntegerType",
    "NumberType", 
    "BooleanType",
    "DateTimeType",
    "ArrayType",
    "ObjectType",
    "FlextSingerSchema",
    "FlextSingerRecord",
    "FlextSingerState",
    "FlextPropertiesList",
    
    # Tap Abstractions - Complete Singer Tap functionality
    "FlextTapAbstract",
    "FlextTapConfig",
    "FlextTapStream",
    "create_flext_tap_config",
    
    # Target Abstractions - Complete Singer Target functionality
    "FlextTargetAbstract",
    "FlextTargetConfig", 
    "FlextTargetStream",
    "create_flext_target_config",

    # Support Layer exports - REAL CLASSES
    "FlextMeltanoConfig",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",  # This is the real class name
    "FlextMeltanoFileManagers",
    "FlextMeltanoConfigBuilders",
]

# =============================================================================
# NO LEGACY COMPATIBILITY - CLASS-BASED API ONLY
# =============================================================================
