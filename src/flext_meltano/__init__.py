"""Enterprise Meltano integration library for FLEXT ecosystem.

This module provides a unified interface for Meltano, Singer, and DBT operations
following flext-core architectural patterns. All external access should go
through the FlextMeltanoAPI class.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.api import FlextMeltanoAPI
from flext_meltano.bridge import FlextMeltanoBridge
from flext_meltano.cli import FlextMeltanoCLI
from flext_meltano.config import (
    FlextMeltanoConfig,
)
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.dbt_service import FlextMeltanoDbtService
from flext_meltano.exceptions import FlextMeltanoExceptions
from flext_meltano.execution_result import FlextMeltanoExecutionResult
from flext_meltano.executor import FlextMeltanoExecutor
from flext_meltano.file_managers import FlextMeltanoFileManagers
from flext_meltano.library_runner import FlextMeltanoLibraryRunner
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.pipeline_service import FlextMeltanoPipelineService
from flext_meltano.plugin_protocols import FlextMeltanoPluginProtocols
from flext_meltano.plugin_service import FlextMeltanoPluginService
from flext_meltano.project_service import FlextMeltanoProjectService
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.services import FlextMeltanoService

# Singer SDK wrapper classes for domain separation
from flext_meltano.singer import (
    FlextMeltanoSinger,
    FlextSink,
    FlextStream,
    FlextTap,
    FlextTapAbstractions,
    FlextTarget,
    FlextTargetAbstractions,
    StreamDefinition,
    TapConfig,
    TapInstance,
)

# Singer types and typing utilities are in FlextMeltanoTypes.Singer namespace
# ALL tap/target projects MUST use FlextMeltanoTypes.Singer.Typing for schema definitions
from flext_meltano.typings import (
    # Export specific types for backward compatibility
    FlextMeltanoTypes,
)
from flext_meltano.utilities import FlextMeltanoUtilities
from flext_meltano.validators import FlextMeltanoValidators

# Type aliases for backward compatibility
DbtTransformationResult = FlextMeltanoTypes.Processing.DbtTransformationResult
EltPipelineResult = FlextMeltanoTypes.Processing.EltPipelineResult
SingerExecutionResult = FlextMeltanoTypes.Processing.SingerExecutionResult

# Type aliases for backward compatibility

# Service class aliases for backward compatibility
FlextSingerTypes = FlextMeltanoTypes
FlextSingerStream = (
    StreamDefinition  # Alias for backward compatibility with tap/target projects
)

__all__ = [
    "ConfigDict",
    "DbtTransformationResult",
    "EltPipelineResult",
    "FlextMeltanoAPI",
    "FlextMeltanoAbstractions",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCLI",
    "FlextMeltanoConfig",
    "FlextMeltanoConstants",
    "FlextMeltanoDbtService",
    "FlextMeltanoExceptions",
    "FlextMeltanoExecutionResult",
    "FlextMeltanoExecutor",
    "FlextMeltanoFileManagers",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoModels",
    "FlextMeltanoPipelineService",
    "FlextMeltanoPluginProtocols",
    "FlextMeltanoPluginService",
    "FlextMeltanoProjectService",
    "FlextMeltanoProtocols",
    "FlextMeltanoService",
    "FlextMeltanoSinger",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "FlextSingerStream",
    "FlextSingerTypes",
    "FlextSink",  # Singer SDK wrapper for domain separation
    "FlextStream",  # Singer SDK wrapper for domain separation
    "FlextTap",  # Singer SDK wrapper for domain separation
    "FlextTapAbstractions",
    "FlextTarget",  # Singer SDK wrapper for domain separation
    "FlextTargetAbstractions",
    "PluginTypes",
    "SingerExecutionResult",
    "StreamDefinition",
    "TapConfig",
    "TapInstance",
]
