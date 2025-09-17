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
from flext_meltano.plugin_protocols import FlextMeltanoPluginProtocols
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
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.utilities import FlextMeltanoUtilities
from flext_meltano.validators import FlextMeltanoValidators

# NO ALIASES - Use FlextMeltanoPluginProtocols directly for all protocol access

__all__ = [
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
    "FlextMeltanoPluginProtocols",  # Main unified class - NO ALIASES
    "FlextMeltanoService",
    # "FlextMeltanoTapService",  # Use FlextMeltanoService.create_tap_service
    # "FlextMeltanoTargetService",  # Use FlextMeltanoService.create_target_service
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "FlextSingerTypes",
    "FlextTapAbstractions",
    "FlextTargetAbstractions",
    # "FlextMeltanoSimpleDbtExecutor",     # Use FlextMeltanoExecutor directly
    # "FlextMeltanoSimpleExecutor", # Use FlextMeltanoExecutor directly
    "StreamDefinition",
    "TapConfig",
    "TapInstance",
    # "flext_meltano_run_cli",  # Use FlextMeltanoExecutor.create_cli_runner
]
