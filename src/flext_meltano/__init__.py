"""Enterprise Meltano integration library for FLEXT ecosystem.

This module provides a unified interface for Meltano, Singer, and DBT operations
following flext-core architectural patterns. All external access should go
through the FlextMeltanoAPI class.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from singer_sdk import Stream as FlextMeltanoStream, Tap as FlextMeltanoTap

from flext_meltano.__version__ import __version__, __version_info__
from flext_meltano.abstractions import FlextMeltanoAbstractions
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.api import FlextMeltano
from flext_meltano.bridge import FlextMeltanoBridge
from flext_meltano.cli import FlextMeltanoCLI
from flext_meltano.config import FlextMeltanoConfig
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
from flext_meltano.singer import FlextMeltanoSinger
from flext_meltano.singer_cli_translator import FlextMeltanoSingerCliTranslator
from flext_meltano.tap_abstractions import FlextMeltanoTapAbstractions
from flext_meltano.target_abstractions import FlextMeltanoTargetAbstractions
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.utilities import FlextMeltanoUtilities
from flext_meltano.validators import FlextMeltanoValidators

__all__ = [
    "FlextMeltano",
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
    "FlextMeltanoSingerCliTranslator",
    "FlextMeltanoStream",
    "FlextMeltanoTap",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTypes",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "__version__",
    "__version_info__",
]
