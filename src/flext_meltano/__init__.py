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
# IMPORT ALIASES FOR SIMPLIFIED USAGE
# =========================================================================
from flext import FlextDecorators,
    FlextExceptions,
    FlextHandlers,
    FlextMixins,
    FlextResult,
    FlextService

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

# =========================================================================
# FOUNDATION LAYER - Core patterns and definitions
# =========================================================================
# Domain-specific aliases
from flext_meltano.constants import (
    FlextMeltanoConstants,
    c,
)

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
from flext_meltano.library_runner import FlextMeltanoLibraryRunner

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
from flext_meltano.models import (
    FlextMeltanoModels,
    FlextMeltanoModels as m,
)
from flext_meltano.protocols import (
    FlextMeltanoPluginProtocols,
    FlextMeltanoProtocols,
    FlextMeltanoSingerProtocols,
    p,
)
from flext_meltano.services import FlextMeltanoService
from flext_meltano.settings import FlextMeltanoSettings

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
from flext_meltano.typings import (
    FlextMeltanoTypes,
    t,
)
from flext_meltano.utilities import (
    FlextMeltanoUtilities,
    u,
)
from flext_meltano.validators import FlextMeltanoValidators

# Core aliases
r = FlextResult
e = FlextExceptions
d = FlextDecorators
s = FlextService
x = FlextMixins
h = FlextHandlers

# =========================================================================
# PUBLIC API EXPORTS
# =========================================================================

__all__ = [
    # Application
    "FlextMeltano",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCatalogManager",
    # Foundation
    "FlextMeltanoConstants",
    # DBT domain - Deep dbt-core integration (NO CLI)
    "FlextMeltanoDbtProjectManager",
    "FlextMeltanoDbtRunner",
    "FlextMeltanoDbtService",
    "FlextMeltanoExecutor",
    # Support modules
    "FlextMeltanoFileManagers",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoMeltanoService",
    # Domain
    "FlextMeltanoModels",
    "FlextMeltanoPluginProtocols",
    # Meltano domain - Deep meltano-sdk integration (NO CLI)
    "FlextMeltanoProjectManager",
    "FlextMeltanoProtocols",
    "FlextMeltanoService",
    "FlextMeltanoSettings",
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
    # Short aliases for simplified usage
    "c",  # FlextMeltanoConstants
    "d",  # FlextDecorators
    "e",  # FlextExceptions
    "h",  # FlextHandlers
    "m",  # FlextMeltanoModels
    "p",  # FlextMeltanoProtocols
    "r",  # FlextResult
    "s",  # FlextService
    "t",  # FlextMeltanoTypes
    "u",  # FlextMeltanoUtilities
    "x",  # x
]
