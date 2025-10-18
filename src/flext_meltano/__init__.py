"""Enterprise Pipeline integration library for FLEXT ecosystem.

This module provides a unified interface for data pipeline operations
following flext-core architectural patterns. All external access should go
through the FlextPipelineAPI class.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from singer_sdk import Stream as FlextPipelineStream, Tap as FlextPipelineTap

from flext_meltano.__version__ import __version__, __version_info__
from flext_meltano.abstractions import FlextPipelineAbstractions
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.api import FlextPipeline
from flext_meltano.bridge import FlextMeltanoBridge
from flext_meltano.cli import FlextMeltanoCLI
from flext_meltano.config import FlextPipelineConfig
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.dbt_service import FlextPipelineTransformationService
from flext_meltano.execution_result import FlextMeltanoExecutionResult
from flext_meltano.executor import FlextMeltanoExecutor
from flext_meltano.file_managers import FlextMeltanoFileManagers
from flext_meltano.library_runner import FlextMeltanoLibraryRunner
from flext_meltano.models import FlextPipelineModels
from flext_meltano.pipeline_service import FlextPipelineOrchestrationService
from flext_meltano.plugin_protocols import FlextMeltanoPluginProtocols
from flext_meltano.plugin_service import FlextPipelineComponentService
from flext_meltano.project_service import FlextPipelineProjectService
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.services import FlextPipelineService
from flext_meltano.singer import FlextMeltanoSinger
from flext_meltano.singer_cli_translator import FlextPipelineSingerCliTranslator
from flext_meltano.tap_abstractions import FlextPipelineSourceAbstractions
from flext_meltano.target_abstractions import FlextPipelineSinkAbstractions
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.utilities import FlextMeltanoUtilities
from flext_meltano.validators import FlextPipelineValidators

__all__ = [
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCLI",
    "FlextMeltanoConstants",
    "FlextMeltanoExecutionResult",
    "FlextMeltanoExecutor",
    "FlextMeltanoFileManagers",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoPluginProtocols",
    "FlextMeltanoProtocols",
    "FlextMeltanoSinger",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextPipeline",
    "FlextPipelineAbstractions",
    "FlextPipelineComponentService",
    "FlextPipelineConfig",
    "FlextPipelineModels",
    "FlextPipelineOrchestrationService",
    "FlextPipelineProjectService",
    "FlextPipelineService",
    "FlextPipelineSingerCliTranslator",
    "FlextPipelineSinkAbstractions",
    "FlextPipelineSourceAbstractions",
    "FlextPipelineStream",
    "FlextPipelineTap",
    "FlextPipelineTransformationService",
    "FlextPipelineValidators",
    "__version__",
    "__version_info__",
]
