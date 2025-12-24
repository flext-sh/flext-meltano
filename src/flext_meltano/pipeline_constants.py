"""FLEXT Pipeline Constants - Generic pipeline constants.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Final, Literal

from flext import FlextConstants
from flext_meltano.constants import c


class FlextMeltanoConstants(FlextConstants):
    """Generic pipeline constants following SOLID principles.

    Single responsibility: Pipeline domain constants only.
    Uses FlextConstants as source of truth for base values.
    """

    # Version metadata - uses FlextConstants as base
    VERSION: Final[str] = "0.9.0"
    APPLICATION_NAME: Final[str] = "flext-pipeline"
    APPLICATION_DESCRIPTION: Final[str] = "FLEXT Generic Data Pipeline Framework"
    APPLICATION_AUTHOR: Final[str] = "FLEXT Team"
    APPLICATION_LICENSE: Final[str] = "MIT"

    # Metadata constants - generic and reusable
    METADATA_CREATED_BY: Final[str] = "flext-pipeline"
    METADATA_DEFAULT_ENVIRONMENTS: Final[tuple[str, ...]] = (
        "dev",
        "staging",
        "prod",
    )

    # File constants - generic file management
    PROJECT_FILE: Final[str] = "pipeline.yml"
    PIPELINE_PROJECT_FILE: Final[str] = "pipeline.yml"
    STATE_DIR: Final[str] = ".pipeline"
    LOGS_DIR: Final[str] = "logs"
    OUTPUT_DIR: Final[str] = "output"

    # Alias for project_service compatibility - no legacy aliases
    PIPELINE_YML_FILENAME: Final[str] = "pipeline.yml"

    # Command constants - generic command interface
    COMMAND_INSTALL: Final[str] = "install"
    COMMAND_RUN: Final[str] = "run"
    COMMAND_PIPELINE: Final[str] = "pipeline"

    # Version requirements - uses FlextConstants as base
    VERSION_REQUIRED: Final[str] = "3.9.1"
    FLEXT_PIPELINE_VERSION: Final[str] = "0.9.0"

    # Default timeout constants - derived from FlextConstants
    PIPELINE_DEFAULT_TIMEOUT: Final[int] = (
        FlextConstants.Performance.DEFAULT_TIMEOUT_LIMIT
    )  # 5 minutes
    DEFAULT_TIMEOUT: Final[int] = FlextConstants.Defaults.TIMEOUT * 10  # 300 seconds
    DISCOVERY_TIMEOUT: Final[int] = FlextConstants.Defaults.TIMEOUT * 2  # 60 seconds
    SOURCE_TIMEOUT: Final[int] = FlextConstants.Defaults.TIMEOUT * 60  # 1800 seconds
    SINK_TIMEOUT: Final[int] = FlextConstants.Defaults.TIMEOUT * 60  # 1800 seconds

    # Database ports - generic database connectivity
    DEFAULT_POSTGRES_PORT: Final[int] = 5432
    DEFAULT_MYSQL_PORT: Final[int] = 3306
    DEFAULT_ORACLE_PORT: Final[int] = 1521


# Pipeline enums moved to constants.py as c.Meltano.Enums.* (DRY pattern)
PipelinePluginTypes = c.Meltano.Enums.PluginType
PipelineReplicationMethods = c.Meltano.Enums.ReplicationMethod
PipelineOperationStatus = c.Meltano.Enums.OperationStatus
PipelineRunMode = c.Meltano.Enums.RunMode
PipelineEnvironment = c.Meltano.Enums.Environment


# Literal types for pipeline domain - Python 3.13+ syntax
PipelinePluginType = Literal["extractors", "loaders", "transforms", "orchestrators"]
PipelineReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"]
PipelineEnvironmentType = Literal[
    "development",
    "staging",
    "production",
    "testing",
    "local",
]


__all__ = [
    "FlextMeltanoConstants",
    "PipelineEnvironment",
    "PipelineOperationStatus",
    "PipelinePluginTypes",
    "PipelineReplicationMethods",
    "PipelineRunMode",
]
