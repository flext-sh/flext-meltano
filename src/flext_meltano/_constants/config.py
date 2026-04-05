"""FLEXT Meltano config constants — logging, service, defaults, capabilities."""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final


class FlextMeltanoConstantsConfig:
    """Meltano configuration, defaults, and operational constants.

    All constants are flat with descriptive prefixes to explain their usage.
    """

    # Logging
    LOGGING_DEFAULT_LEVEL: Final[str] = "INFO"
    LOGGING_INCLUDE_TRANSFORM_NAME: Final[bool] = True
    LOGGING_INCLUDE_RECORD_COUNT: Final[bool] = True
    LOGGING_LOG_FORMAT: Final[str] = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    LOGGING_MELTANO_PERFORMANCE_THRESHOLD_WARNING: Final[int] = 5000
    LOGGING_MELTANO_PERFORMANCE_THRESHOLD_CRITICAL: Final[int] = 10000

    # Service
    SERVICE_MIN_NAME_LENGTH: Final[int] = 3
    SERVICE_MAX_NAME_LENGTH: Final[int] = 50
    SERVICE_VALID_NAME_PATTERN: Final[str] = "^[a-zA-Z0-9_-]+$"

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

    # Environments
    ENVIRONMENTS_VALID: Final[frozenset[str]] = frozenset({
        "development",
        "staging",
        "production",
        "testing",
    })

    # ComponentTypes
    COMPONENT_TYPES_VALID: Final[frozenset[str]] = frozenset({
        "sources",
        "sinks",
        "transformers",
        "orchestrators",
    })

    # Defaults
    DEFAULT_SERVICE_VERSION: Final[str] = "0.9.9"
    DEFAULT_API_VERSION: Final[str] = "0.9.0"
    DEFAULT_TIMEOUT_SECONDS: Final[int] = 300
    DEFAULT_TEST_MULTIPLIER: Final[int] = 3
    DEFAULT_MOCK_RECORD_COUNT: Final[int] = 3

    # CliDefaults
    CLI_DEFAULT_MIN_ARGS_WITH_CONFIG: Final[int] = 2
    CLI_DEFAULT_PIPELINES_ROOT_ENV: Final[str] = "FLEXT_MELTANO_PIPELINES_DIR"
    CLI_DEFAULT_PIPELINE_CONFIG_FILE: Final[str] = "pipeline.json"
    CLI_DEFAULT_PIPELINE_PID_FILE: Final[str] = "pipeline.pid"

    # Capabilities
    CAPABILITY_DBT: Final[tuple[str, ...]] = ("run", "test", "docs", "seed")
    CAPABILITY_SINGER: Final[tuple[str, ...]] = ("discover", "sync", "validate")

    # Operations
    OPERATION_ALL: Final[tuple[str, ...]] = (
        "pipeline",
        "plugin",
        "dbt",
        "environment",
    )
    OPERATION_DISPATCH: Final[tuple[str, ...]] = (
        "create_pipeline",
        "execute_pipeline",
        "install_plugin",
        "list_plugins",
        "configure_environment",
        "run_dbt_models",
        "test_dbt_models",
        "run_elt_pipeline",
    )

    # Handlers
    HANDLER_ALL: Final[tuple[str, ...]] = ("source", "sink", "pipeline")

    # MockValues
    MOCK_EXECUTION_DURATION: Final[float] = 0.5
    MOCK_STAGE_DURATIONS: Final[tuple[float, ...]] = (0.3, 0.2)
    MOCK_DBT_EXECUTION_TIME: Final[float] = 45.2
    MOCK_DEFAULT_MOCK_INT: Final[int] = 1
    MOCK_DEFAULT_MOCK_FLOAT: Final[float] = 1.0

    # FilePaths
    FILE_PATH_DBT_OUTPUT_DIR: Final[str] = "target"
    FILE_PATH_DBT_DOCS_INDEX: Final[str] = "index.html"
    FILE_PATH_STANDARD_DIRS: Final[tuple[str, ...]] = (
        "extract",
        "load",
        "transform",
        "analyze",
        "notebook",
        "orchestrate",
    )

    # BatchDefaults
    BATCH_DEFAULT_DEFAULT_BATCH_SIZE: Final[int] = 1000
    BATCH_DEFAULT_COMMAND_TIMEOUT: Final[int] = 300
