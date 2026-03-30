# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT Meltano Services - Service mixins for the Meltano facade.

This package contains service mixin classes that compose via MRO
to form the FlextMeltano public facade in api.py.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano.services import (
        abstractions as abstractions,
        adapter_extensions as adapter_extensions,
        adapters as adapters,
        bridge as bridge,
        cli_managers as cli_managers,
        executor as executor,
        file_managers as file_managers,
        library_runner as library_runner,
        project_service as project_service,
        services as services,
        validators as validators,
        yaml_operations as yaml_operations,
    )
    from flext_meltano.services.abstractions import (
        FlextMeltanoAbstractions as FlextMeltanoAbstractions,
    )
    from flext_meltano.services.adapter_extensions import (
        FlextMeltanoDbtAdapter as FlextMeltanoDbtAdapter,
        FlextMeltanoPipelineAdapter as FlextMeltanoPipelineAdapter,
    )
    from flext_meltano.services.adapters import (
        FlextMeltanoAdapter as FlextMeltanoAdapter,
    )
    from flext_meltano.services.bridge import FlextMeltanoBridge as FlextMeltanoBridge
    from flext_meltano.services.cli_managers import (
        FlextMeltanoCommandRouter as FlextMeltanoCommandRouter,
        FlextMeltanoDbtManager as FlextMeltanoDbtManager,
        FlextMeltanoPipelineManager as FlextMeltanoPipelineManager,
        FlextMeltanoPluginManager as FlextMeltanoPluginManager,
        FlextMeltanoSingerManager as FlextMeltanoSingerManager,
        FlextMeltanoStatusManager as FlextMeltanoStatusManager,
    )
    from flext_meltano.services.executor import (
        FlextMeltanoExecutor as FlextMeltanoExecutor,
    )
    from flext_meltano.services.file_managers import (
        FlextMeltanoFileManagers as FlextMeltanoFileManagers,
    )
    from flext_meltano.services.library_runner import (
        FlextMeltanoLibraryRunner as FlextMeltanoLibraryRunner,
    )
    from flext_meltano.services.project_service import (
        FlextMeltanoProjectService as FlextMeltanoProjectService,
    )
    from flext_meltano.services.services import (
        FlextMeltanoService as FlextMeltanoService,
    )
    from flext_meltano.services.validators import (
        FlextMeltanoValidators as FlextMeltanoValidators,
    )
    from flext_meltano.services.yaml_operations import (
        FlextMeltanoYamlOperationsMixin as FlextMeltanoYamlOperationsMixin,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextMeltanoAbstractions": [
        "flext_meltano.services.abstractions",
        "FlextMeltanoAbstractions",
    ],
    "FlextMeltanoAdapter": ["flext_meltano.services.adapters", "FlextMeltanoAdapter"],
    "FlextMeltanoBridge": ["flext_meltano.services.bridge", "FlextMeltanoBridge"],
    "FlextMeltanoCommandRouter": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoCommandRouter",
    ],
    "FlextMeltanoDbtAdapter": [
        "flext_meltano.services.adapter_extensions",
        "FlextMeltanoDbtAdapter",
    ],
    "FlextMeltanoDbtManager": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoDbtManager",
    ],
    "FlextMeltanoExecutor": ["flext_meltano.services.executor", "FlextMeltanoExecutor"],
    "FlextMeltanoFileManagers": [
        "flext_meltano.services.file_managers",
        "FlextMeltanoFileManagers",
    ],
    "FlextMeltanoLibraryRunner": [
        "flext_meltano.services.library_runner",
        "FlextMeltanoLibraryRunner",
    ],
    "FlextMeltanoPipelineAdapter": [
        "flext_meltano.services.adapter_extensions",
        "FlextMeltanoPipelineAdapter",
    ],
    "FlextMeltanoPipelineManager": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoPipelineManager",
    ],
    "FlextMeltanoPluginManager": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoPluginManager",
    ],
    "FlextMeltanoProjectService": [
        "flext_meltano.services.project_service",
        "FlextMeltanoProjectService",
    ],
    "FlextMeltanoService": ["flext_meltano.services.services", "FlextMeltanoService"],
    "FlextMeltanoSingerManager": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoSingerManager",
    ],
    "FlextMeltanoStatusManager": [
        "flext_meltano.services.cli_managers",
        "FlextMeltanoStatusManager",
    ],
    "FlextMeltanoValidators": [
        "flext_meltano.services.validators",
        "FlextMeltanoValidators",
    ],
    "FlextMeltanoYamlOperationsMixin": [
        "flext_meltano.services.yaml_operations",
        "FlextMeltanoYamlOperationsMixin",
    ],
    "abstractions": ["flext_meltano.services.abstractions", ""],
    "adapter_extensions": ["flext_meltano.services.adapter_extensions", ""],
    "adapters": ["flext_meltano.services.adapters", ""],
    "bridge": ["flext_meltano.services.bridge", ""],
    "cli_managers": ["flext_meltano.services.cli_managers", ""],
    "executor": ["flext_meltano.services.executor", ""],
    "file_managers": ["flext_meltano.services.file_managers", ""],
    "library_runner": ["flext_meltano.services.library_runner", ""],
    "project_service": ["flext_meltano.services.project_service", ""],
    "services": ["flext_meltano.services.services", ""],
    "validators": ["flext_meltano.services.validators", ""],
    "yaml_operations": ["flext_meltano.services.yaml_operations", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextMeltanoAbstractions",
    "FlextMeltanoAdapter",
    "FlextMeltanoBridge",
    "FlextMeltanoCommandRouter",
    "FlextMeltanoDbtAdapter",
    "FlextMeltanoDbtManager",
    "FlextMeltanoExecutor",
    "FlextMeltanoFileManagers",
    "FlextMeltanoLibraryRunner",
    "FlextMeltanoPipelineAdapter",
    "FlextMeltanoPipelineManager",
    "FlextMeltanoPluginManager",
    "FlextMeltanoProjectService",
    "FlextMeltanoService",
    "FlextMeltanoSingerManager",
    "FlextMeltanoStatusManager",
    "FlextMeltanoValidators",
    "FlextMeltanoYamlOperationsMixin",
    "abstractions",
    "adapter_extensions",
    "adapters",
    "bridge",
    "cli_managers",
    "executor",
    "file_managers",
    "library_runner",
    "project_service",
    "services",
    "validators",
    "yaml_operations",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
