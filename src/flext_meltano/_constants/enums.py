"""FLEXT Meltano enum constants — domain-specific enumerations."""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

from flext_core import c


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
        TRANSFORMS = "transforms"
        ORCHESTRATORS = "orchestrators"

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

        MODELS = "models"
        ANALYSIS = "analysis"
        TESTS = "tests"
        SEEDS = "seeds"
        MACROS = "macros"

    @unique
    class DbtFileName(StrEnum):
        """Canonical dbt file names."""

        PROJECT = "dbt_project.yml"
        MANIFEST = "manifest.json"

    @unique
    class SingerCapability(StrEnum):
        """Singer operations exposed by the Meltano service layer."""

        DISCOVER = "discover"
        SYNC = "sync"
        VALIDATE = "validate"

    @unique
    class SingerCliOption(StrEnum):
        """Singer CLI options shared by tap and target translators."""

        CONFIG = "--config"
        CATALOG = "--catalog"
        STATE = "--state"
        PROPERTIES = "--properties"
        INPUT = "--input"
        DISCOVER = "--discover"

    @unique
    class SingerMessageType(StrEnum):
        """Singer protocol message kinds."""

        RECORD = "RECORD"
        SCHEMA = "SCHEMA"
        STATE = "STATE"
        ACTIVATE_VERSION = "ACTIVATE_VERSION"
        CATALOG = "CATALOG"

    @unique
    class OperationScope(StrEnum):
        """Top-level operational areas managed by the Meltano API."""

        PIPELINE = "pipeline"
        PLUGIN = "plugin"
        DBT = "dbt"
        ENVIRONMENT = "environment"

    @unique
    class DispatchOperation(StrEnum):
        """High-level API operations dispatched by the service layer."""

    @unique
    class HandlerType(StrEnum):
        """Named handler groups exposed by the public API."""

        SOURCE = "source"
        SINK = "sink"
        PIPELINE = "pipeline"

    @unique
    class PipelineDirectory(StrEnum):
        """Standard directory layout for generated Meltano projects."""

        EXTRACT = "extract"
        LOAD = "load"
        TRANSFORM = "transform"
        ANALYZE = "analyze"
        NOTEBOOK = "notebook"
        ORCHESTRATE = "orchestrate"

    @unique
    class ServiceType(StrEnum):
        """Service identity tokens reported by Meltano service metadata."""

        PIPELINE = "pipeline_service"
        DBT = "dbt"

    @unique
    class PublicFactoryName(StrEnum):
        """Public factory names exposed by Meltano runtime helpers."""

        TAP = "Tap"
        TARGET = "Target"
        DBT = "Dbt"

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

        SIMPLE = "simple"
        MODERATE = "moderate"
        COMPLEX = "complex"

    @unique
    class ProjectSdkState(StrEnum):
        """Lifecycle states reported by the Meltano SDK manager."""

        INITIALIZED = "initialized"
        LOADED = "loaded"

    @unique
    class ProductionEnvironmentToken(StrEnum):
        """Tokens that indicate production-like runtime presence."""

        PROD = "prod"
        PRODUCTION = "production"
        LIVE = "live"

    @unique
    class StreamStatus(StrEnum):
        """Meltano stream statuses — single source of truth."""

        COMPLETED = c.Status.COMPLETED.value
        ERROR = c.HealthStatus.ERROR.value
        SUCCESS = c.Status.SUCCESS.value
        FAILED = c.Status.FAILED.value
        IN_PROGRESS = "in_progress"
        PENDING = c.Status.PENDING.value
        INITIALIZED = "initialized"
        PROCESSING = c.Status.PROCESSING.value
        DISCOVERED = "discovered"
        SELECTED = "selected"
        EXTRACTING = "extracting"

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
        SELECT = "select"

    @unique
    class SchemaKey(StrEnum):
        """JSON Schema structure field names."""

        SCHEMA = "schema"
        TYPE = "type"
        PROPERTIES = "properties"
        OBJECT = "object"
        INTEGER = "integer"
        STRING = "string"
        NUMBER = "number"
