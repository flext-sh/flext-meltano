"""FLEXT Meltano - Enterprise Meltano/Singer SDK/DBT integration library.

High-level Meltano integration library providing type-safe, railway-oriented programming
patterns for ELT pipeline operations with Singer SDK and DBT Core.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import FlextTypes


# =============================================================================
# VERSION DEFINITION
# =============================================================================

__version__ = "2.0.0-enterprise"

# =============================================================================
# FOUNDATION LAYER - Import first, no dependencies on other modules
# =============================================================================

# Constants and types
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.typings import FlextMeltanoTypes

# Exception handling
from flext_meltano.exceptions import (
    FlextMeltanoAuthenticationError,
    FlextMeltanoConfigurationError,
    FlextMeltanoConnectionError,
    FlextMeltanoDBTError,
    FlextMeltanoError,
    FlextMeltanoExceptions,
    FlextMeltanoExecutionError,
    FlextMeltanoPluginError,
    FlextMeltanoProcessingError,
    FlextMeltanoSingerError,
    FlextMeltanoTimeoutError,
    FlextMeltanoValidationError,
)

# =============================================================================
# SERVICE LAYER - Core business logic and integrations
# =============================================================================

# Core adapters and services
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.services import FlextMeltanoService

# Service implementations
from flext_meltano.service_implementations import (
    FlextMeltanoDbtService,
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
)

# Plugin protocols
from flext_meltano.plugin_protocols import (
    DbtServiceProtocol,
    FlextDbtPlugin,
    FlextMeltanoPluginTypes,
    FlextTapPlugin,
    FlextTargetPlugin,
    TapServiceProtocol,
    TargetServiceProtocol,
)

# =============================================================================
# EXECUTION LAYER - Command processing and execution
# =============================================================================

# Core executors
from flext_meltano.executors import FlextMeltanoExecutor
from flext_meltano.executors_bridge import FlextMeltanoBridge

# CLI executors
from flext_meltano.executors_cli import (
    FlextMeltanoCli,
    flext_meltano_run_cli,
)

# Meltano executors
from flext_meltano.executors_meltano import (
    FlextExecutionResult,
    FlextMeltanoExecutors,
    SimpleDbtExecutor,
    SimpleMeltanoExecutor,
)

# =============================================================================
# INTEGRATION LAYER - External library integrations
# =============================================================================


# =============================================================================
# COMPLETE ABSTRACTION LAYER - Zero dependency on singer_sdk/meltano/dbt
# =============================================================================

# Singer types and abstractions
from flext_meltano.singer_types import FlextSingerTypes
from flext_meltano.tap_abstractions import (
    FlextTapAbstractions,
    StreamDefinition,
    TapConfig,
    TapInstance,
)
from flext_meltano.target_abstractions import FlextTargetAbstractions

# =============================================================================
# SUPPORT LAYER - Utilities, config, validation
# =============================================================================

# Configuration and builders
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.config_builders import FlextMeltanoConfigBuilders

# Utilities and validation
from flext_meltano.utilities import FlextMeltanoUtilities
from flext_meltano.validators import FlextMeltanoValidators
from flext_meltano.file_managers import FlextMeltanoFileManagers

# =============================================================================
# MANUAL PUBLIC EXPORTS - All public classes explicitly listed
# =============================================================================

__all__ = [
    # Foundation Layer
    "FlextMeltanoConstants",
    "FlextMeltanoTypes",
    # Exception handling
    "FlextMeltanoAuthenticationError",
    "FlextMeltanoConfigurationError",
    "FlextMeltanoConnectionError",
    "FlextMeltanoDBTError",
    "FlextMeltanoError",
    "FlextMeltanoExceptions",
    "FlextMeltanoExecutionError",
    "FlextMeltanoPluginError",
    "FlextMeltanoProcessingError",
    "FlextMeltanoSingerError",
    "FlextMeltanoTimeoutError",
    "FlextMeltanoValidationError",
    # Service Layer
    "FlextMeltanoAdapter",
    "FlextMeltanoService",
    "FlextMeltanoDbtService",
    "FlextMeltanoTapService",
    "FlextMeltanoTargetService",
    # Plugin protocols
    "DbtServiceProtocol",
    "FlextDbtPlugin",
    "FlextMeltanoPluginTypes",
    "FlextTapPlugin",
    "FlextTargetPlugin",
    "TapServiceProtocol",
    "TargetServiceProtocol",
    # Execution Layer
    "FlextMeltanoExecutor",
    "FlextMeltanoBridge",
    "FlextMeltanoCli",
    "flext_meltano_run_cli",
    "FlextExecutionResult",
    "FlextMeltanoExecutors",
    "SimpleDbtExecutor",
    "SimpleMeltanoExecutor",
    # Integration Layer
    "FlextSingerTypes",
    "FlextTapAbstractions",
    "StreamDefinition",
    "TapConfig",
    "TapInstance",
    "FlextTargetAbstractions",
    # Support Layer
    "FlextMeltanoConfig",
    "FlextMeltanoConfigBuilders",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "FlextMeltanoFileManagers",
]
