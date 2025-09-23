"""Enterprise Meltano integration library for FLEXT ecosystem.

This module provides a unified interface for Meltano, Singer, and DBT operations
following flext-core architectural patterns. All external access should go
through the FlextMeltanoAPI class.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Internal services - for advanced use cases
from flext_meltano.adapters import FlextMeltanoAdapter

# Main unified API - RECOMMENDED for external use
from flext_meltano.api import FlextMeltanoAPI
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.config_builders import FlextMeltanoConfigBuilders

# Centralized definitions
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.exceptions import FlextMeltanoExceptions
from flext_meltano.executors import FlextMeltanoExecutor

# Legacy support - to be removed in 2.0.0
from flext_meltano.executors_bridge import FlextMeltanoBridge
from flext_meltano.file_managers import FlextMeltanoFileManagers
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.protocols import FlextMeltanoProtocols
from flext_meltano.services import FlextMeltanoService
from flext_meltano.singer_types import FlextSingerTypes
from flext_meltano.tap_abstractions import FlextTapAbstractions
from flext_meltano.target_abstractions import FlextTargetAbstractions
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.utilities import FlextMeltanoUtilities
from flext_meltano.validators import FlextMeltanoValidators

__all__ = [
    "FlextMeltanoAPI",  # Main API - RECOMMENDED
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoConfig",
    "FlextMeltanoConfigBuilders",
    "FlextMeltanoConstants",
    "FlextMeltanoExceptions",
    "FlextMeltanoExecutor",
    "FlextMeltanoFileManagers",
    "FlextMeltanoModels",
    "FlextMeltanoProtocols",
    "FlextMeltanoService",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "FlextSingerTypes",
    "FlextTapAbstractions",
    "FlextTargetAbstractions",
]
