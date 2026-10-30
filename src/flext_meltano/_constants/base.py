"""FLEXT Meltano base constants — project metadata, paths, network, plugins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import warnings
from typing import Annotated, ClassVar

from flext_cli import c

from flext_meltano._constants import FlextMeltanoConstantsEnums


class FlextMeltanoConstantsBase:
    """Base meltano constants: metadata, versions, paths, network, plugins.

    All constants are flat with descriptive prefixes to explain their usage.
    """

    CONSTANTS_VERSION: ClassVar[str] = "1.0.0"

    # Metadata
    METADATA_DEFAULT_ENVIRONMENTS: ClassVar[
        tuple[FlextMeltanoConstantsEnums.ProjectEnvironment, ...]
    ] = (
        FlextMeltanoConstantsEnums.ProjectEnvironment.DEV,
        FlextMeltanoConstantsEnums.ProjectEnvironment.STAGING,
        FlextMeltanoConstantsEnums.ProjectEnvironment.PROD,
    )

    # Versions
    VERSION_MELTANO_REQUIRED: ClassVar[str] = "3.9.1"
    VERSION_MELTANO_REQUIREMENT: ClassVar[str] = f">={VERSION_MELTANO_REQUIRED}"

    # Paths
    PATH_MELTANO_PROJECT_FILE: ClassVar[str] = "meltano.yml"

    # Commands
    CMD_BINARY: ClassVar[str] = "meltano"
    CMD_ALL_OPTION: ClassVar[str] = "--all"
    CMD_CWD_OPTION: ClassVar[str] = "--cwd"
    CMD_ENVIRONMENT_OPTION: ClassVar[str] = "--environment"
    CMD_HELP_OPTION: ClassVar[str] = "--help"
    CMD_LIST_OPTION: ClassVar[str] = "--list"
    CMD_NO_ENVIRONMENT_OPTION: ClassVar[str] = "--no-environment"
    CMD_SHORT_HELP_OPTION: ClassVar[str] = "-h"
    CMD_VERSION_OPTION: ClassVar[str] = "--version"
    CMD_INVOKE: ClassVar[str] = "invoke"
    CMD_SELECT: ClassVar[str] = "select"

    # Operation labels and failure messages
    LOG_MESSAGE_DISCOVER_STREAMS_FAILED: ClassVar[str] = "Failed to discover streams"
    OPERATION_DISCOVER_STREAMS: ClassVar[str] = "discover streams"

    # Plugin
    PLUGIN_DBT_DEFAULT_NAME: ClassVar[str] = "dbt-postgres"
    PREFIX_TARGET: ClassVar[str] = "target"

    OPERATION_ERRORS: Annotated[
        ClassVar[tuple[type[Exception], ...]],
        warnings.deprecated(
            "compat: c.Meltano.OPERATION_ERRORS -> c.EXC_ATTR_KEY_OS_TYPE_VALUE; "
            "fix: read c.EXC_ATTR_KEY_OS_TYPE_VALUE"
        ),
    ] = c.EXC_ATTR_KEY_OS_TYPE_VALUE

    # Singer
    SINGER_SAFE_EXCEPTIONS: ClassVar[tuple[type[Exception], ...]] = (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
        RuntimeError,
        ImportError,
        c.ValidationError,
    )

    # Dbt
    DBT_MATERIALIZATION_TABLE: ClassVar[str] = "table"


__all__: list[str] = [
    "FlextMeltanoConstantsBase",
    "FlextMeltanoConstantsEnums",
]
