"""FLEXT Meltano base constants parts — domain-specific enumerations.

Split parts of the ``_constants`` family base: the enumerations the family
base and its settings part consume without importing a sibling family module.

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

from enum import StrEnum, unique
from typing import ClassVar

from flext_cli import c


class FlextMeltanoConstantsEnums:
    """Meltano domain enumerations."""

    @unique
    class CliCommand(StrEnum):
        """Top-level CLI command routing identifiers."""

        PIPELINE = "pipeline"
        TAP = "tap"
        TARGET = "target"
        DBT = "dbt"
        PLUGIN = "plugin"
        STATUS = "status"
        VERSION = "version"

    @unique
    class PluginType(StrEnum):
        """Supported Meltano plugin categories.

        DRY Pattern:
            StrEnum is the single source of truth. Use PluginType.EXTRACTORS.value
            or PluginType.EXTRACTORS directly - no base strings needed.
        """

        EXTRACTORS = "extractors"
        LOADERS = "loaders"
        ORCHESTRATORS = "orchestrators"
        TRANSFORMS = "transforms"

    @unique
    class SingerReplicationMethod(StrEnum):
        """Singer replication method identifiers."""

        FULL_TABLE = "FULL_TABLE"
        INCREMENTAL = "INCREMENTAL"
        LOG_BASED = "LOG_BASED"

    @unique
    class OperationStatus(StrEnum):
        """Operation execution lifecycle status values."""

        AVAILABLE = "available"
        CANCELLED = c.Status.CANCELLED.value
        CONFIGURED = "configured"
        CREATED = "created"
        ERROR = c.HealthStatus.ERROR.value
        EXECUTED = "executed"
        HEALTHY = c.HealthStatus.HEALTHY.value
        OK = "OK"
        PASSED = "passed"
        PENDING = c.Status.PENDING.value
        READY = "ready"
        RUNNING = c.Status.RUNNING.value
        SUCCESS = c.Status.SUCCESS.value
        TIMEOUT = "timeout"

    @unique
    class Environment(StrEnum):
        """Deployment environments for Meltano pipelines."""

        DEVELOPMENT = "development"
        LOCAL = "local"
        PRODUCTION = "production"
        STAGING = "staging"
        TESTING = "testing"

    @unique
    class ProjectEnvironment(StrEnum):
        """Canonical environment names used in generated Meltano projects."""

        DEV = "dev"
        PROD = "prod"
        STAGING = "staging"

    @unique
    class EnvironmentAlias(StrEnum):
        """Short environment aliases accepted by settings helpers."""

        DEV = "dev"
        PROD = "prod"
        TEST = "test"

    @unique
    class DbtCommand(StrEnum):
        """dbt CLI commands used across Meltano integrations."""

        BUILD = "build"
        COMPILE = "compile"
        DOCS = "docs"
        GENERATE = "generate"
        RUN = "run"
        TEST = "test"

    @unique
    class SingerMessageType(StrEnum):
        """Singer protocol message kinds."""

        ACTIVATE_VERSION = "ACTIVATE_VERSION"
        CATALOG = "CATALOG"
        RECORD = "RECORD"
        SCHEMA = "SCHEMA"
        STATE = "STATE"

    @unique
    class HandlerType(StrEnum):
        """Named handler groups exposed by the public API."""

        PIPELINE = "pipeline"
        SINK = "sink"
        SOURCE = "source"

    @unique
    class ServiceType(StrEnum):
        """Service identity tokens reported by Meltano service metadata."""

        DBT = "dbt"
        PIPELINE = "pipeline_service"

    @unique
    class StreamStatus(StrEnum):
        """Meltano stream statuses — single source of truth."""

        COMPLETED = c.Status.COMPLETED.value
        DISCOVERED = "discovered"
        ERROR = c.HealthStatus.ERROR.value
        EXTRACTING = "extracting"
        FAILED = c.Status.FAILED.value
        IN_PROGRESS = "in_progress"
        INITIALIZED = "initialized"
        PENDING = c.Status.PENDING.value
        PROCESSING = c.Status.PROCESSING.value
        SELECTED = "selected"
        SUCCESS = c.Status.SUCCESS.value

    VALID_STATUSES: ClassVar[frozenset[StreamStatus]] = frozenset({
        StreamStatus.INITIALIZED,
        StreamStatus.PROCESSING,
        StreamStatus.COMPLETED,
        StreamStatus.ERROR,
    })
    ACTIVE_STATUSES: ClassVar[frozenset[StreamStatus]] = frozenset({
        StreamStatus.DISCOVERED,
        StreamStatus.SELECTED,
        StreamStatus.EXTRACTING,
    })

    @unique
    class PipelineCommand(StrEnum):
        """Pipeline CLI subcommands."""

        CREATE = "create"
        DELETE = "delete"
        LIST = c.Action.LIST
        RUN = "run"
        STATUS = "status"
        STOP = "stop"

    @unique
    class ExecutorCommand(StrEnum):
        """Executor available commands."""

        HEALTH = "health"
        HELP = "help"
        INFO = "info"
        INSTALL = "install"
        LIST = c.Action.LIST
        PIPELINE = "pipeline"
        RUN = "run"
        SELECT = "select"
        VERSION = "version"

    @unique
    class PayloadKey(StrEnum):
        """Payload field names emitted by Meltano service helpers."""

        NAME = "name"
        STATUS = "status"
        STREAM_NAME = "stream_name"
        STREAMS = "streams"
        TAP_STREAM_ID = "tap_stream_id"
        VERSION = "version"


__all__: list[str] = ["FlextMeltanoConstantsEnums"]
