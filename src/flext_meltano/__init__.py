"""Enterprise Meltano integration library for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.config_builders import FlextMeltanoConfigBuilders
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.exceptions import FlextMeltanoExceptions
from flext_meltano.executors import FlextMeltanoExecutor
from flext_meltano.executors_bridge import FlextMeltanoBridge
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

__all__ = [
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    "FlextMeltanoConfigBuilders",
    "FlextMeltanoConstants",
    "FlextMeltanoExceptions",
    "FlextMeltanoExecutor",
    "FlextMeltanoFileManagers",
    "FlextMeltanoPluginProtocols",
    "FlextMeltanoService",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "FlextSingerTypes",
    "FlextTapAbstractions",
    "FlextTargetAbstractions",
    "StreamDefinition",
    "TapConfig",
    "TapInstance",
]
