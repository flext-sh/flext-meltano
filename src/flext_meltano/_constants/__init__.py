# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Meltano. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_meltano._constants.base import FlextMeltanoConstantsBase
    from flext_meltano._constants.enums import FlextMeltanoConstantsEnums
    from flext_meltano._constants.settings import FlextMeltanoConstantsSettings


__all__: tuple[str, ...] = (
    "FlextMeltanoConstantsBase",
    "FlextMeltanoConstantsEnums",
    "FlextMeltanoConstantsSettings",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "FlextMeltanoConstantsBase": ".base",
        "FlextMeltanoConstantsEnums": ".enums",
        "FlextMeltanoConstantsSettings": ".settings",
    },
    public_exports=__all__,
    deferred_members={
        "FlextMeltanoConstantsBase": (
            "CONSTANTS_VERSION",
            "METADATA_DEFAULT_ENVIRONMENTS",
            "VERSION_MELTANO_REQUIRED",
            "VERSION_MELTANO_REQUIREMENT",
            "PATH_MELTANO_PROJECT_FILE",
            "CMD_BINARY",
            "CMD_ALL_OPTION",
            "CMD_CWD_OPTION",
            "CMD_ENVIRONMENT_OPTION",
            "CMD_HELP_OPTION",
            "CMD_LIST_OPTION",
            "CMD_NO_ENVIRONMENT_OPTION",
            "CMD_SHORT_HELP_OPTION",
            "CMD_VERSION_OPTION",
            "CMD_INVOKE",
            "CMD_SELECT",
            "LOG_MESSAGE_DISCOVER_STREAMS_FAILED",
            "OPERATION_DISCOVER_STREAMS",
            "PLUGIN_DBT_DEFAULT_NAME",
            "PREFIX_TARGET",
            "OPERATION_ERRORS",
            "SINGER_SAFE_EXCEPTIONS",
            "DBT_MATERIALIZATION_TABLE",
        ),
        "FlextMeltanoConstantsEnums": (
            "CliCommand",
            "PluginType",
            "SingerReplicationMethod",
            "OperationStatus",
            "ProjectEnvironment",
            "EnvironmentAlias",
            "DbtCommand",
            "SingerMessageType",
            "HandlerGroup",
            "ServiceType",
            "StreamStatus",
            "VALID_STATUSES",
            "ACTIVE_STATUSES",
            "PipelineCommand",
            "ExecutorCommand",
            "PayloadKey",
        ),
        "FlextMeltanoConstantsSettings": (
            "ENVIRONMENT_RUNTIME_ALIASES",
            "DEFAULT_SERVICE_VERSION",
            "DEFAULT_TIMEOUT_SECONDS",
            "CLI_DEFAULT_PIPELINES_ROOT_ENV",
            "CLI_DEFAULT_PIPELINE_CONFIG_FILE",
            "CLI_DEFAULT_PIPELINE_PID_FILE",
            "PLUGIN_GROUP_ALIASES",
            "DBT_DEFAULT_DOCS_ARGS",
            "HANDLER_ALL",
            "BATCH_DEFAULT_DEFAULT_BATCH_SIZE",
        ),
    },
)
