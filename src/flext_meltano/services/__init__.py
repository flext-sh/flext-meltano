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
        abstractions,
        adapter_extensions,
        adapters,
        bridge,
        cli_managers,
        executor,
        file_managers,
        library_runner,
        project_service,
        services,
        validators,
        yaml_operations,
    )
    from flext_meltano.services.abstractions import *
    from flext_meltano.services.adapter_extensions import *
    from flext_meltano.services.adapters import *
    from flext_meltano.services.bridge import *
    from flext_meltano.services.cli_managers import *
    from flext_meltano.services.executor import *
    from flext_meltano.services.file_managers import *
    from flext_meltano.services.library_runner import *
    from flext_meltano.services.project_service import *
    from flext_meltano.services.services import *
    from flext_meltano.services.validators import *
    from flext_meltano.services.yaml_operations import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextMeltanoAbstractions": "flext_meltano.services.abstractions",
    "FlextMeltanoAdapter": "flext_meltano.services.adapters",
    "FlextMeltanoBridge": "flext_meltano.services.bridge",
    "FlextMeltanoCommandRouter": "flext_meltano.services.cli_managers",
    "FlextMeltanoDbtAdapter": "flext_meltano.services.adapter_extensions",
    "FlextMeltanoDbtManager": "flext_meltano.services.cli_managers",
    "FlextMeltanoExecutor": "flext_meltano.services.executor",
    "FlextMeltanoFileManagers": "flext_meltano.services.file_managers",
    "FlextMeltanoLibraryRunner": "flext_meltano.services.library_runner",
    "FlextMeltanoPipelineAdapter": "flext_meltano.services.adapter_extensions",
    "FlextMeltanoPipelineManager": "flext_meltano.services.cli_managers",
    "FlextMeltanoPluginManager": "flext_meltano.services.cli_managers",
    "FlextMeltanoProjectService": "flext_meltano.services.project_service",
    "FlextMeltanoService": "flext_meltano.services.services",
    "FlextMeltanoSingerManager": "flext_meltano.services.cli_managers",
    "FlextMeltanoStatusManager": "flext_meltano.services.cli_managers",
    "FlextMeltanoValidators": "flext_meltano.services.validators",
    "FlextMeltanoYamlOperationsMixin": "flext_meltano.services.yaml_operations",
    "abstractions": "flext_meltano.services.abstractions",
    "adapter_extensions": "flext_meltano.services.adapter_extensions",
    "adapters": "flext_meltano.services.adapters",
    "bridge": "flext_meltano.services.bridge",
    "cli_managers": "flext_meltano.services.cli_managers",
    "executor": "flext_meltano.services.executor",
    "file_managers": "flext_meltano.services.file_managers",
    "library_runner": "flext_meltano.services.library_runner",
    "project_service": "flext_meltano.services.project_service",
    "services": "flext_meltano.services.services",
    "validators": "flext_meltano.services.validators",
    "yaml_operations": "flext_meltano.services.yaml_operations",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
