"""Oracle Tap specific type definitions - Maximum flext-core integration.

This module provides Oracle Tap specific type definitions using flext-core as the
foundation. All common Oracle types are inherited from flext-core to ensure
consistency and eliminate code duplication across Oracle projects.
"""

from __future__ import annotations

from typing import Annotated, Any, Literal, TypedDict

from pydantic import Field, StringConstraints

# ARCHITECTURAL FIX: Oracle-specific types defined locally (not in flext-core)
# flext-core is abstract and should NEVER contain concrete technology types
# Import from flext-core for foundational patterns (standardized)

# Define missing type aliases
PositiveInt = Annotated[int, Field(gt=0)]
NonEmptyStr = Annotated[str, StringConstraints(min_length=1)]
TimeoutSeconds = Annotated[int, Field(ge=1, le=3600)]

# Oracle-specific types defined locally (CLEAN ARCHITECTURE COMPLIANCE)
OracleHost = Annotated[str, StringConstraints(min_length=1, max_length=255)]
OraclePort = Annotated[int, Field(ge=1, le=65535)]
OracleUsername = Annotated[str, StringConstraints(min_length=1, max_length=128)]
OraclePassword = Annotated[str, StringConstraints(min_length=1, max_length=256)]
OracleServiceName = Annotated[str, StringConstraints(min_length=1, max_length=64)]
OracleSID = Annotated[str, StringConstraints(min_length=1, max_length=64)]
OracleSchema = Annotated[str, StringConstraints(min_length=1, max_length=64)]
OracleQueryTimeout = Annotated[int, Field(ge=1, le=3600)]
OracleFetchSize = Annotated[int, Field(ge=1, le=10000)]
OracleArraySize = Annotated[int, Field(ge=1, le=10000)]

# Singer-specific types defined locally
SingerBatchSize = Annotated[int, Field(ge=1, le=100000)]
SingerMaxRecords = Annotated[int, Field(ge=1)]
SingerParallelStreams = Annotated[int, Field(ge=1, le=100)]
SingerReplicationMethod = Literal["FULL_TABLE", "INCREMENTAL", "LOG_BASED"]
SingerStateInterval = Annotated[int, Field(ge=1, le=10000)]

# ==============================================================================
# TAP-SPECIFIC TYPES - Only types unique to tap operations
# ==============================================================================

# Discovery and Schema Detection Types
TapDiscoveryMode = Literal["automatic", "manual", "catalog_only"]
TapTablePattern = Annotated[
    str,
    StringConstraints(min_length=1, max_length=128),
    Field(description="SQL LIKE pattern for table discovery"),
]
TapSchemaPattern = Annotated[
    str,
    StringConstraints(min_length=1, max_length=64),
    Field(description="SQL LIKE pattern for schema discovery"),
]


# Stream Selection Types
class TapStreamSelection(TypedDict):
    """Stream selection configuration for tap."""

    selected: bool
    replication_method: SingerReplicationMethod
    replication_key: str | None
    key_properties: list[str]
    forced_replication_method: SingerReplicationMethod | None


class TapCatalogEntry(TypedDict):
    """Catalog entry for Oracle tap stream."""

    tap_stream_id: str
    stream: str
    table_name: str
    schema: dict[str, Any]
    metadata: list[dict[str, Any]]


# Incremental Replication Types
TapBookmarkType = Literal["timestamp", "integer", "date", "datetime"]
TapBookmarkValue = str | int | float  # Can be various types depending on column


class TapStateMessage(TypedDict):
    """State message for incremental syncing."""

    bookmarks: dict[str, dict[str, TapBookmarkValue]]
    currently_syncing: str | None


# Connection Pool Types (Tap-specific configuration)
class TapConnectionPoolConfig(TypedDict):
    """Connection pool configuration for Oracle tap."""

    size: PositiveInt
    max_overflow: PositiveInt
    timeout: TimeoutSeconds
    recycle: TimeoutSeconds
    pre_ping: bool


# Performance Tuning Types
TapPerformanceProfile = Literal["development", "staging", "production", "high_volume"]


class TapCircuitBreakerConfig(TypedDict):
    """Circuit breaker configuration for Oracle connection resilience."""

    failure_threshold: PositiveInt
    timeout: TimeoutSeconds
    expected_exception: type[Exception] | None


# Schema Flattening Types (Tap-specific feature)
class TapFlatteningConfig(TypedDict):
    """Schema flattening configuration for complex Oracle types."""

    enabled: bool
    max_depth: PositiveInt
    separator: NonEmptyStr
    preserve_arrays: bool
    flatten_objects: bool


# Oracle Query Optimization Types
TapQueryHint = Annotated[
    str,
    StringConstraints(pattern=r"^/\*\+.*\*/$"),
    Field(description="Oracle SQL hint in /*+ hint */ format"),
]


class TapQueryOptimization(TypedDict):
    """Query optimization configuration for Oracle performance."""

    use_hints: bool
    hints: list[TapQueryHint]
    parallel_degree: PositiveInt | None
    use_index: str | None


# Column Metadata for Discovery
class TapColumnMetadata(TypedDict):
    """Oracle column metadata for schema discovery."""

    column_name: str
    data_type: str
    is_nullable: bool
    column_default: str | None
    character_maximum_length: int | None
    numeric_precision: int | None
    numeric_scale: int | None
    is_primary_key: bool
    is_foreign_key: bool


class TapTableMetadata(TypedDict):
    """Oracle table metadata for schema discovery."""

    table_name: str
    schema_name: str
    table_type: Literal["TABLE", "VIEW", "MATERIALIZED VIEW"]
    row_count: int | None
    columns: list[TapColumnMetadata]
    primary_keys: list[str]
    foreign_keys: list[dict[str, str]]


# ==============================================================================
# COMPOSITE CONFIGURATION TYPES - For maximum code reduction
# ==============================================================================


# Complete Tap Configuration (combines all settings)
class TapOracleCompleteConfig(TypedDict):
    """Complete Oracle tap configuration with all options."""

    host: OracleHost
    port: OraclePort
    service_name: OracleServiceName | None
    sid: OracleSID | None
    username: OracleUsername
    password: OraclePassword
    schema: OracleSchema | None
    batch_size: SingerBatchSize
    max_parallel_streams: SingerParallelStreams
    connection_pool_size: PositiveInt
    query_timeout: OracleQueryTimeout
    fetch_size: OracleFetchSize
    array_size: OracleArraySize
    discovery_mode: TapDiscoveryMode
    table_pattern: TapTablePattern | None
    schema_pattern: TapSchemaPattern | None
    replication_method: SingerReplicationMethod
    max_records: SingerMaxRecords
    state_interval: SingerStateInterval
    flattening: TapFlatteningConfig
    circuit_breaker: TapCircuitBreakerConfig
    performance_profile: TapPerformanceProfile
    query_optimization: TapQueryOptimization
    log_level: str
    enable_sql_logging: bool
    enable_metrics: bool


# Environment-specific Configuration
class TapEnvironmentConfig(TypedDict):
    """Environment-specific Oracle tap configurations."""

    development: TapOracleCompleteConfig
    staging: TapOracleCompleteConfig
    production: TapOracleCompleteConfig
