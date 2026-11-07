"""FLEXT Meltano settings constants — logging, service, defaults, capabilities.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from types import MappingProxyType
from typing import ClassVar

from flext_cli import c

from flext_meltano._constants import FlextMeltanoConstantsEnums


class FlextMeltanoConstantsSettings:
    """Meltano configuration, defaults, and operational constants.

    All constants are flat with descriptive prefixes to explain their usage.
    """

    # Environments
    ENVIRONMENT_RUNTIME_ALIASES: ClassVar[Mapping[str, str]] = MappingProxyType({
        c.Environment.DEVELOPMENT.value: (
            FlextMeltanoConstantsEnums.ProjectEnvironment.DEV
        ),
        c.Environment.TESTING.value: (FlextMeltanoConstantsEnums.EnvironmentAlias.TEST),
        c.Environment.PRODUCTION.value: (
            FlextMeltanoConstantsEnums.ProjectEnvironment.PROD
        ),
    })

    # Defaults
    DEFAULT_SERVICE_VERSION: ClassVar[str] = "0.9.9"
    DEFAULT_TIMEOUT_SECONDS: ClassVar[int] = 300

    # CliDefaults
    CLI_DEFAULT_PIPELINES_ROOT_ENV: ClassVar[str] = "FLEXT_MELTANO_PIPELINES_DIR"
    CLI_DEFAULT_PIPELINE_CONFIG_FILE: ClassVar[str] = "pipeline.json"
    CLI_DEFAULT_PIPELINE_PID_FILE: ClassVar[str] = "pipeline.pid"

    # Capabilities
    PLUGIN_GROUP_ALIASES: ClassVar[
        Mapping[str, FlextMeltanoConstantsEnums.PluginType]
    ] = MappingProxyType({
        "extractor": FlextMeltanoConstantsEnums.PluginType.EXTRACTORS,
        FlextMeltanoConstantsEnums.PluginType.EXTRACTORS: (
            FlextMeltanoConstantsEnums.PluginType.EXTRACTORS
        ),
        "tap": FlextMeltanoConstantsEnums.PluginType.EXTRACTORS,
        "loader": FlextMeltanoConstantsEnums.PluginType.LOADERS,
        FlextMeltanoConstantsEnums.PluginType.LOADERS: (
            FlextMeltanoConstantsEnums.PluginType.LOADERS
        ),
        "target": FlextMeltanoConstantsEnums.PluginType.LOADERS,
        "transformer": FlextMeltanoConstantsEnums.PluginType.TRANSFORMS,
        "transformers": FlextMeltanoConstantsEnums.PluginType.TRANSFORMS,
        FlextMeltanoConstantsEnums.PluginType.TRANSFORMS: (
            FlextMeltanoConstantsEnums.PluginType.TRANSFORMS
        ),
        "dbt": FlextMeltanoConstantsEnums.PluginType.TRANSFORMS,
    })
    DBT_DEFAULT_DOCS_ARGS: ClassVar[
        tuple[FlextMeltanoConstantsEnums.DbtCommand, ...]
    ] = (FlextMeltanoConstantsEnums.DbtCommand.GENERATE,)

    # Handlers
    HANDLER_ALL: ClassVar[tuple[FlextMeltanoConstantsEnums.HandlerType, ...]] = (
        FlextMeltanoConstantsEnums.HandlerType.SOURCE,
        FlextMeltanoConstantsEnums.HandlerType.SINK,
        FlextMeltanoConstantsEnums.HandlerType.PIPELINE,
    )

    # BatchDefaults
    BATCH_DEFAULT_DEFAULT_BATCH_SIZE: ClassVar[int] = 1000


__all__: list[str] = ["FlextMeltanoConstantsSettings"]
