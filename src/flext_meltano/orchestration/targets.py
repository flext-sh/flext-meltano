"""Generic Target Orchestrators - Consolidated Implementation.

Centralized orchestration for all FLEXT target operations, eliminating
duplication across flext-target-* projects.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from flext_core import FlextResult, FlextValueObject, get_logger

logger = get_logger(__name__)


class FlextTargetConfig(FlextValueObject):
    """Base configuration for all FLEXT targets."""

    target_type: str
    batch_size: int = 1000
    max_connections: int = 10
    connection_timeout: int = 30


class FlextTargetOrchestrator(ABC):
    """Base orchestrator for all FLEXT targets.

    This eliminates duplication across flext-target-oracle-wms,
    flext-target-ldap, flext-target-oracle-oic, etc.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize target orchestrator."""
        self.config = config
        self.batch_size = config.get("batch_size", 1000)
        self.current_batch: dict[str, list[dict[str, Any]]] = {}
        self._initialized = False

    @abstractmethod
    def _create_connection(self, config: dict[str, Any]) -> object:
        """Create target-specific connection."""

    @abstractmethod
    def _process_schema_message(self, message: dict[str, Any]) -> FlextResult[None]:
        """Process SCHEMA message for specific target."""

    @abstractmethod
    def _insert_batch(
        self, stream_name: str, records: list[dict[str, Any]],
    ) -> FlextResult[None]:
        """Insert batch into specific target."""

    def initialize(self) -> FlextResult[None]:
        """Initialize the orchestrator."""
        try:
            if self._initialized:
                return FlextResult.ok(None)

            # Create target-specific connection
            self.connection = self._create_connection(self.config)

            target_type = self.config.get("target_type", "unknown")
            logger.info("Target orchestrator initialized: %s", target_type)
            self._initialized = True

            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Target orchestrator initialization failed")
            return FlextResult.fail(f"Initialization failed: {e}")

    def process_singer_message(self, message: dict[str, Any]) -> FlextResult[None]:
        """Process Singer message using appropriate handler."""
        try:
            if not self._initialized:
                init_result = self.initialize()
                if not init_result.is_success:
                    return init_result

            message_type = message.get("type")

            if message_type == "SCHEMA":
                return self._handle_schema_message(message)
            if message_type == "RECORD":
                return self._handle_record_message(message)
            if message_type == "STATE":
                return self._handle_state_message(message)

            return FlextResult.fail(f"Unknown message type: {message_type}")

        except Exception as e:
            logger.exception("Singer message processing failed")
            return FlextResult.fail(f"Message processing failed: {e}")

    def _handle_schema_message(self, message: dict[str, Any]) -> FlextResult[None]:
        """Handle SCHEMA message."""
        try:
            stream_name = message.get("stream")
            schema = message.get("schema")

            if not stream_name or not schema:
                return FlextResult.fail("Invalid SCHEMA message")

            # Process through target-specific handler
            result = self._process_schema_message(message)
            if not result.is_success:
                return result

            # Initialize batch for this stream
            self.current_batch[stream_name] = []

            logger.info("SCHEMA message processed for stream: %s", stream_name)
            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("SCHEMA message handling failed")
            return FlextResult.fail(f"SCHEMA handling failed: {e}")

    def _handle_record_message(self, message: dict[str, Any]) -> FlextResult[None]:
        """Handle RECORD message with batching."""
        try:
            stream_name = message.get("stream")
            record = message.get("record")

            if not stream_name or not record:
                return FlextResult.fail("Invalid RECORD message")

            # Add to batch
            if stream_name not in self.current_batch:
                self.current_batch[stream_name] = []

            self.current_batch[stream_name].append(record)

            # Check if batch is full
            if len(self.current_batch[stream_name]) >= self.batch_size:
                flush_result = self._flush_batch(stream_name)
                if not flush_result.is_success:
                    return flush_result

            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("RECORD message handling failed")
            return FlextResult.fail(f"RECORD handling failed: {e}")

    def _handle_state_message(self, message: dict[str, Any]) -> FlextResult[None]:
        """Handle STATE message."""
        try:
            # State handling is generic for most targets
            logger.debug("STATE message processed: %s", message.get("value", {}))
            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("STATE message handling failed")
            return FlextResult.fail(f"STATE handling failed: {e}")

    def _flush_batch(self, stream_name: str) -> FlextResult[None]:
        """Flush batch of records."""
        try:
            if (
                stream_name not in self.current_batch
                or not self.current_batch[stream_name]
            ):
                return FlextResult.ok(None)

            records = self.current_batch[stream_name]

            # Insert batch using target-specific implementation
            insert_result = self._insert_batch(stream_name, records)
            if not insert_result.is_success:
                return insert_result

            # Clear batch
            self.current_batch[stream_name] = []

            logger.info("Flushed batch for %s: %d records", stream_name, len(records))
            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Batch flush failed for stream: %s", stream_name)
            return FlextResult.fail(f"Batch flush failed: {e}")

    def finalize(self) -> FlextResult[dict[str, Any]]:
        """Finalize processing and get summary."""
        try:
            # Flush any remaining batches
            for stream_name in list(self.current_batch.keys()):
                if self.current_batch[stream_name]:
                    flush_result = self._flush_batch(stream_name)
                    if not flush_result.is_success:
                        logger.warning(
                            "Final batch flush failed for %s: %s",
                            stream_name,
                            flush_result.error,
                        )

            summary = {
                "target_type": self.config.get("target_type", "unknown"),
                "streams_processed": list(self.current_batch.keys()),
                "batch_size": self.batch_size,
            }

            logger.info("Target orchestrator finalized: %s", summary)
            return FlextResult.ok(summary)

        except Exception as e:
            logger.exception("Target orchestrator finalization failed")
            return FlextResult.fail(f"Finalization failed: {e}")

    def cleanup(self) -> FlextResult[None]:
        """Cleanup all resources."""
        try:
            # Clear batches
            self.current_batch.clear()
            self._initialized = False

            logger.info("Target orchestrator cleanup completed")
            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Target orchestrator cleanup failed")
            return FlextResult.fail(f"Cleanup failed: {e}")


class FlextOracleTargetOrchestrator(FlextTargetOrchestrator):
    """Oracle-specific target orchestrator."""

    def _create_connection(self, config: dict[str, Any]) -> object:
        """Create Oracle connection."""
        # Lazy import to avoid circular dependencies
        try:
            from flext_db_oracle.connection.factory import (  # noqa: PLC0415
                create_oracle_connection,
            )
        except ImportError:
            msg = "flext-db-oracle package required for Oracle targets"
            raise ImportError(msg) from None

        oracle_config = {
            "host": config.get("host", "localhost"),
            "port": config.get("port", 1521),
            "service_name": config.get("service_name", "XE"),
            "username": config.get("username"),
            "password": config.get("password"),
            "schema": config.get("default_target_schema", "FLEXT"),
        }

        return create_oracle_connection(oracle_config)

    def _process_schema_message(self, message: dict[str, Any]) -> FlextResult[None]:
        """Process SCHEMA message for Oracle target."""
        try:
            # Oracle-specific schema processing
            stream_name = message.get("stream")
            message.get("schema")

            # Could create/validate table here
            logger.debug("Oracle schema processed for stream: %s", stream_name)
            return FlextResult.ok(None)

        except (KeyError, ValueError, TypeError) as e:
            return FlextResult.fail(f"Oracle schema processing failed: {e}")

    def _insert_batch(
        self, stream_name: str, records: list[dict[str, Any]],
    ) -> FlextResult[None]:
        """Insert batch into Oracle."""
        try:
            if not records:
                return FlextResult.ok(None)

            # Oracle-specific batch insert logic
            table_name = f"flext_{stream_name}".upper()

            # Build parameterized INSERT (safe)
            columns = list(records[0].keys())
            quoted_columns = [f'"{col.upper()}"' for col in columns]
            placeholders = [f":{i + 1}" for i in range(len(columns))]

            # Safe parameterized query - no SQL injection risk
            insert_sql = (
                f'INSERT INTO "{table_name}" '  # noqa: S608
                f"({', '.join(quoted_columns)}) "
                f"VALUES ({', '.join(placeholders)})"
            )

            # Prepare batch parameters
            batch_params = [list(record.values()) for record in records]

            # Execute via connection
            result = self.connection.execute_batch(insert_sql, batch_params)
            if not result.is_success:
                return FlextResult.fail(f"Oracle batch insert failed: {result.error}")

            logger.info(
                "Inserted %d records into Oracle table %s", len(records), table_name,
            )
            return FlextResult.ok(None)

        except (KeyError, ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Oracle batch insertion failed: {e}")


class FlextLDAPTargetOrchestrator(FlextTargetOrchestrator):
    """LDAP-specific target orchestrator."""

    def _create_connection(self, config: dict[str, Any]) -> object:
        """Create LDAP connection."""
        # Import LDAP-specific connection from flext-ldap
        from flext_ldap.client import FlextLdapClient  # noqa: PLC0415

        ldap_config = {
            "host": config.get("host"),
            "port": config.get("port", 389),
            "bind_dn": config.get("bind_dn"),
            "bind_password": config.get("bind_password"),
            "base_dn": config.get("base_dn"),
        }

        return FlextLdapClient(ldap_config)

    def _process_schema_message(self, message: dict[str, Any]) -> FlextResult[None]:
        """Process SCHEMA message for LDAP target."""
        try:
            # LDAP-specific schema processing
            stream_name = message.get("stream")
            logger.debug("LDAP schema processed for stream: %s", stream_name)
            return FlextResult.ok(None)

        except (KeyError, ValueError, TypeError) as e:
            return FlextResult.fail(f"LDAP schema processing failed: {e}")

    def _insert_batch(
        self, stream_name: str, records: list[dict[str, Any]],
    ) -> FlextResult[None]:
        """Insert batch into LDAP."""
        try:
            if not records:
                return FlextResult.ok(None)

            # LDAP-specific batch insert logic
            for record in records:
                # Convert record to LDAP entry format
                dn = (
                    record.get("dn")
                    or f"cn={record.get('name', 'unknown')},ou={stream_name}"
                )
                attributes = {k: v for k, v in record.items() if k != "dn"}

                # Add entry to LDAP
                result = self.connection.add_entry(dn, attributes)
                if not result.is_success:
                    logger.warning("Failed to add LDAP entry %s: %s", dn, result.error)

            logger.info(
                "Processed %d LDAP entries for stream %s", len(records), stream_name,
            )
            return FlextResult.ok(None)

        except (KeyError, ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"LDAP batch insertion failed: {e}")


# Factory functions
def create_target_orchestrator(config: dict[str, Any]) -> FlextTargetOrchestrator:
    """Create appropriate target orchestrator based on config."""
    target_type = config.get("target_type", "").lower()

    if "oracle" in target_type:
        return FlextOracleTargetOrchestrator(config)
    if "ldap" in target_type:
        return FlextLDAPTargetOrchestrator(config)
    msg = f"Unsupported target type: {target_type}"
    raise ValueError(msg)


__all__ = [
    "FlextLDAPTargetOrchestrator",
    "FlextOracleTargetOrchestrator",
    "FlextTargetConfig",
    "FlextTargetOrchestrator",
    "create_target_orchestrator",
]
