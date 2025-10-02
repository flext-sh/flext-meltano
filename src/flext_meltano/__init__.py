"""Enterprise Meltano integration library for FLEXT ecosystem.

This module provides a unified interface for Meltano, Singer, and DBT operations
following flext-core architectural patterns. All external access should go
through the FlextMeltanoAPI class.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.api import FlextMeltanoAPI
from flext_meltano.cli import FlextMeltanoCLI
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.config_builders import FlextMeltanoConfigBuilders
from flext_meltano.constants import FlextMeltanoConstants, PluginTypes
from flext_meltano.exceptions import FlextMeltanoExceptions
from flext_meltano.execution_result import FlextMeltanoExecutionResult
from flext_meltano.executors import FlextMeltanoExecutor
from flext_meltano.executors_bridge import FlextMeltanoBridge
from flext_meltano.file_managers import ConfigDict, FlextMeltanoFileManagers
from flext_meltano.library_runner import FlextMeltanoLibraryRunner
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.plugin_protocols import FlextMeltanoPluginProtocols
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.services import FlextMeltanoService
from flext_meltano.tap_abstractions import (
    FlextTapAbstractions,
    StreamDefinition,
    TapConfig,
    TapInstance,
)
from flext_meltano.target_abstractions import FlextTargetAbstractions
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.utilities import FlextMeltanoUtilities
from flext_meltano.validators import FlextMeltanoValidators

# Type aliases for backward compatibility (deprecated - use FlextMeltanoTypes.Processing.*)
DbtTransformationResult = FlextMeltanoTypes.Processing.DbtTransformationResult
EltPipelineResult = FlextMeltanoTypes.Processing.EltPipelineResult
SingerExecutionResult = FlextMeltanoTypes.Processing.SingerExecutionResult
SingerProcessingResult = FlextMeltanoTypes.Processing.SingerProcessingResult

# Service class aliases for backward compatibility
FlextSingerTypes = FlextMeltanoService.FlextSingerTypes

__all__ = [
    "ConfigDict",
    "DbtTransformationResult",
    "EltPipelineResult",
    "FlextMeltanoAPI",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCLI",
    "FlextMeltanoConfig",
    "FlextMeltanoConfigBuilders",
    "FlextMeltanoConstants",
    "FlextMeltanoExceptions",
    "FlextMeltanoExecutionResult",
    "FlextMeltanoExecutor",
    "FlextMeltanoFileManagers",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoModels",
    "FlextMeltanoPluginProtocols",
    "FlextMeltanoProtocols",
    "FlextMeltanoService",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "FlextSingerTypes",
    "FlextTapAbstractions",
    "FlextTargetAbstractions",
    "PluginTypes",
    "SingerExecutionResult",
    "SingerProcessingResult",
    "StreamDefinition",
    "TapConfig",
    "TapInstance",
]
