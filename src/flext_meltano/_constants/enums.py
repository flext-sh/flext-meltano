"""FLEXT Meltano enum constants — domain-specific enumerations."""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final


class FlextMeltanoConstantsEnums:
    """Meltano domain enumerations."""

    @unique
    class MeltanoProjectType(StrEnum):
        """Meltano project type enumeration."""

        LIBRARY = "library"
        APPLICATION = "application"
        SERVICE = "service"
        MELTANO_PROJECT = "meltano-project"
        ELT_PIPELINE = "elt-pipeline"
        DATA_PIPELINE = "data-pipeline"
        ETL_SERVICE = "etl-service"
        SINGER_TAP = "singer-tap"
        SINGER_TARGET = "singer-target"
        DBT_PROJECT = "dbt-project"
        DATA_INTEGRATION = "data-integration"
        PIPELINE_ORCHESTRATOR = "pipeline-orchestrator"
        DATA_EXTRACTOR = "data-extractor"
        DATA_LOADER = "data-loader"
        TRANSFORMATION_SERVICE = "transformation-service"

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
        """Execution modes for Meltano operations."""

        FULL = "full"
        INCREMENTAL = "incremental"
        DRY_RUN = "dry_run"
        TEST = "test"

    @unique
    class Environment(StrEnum):
        """Deployment environments for Meltano pipelines."""

        DEVELOPMENT = "development"
        STAGING = "staging"
        PRODUCTION = "production"
        TESTING = "testing"
        LOCAL = "local"

    @unique
    class ProjectEnvironment(StrEnum):
        """Canonical environment names used in generated Meltano projects."""

        DEV = "dev"
        STAGING = "staging"
        PROD = "prod"

    @unique
    class EnvironmentAlias(StrEnum):
        """Short environment aliases accepted by settings helpers."""

        DEV = "dev"
        TEST = "test"
        PROD = "prod"

    @unique
    class ComponentType(StrEnum):
        """Supported service component groups."""

        SOURCES = "sources"
        SINKS = "sinks"
        TRANSFORMERS = "transformers"
        ORCHESTRATORS = "orchestrators"

    @unique
    class DbtCapability(StrEnum):
        """dbt operations exposed by the Meltano service layer."""

        RUN = "run"
        TEST = "test"
        DOCS = "docs"
        SEED = "seed"

    @unique
    class DbtCommand(StrEnum):
        """dbt CLI commands used across Meltano integrations."""

        RUN = "run"
        TEST = "test"
        BUILD = "build"
        COMPILE = "compile"
        DOCS = "docs"
        GENERATE = "generate"

    @unique
    class DbtOption(StrEnum):
        """dbt CLI options used by Meltano runners."""

        PROJECTS_DIR = "--projects-dir"
        MODELS = "--models"
        SELECT = "--select"
        EXCLUDE = "--exclude"
        FULL_REFRESH = "--full-refresh"

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
        PROFILES = "profiles.yml"
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
        METRIC = "METRIC"
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

        CREATE_PIPELINE = "create_pipeline"
        EXECUTE_PIPELINE = "execute_pipeline"
        INSTALL_PLUGIN = "install_plugin"
        LIST_PLUGINS = "list_plugins"
        CONFIGURE_ENVIRONMENT = "configure_environment"
        RUN_DBT_MODELS = "run_dbt_models"
        TEST_DBT_MODELS = "test_dbt_models"
        RUN_ELT_PIPELINE = "run_elt_pipeline"

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

        SCHEMA = "schema"
        TYPE = "type"
        PROPERTIES = "properties"
        OBJECT = "object"
        INTEGER = "integer"
        STRING = "string"
        NUMBER = "number"
