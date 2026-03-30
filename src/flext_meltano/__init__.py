# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext meltano package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_meltano.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_cli import *

    from flext_meltano import (
        _constants,
        _models,
        _protocols,
        _typings,
        _utilities,
        api,
        base,
        cli,
        constants,
        dbt,
        models,
        protocols,
        settings,
        typings,
        utilities,
    )
    from flext_meltano._constants import config, enums
    from flext_meltano._constants.base import *
    from flext_meltano._constants.config import *
    from flext_meltano._constants.enums import *
    from flext_meltano._models import (
        cli_params,
        context,
        core,
        discovery,
        instances,
        instances_data,
        logging_config,
        payloads,
        payloads_data,
        projects,
        projects_plugin,
        results,
        results_dbt,
        results_pipeline,
        singer,
        singer_catalog,
        singer_sdk,
        sources,
        sources_params,
        transformations,
    )
    from flext_meltano._models.cli_params import *
    from flext_meltano._models.context import *
    from flext_meltano._models.core import *
    from flext_meltano._models.discovery import *
    from flext_meltano._models.instances import *
    from flext_meltano._models.instances_data import *
    from flext_meltano._models.logging_config import *
    from flext_meltano._models.payloads import *
    from flext_meltano._models.payloads_data import *
    from flext_meltano._models.projects import *
    from flext_meltano._models.projects_plugin import *
    from flext_meltano._models.results import *
    from flext_meltano._models.results_dbt import *
    from flext_meltano._models.results_pipeline import *
    from flext_meltano._models.singer import *
    from flext_meltano._models.singer_catalog import *
    from flext_meltano._models.singer_sdk import *
    from flext_meltano._models.sources import *
    from flext_meltano._models.sources_params import *
    from flext_meltano._models.transformations import *
    from flext_meltano._protocols import plugin, project, services
    from flext_meltano._protocols.cli import *
    from flext_meltano._protocols.plugin import *
    from flext_meltano._protocols.project import *
    from flext_meltano._protocols.services import *
    from flext_meltano._protocols.singer import *
    from flext_meltano._typings import domains
    from flext_meltano._typings.base import *
    from flext_meltano._typings.domains import *
    from flext_meltano._typings.singer import *
    from flext_meltano._utilities import yaml
    from flext_meltano._utilities.config import *
    from flext_meltano._utilities.project import *
    from flext_meltano._utilities.singer import *
    from flext_meltano._utilities.yaml import *
    from flext_meltano.api import *
    from flext_meltano.base import *
    from flext_meltano.cli import *
    from flext_meltano.constants import *
    from flext_meltano.dbt import runner, service
    from flext_meltano.dbt.project import *
    from flext_meltano.dbt.runner import *
    from flext_meltano.dbt.service import *
    from flext_meltano.meltano import pipelines, plugin_discovery, plugins
    from flext_meltano.meltano.pipelines import *
    from flext_meltano.meltano.plugin_discovery import *
    from flext_meltano.meltano.plugins import *
    from flext_meltano.meltano.project import *
    from flext_meltano.meltano.runner import *
    from flext_meltano.meltano.service import *
    from flext_meltano.models import *
    from flext_meltano.protocols import *
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
        validators,
        yaml_operations,
    )
    from flext_meltano.services._abstractions_base import *
    from flext_meltano.services._cli_small_managers import *
    from flext_meltano.services._executor_base import *
    from flext_meltano.services._pipeline_lifecycle import *
    from flext_meltano.services._pipeline_mgr import *
    from flext_meltano.services._pipeline_ops import *
    from flext_meltano.services.abstractions import *
    from flext_meltano.services.adapter_extensions import *
    from flext_meltano.services.adapters import *
    from flext_meltano.services.bridge import *
    from flext_meltano.services.cli_managers import *
    from flext_meltano.services.executor import *
    from flext_meltano.services.file_managers import *
    from flext_meltano.services.project_service import *
    from flext_meltano.services.services import *
    from flext_meltano.services.validators import *
    from flext_meltano.services.yaml_operations import *
    from flext_meltano.settings import *
    from flext_meltano.singer import (
        catalog,
        sdk,
        state,
        tap,
        tap_source,
        target,
        translator,
    )
    from flext_meltano.singer.catalog import *
    from flext_meltano.singer.sdk import *
    from flext_meltano.singer.service import *
    from flext_meltano.singer.state import *
    from flext_meltano.singer.tap import *
    from flext_meltano.singer.tap_source import *
    from flext_meltano.singer.target import *
    from flext_meltano.singer.translator import *
    from flext_meltano.typings import *
    from flext_meltano.utilities import *

from flext_meltano._constants import _LAZY_IMPORTS as __CONSTANTS_LAZY
from flext_meltano._models import _LAZY_IMPORTS as __MODELS_LAZY
from flext_meltano._protocols import _LAZY_IMPORTS as __PROTOCOLS_LAZY
from flext_meltano._typings import _LAZY_IMPORTS as __TYPINGS_LAZY
from flext_meltano._utilities import _LAZY_IMPORTS as __UTILITIES_LAZY
from flext_meltano.dbt import _LAZY_IMPORTS as _DBT_LAZY
from flext_meltano.meltano import _LAZY_IMPORTS as _MELTANO_LAZY
from flext_meltano.services import _LAZY_IMPORTS as _SERVICES_LAZY
from flext_meltano.singer import _LAZY_IMPORTS as _SINGER_LAZY

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **__CONSTANTS_LAZY,
    **__MODELS_LAZY,
    **__PROTOCOLS_LAZY,
    **__TYPINGS_LAZY,
    **__UTILITIES_LAZY,
    **_DBT_LAZY,
    **_MELTANO_LAZY,
    **_SERVICES_LAZY,
    **_SINGER_LAZY,
    "FlextMeltano": "flext_meltano.api",
    "FlextMeltanoCLI": "flext_meltano.cli",
    "FlextMeltanoConstants": "flext_meltano.constants",
    "FlextMeltanoModels": "flext_meltano.models",
    "FlextMeltanoProtocols": "flext_meltano.protocols",
    "FlextMeltanoServiceBase": "flext_meltano.base",
    "FlextMeltanoSettings": "flext_meltano.settings",
    "FlextMeltanoTypes": "flext_meltano.typings",
    "FlextMeltanoUtilities": "flext_meltano.utilities",
    "_constants": "flext_meltano._constants",
    "_models": "flext_meltano._models",
    "_protocols": "flext_meltano._protocols",
    "_typings": "flext_meltano._typings",
    "_utilities": "flext_meltano._utilities",
    "api": "flext_meltano.api",
    "base": "flext_meltano.base",
    "c": ["flext_meltano.constants", "FlextMeltanoConstants"],
    "cli": "flext_meltano.cli",
    "constants": "flext_meltano.constants",
    "d": "flext_cli",
    "dbt": "flext_meltano.dbt",
    "e": "flext_cli",
    "h": "flext_cli",
    "m": ["flext_meltano.models", "FlextMeltanoModels"],
    "main": "flext_meltano.cli",
    "meltano": "flext_meltano.api",
    "models": "flext_meltano.models",
    "p": ["flext_meltano.protocols", "FlextMeltanoProtocols"],
    "protocols": "flext_meltano.protocols",
    "r": "flext_cli",
    "s": "flext_cli",
    "settings": "flext_meltano.settings",
    "t": ["flext_meltano.typings", "FlextMeltanoTypes"],
    "typings": "flext_meltano.typings",
    "u": ["flext_meltano.utilities", "FlextMeltanoUtilities"],
    "utilities": "flext_meltano.utilities",
    "x": "flext_cli",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
