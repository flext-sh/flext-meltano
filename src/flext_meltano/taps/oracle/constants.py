"""Oracle Tap Constants - Maximum flext-core integration with zero duplication.

This module provides Oracle Tap specific constants using flext-core patterns.
All Oracle DB constants are inherited from flext-core to ensure consistency
and eliminate code duplication across Oracle projects.
"""

from __future__ import annotations

from typing import ClassVar, Final


# Define Oracle-specific constants locally
class ConnectionProtocols:
    """Database connection protocol constants."""

    TCP: Final = "tcp"
    TCPS: Final = "tcps"
    IPC: Final = "ipc"
    ALL: Final = [TCP, TCPS, IPC]
    DEFAULT: Final = TCP


class OracleDBConstants:
    """Oracle database constants."""

    DEFAULT_PORT: Final = 1521
    DEFAULT_SERVICE_NAME: Final = "XE"
    DEFAULT_SCHEMA: Final = "SYSTEM"
    DEFAULT_ENCODING: Final = "utf-8"


class OracleDefaults:
    """Oracle default values."""

    CONNECTION_TIMEOUT: Final = 30
    QUERY_TIMEOUT: Final = 300
    POOL_SIZE: Final = 5
    POOL_MAX_OVERFLOW: Final = 10
    BATCH_SIZE: Final = 1000


class OracleLimits:
    """Oracle limits and constraints."""

    MAX_IDENTIFIER_LENGTH: Final = 128
    MAX_VARCHAR_LENGTH: Final = 4000
    MAX_BATCH_SIZE: Final = 10000
    MIN_BATCH_SIZE: Final = 1


class SingerOracleConstants:
    """Singer Oracle tap constants."""

    DEFAULT_STREAM_PREFIX: Final = "oracle"
    DEFAULT_BOOKMARK_KEY: Final = "replication_key_value"
    SUPPORTED_REPLICATION_METHODS: Final = ["FULL_TABLE", "INCREMENTAL"]


class SSLModes:
    """SSL mode constants."""

    DISABLE: Final = "disable"
    ALLOW: Final = "allow"
    PREFER: Final = "prefer"
    REQUIRE: Final = "require"
    VERIFY_CA: Final = "verify_ca"
    VERIFY_FULL: Final = "verify_full"
    ALL: Final = [DISABLE, ALLOW, PREFER, REQUIRE, VERIFY_CA, VERIFY_FULL]
    DEFAULT: Final = PREFER


class StandardLogLevels:
    """Standard logging levels."""

    DEBUG: Final = "DEBUG"
    INFO: Final = "INFO"
    WARNING: Final = "WARNING"
    ERROR: Final = "ERROR"
    CRITICAL: Final = "CRITICAL"


