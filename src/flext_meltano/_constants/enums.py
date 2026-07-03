"""FLEXT Meltano enum constants — domain-specific enumerations."""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

from flext_meltano.constants import c


class FlextMeltanoConstantsEnums:
    """Meltano domain enumerations."""

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
        INSTALLED = "installed"
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
    class ComponentType(StrEnum):
        """Supported service component groups."""

        ORCHESTRATORS = "orchestrators"
        SINKS = "sinks"
        SOURCES = "sources"
        TRANSFORMERS = "transformers"

    @unique
    class DbtCapability(StrEnum):
        """dbt operations exposed by the Meltano service layer."""

        DOCS = "docs"
        RUN = "run"
        SEED = "seed"
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
    class DbtOption(StrEnum):
        """dbt CLI options used by Meltano runners."""

        EXCLUDE = "--exclude"
        FULL_REFRESH = "--full-refresh"
        MODELS = "--models"
        PROJECTS_DIR = "--projects-dir"
        SELECT = "--select"

    @unique
    class DbtResourceType(StrEnum):
        """dbt manifest resource types used by project helpers."""

        MODEL = "model"
        TEST = "test"

    @unique
    class DbtPathName(StrEnum):
        """Canonical dbt project path names."""

        ANALYSIS = "analysis"
        MACROS = "macros"
        MODELS = "models"
        SEEDS = "seeds"
        TESTS = "tests"

    @unique
    class DbtFileName(StrEnum):
        """Canonical dbt file names."""

        MANIFEST = "manifest.json"
        PROJECT = "dbt_project.yml"

    @unique
    class SingerCapability(StrEnum):
        """Singer operations exposed by the Meltano service layer."""

        DISCOVER = "discover"
        SYNC = "sync"
        VALIDATE = "validate"

    @unique
    class SingerCliOption(StrEnum):
        """Singer CLI options shared by tap and target translators."""

        CATALOG = "--catalog"
        CONFIG = "--config"
        DISCOVER = "--discover"
        INPUT = "--input"
        PROPERTIES = "--properties"
        STATE = "--state"

    @unique
    class SingerMessageType(StrEnum):
        """Singer protocol message kinds."""

        ACTIVATE_VERSION = "ACTIVATE_VERSION"
        CATALOG = "CATALOG"
        RECORD = "RECORD"
        SCHEMA = "SCHEMA"
        STATE = "STATE"

    @unique
    class OperationScope(StrEnum):
        """Top-level operational areas managed by the Meltano API."""

        DBT = "dbt"
        ENVIRONMENT = "environment"
        PIPELINE = "pipeline"
        PLUGIN = "plugin"

    @unique
    class DispatchOperation(StrEnum):
        """High-level API operations dispatched by the service layer."""

    @unique
    class HandlerType(StrEnum):
        """Named handler groups exposed by the public API."""

        PIPELINE = "pipeline"
        SINK = "sink"
        SOURCE = "source"

    @unique
    class PipelineDirectory(StrEnum):
        """Standard directory layout for generated Meltano projects."""

        ANALYZE = "analyze"
        EXTRACT = "extract"
        LOAD = "load"
        NOTEBOOK = "notebook"
        ORCHESTRATE = "orchestrate"
        TRANSFORM = "transform"

    @unique
    class ServiceType(StrEnum):
        """Service identity tokens reported by Meltano service metadata."""

        DBT = "dbt"
        PIPELINE = "pipeline_service"

    @unique
    class PublicFactoryName(StrEnum):
        """Public factory names exposed by Meltano runtime helpers."""

        DBT = "Dbt"
        TAP = "Tap"
        TARGET = "Target"

    @unique
    class PluginDiscoveryLabel(StrEnum):
        """Public plugin labels returned by discovery helpers."""

        EXTRACTOR = "extractor"
        LOADER = "loader"
        TRANSFORMER = "transformer"

    @unique
    class ProjectMaturity(StrEnum):
        """Maturity levels inferred from project environment layout."""

        BASIC = "basic"
        DEVELOPING = "developing"
        MATURE = "mature"

    @unique
    class ProjectStructureComplexity(StrEnum):
        """Complexity levels inferred from dbt path customization."""

        COMPLEX = "complex"
        MODERATE = "moderate"
        SIMPLE = "simple"

    @unique
    class ProjectSdkState(StrEnum):
        """Lifecycle states reported by the Meltano SDK manager."""

        INITIALIZED = "initialized"
        LOADED = "loaded"

    @unique
    class ProductionEnvironmentToken(StrEnum):
        """Tokens that indicate production-like runtime presence."""

        LIVE = "live"
        PROD = "prod"
        PRODUCTION = "production"

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

    VALID_STATUSES: Final[frozenset[StreamStatus]] = frozenset({
        StreamStatus.INITIALIZED,
        StreamStatus.PROCESSING,
        StreamStatus.COMPLETED,
        StreamStatus.ERROR,
    })
    ACTIVE_STATUSES: Final[frozenset[StreamStatus]] = frozenset({
        StreamStatus.DISCOVERED,
        StreamStatus.SELECTED,
        StreamStatus.EXTRACTING,
    })

    @unique
    class PipelineCommand(StrEnum):
        """Pipeline CLI subcommands."""

        CREATE = "create"
        DELETE = "delete"
        LIST = "list"
        RUN = "run"
        STATUS = "status"
        STOP = "stop"

    @unique
    class CliCommand(StrEnum):
        """Top-level CLI command routing identifiers."""

        DBT = "dbt"
        PIPELINE = "pipeline"
        PLUGIN = "plugin"
        STATUS = "status"
        TAP = "tap"
        TARGET = "target"
        VERSION = "version"

    @unique
    class ExecutorCommand(StrEnum):
        """Executor available commands."""

        HEALTH = "health"
        HELP = "help"
        INFO = "info"
        INSTALL = "install"
        LIST = "list"
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
        TAP_ID = "tap_id"
        TAP_STREAM_ID = "tap_stream_id"
        TAP_TYPE = "tap_type"
        TARGET_LOADED = "target_loaded"
        VERSION = "version"

    @unique
    class SchemaKey(StrEnum):
        """JSON Schema structure field names."""

        INTEGER = "integer"
        NUMBER = "number"
        OBJECT = "object"
        PROPERTIES = "properties"
        SCHEMA = "schema"
        STRING = "string"
        TYPE = "type"
