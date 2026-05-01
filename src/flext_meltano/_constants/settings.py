"""FLEXT Meltano settings constants — logging, service, defaults, capabilities."""

from __future__ import annotations

from types import MappingProxyType
from typing import Final

from flext_core import c, t
from flext_meltano import FlextMeltanoConstantsEnums


class FlextMeltanoConstantsSettings:
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

    # Environments
    ENVIRONMENTS_VALID: Final[frozenset[FlextMeltanoConstantsEnums.Environment]] = (
        frozenset({
            FlextMeltanoConstantsEnums.Environment.DEVELOPMENT,
            FlextMeltanoConstantsEnums.Environment.STAGING,
            FlextMeltanoConstantsEnums.Environment.PRODUCTION,
            FlextMeltanoConstantsEnums.Environment.TESTING,
        })
    )
    SETTINGS_ENVIRONMENTS: Final[tuple[FlextMeltanoConstantsEnums.Environment, ...]] = (
        FlextMeltanoConstantsEnums.Environment.DEVELOPMENT,
        FlextMeltanoConstantsEnums.Environment.TESTING,
        FlextMeltanoConstantsEnums.Environment.PRODUCTION,
    )
    ENVIRONMENT_ALIASES: Final[
        t.MappingKV[str, FlextMeltanoConstantsEnums.Environment]
    ] = MappingProxyType({
        FlextMeltanoConstantsEnums.EnvironmentAlias.DEV: (
            FlextMeltanoConstantsEnums.Environment.DEVELOPMENT
        ),
        FlextMeltanoConstantsEnums.EnvironmentAlias.TEST: (
            FlextMeltanoConstantsEnums.Environment.TESTING
        ),
        FlextMeltanoConstantsEnums.EnvironmentAlias.PROD: (
            FlextMeltanoConstantsEnums.Environment.PRODUCTION
        ),
    })
    ENVIRONMENT_RUNTIME_ALIASES: Final[t.StrMapping] = MappingProxyType({
        FlextMeltanoConstantsEnums.Environment.DEVELOPMENT.value: (
            FlextMeltanoConstantsEnums.ProjectEnvironment.DEV
        ),
        FlextMeltanoConstantsEnums.Environment.TESTING.value: (
            FlextMeltanoConstantsEnums.EnvironmentAlias.TEST
        ),
        FlextMeltanoConstantsEnums.Environment.PRODUCTION.value: (
            FlextMeltanoConstantsEnums.ProjectEnvironment.PROD
        ),
    })
    PRODUCTION_ENVIRONMENT_MARKERS: Final[
        frozenset[FlextMeltanoConstantsEnums.ProductionEnvironmentToken]
    ] = frozenset({
        FlextMeltanoConstantsEnums.ProductionEnvironmentToken.PROD,
        FlextMeltanoConstantsEnums.ProductionEnvironmentToken.PRODUCTION,
        FlextMeltanoConstantsEnums.ProductionEnvironmentToken.LIVE,
    })

    # ComponentTypes
    COMPONENT_TYPES_VALID: Final[
        frozenset[FlextMeltanoConstantsEnums.ComponentType]
    ] = frozenset({
        FlextMeltanoConstantsEnums.ComponentType.SOURCES,
        FlextMeltanoConstantsEnums.ComponentType.SINKS,
        FlextMeltanoConstantsEnums.ComponentType.TRANSFORMERS,
        FlextMeltanoConstantsEnums.ComponentType.ORCHESTRATORS,
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
    SUPPORTED_PLUGIN_TYPES: Final[tuple[FlextMeltanoConstantsEnums.PluginType, ...]] = (
        FlextMeltanoConstantsEnums.PluginType.EXTRACTORS,
        FlextMeltanoConstantsEnums.PluginType.LOADERS,
        FlextMeltanoConstantsEnums.PluginType.TRANSFORMS,
    )
    PLUGIN_GROUP_ALIASES: Final[
        t.MappingKV[str, FlextMeltanoConstantsEnums.PluginType]
    ] = MappingProxyType({
        "extractor": FlextMeltanoConstantsEnums.PluginType.EXTRACTORS,
        FlextMeltanoConstantsEnums.PluginType.EXTRACTORS: (
            FlextMeltanoConstantsEnums.PluginType.EXTRACTORS
        ),
        "tap": FlextMeltanoConstantsEnums.PluginType.EXTRACTORS,
        "loader": FlextMeltanoConstantsEnums.PluginType.LOADERS,
        FlextMeltanoConstantsEnums.PluginType.LOADERS: (
            FlextMeltanoConstantsEnums.PluginType.LOADERS
        ),
        "target": FlextMeltanoConstantsEnums.PluginType.LOADERS,
        "transformer": FlextMeltanoConstantsEnums.PluginType.TRANSFORMS,
        "transformers": FlextMeltanoConstantsEnums.PluginType.TRANSFORMS,
        FlextMeltanoConstantsEnums.PluginType.TRANSFORMS: (
            FlextMeltanoConstantsEnums.PluginType.TRANSFORMS
        ),
        "dbt": FlextMeltanoConstantsEnums.PluginType.TRANSFORMS,
    })
    PLUGIN_DISCOVERY_LABELS: Final[
        t.MappingKV[
            FlextMeltanoConstantsEnums.PluginType,
            FlextMeltanoConstantsEnums.PluginDiscoveryLabel,
        ]
    ] = MappingProxyType({
        FlextMeltanoConstantsEnums.PluginType.EXTRACTORS: (
            FlextMeltanoConstantsEnums.PluginDiscoveryLabel.EXTRACTOR
        ),
        FlextMeltanoConstantsEnums.PluginType.LOADERS: (
            FlextMeltanoConstantsEnums.PluginDiscoveryLabel.LOADER
        ),
        FlextMeltanoConstantsEnums.PluginType.TRANSFORMS: (
            FlextMeltanoConstantsEnums.PluginDiscoveryLabel.TRANSFORMER
        ),
    })
    CAPABILITY_DBT: Final[tuple[FlextMeltanoConstantsEnums.DbtCapability, ...]] = (
        FlextMeltanoConstantsEnums.DbtCapability.RUN,
        FlextMeltanoConstantsEnums.DbtCapability.TEST,
        FlextMeltanoConstantsEnums.DbtCapability.DOCS,
        FlextMeltanoConstantsEnums.DbtCapability.SEED,
    )
    DBT_COMMANDS: Final[tuple[FlextMeltanoConstantsEnums.DbtCommand, ...]] = (
        FlextMeltanoConstantsEnums.DbtCommand.RUN,
        FlextMeltanoConstantsEnums.DbtCommand.TEST,
        FlextMeltanoConstantsEnums.DbtCommand.BUILD,
        FlextMeltanoConstantsEnums.DbtCommand.COMPILE,
        FlextMeltanoConstantsEnums.DbtCommand.DOCS,
    )
    DBT_DEFAULT_DOCS_ARGS: Final[tuple[FlextMeltanoConstantsEnums.DbtCommand, ...]] = (
        FlextMeltanoConstantsEnums.DbtCommand.GENERATE,
    )
    DBT_DEFAULT_PATHS: Final[frozenset[FlextMeltanoConstantsEnums.DbtPathName]] = (
        frozenset({
            FlextMeltanoConstantsEnums.DbtPathName.MODELS,
            FlextMeltanoConstantsEnums.DbtPathName.ANALYSIS,
            FlextMeltanoConstantsEnums.DbtPathName.TESTS,
            FlextMeltanoConstantsEnums.DbtPathName.SEEDS,
            FlextMeltanoConstantsEnums.DbtPathName.MACROS,
        })
    )
    CAPABILITY_SINGER: Final[
        tuple[FlextMeltanoConstantsEnums.SingerCapability, ...]
    ] = (
        FlextMeltanoConstantsEnums.SingerCapability.DISCOVER,
        FlextMeltanoConstantsEnums.SingerCapability.SYNC,
        FlextMeltanoConstantsEnums.SingerCapability.VALIDATE,
    )
    SUPPORTED_LOG_LEVELS: Final[tuple[c.LogLevel, ...]] = (
        c.LogLevel.DEBUG,
        c.LogLevel.INFO,
        c.LogLevel.WARNING,
        c.LogLevel.ERROR,
        c.LogLevel.CRITICAL,
    )

    # Operations
    OPERATION_ALL: Final[tuple[FlextMeltanoConstantsEnums.OperationScope, ...]] = (
        FlextMeltanoConstantsEnums.OperationScope.PIPELINE,
        FlextMeltanoConstantsEnums.OperationScope.PLUGIN,
        FlextMeltanoConstantsEnums.OperationScope.DBT,
        FlextMeltanoConstantsEnums.OperationScope.ENVIRONMENT,
    )
    OPERATION_DISPATCH: Final[
        tuple[FlextMeltanoConstantsEnums.DispatchOperation, ...]
    ] = (
        FlextMeltanoConstantsEnums.DispatchOperation.CREATE_PIPELINE,
        FlextMeltanoConstantsEnums.DispatchOperation.EXECUTE_PIPELINE,
        FlextMeltanoConstantsEnums.DispatchOperation.INSTALL_PLUGIN,
        FlextMeltanoConstantsEnums.DispatchOperation.LIST_PLUGINS,
        FlextMeltanoConstantsEnums.DispatchOperation.CONFIGURE_ENVIRONMENT,
        FlextMeltanoConstantsEnums.DispatchOperation.RUN_DBT_MODELS,
        FlextMeltanoConstantsEnums.DispatchOperation.TEST_DBT_MODELS,
        FlextMeltanoConstantsEnums.DispatchOperation.RUN_ELT_PIPELINE,
    )

    # Handlers
    HANDLER_ALL: Final[tuple[FlextMeltanoConstantsEnums.HandlerType, ...]] = (
        FlextMeltanoConstantsEnums.HandlerType.SOURCE,
        FlextMeltanoConstantsEnums.HandlerType.SINK,
        FlextMeltanoConstantsEnums.HandlerType.PIPELINE,
    )

    # MockValues
    MOCK_EXECUTION_DURATION: Final[float] = 0.5
    MOCK_STAGE_DURATIONS: Final[tuple[float, ...]] = (0.3, 0.2)
    MOCK_DBT_EXECUTION_TIME: Final[float] = 45.2
    MOCK_DEFAULT_MOCK_INT: Final[int] = 1
    MOCK_DEFAULT_MOCK_FLOAT: Final[float] = 1.0

    # FilePaths
    FILE_PATH_DBT_OUTPUT_DIR: Final[str] = "target"
    FILE_PATH_DBT_DOCS_INDEX: Final[str] = "index.html"
    FILE_PATH_STANDARD_DIRS: Final[
        tuple[FlextMeltanoConstantsEnums.PipelineDirectory, ...]
    ] = (
        FlextMeltanoConstantsEnums.PipelineDirectory.EXTRACT,
        FlextMeltanoConstantsEnums.PipelineDirectory.LOAD,
        FlextMeltanoConstantsEnums.PipelineDirectory.TRANSFORM,
        FlextMeltanoConstantsEnums.PipelineDirectory.ANALYZE,
        FlextMeltanoConstantsEnums.PipelineDirectory.NOTEBOOK,
        FlextMeltanoConstantsEnums.PipelineDirectory.ORCHESTRATE,
    )

    # BatchDefaults
    BATCH_DEFAULT_DEFAULT_BATCH_SIZE: Final[int] = 1000
    BATCH_DEFAULT_COMMAND_TIMEOUT: Final[int] = 300