class OracleTapConstants:
    """Oracle Tap specific constants following flext-core patterns."""

    # ==============================================================================
    # CONNECTION TYPES - Tap specific
    # ==============================================================================

    CONNECTION_TYPE_DATABASE: Final = "database"
    VALID_CONNECTION_TYPES: ClassVar[set[str]] = {CONNECTION_TYPE_DATABASE}

    # ==============================================================================
    # REPLICATION METHODS - Singer spec compliant
    # ==============================================================================

    REPLICATION_METHOD_FULL_TABLE: Final = "FULL_TABLE"
    REPLICATION_METHOD_INCREMENTAL: Final = "INCREMENTAL"
    VALID_REPLICATION_METHODS: ClassVar[set[str]] = {
        REPLICATION_METHOD_FULL_TABLE,
        REPLICATION_METHOD_INCREMENTAL,
    }

    # ==============================================================================
    # SSL MODES - Use flext-core consolidated SSL modes
    # ==============================================================================

    SSL_MODE_DISABLE: Final = SSLModes.DISABLE
    SSL_MODE_ALLOW: Final = SSLModes.ALLOW
    SSL_MODE_PREFER: Final = SSLModes.PREFER
    SSL_MODE_REQUIRE: Final = SSLModes.REQUIRE
    VALID_SSL_MODES: ClassVar[set[str]] = set(SSLModes.ALL)

    # ==============================================================================
    # ORACLE CONNECTION - Use flext-core Oracle constants exclusively
    # ==============================================================================

    # Port and Protocol
    DEFAULT_PORT: Final = OracleDBConstants.DEFAULT_PORT
    DEFAULT_PROTOCOL: Final = ConnectionProtocols.DEFAULT
    VALID_PROTOCOLS: ClassVar[set[str]] = set(ConnectionProtocols.ALL)

    # Timeouts
    DEFAULT_TIMEOUT: Final = OracleDefaults.CONNECTION_TIMEOUT
    DEFAULT_CONNECT_TIMEOUT: Final = OracleDefaults.CONNECTION_TIMEOUT
    DEFAULT_QUERY_TIMEOUT: Final = OracleDefaults.QUERY_TIMEOUT
    MAX_TIMEOUT: Final = 600

    # ==============================================================================
    # PERFORMANCE - Use Oracle defaults from flext-core
    # ==============================================================================

    # Batch sizes
    DEFAULT_BATCH_SIZE: Final = OracleDefaults.BATCH_SIZE
    MAX_BATCH_SIZE: Final = OracleLimits.MAX_BATCH_SIZE
    MIN_BATCH_SIZE: Final = OracleLimits.MIN_BATCH_SIZE
    OPTIMAL_BATCH_SIZE: Final = OracleDefaults.BATCH_SIZE

    # Parallel processing
    DEFAULT_PARALLEL_STREAMS: Final = 1
    MAX_PARALLEL_STREAMS: Final = 8
    OPTIMAL_PARALLEL_STREAMS: Final = 4

    # Connection pooling
    DEFAULT_POOL_SIZE: Final = OracleDefaults.POOL_SIZE
    DEFAULT_CONNECTION_POOL_SIZE: Final = OracleDefaults.POOL_SIZE
    MAX_POOL_SIZE: Final = OracleDefaults.POOL_MAX_OVERFLOW
    MAX_CONNECTION_POOL_SIZE: Final = OracleDefaults.POOL_MAX_OVERFLOW
    MIN_POOL_SIZE: Final = 1

    # Discovery
    DEFAULT_DISCOVERY_BATCH_SIZE: Final = OracleDefaults.BATCH_SIZE
    MAX_DISCOVERY_TIMEOUT: Final = 300

    # State management
    DEFAULT_STATE_INTERVAL: Final = 1000
    STATE_MESSAGE_VERSION: Final = "1.0"

    # ==============================================================================
    # ORACLE FETCH SETTINGS - Use Oracle DB constants from flext-core
    # ==============================================================================

    DEFAULT_FETCH_SIZE: Final = 1000
    DEFAULT_ARRAY_SIZE: Final = 100
    MAX_FETCH_SIZE: Final = OracleLimits.MAX_BATCH_SIZE
    MAX_ARRAY_SIZE: Final = 10000  # Standard Oracle array processing limit

    # ==============================================================================
    # CIRCUIT BREAKER - Use flext-core patterns
    # ==============================================================================

    CIRCUIT_BREAKER_FAILURE_THRESHOLD: Final = 3
    CIRCUIT_BREAKER_TIMEOUT: Final = 60
    DEFAULT_CIRCUIT_BREAKER_FAILURES: Final = 3
    DEFAULT_CIRCUIT_BREAKER_TIMEOUT: Final = 60

    # ==============================================================================
    # SCHEMA FLATTENING - Tap specific settings
    # ==============================================================================

    DEFAULT_FLATTENING_ENABLED: Final = False
    DEFAULT_FLATTENING_MAX_DEPTH: Final = 5
    DEFAULT_FLATTENING_SEPARATOR: Final = "__"
    MAX_FLATTENING_DEPTH: Final = 10
    VALID_FLATTENING_SEPARATORS: ClassVar[set[str]] = {"__", "_", "-", "."}

    # ==============================================================================
    # LOG LEVELS - Use flext-core consolidated log levels
    # ==============================================================================

    DEFAULT_LOG_LEVEL: Final = StandardLogLevels.INFO
    VALID_LOG_LEVELS: ClassVar[set[str]] = {
        StandardLogLevels.DEBUG,
        StandardLogLevels.INFO,
        StandardLogLevels.WARNING,
        StandardLogLevels.ERROR,
        StandardLogLevels.CRITICAL,
    }
