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
from flext_meltano.executors_cli import FlextMeltanoCli, flext_meltano_run_cli
from flext_meltano.executors_meltano import (
    FlextMeltanoExecutors,
    SimpleDbtExecutor,
    SimpleMeltanoExecutor,
)
from flext_meltano.file_managers import FlextMeltanoFileManagers
from flext_meltano.plugin_protocols import (
    DbtServiceProtocol,
    FlextDbtPlugin,
    FlextMeltanoPluginTypes,
    FlextTapPlugin,
    FlextTargetPlugin,
    TapServiceProtocol,
    TargetServiceProtocol,
)
from flext_meltano.service_implementations import (
    FlextMeltanoDbtService,
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
)
from flext_meltano.services import FlextMeltanoService
from flext_meltano.singer_types import FlextSingerTypes
from flext_meltano.tap_abstractions import (
    FlextTapAbstractions,
    StreamDefinition,
    TapConfig,
    TapInstance,
)
from flext_meltano.target_abstractions import (
    FlextStreamInfo,
    FlextTargetAbstractions,
    FlextTargetConfig,
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
    "FlextMeltanoCli",
    "FlextMeltanoConfig",
    "FlextMeltanoConfigBuilders",
    "FlextMeltanoConfigurationError",
    "FlextMeltanoConstants",
    "FlextMeltanoDbtService",
    "FlextMeltanoError",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutors",
    "FlextMeltanoFileManagers",
    "FlextMeltanoPluginTypes",
    "FlextMeltanoService",
    "FlextMeltanoTapService",
    "FlextMeltanoTargetService",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "FlextSingerTypes",
    "FlextStreamInfo",
    "FlextTapAbstractions",
    "FlextTapPlugin",
    "FlextTargetAbstractions",
    "FlextTargetConfig",
    "FlextTargetPlugin",
    "SimpleDbtExecutor",
    "SimpleMeltanoExecutor",
    "StreamDefinition",
    "TapConfig",
    "TapInstance",
    "TapServiceProtocol",
    "TargetServiceProtocol",
    "flext_meltano_run_cli",
]
