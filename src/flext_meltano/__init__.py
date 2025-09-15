"""Enterprise Meltano integration library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.config_builders import FlextMeltanoConfigBuilders
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.exceptions import FlextMeltanoConfigurationError, FlextMeltanoError
from flext_meltano.executors import FlextMeltanoExecutor
from flext_meltano.executors_bridge import FlextMeltanoBridge

# FlextMeltanoCli functionality available through FlextMeltanoExecutor.create_cli_runner
# Executor functionality available through FlextMeltanoExecutor directly
# No compatibility wrappers - use FlextMeltanoExecutor unified class
from flext_meltano.file_managers import FlextMeltanoFileManagers
from flext_meltano.plugin_protocols import (
    DbtServiceProtocol,
    FlextDbtPlugin,
    FlextMeltanoPluginProtocols,  # Updated unified class name
    FlextTapPlugin,
    FlextTargetPlugin,
    TapServiceProtocol,
    TargetServiceProtocol,
)

# Service implementations available through FlextMeltanoService methods:
# FlextMeltanoService.create_tap_service, create_target_service, create_dbt_service
from flext_meltano.services import FlextMeltanoService
from flext_meltano.singer_types import FlextSingerTypes
from flext_meltano.tap_abstractions import (
    FlextTapAbstractions,
    StreamDefinition,
    TapConfig,
    TapInstance,
)
from flext_meltano.target_abstractions import (
    FlextTargetAbstractions,
)

# Exception handling - DIRECT flext-core generated exceptions only
# Core executors
# CLI executors
# Meltano executors
# Plugin protocols
# Service implementations
# Singer types and abstractions
# Utilities and validation
# Import test compatibility classes and functions from dedicated module
# NOTE: Test compatibility classes available through existing abstraction modules
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.utilities import FlextMeltanoUtilities
from flext_meltano.validators import FlextMeltanoValidators

__all__ = [
    "DbtServiceProtocol",
    "FlextDbtPlugin",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    # "FlextMeltanoCli",  # Use FlextMeltanoExecutor.create_cli_runner
    "FlextMeltanoConfig",
    "FlextMeltanoConfigBuilders",
    "FlextMeltanoConfigurationError",
    "FlextMeltanoConstants",
    # "FlextMeltanoDbtService",  # Use FlextMeltanoService.create_dbt_service
    "FlextMeltanoError",
    "FlextMeltanoExecutor",
    # "FlextMeltanoExecutors",  # Use FlextMeltanoExecutor directly
    "FlextMeltanoFileManagers",
    "FlextMeltanoPluginProtocols",  # Updated unified class name
    "FlextMeltanoService",
    # "FlextMeltanoTapService",  # Use FlextMeltanoService.create_tap_service
    # "FlextMeltanoTargetService",  # Use FlextMeltanoService.create_target_service
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "FlextSingerTypes",
    "FlextTapAbstractions",
    "FlextTapPlugin",
    "FlextTargetAbstractions",
    "FlextTargetPlugin",
    # "SimpleDbtExecutor",     # Use FlextMeltanoExecutor directly
    # "SimpleMeltanoExecutor", # Use FlextMeltanoExecutor directly
    "StreamDefinition",
    "TapConfig",
    "TapInstance",
    "TapServiceProtocol",
    "TargetServiceProtocol",
    # "flext_meltano_run_cli",  # Use FlextMeltanoExecutor.create_cli_runner
]
