"""FLEXT Meltano enum constants — domain-specific enumerations."""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final


class FlextMeltanoConstantsEnums:
    """Meltano domain enumerations."""

    class Enums:
        """Domain specific enumerations."""

        @unique
        class PluginType(StrEnum):
            """Supported Meltano plugin categories.

            DRY Pattern:
                StrEnum is the single source of truth. Use PluginType.EXTRACTORS.value
                or PluginType.EXTRACTORS directly - no base strings needed.
            """

            EXTRACTORS = "extractors"
            LOADERS = "loaders"
            TRANSFORMS = "transforms"
            ORCHESTRATORS = "orchestrators"

        @unique
        class ReplicationMethod(StrEnum):
            """Singer replication method identifiers.

            DRY Pattern:
                StrEnum is the single source of truth. Use ReplicationMethod.FULL_TABLE.value
                or ReplicationMethod.FULL_TABLE directly - no base strings needed.
            """

            FULL_TABLE = "FULL_TABLE"
            INCREMENTAL = "INCREMENTAL"
            LOG_BASED = "LOG_BASED"

        @unique
        class OperationStatus(StrEnum):
            """Operation execution lifecycle status values.

            DRY Pattern:
                StrEnum is the single source of truth. Use OperationStatus.PENDING.value
                or OperationStatus.PENDING directly - no base strings needed.
            """

            PENDING = "pending"
            RUNNING = "running"
            SUCCESS = "success"
            ERROR = "error"
            TIMEOUT = "timeout"
            CANCELLED = "cancelled"
            CONFIGURED = "configured"
            INSTALLED = "installed"
            CREATED = "created"
            READY = "ready"
            AVAILABLE = "available"
            EXECUTED = "executed"
            HEALTHY = "healthy"
            OK = "OK"
            PASSED = "passed"
            PROCESSED = "processed"

        @unique
        class RunMode(StrEnum):
            """Execution modes for Meltano operations.

            DRY Pattern:
                StrEnum is the single source of truth. Use RunMode.FULL.value
                or RunMode.FULL directly - no base strings needed.
            """

            FULL = "full"
            INCREMENTAL = "incremental"
            DRY_RUN = "dry_run"
            TEST = "test"

        @unique
        class Environment(StrEnum):
            """Deployment environments for Meltano pipelines.

            DRY Pattern:
                StrEnum is the single source of truth. Use Environment.DEVELOPMENT.value
                or Environment.DEVELOPMENT directly - no base strings needed.
            """

            DEVELOPMENT = "development"
            STAGING = "staging"
            PRODUCTION = "production"
            TESTING = "testing"
            LOCAL = "local"

        @unique
        class StreamStatus(StrEnum):
            """Meltano stream statuses — single source of truth."""

            COMPLETED = "completed"
            ERROR = "error"
            SUCCESS = "success"
            FAILED = "failed"
            IN_PROGRESS = "in_progress"
            PENDING = "pending"
            INITIALIZED = "initialized"
            PROCESSING = "processing"
            DISCOVERED = "discovered"
            SELECTED = "selected"
            EXTRACTING = "extracting"

        VALID_STATUSES: Final[frozenset[str]] = frozenset({
            StreamStatus.INITIALIZED,
            StreamStatus.PROCESSING,
            StreamStatus.COMPLETED,
            StreamStatus.ERROR,
        })
        ACTIVE_STATUSES: Final[frozenset[str]] = frozenset({
            StreamStatus.DISCOVERED,
            StreamStatus.SELECTED,
            StreamStatus.EXTRACTING,
        })

        @unique
        class PipelineCommand(StrEnum):
            """Pipeline CLI subcommands."""

            CREATE = "create"
            RUN = "run"
            LIST = "list"
            STATUS = "status"
            STOP = "stop"
            DELETE = "delete"

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
        class ExecutorCommand(StrEnum):
            """Executor available commands."""

            VERSION = "version"
            HELP = "help"
            HEALTH = "health"
            PIPELINE = "pipeline"
            RUN = "run"
            INSTALL = "install"
            LIST = "list"
            INVOKE = "invoke"
            SELECT = "select"

        @unique
        class SingerMetadataKey(StrEnum):
            """Singer catalog metadata field names."""

            TABLE_KEY_PROPERTIES = "table-key-properties"
            FORCED_REPLICATION_METHOD = "forced-replication-method"
            VALID_REPLICATION_KEYS = "valid-replication-keys"

        @unique
        class SchemaKey(StrEnum):
            """JSON Schema structure field names."""

            TYPE = "type"
            PROPERTIES = "properties"
            OBJECT = "object"
            INTEGER = "integer"
            STRING = "string"
            NUMBER = "number"
