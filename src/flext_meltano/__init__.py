"""ELT pipeline integration library for FLEXT.

Provides programmatic APIs for singer-sdk, meltano-sdk, and dbt-core integration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import (
    FlextDecorators as d,
    FlextExceptions as e,
    FlextHandlers as h,
    r,
    s,
    x,
)

from flext_meltano.__version__ import __version__, __version_info__
from flext_meltano.adapters import FlextMeltanoAdapter
from flext_meltano.api import FlextMeltano
from flext_meltano.bridge import FlextMeltanoBridge
from flext_meltano.constants import (
    FlextMeltanoConstants,
    FlextMeltanoConstants as c,
)
from flext_meltano.dbt import (
    FlextMeltanoDbtProjectManager,
    FlextMeltanoDbtRunner,
    FlextMeltanoDbtService,
)
from flext_meltano.executor import FlextMeltanoExecutor
from flext_meltano.file_managers import FlextMeltanoFileManagers
from flext_meltano.library_runner import FlextMeltanoLibraryRunner
from flext_meltano.meltano import (
    FlextMeltanoMeltanoService,
    FlextMeltanoProjectManager,
)
from flext_meltano.models import (
    FlextMeltanoModels,
    FlextMeltanoModels as m,
)
from flext_meltano.protocols import (
    FlextMeltanoProtocols,
    p,
)
from flext_meltano.services import FlextMeltanoService
from flext_meltano.settings import FlextMeltanoSettings
from flext_meltano.singer.catalog import FlextMeltanoCatalogManager
from flext_meltano.singer.service import FlextMeltanoSingerService
from flext_meltano.singer.state import FlextMeltanoStateManager
from flext_meltano.singer.tap import (
    FlextMeltanoStream,
    FlextMeltanoTap,
    FlextMeltanoTapAbstractions,
)
from flext_meltano.singer.target import (
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

# Standard FLEXT aliases (11 total)
c = FlextMeltanoConstants
d = FlextDecorators
e = FlextExceptions
h = FlextHandlers
m = FlextMeltanoModels
p = FlextMeltanoProtocols
r = FlextResult
s = FlextService
t = FlextMeltanoTypes
u = FlextMeltanoUtilities
x = FlextMixins

__all__ = [
    "FlextMeltano",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCatalogManager",
    "FlextMeltanoConstants",
    "FlextMeltanoDbtProjectManager",
    "FlextMeltanoDbtRunner",
    "FlextMeltanoDbtService",
    "FlextMeltanoExecutor",
    "FlextMeltanoFileManagers",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoMeltanoService",
    "FlextMeltanoModels",
    "FlextMeltanoProjectManager",
    "FlextMeltanoProtocols",
    "FlextMeltanoService",
    "FlextMeltanoSettings",
    "FlextMeltanoSingerService",
    "FlextMeltanoStateManager",
    "FlextMeltanoStream",
    "FlextMeltanoTap",
    "FlextMeltanoTapAbstractions",
    "FlextMeltanoTarget",
    "FlextMeltanoTargetAbstractions",
    "FlextMeltanoTypes",
    "FlextMeltanoUtilities",
    "FlextMeltanoValidators",
    "__version__",
    "__version_info__",
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
