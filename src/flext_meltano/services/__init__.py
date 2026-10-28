# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano.services package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.services.abstractions import FlextMeltanoAbstractions
    from flext_meltano.services.declarative_tap import FlextMeltanoDeclarativeTap
    from flext_meltano.services.executor import FlextMeltanoExecutor
    from flext_meltano.services.executor_base import FlextMeltanoExecutorBase
    from flext_meltano.services.library_runner import FlextMeltanoLibraryRunner
    from flext_meltano.services.meltano_plugin_discovery import (
        FlextMeltanoPluginDiscovery,
    )
    from flext_meltano.services.project_service import FlextMeltanoProjectService
    from flext_meltano.services.service import FlextMeltanoService
    from flext_meltano.services.singer_sdk import FlextMeltanoSingerTapAdapter
    from flext_meltano.services.singer_target import FlextMeltanoTargetAbstractions


__all__: tuple[str, ...] = (
    "FlextMeltanoAbstractions",
    "FlextMeltanoDeclarativeTap",
    "FlextMeltanoExecutor",
    "FlextMeltanoExecutorBase",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoPluginDiscovery",
    "FlextMeltanoProjectService",
    "FlextMeltanoService",
    "FlextMeltanoSingerTapAdapter",
    "FlextMeltanoTargetAbstractions",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextMeltanoAbstractions": ".abstractions",
        "FlextMeltanoDeclarativeTap": ".declarative_tap",
        "FlextMeltanoExecutor": ".executor",
        "FlextMeltanoExecutorBase": ".executor_base",
        "FlextMeltanoLibraryRunner": ".library_runner",
        "FlextMeltanoPluginDiscovery": ".meltano_plugin_discovery",
        "FlextMeltanoProjectService": ".project_service",
        "FlextMeltanoService": ".service",
        "FlextMeltanoSingerTapAdapter": ".singer_sdk",
        "FlextMeltanoTargetAbstractions": ".singer_target",
    }),
    public_exports=__all__,
)
