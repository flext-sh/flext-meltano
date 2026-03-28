"""FLEXT Meltano config constants — logging, service, defaults, capabilities."""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final


class FlextMeltanoConstantsConfig:
    """Meltano configuration, defaults, and operational constants."""

    class Logging:
        """Logging configuration constants."""

        DEFAULT_LEVEL: Final[str] = "INFO"
        INCLUDE_TRANSFORM_NAME: Final[bool] = True
        INCLUDE_RECORD_COUNT: Final[bool] = True
        LOG_FORMAT: Final[str] = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        MELTANO_PERFORMANCE_THRESHOLD_WARNING: Final[int] = 5000
        MELTANO_PERFORMANCE_THRESHOLD_CRITICAL: Final[int] = 10000

    class Service:
        """Service validation constants."""

        MIN_NAME_LENGTH: Final[int] = 3
        MAX_NAME_LENGTH: Final[int] = 50
        VALID_NAME_PATTERN: Final[str] = "^[a-zA-Z0-9_-]+$"

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

    class Environments:
        """Valid environment sets for validation."""

        VALID: Final[frozenset[str]] = frozenset({
            "development",
            "staging",
            "production",
            "testing",
        })

    class ComponentTypes:
        """Valid component/plugin type sets."""

        VALID: Final[frozenset[str]] = frozenset({
            "sources",
            "sinks",
            "transformers",
            "orchestrators",
        })

    class Prefixes:
        """Plugin name prefix conventions."""

        TAP: Final[str] = "tap-"
        TARGET: Final[str] = "target-"
        DBT: Final[str] = "dbt-"

    class Defaults:
        """Default values used across services."""

        SERVICE_VERSION: Final[str] = "0.9.9"
        API_VERSION: Final[str] = "0.9.0"
        TIMEOUT_SECONDS: Final[int] = 300
        TEST_MULTIPLIER: Final[int] = 3
        MOCK_RECORD_COUNT: Final[int] = 3

    class CliDefaults:
        """CLI-specific default values."""

        MIN_ARGS_WITH_CONFIG: Final[int] = 2
        PIPELINES_ROOT_ENV: Final[str] = "FLEXT_MELTANO_PIPELINES_DIR"
        PIPELINE_CONFIG_FILE: Final[str] = "pipeline.json"
        PIPELINE_PID_FILE: Final[str] = "pipeline.pid"

    class Capabilities:
        """Plugin capability lists."""

        DBT: Final[tuple[str, ...]] = ("run", "test", "docs", "seed")
        SINGER: Final[tuple[str, ...]] = ("discover", "sync", "validate")

    class Operations:
        """API operation identifiers."""

        ALL: Final[tuple[str, ...]] = (
            "pipeline",
            "plugin",
            "dbt",
            "environment",
        )
        DISPATCH: Final[tuple[str, ...]] = (
            "create_pipeline",
            "execute_pipeline",
            "install_plugin",
            "list_plugins",
            "configure_environment",
            "run_dbt_models",
            "test_dbt_models",
            "run_elt_pipeline",
        )

    class Handlers:
        """Service handler type identifiers."""

        ALL: Final[tuple[str, ...]] = ("source", "sink", "pipeline")

    class MockValues:
        """Default values for mock/stub data generation."""

        EXECUTION_DURATION: Final[float] = 0.5
        STAGE_DURATIONS: Final[tuple[float, ...]] = (0.3, 0.2)
        DBT_EXECUTION_TIME: Final[float] = 45.2
        DEFAULT_MOCK_INT: Final[int] = 1
        DEFAULT_MOCK_FLOAT: Final[float] = 1.0

    class FilePaths:
        """Additional file/directory path constants."""

        DBT_OUTPUT_DIR: Final[str] = "target"
        DBT_DOCS_INDEX: Final[str] = "index.html"
        STANDARD_DIRS: Final[tuple[str, ...]] = (
            "extract",
            "load",
            "transform",
            "analyze",
            "notebook",
            "orchestrate",
        )

    class BatchDefaults:
        """Batch processing defaults."""

        DEFAULT_BATCH_SIZE: Final[int] = 1000
        COMMAND_TIMEOUT: Final[int] = 300
