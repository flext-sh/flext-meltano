"""FLEXT Meltano base constants — project metadata, paths, network, plugins.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_cli import c

from flext_meltano._constants._base_parts import FlextMeltanoConstantsEnums


class FlextMeltanoConstantsBase:
    """Base meltano constants: metadata, versions, paths, network, plugins.

    All constants are flat with descriptive prefixes to explain their usage.
    """

    CONSTANTS_VERSION: ClassVar[str] = "1.0.0"
    PROJECT_NAME: ClassVar[str] = "FLEXT Meltano"

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
    VERSION_SINGER_SDK_REQUIRED: ClassVar[str] = "0.48.0"

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
    CMD_ELT: ClassVar[str] = "elt"
    CMD_INVOKE: ClassVar[str] = "invoke"
    CMD_SELECT: ClassVar[str] = "select"

    # Operation labels and failure messages
    LOG_MESSAGE_DISCOVER_STREAMS_FAILED: ClassVar[str] = "Failed to discover streams"
    OPERATION_DISCOVER_STREAMS: ClassVar[str] = "discover streams"

    # Network
    NETWORK_DEFAULT_TIMEOUT: ClassVar[int] = c.DEFAULT_TIMEOUT_SECONDS

    # Plugin
    PLUGIN_DBT_DEFAULT_NAME: ClassVar[str] = "dbt-postgres"
    PLUGIN_MIN_TAP_PLUGIN_NAME_LENGTH: ClassVar[int] = 5
    PLUGIN_MIN_TARGET_PLUGIN_NAME_LENGTH: ClassVar[int] = 8
    PREFIX_DBT: ClassVar[str] = "dbt"
    PREFIX_TARGET: ClassVar[str] = "target"

    OPERATION_ERRORS: ClassVar[tuple[type[Exception], ...]] = (
        ValueError,
        TypeError,
        KeyError,
        AttributeError,
        OSError,
    )

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
    DBT_MATERIALIZATION_VIEW: ClassVar[str] = "view"

    # ModelValidation
    VALIDATION_COMPLEXITY_SIMPLE_MAX_SETTINGS: ClassVar[int] = 5
    VALIDATION_COMPLEXITY_MODERATE_MAX_SETTINGS: ClassVar[int] = 20
    VALIDATION_EXECUTION_GOOD_PERFORMANCE_THRESHOLD: ClassVar[int] = 100
    VALIDATION_EXECUTION_HIGH_PERFORMANCE_THRESHOLD: ClassVar[int] = 1000
    VALIDATION_MATURITY_DEVELOPING_ENV_COUNT: ClassVar[int] = 2
    VALIDATION_MATURITY_MATURE_ENV_COUNT: ClassVar[int] = 3


__all__: list[str] = [
    "FlextMeltanoConstantsBase",
    "FlextMeltanoConstantsEnums",
]
