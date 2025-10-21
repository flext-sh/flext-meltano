"""Enterprise ELT Pipeline Integration Library for FLEXT Ecosystem.

This library provides deep integration with singer-sdk, meltano-sdk, and
dbt-core with programmatic APIs, railway-oriented programming, and FLEXT
ecosystem patterns.

NO CLI - Pure programmatic APIs only.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# =========================================================================
# VERSION
# =========================================================================
from flext_meltano.__version__ import __version__, __version_info__

# =========================================================================
# APPLICATION LAYER - Main API and configuration
# =========================================================================
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.api import FlextMeltano
from flext_meltano.bridge import FlextMeltanoBridge
from flext_meltano.config import FlextMeltanoConfig

# =========================================================================
# FOUNDATION LAYER - Core patterns and definitions
# =========================================================================
from flext_meltano.constants import FlextMeltanoConstants

# =========================================================================
# DBT DOMAIN - Deep dbt-core integration (NO CLI)
# Programmatic APIs only for DBT projects and transformations
# =========================================================================
from flext_meltano.dbt import (
    FlextMeltanoDbtProjectManager,
    FlextMeltanoDbtRunner,
    FlextMeltanoDbtService,
)
from flext_meltano.executor import FlextMeltanoExecutor

# =========================================================================
# SUPPORT MODULES
# =========================================================================
from flext_meltano.file_managers import FlextMeltanoFileManagers

# =========================================================================
# MELTANO DOMAIN - Deep meltano-sdk integration (NO CLI)
# Programmatic APIs only for Meltano projects and pipelines
# =========================================================================
from flext_meltano.meltano import (
    FlextMeltanoMeltanoService,
    FlextMeltanoProjectManager,
)

# =========================================================================
# DOMAIN LAYER - Models and services
# =========================================================================
from flext_meltano.models import FlextMeltanoModels
from flext_meltano.protocols import (
    FlextMeltanoPluginProtocols,
    FlextMeltanoProtocols,
    FlextMeltanoSingerProtocols,
)
from flext_meltano.services import FlextMeltanoService

# =========================================================================
# SINGER DOMAIN - Deep singer-sdk integration (NO CLI)
# Programmatic APIs only for Singer taps and targets
# =========================================================================
from flext_meltano.singer import (
    FlextMeltanoCatalogManager,
    FlextMeltanoSingerService,
    FlextMeltanoStateManager,
    FlextMeltanoStream,
    FlextMeltanoTap,
    FlextMeltanoTapAbstractions,
    FlextMeltanoTarget,
    FlextMeltanoTargetAbstractions,
)
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.utilities import FlextMeltanoUtilities
from flext_meltano.validators import FlextMeltanoValidators

# =========================================================================
# PUBLIC API EXPORTS
# =========================================================================

__all__ = [
    # Application
    "FlextMeltano",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCatalogManager",
    "FlextMeltanoConfig",
    # Foundation
    "FlextMeltanoConstants",
    # DBT domain - Deep dbt-core integration (NO CLI)
    "FlextMeltanoDbtProjectManager",
    "FlextMeltanoDbtRunner",
    "FlextMeltanoDbtService",
    "FlextMeltanoExecutor",
    # Support modules
    "FlextMeltanoFileManagers",
    "FlextMeltanoMeltanoService",
    # Domain
    "FlextMeltanoModels",
    "FlextMeltanoPluginProtocols",
    # Meltano domain - Deep meltano-sdk integration (NO CLI)
    "FlextMeltanoProjectManager",
    "FlextMeltanoProtocols",
    "FlextMeltanoService",
    "FlextMeltanoSingerProtocols",
    "FlextMeltanoSingerService",
    "FlextMeltanoStateManager",
    # Singer domain - Deep singer-sdk integration (NO CLI)
    "FlextMeltanoStream",
    "FlextMeltanoTap",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTarget",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    # Version
    "__version__",
    "__version_info__",
]
