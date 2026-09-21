"""FLEXT Meltano settings constants — logging, service, defaults, capabilities."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING, ClassVar, Self

from flext_cli import c

from flext_core import FlextSettings

from .enums import FlextMeltanoConstantsEnums

if TYPE_CHECKING:
    from flext_cli import t


class FlextMeltanoConstantsSettings(FlextSettings):
    """Meltano configuration, defaults, and operational constants.

    All constants are flat with descriptive prefixes to explain their usage.
    The MRO carries ``FlextSettings`` (ENFORCE-042); the class is a namespace
    holder, never instantiated — class-attribute access resolves via the MRO.
    """

    # ENFORCE-042 namespace-holder contract: ``FlextSettings`` contributes
    # namespacing only — instance machinery stays plain object semantics so the
    # settings singleton/validation machinery cannot leak into instantiated
    # facade composites (e.g. the ``u`` logging facade).
    def __new__(cls, *args: object, **kwargs: object) -> Self:
        _ = args, kwargs
        return object.__new__(cls)

    def __init__(self, *args: object, **kwargs: object) -> None:
        _ = self, args, kwargs

    def __setattr__(self, name: str, value: object) -> None:
        object.__setattr__(self, name, value)

    __eq__ = object.__eq__

    __hash__ = object.__hash__

    # Logging
    LOGGING_DEFAULT_LEVEL: ClassVar[str] = "INFO"
    LOGGING_INCLUDE_RECORD_COUNT: ClassVar[bool] = True
    LOGGING_INCLUDE_TRANSFORM_NAME: ClassVar[bool] = True
    LOGGING_MELTANO_PERFORMANCE_THRESHOLD_CRITICAL: ClassVar[int] = 10000

    # Service
    SERVICE_MIN_NAME_LENGTH: ClassVar[int] = 3

    # Environments
    ENVIRONMENTS_VALID: ClassVar[frozenset[FlextMeltanoConstantsEnums.Environment]] = (
        frozenset({
            FlextMeltanoConstantsEnums.Environment.DEVELOPMENT,
            FlextMeltanoConstantsEnums.Environment.STAGING,
            FlextMeltanoConstantsEnums.Environment.PRODUCTION,
            FlextMeltanoConstantsEnums.Environment.TESTING,
        })
    )
    SETTINGS_ENVIRONMENTS: ClassVar[
        tuple[FlextMeltanoConstantsEnums.Environment, ...]
    ] = (
        FlextMeltanoConstantsEnums.Environment.DEVELOPMENT,
        FlextMeltanoConstantsEnums.Environment.TESTING,
        FlextMeltanoConstantsEnums.Environment.PRODUCTION,
    )
    ENVIRONMENT_ALIASES: ClassVar[
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
    ENVIRONMENT_RUNTIME_ALIASES: ClassVar[t.StrMapping] = MappingProxyType({
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
    PRODUCTION_ENVIRONMENT_MARKERS: ClassVar[
        frozenset[FlextMeltanoConstantsEnums.ProductionEnvironmentToken]
    ] = frozenset({
        FlextMeltanoConstantsEnums.ProductionEnvironmentToken.PROD,
        FlextMeltanoConstantsEnums.ProductionEnvironmentToken.PRODUCTION,
        FlextMeltanoConstantsEnums.ProductionEnvironmentToken.LIVE,
    })

    # ComponentTypes
    COMPONENT_TYPES_VALID: ClassVar[
        frozenset[FlextMeltanoConstantsEnums.ComponentType]
    ] = frozenset({
        FlextMeltanoConstantsEnums.ComponentType.SOURCES,
        FlextMeltanoConstantsEnums.ComponentType.SINKS,
        FlextMeltanoConstantsEnums.ComponentType.TRANSFORMERS,
        FlextMeltanoConstantsEnums.ComponentType.ORCHESTRATORS,
    })

    # Defaults
    DEFAULT_SERVICE_VERSION: ClassVar[str] = "0.9.9"
    DEFAULT_API_VERSION: ClassVar[str] = "0.9.0"
    DEFAULT_TIMEOUT_SECONDS: ClassVar[int] = 300

    # CliDefaults
    CLI_DEFAULT_MIN_ARGS_WITH_CONFIG: ClassVar[int] = 2
    CLI_DEFAULT_PIPELINES_ROOT_ENV: ClassVar[str] = "FLEXT_MELTANO_PIPELINES_DIR"
    CLI_DEFAULT_PIPELINE_CONFIG_FILE: ClassVar[str] = "pipeline.json"
    CLI_DEFAULT_PIPELINE_PID_FILE: ClassVar[str] = "pipeline.pid"

    # Capabilities
    SUPPORTED_PLUGIN_TYPES: ClassVar[
        tuple[FlextMeltanoConstantsEnums.PluginType, ...]
    ] = (
        FlextMeltanoConstantsEnums.PluginType.EXTRACTORS,
        FlextMeltanoConstantsEnums.PluginType.LOADERS,
        FlextMeltanoConstantsEnums.PluginType.TRANSFORMS,
    )
    PLUGIN_GROUP_ALIASES: ClassVar[
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
    PLUGIN_DISCOVERY_LABELS: ClassVar[
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
    DBT_COMMANDS: ClassVar[tuple[FlextMeltanoConstantsEnums.DbtCommand, ...]] = (
        FlextMeltanoConstantsEnums.DbtCommand.RUN,
        FlextMeltanoConstantsEnums.DbtCommand.TEST,
        FlextMeltanoConstantsEnums.DbtCommand.BUILD,
        FlextMeltanoConstantsEnums.DbtCommand.COMPILE,
        FlextMeltanoConstantsEnums.DbtCommand.DOCS,
    )
    DBT_DEFAULT_DOCS_ARGS: ClassVar[
        tuple[FlextMeltanoConstantsEnums.DbtCommand, ...]
    ] = (FlextMeltanoConstantsEnums.DbtCommand.GENERATE,)
    DBT_DEFAULT_PATHS: ClassVar[frozenset[FlextMeltanoConstantsEnums.DbtPathName]] = (
        frozenset({
            FlextMeltanoConstantsEnums.DbtPathName.MODELS,
            FlextMeltanoConstantsEnums.DbtPathName.ANALYSIS,
            FlextMeltanoConstantsEnums.DbtPathName.TESTS,
            FlextMeltanoConstantsEnums.DbtPathName.SEEDS,
            FlextMeltanoConstantsEnums.DbtPathName.MACROS,
        })
    )
    SUPPORTED_LOG_LEVELS: ClassVar[tuple[c.LogLevel, ...]] = (
        c.LogLevel.DEBUG,
        c.LogLevel.INFO,
        c.LogLevel.WARNING,
        c.LogLevel.ERROR,
        c.LogLevel.CRITICAL,
    )

    # Operations

    # Handlers
    HANDLER_ALL: ClassVar[tuple[FlextMeltanoConstantsEnums.HandlerType, ...]] = (
        FlextMeltanoConstantsEnums.HandlerType.SOURCE,
        FlextMeltanoConstantsEnums.HandlerType.SINK,
        FlextMeltanoConstantsEnums.HandlerType.PIPELINE,
    )

    # MockValues

    # FilePaths
    FILE_PATH_DBT_OUTPUT_DIR: ClassVar[str] = "target"
    FILE_PATH_STANDARD_DIRS: ClassVar[
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
    BATCH_DEFAULT_COMMAND_TIMEOUT: ClassVar[int] = 300
    BATCH_DEFAULT_DEFAULT_BATCH_SIZE: ClassVar[int] = 1000
