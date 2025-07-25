"""Generic Tap Orchestrators - Consolidated Implementation.

Centralized orchestration for all FLEXT tap operations, eliminating
duplication across flext-tap-* projects.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from flext_core import FlextResult, FlextValueObject, get_logger

if TYPE_CHECKING:
    from collections.abc import Iterator

logger = get_logger(__name__)


class FlextTapConfig(FlextValueObject):
    """Base configuration for all FLEXT taps."""

    tap_type: str
    batch_size: int = 1000
    max_connections: int = 10
    connection_timeout: int = 30


class FlextTapOrchestrator(ABC):
    """Base orchestrator for all FLEXT taps.

    This eliminates duplication across flext-tap-oracle-wms,
    flext-tap-ldap, flext-tap-oracle-oic, etc.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """Initialize tap orchestrator."""
        self.config = config
        self.batch_size = config.get("batch_size", 1000)
        self._initialized = False
        self._streams: dict[str, Any] = {}

    @abstractmethod
    def _create_connection(self, config: dict[str, Any]) -> object:
        """Create tap-specific connection."""

    @abstractmethod
    def _discover_streams(self) -> FlextResult[dict[str, Any]]:
        """Discover available streams from source."""

    @abstractmethod
    def _extract_records(
        self,
        stream_name: str,
        state: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Extract records from specific stream."""

    def initialize(self) -> FlextResult[None]:
        """Initialize the orchestrator."""
        try:
            if self._initialized:
                return FlextResult.ok(None)

            # Create tap-specific connection
            self.connection = self._create_connection(self.config)

            # Discover streams
            discovery_result = self._discover_streams()
            if not discovery_result.is_success:
                return FlextResult.fail(
                    f"Stream discovery failed: {discovery_result.error}",
                )

            self._streams = discovery_result.data

            logger.info(
                "Tap orchestrator initialized: %s",
                self.config.get("tap_type", "unknown"),
            )
            logger.info("Discovered %d streams", len(self._streams))
            self._initialized = True

            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Tap orchestrator initialization failed")
            return FlextResult.fail(f"Initialization failed: {e}")

    def get_catalog(self) -> FlextResult[dict[str, Any]]:
        """Get Singer catalog with discovered streams."""
        try:
            if not self._initialized:
                init_result = self.initialize()
                if not init_result.is_success:
                    return init_result

            catalog = {
                "streams": [
                    {
                        "tap_stream_id": stream_name,
                        "schema": stream_info.get("schema", {}),
                        "metadata": stream_info.get("metadata", []),
                    }
                    for stream_name, stream_info in self._streams.items()
                ],
            }

            logger.info("Generated catalog with %d streams", len(catalog["streams"]))
            return FlextResult.ok(catalog)

        except Exception as e:
            logger.exception("Catalog generation failed")
            return FlextResult.fail(f"Catalog generation failed: {e}")

    def sync_stream(
        self,
        stream_name: str,
        state: dict[str, Any] | None = None,
    ) -> FlextResult[Iterator[dict[str, Any]]]:
        """Sync specific stream and yield Singer messages."""
        try:
            if not self._initialized:
                init_result = self.initialize()
                if not init_result.is_success:
                    return init_result

            if stream_name not in self._streams:
                return FlextResult.fail(f"Stream not found: {stream_name}")

            # Emit SCHEMA message
            schema_message = {
                "type": "SCHEMA",
                "stream": stream_name,
                "schema": self._streams[stream_name].get("schema", {}),
                "key_properties": self._streams[stream_name].get("key_properties", []),
            }

            def message_generator() -> Iterator[dict[str, Any]]:
                yield schema_message

                # Extract and emit RECORD messages
                record_count = 0
                for record in self._extract_records(stream_name, state):
                    record_message = {
                        "type": "RECORD",
                        "stream": stream_name,
                        "record": record,
                    }
                    yield record_message
                    record_count += 1

                    # Yield STATE message periodically
                    if record_count % self.batch_size == 0:
                        state_message = {
                            "type": "STATE",
                            "value": {
                                "bookmarks": {
                                    stream_name: {
                                        "replication_key_value": record.get(
                                            "updated_at",
                                        ),
                                        "version": 1,
                                    },
                                },
                            },
                        }
                        yield state_message

                logger.info(
                    "Sync completed for %s: %d records",
                    stream_name,
                    record_count,
                )

            return FlextResult.ok(message_generator())

        except Exception as e:
            logger.exception("Stream sync failed: %s", stream_name)
            return FlextResult.fail(f"Stream sync failed: {e}")

    def sync_all_streams(
        self,
        catalog: dict[str, Any],
        state: dict[str, Any] | None = None,
    ) -> FlextResult[Iterator[dict[str, Any]]]:
        """Sync all selected streams based on catalog."""
        try:
            if not self._initialized:
                init_result = self.initialize()
                if not init_result.is_success:
                    return init_result

            # Get selected streams from catalog
            selected_streams = []
            for stream in catalog.get("streams", []):
                metadata = stream.get("metadata", [])
                # Check if stream is selected (simplified logic)
                is_selected = any(
                    entry.get("metadata", {}).get("selected", False)
                    for entry in metadata
                    if entry.get("breadcrumb") == []
                )
                if is_selected:
                    selected_streams.append(stream["tap_stream_id"])

            if not selected_streams:
                logger.warning("No streams selected for sync")
                return FlextResult.ok(iter([]))

            def all_streams_generator() -> Iterator[dict[str, Any]]:
                for stream_name in selected_streams:
                    logger.info("Starting sync for stream: %s", stream_name)

                    stream_state = (
                        state.get("bookmarks", {}).get(stream_name) if state else None
                    )
                    sync_result = self.sync_stream(stream_name, stream_state)

                    if sync_result.is_success:
                        yield from sync_result.data
                    else:
                        logger.error(
                            "Failed to sync stream %s: %s",
                            stream_name,
                            sync_result.error,
                        )

            return FlextResult.ok(all_streams_generator())

        except Exception as e:
            logger.exception("All streams sync failed")
            return FlextResult.fail(f"All streams sync failed: {e}")

    def cleanup(self) -> FlextResult[None]:
        """Cleanup all resources."""
        try:
            self._streams.clear()
            self._initialized = False

            logger.info("Tap orchestrator cleanup completed")
            return FlextResult.ok(None)

        except Exception as e:
            logger.exception("Tap orchestrator cleanup failed")
            return FlextResult.fail(f"Cleanup failed: {e}")


class FlextOracleTapOrchestrator(FlextTapOrchestrator):
    """Oracle-specific tap orchestrator."""

    def _create_connection(self, config: dict[str, Any]) -> object:
        """Create Oracle connection."""
        from flext_db_oracle.connection.factory import (  # noqa: PLC0415
            create_oracle_connection,
        )

        oracle_config = {
            "host": config.get("host", "localhost"),
            "port": config.get("port", 1521),
            "service_name": config.get("service_name", "XE"),
            "username": config.get("username"),
            "password": config.get("password"),
            "schema": config.get("default_source_schema", "ORACLE"),
        }

        return create_oracle_connection(oracle_config)

    def _discover_streams(self) -> FlextResult[dict[str, Any]]:
        """Discover Oracle tables as streams."""
        try:
            # Query Oracle system tables to discover available tables
            query = """
                SELECT table_name, column_name, data_type, nullable
                FROM user_tab_columns
                ORDER BY table_name, column_id
            """

            result = self.connection.execute_query(query)
            if not result.is_success:
                return FlextResult.fail(
                    f"Oracle discovery query failed: {result.error}",
                )

            # Group columns by table
            tables = {}
            for row in result.data:
                table_name = row["table_name"].lower()
                if table_name not in tables:
                    tables[table_name] = {
                        "schema": {
                            "type": "object",
                            "properties": {},
                        },
                        "metadata": [],
                        "key_properties": ["id"],  # Assume ID column
                    }

                # Add column to schema
                column_name = row["column_name"].lower()
                oracle_type = row["data_type"]

                # Map Oracle types to JSON Schema types
                json_type = "string"  # default
                if oracle_type in ("NUMBER", "INTEGER"):
                    json_type = "number"
                elif oracle_type in ("DATE", "TIMESTAMP"):
                    json_type = "string"

                tables[table_name]["schema"]["properties"][column_name] = {
                    "type": json_type,
                }

            logger.info("Discovered %d Oracle tables", len(tables))
            return FlextResult.ok(tables)

        except (KeyError, ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"Oracle stream discovery failed: {e}")

    def _extract_records(
        self,
        stream_name: str,
        state: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Extract records from Oracle table."""
        try:
            # Build SELECT query (table name is validated during discovery)
            query = f'SELECT * FROM "{stream_name.upper()}"'  # noqa: S608

            # Add WHERE clause for incremental extraction if state exists
            if state and "replication_key_value" in state:
                replication_key = "updated_at"  # Assume this column exists
                last_value = state["replication_key_value"]
                query += f" WHERE {replication_key} > :1"
                params = [last_value]
            else:
                params = []

            # Execute query in batches
            offset = 0
            while True:
                batch_query = f"{query} OFFSET {offset} ROWS FETCH NEXT {self.batch_size} ROWS ONLY"

                result = self.connection.execute_query(batch_query, params)
                if not result.is_success:
                    logger.error("Oracle query failed: %s", result.error)
                    break

                batch_records = result.data
                if not batch_records:
                    break

                for record in batch_records:
                    # Convert Oracle record to dict with lowercase keys
                    yield {k.lower(): v for k, v in record.items()}

                offset += self.batch_size

                if len(batch_records) < self.batch_size:
                    break

        except Exception:
            logger.exception(
                "Oracle record extraction failed for stream: %s",
                stream_name,
            )


class FlextLDAPTapOrchestrator(FlextTapOrchestrator):
    """LDAP-specific tap orchestrator."""

    def _create_connection(self, config: dict[str, Any]) -> object:
        """Create LDAP connection."""
        from flext_ldap.client import FlextLdapClient  # noqa: PLC0415

        ldap_config = {
            "host": config.get("host"),
            "port": config.get("port", 389),
            "bind_dn": config.get("bind_dn"),
            "bind_password": config.get("bind_password"),
            "base_dn": config.get("base_dn"),
        }

        return FlextLdapClient(ldap_config)

    def _discover_streams(self) -> FlextResult[dict[str, Any]]:
        """Discover LDAP object classes as streams."""
        try:
            # Query LDAP schema to discover object classes
            result = self.connection.search_schema()
            if not result.is_success:
                return FlextResult.fail(f"LDAP schema discovery failed: {result.error}")

            # Create streams for common object classes
            streams = {
                "users": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "dn": {"type": "string"},
                            "cn": {"type": "string"},
                            "mail": {"type": "string"},
                            "uid": {"type": "string"},
                            "objectClass": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                    },
                    "metadata": [],
                    "key_properties": ["dn"],
                },
                "groups": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "dn": {"type": "string"},
                            "cn": {"type": "string"},
                            "member": {"type": "array", "items": {"type": "string"}},
                            "objectClass": {
                                "type": "array",
                                "items": {"type": "string"},
                            },
                        },
                    },
                    "metadata": [],
                    "key_properties": ["dn"],
                },
            }

            logger.info("Discovered %d LDAP streams", len(streams))
            return FlextResult.ok(streams)

        except (KeyError, ValueError, TypeError, AttributeError) as e:
            return FlextResult.fail(f"LDAP stream discovery failed: {e}")

    def _extract_records(
        self,
        stream_name: str,
        state: dict[str, Any] | None = None,
    ) -> Iterator[dict[str, Any]]:
        """Extract records from LDAP."""
        try:
            # Map stream names to LDAP filters
            filters = {
                "users": "(objectClass=inetOrgPerson)",
                "groups": "(objectClass=groupOfNames)",
            }

            ldap_filter = filters.get(stream_name, "(objectClass=*)")

            # Search LDAP directory
            result = self.connection.search_entries(
                search_filter=ldap_filter,
                base_dn=self.config.get("base_dn", ""),
                scope="subtree",
            )

            if not result.is_success:
                logger.error("LDAP search failed: %s", result.error)
                return

            for entry in result.data:
                # Convert LDAP entry to record
                record = {"dn": entry.get("dn", "")}

                for attr_name, attr_values in entry.get("attributes", {}).items():
                    if isinstance(attr_values, list) and len(attr_values) == 1:
                        record[attr_name] = attr_values[0]
                    else:
                        record[attr_name] = attr_values

                yield record

        except Exception:
            logger.exception(
                "LDAP record extraction failed for stream: %s",
                stream_name,
            )


# Factory functions
def create_tap_orchestrator(config: dict[str, Any]) -> FlextTapOrchestrator:
    """Create appropriate tap orchestrator based on config."""
    tap_type = config.get("tap_type", "").lower()

    if "oracle" in tap_type:
        return FlextOracleTapOrchestrator(config)
    if "ldap" in tap_type:
        return FlextLDAPTapOrchestrator(config)
    msg = f"Unsupported tap type: {tap_type}"
    raise ValueError(msg)


__all__ = [
    "FlextLDAPTapOrchestrator",
    "FlextOracleTapOrchestrator",
    "FlextTapConfig",
    "FlextTapOrchestrator",
    "create_tap_orchestrator",
]
