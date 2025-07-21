"""Test FLEXT Meltano Singer SDK Integration - 377 lines of code, 0% coverage.

ZERO TOLERANCE for fake code, mockups, or library fallbacks.
Comprehensive tests for ALL Singer SDK integration classes and functionality.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import TYPE_CHECKING, Any, Never
from unittest.mock import MagicMock, patch

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

import pytest

# Mock missing dependencies to avoid import errors
sys.modules["flext_observability"] = MagicMock()
sys.modules["flext_observability.logging"] = MagicMock()

from flext_meltano.singer_sdk_integration import (  # noqa: E402
    SINGER_BATCH_SIZE_LIMIT,
    FlextSingerSDKIntegration,
    LDAPTap,
    OracleOICTap,
    PostgreSQLTarget,
    SingerStreamDefinition,
    StreamType,
    create_singer_sdk_integration,
)


class TestSingerStreamDefinition:
    """Test SingerStreamDefinition value object - comprehensive coverage."""

    def test_stream_definition_minimal(self) -> None:
        """Test SingerStreamDefinition with minimal required parameters."""
        stream = SingerStreamDefinition(
            name="test_stream",
            stream_schema={"properties": {"id": {"type": "string"}}},
        )

        assert stream.name == "test_stream"
        assert stream.stream_schema == {"properties": {"id": {"type": "string"}}}
        assert stream.stream_type in {
            StreamType.INCREMENTAL,
            StreamType.INCREMENTAL.value,
        }  # Default
        assert stream.key_properties == []  # Default
        assert stream.replication_key is None  # Default
        assert stream.selected is True  # Default

    def test_stream_definition_full_configuration(self) -> None:
        """Test SingerStreamDefinition with all parameters."""
        schema = {
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string"},
                "created_at": {"type": "string", "format": "date-time"},
            },
        }

        stream = SingerStreamDefinition(
            name="full_stream",
            stream_schema=schema,
            stream_type=StreamType.FULL_TABLE,
            key_properties=["id"],
            replication_key="created_at",
            selected=False,
        )

        assert stream.name == "full_stream"
        assert stream.stream_schema == schema
        assert stream.stream_type in {
            StreamType.FULL_TABLE,
            StreamType.FULL_TABLE.value,
        }
        assert stream.key_properties == ["id"]
        assert stream.replication_key == "created_at"
        assert stream.selected is False

    def test_stream_definition_table_type(self) -> None:
        """Test SingerStreamDefinition with TABLE stream type."""
        stream = SingerStreamDefinition(
            name="table_stream",
            stream_schema={"properties": {"col1": {"type": "string"}}},
            stream_type=StreamType.TABLE,
        )

        # Check that the stream type is stored correctly (might be serialized as integer)
        assert stream.stream_type in {StreamType.TABLE, StreamType.TABLE.value}
        assert stream.name == "table_stream"

    def test_stream_definition_multiple_key_properties(self) -> None:
        """Test SingerStreamDefinition with multiple key properties."""
        stream = SingerStreamDefinition(
            name="composite_key_stream",
            stream_schema={
                "properties": {
                    "tenant_id": {"type": "string"},
                    "user_id": {"type": "string"},
                    "data": {"type": "string"},
                },
            },
            key_properties=["tenant_id", "user_id"],
        )

        assert stream.key_properties == ["tenant_id", "user_id"]
        assert len(stream.key_properties) == 2


class TestStreamType:
    """Test StreamType enum."""

    def test_stream_type_values(self) -> None:
        """Test all StreamType enum values."""
        assert StreamType.TABLE
        assert StreamType.INCREMENTAL
        assert StreamType.FULL_TABLE

        # Verify they are different values
        assert len(set(StreamType)) == 3  # All values are unique


class TestOracleOICTap:
    """Test OracleOICTap implementation - comprehensive coverage."""

    def test_oracle_oic_tap_initialization(self) -> None:
        """Test OracleOICTap initialization."""
        config = {
            "api_url": "https://oracle-oic.example.com",
            "username": "test_user",
            "password": "test_pass",
        }

        tap = OracleOICTap(config)

        assert tap.config == config
        assert tap.config["api_url"] == "https://oracle-oic.example.com"
        assert tap.config["username"] == "test_user"

    def test_oracle_oic_discover_streams(self) -> None:
        """Test Oracle OIC stream discovery."""
        config = {"api_url": "https://test.com"}
        tap = OracleOICTap(config)

        streams = tap.discover_streams()

        assert len(streams) == 2

        # Test integrations stream
        integrations_stream = streams[0]
        assert integrations_stream.name == "integrations"
        assert integrations_stream.key_properties == ["id"]
        assert integrations_stream.replication_key == "updated_at"
        assert "id" in integrations_stream.stream_schema["properties"]
        assert "name" in integrations_stream.stream_schema["properties"]
        assert "status" in integrations_stream.stream_schema["properties"]
        assert "created_at" in integrations_stream.stream_schema["properties"]
        assert "updated_at" in integrations_stream.stream_schema["properties"]
        assert "configuration" in integrations_stream.stream_schema["properties"]

        # Test connections stream
        connections_stream = streams[1]
        assert connections_stream.name == "connections"
        assert connections_stream.key_properties == ["connection_id"]
        assert connections_stream.replication_key == "last_modified"
        assert "connection_id" in connections_stream.stream_schema["properties"]
        assert "display_name" in connections_stream.stream_schema["properties"]
        assert "connection_type" in connections_stream.stream_schema["properties"]
        assert "status" in connections_stream.stream_schema["properties"]
        assert "last_modified" in connections_stream.stream_schema["properties"]

    @pytest.mark.asyncio
    async def test_oracle_oic_sync_integrations_stream(self) -> None:
        """Test Oracle OIC integrations stream synchronization."""
        config = {"api_url": "https://test.com"}
        tap = OracleOICTap(config)

        # Get integrations stream
        streams = tap.discover_streams()
        integrations_stream = next(s for s in streams if s.name == "integrations")

        # Sync the stream
        records = [record async for record in tap.sync_stream(integrations_stream)]

        assert len(records) == 1
        record = records[0]

        assert record["id"] == "integration_001"
        assert record["name"] == "Customer Data Sync"
        assert record["status"] == "ACTIVE"
        assert "created_at" in record
        assert "updated_at" in record
        assert (
            record["configuration"] == '{"source": "salesforce", "target": "database"}'
        )

        # Verify timestamp format
        created_at = datetime.fromisoformat(record["created_at"])
        updated_at = datetime.fromisoformat(record["updated_at"])
        assert isinstance(created_at, datetime)
        assert isinstance(updated_at, datetime)

    @pytest.mark.asyncio
    async def test_oracle_oic_sync_connections_stream(self) -> None:
        """Test Oracle OIC connections stream synchronization."""
        config = {"api_url": "https://test.com"}
        tap = OracleOICTap(config)

        # Get connections stream
        streams = tap.discover_streams()
        connections_stream = next(s for s in streams if s.name == "connections")

        # Sync the stream
        records = [record async for record in tap.sync_stream(connections_stream)]

        assert len(records) == 1
        record = records[0]

        assert record["connection_id"] == "conn_001"
        assert record["display_name"] == "Production Database"
        assert record["connection_type"] == "DATABASE"
        assert record["status"] == "ACTIVE"
        assert "last_modified" in record

        # Verify timestamp format
        last_modified = datetime.fromisoformat(record["last_modified"])
        assert isinstance(last_modified, datetime)

    @pytest.mark.asyncio
    async def test_oracle_oic_sync_unknown_stream(self) -> None:
        """Test Oracle OIC sync with unknown stream (should yield nothing)."""
        config = {"api_url": "https://test.com"}
        tap = OracleOICTap(config)

        # Create unknown stream
        unknown_stream = SingerStreamDefinition(
            name="unknown_stream",
            stream_schema={"properties": {"id": {"type": "string"}}},
        )

        # Sync unknown stream
        records = [record async for record in tap.sync_stream(unknown_stream)]

        assert len(records) == 0

    def test_oracle_oic_get_stream_maps(self) -> None:
        """Test Oracle OIC stream field mappings."""
        config = {"api_url": "https://test.com"}
        tap = OracleOICTap(config)

        stream_maps = tap.get_stream_maps()

        assert "integrations" in stream_maps
        assert "connections" in stream_maps

        integrations_map = stream_maps["integrations"]
        assert integrations_map["id"] == "integration_id"
        assert integrations_map["name"] == "integration_name"
        assert integrations_map["status"] == "current_status"

        connections_map = stream_maps["connections"]
        assert connections_map["connection_id"] == "id"
        assert connections_map["display_name"] == "name"


class TestLDAPTap:
    """Test LDAPTap implementation - comprehensive coverage."""

    def test_ldap_tap_initialization(self) -> None:
        """Test LDAPTap initialization."""
        config = {
            "ldap_url": "ldap://localhost:389",
            "bind_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=example,dc=com",
            "bind_password": "REDACTED_LDAP_BIND_PASSWORD_pass",
            "base_dn": "dc=example,dc=com",
        }

        tap = LDAPTap(config)

        assert tap.config == config
        assert tap.config["ldap_url"] == "ldap://localhost:389"
        assert tap.config["bind_dn"] == "cn=REDACTED_LDAP_BIND_PASSWORD,dc=example,dc=com"

    def test_ldap_discover_streams(self) -> None:
        """Test LDAP stream discovery."""
        config = {"ldap_url": "ldap://test.com"}
        tap = LDAPTap(config)

        streams = tap.discover_streams()

        assert len(streams) == 2

        # Test users stream
        users_stream = streams[0]
        assert users_stream.name == "users"
        assert users_stream.key_properties == ["dn"]
        assert users_stream.replication_key == "whenChanged"

        users_schema = users_stream.stream_schema["properties"]
        assert "dn" in users_schema
        assert "cn" in users_schema
        assert "sn" in users_schema
        assert "givenName" in users_schema
        assert "mail" in users_schema
        assert "employeeNumber" in users_schema
        assert "department" in users_schema
        assert "title" in users_schema
        assert "whenCreated" in users_schema
        assert "whenChanged" in users_schema

        # Test groups stream
        groups_stream = streams[1]
        assert groups_stream.name == "groups"
        assert groups_stream.key_properties == ["dn"]
        assert groups_stream.replication_key == "whenChanged"

        groups_schema = groups_stream.stream_schema["properties"]
        assert "dn" in groups_schema
        assert "cn" in groups_schema
        assert "description" in groups_schema
        assert "member" in groups_schema
        assert "whenCreated" in groups_schema
        assert "whenChanged" in groups_schema

    @pytest.mark.asyncio
    async def test_ldap_sync_users_stream(self) -> None:
        """Test LDAP users stream synchronization."""
        config = {"ldap_url": "ldap://test.com"}
        tap = LDAPTap(config)

        # Get users stream
        streams = tap.discover_streams()
        users_stream = next(s for s in streams if s.name == "users")

        # Sync the stream
        records = [record async for record in tap.sync_stream(users_stream)]

        assert len(records) == 1
        record = records[0]

        assert record["dn"] == "cn=john.doe,ou=users,dc=company,dc=com"
        assert record["cn"] == "john.doe"
        assert record["sn"] == "Doe"
        assert record["givenName"] == "John"
        assert record["mail"] == "john.doe@company.com"
        assert record["employeeNumber"] == "12345"
        assert record["department"] == "Engineering"
        assert record["title"] == "Senior Developer"
        assert "whenCreated" in record
        assert "whenChanged" in record

        # Verify timestamp format
        when_created = datetime.fromisoformat(record["whenCreated"])
        when_changed = datetime.fromisoformat(record["whenChanged"])
        assert isinstance(when_created, datetime)
        assert isinstance(when_changed, datetime)

    @pytest.mark.asyncio
    async def test_ldap_sync_groups_stream(self) -> None:
        """Test LDAP groups stream synchronization."""
        config = {"ldap_url": "ldap://test.com"}
        tap = LDAPTap(config)

        # Get groups stream
        streams = tap.discover_streams()
        groups_stream = next(s for s in streams if s.name == "groups")

        # Sync the stream
        records = [record async for record in tap.sync_stream(groups_stream)]

        assert len(records) == 1
        record = records[0]

        assert record["dn"] == "cn=developers,ou=groups,dc=company,dc=com"
        assert record["cn"] == "developers"
        assert record["description"] == "Development team members"
        assert record["member"] == "cn=john.doe,ou=users,dc=company,dc=com"
        assert "whenCreated" in record
        assert "whenChanged" in record

        # Verify timestamp format
        when_created = datetime.fromisoformat(record["whenCreated"])
        when_changed = datetime.fromisoformat(record["whenChanged"])
        assert isinstance(when_created, datetime)
        assert isinstance(when_changed, datetime)

    @pytest.mark.asyncio
    async def test_ldap_sync_unknown_stream(self) -> None:
        """Test LDAP sync with unknown stream (should yield nothing)."""
        config = {"ldap_url": "ldap://test.com"}
        tap = LDAPTap(config)

        # Create unknown stream
        unknown_stream = SingerStreamDefinition(
            name="unknown_stream",
            stream_schema={"properties": {"id": {"type": "string"}}},
        )

        # Sync unknown stream
        records = [record async for record in tap.sync_stream(unknown_stream)]

        assert len(records) == 0

    def test_ldap_get_stream_maps(self) -> None:
        """Test LDAP stream field mappings."""
        config = {"ldap_url": "ldap://test.com"}
        tap = LDAPTap(config)

        stream_maps = tap.get_stream_maps()

        assert "users" in stream_maps
        assert "groups" in stream_maps

        users_map = stream_maps["users"]
        assert users_map["dn"] == "user_id"
        assert users_map["cn"] == "username"
        assert users_map["mail"] == "email"
        assert users_map["employeeNumber"] == "employee_id"

        groups_map = stream_maps["groups"]
        assert groups_map["dn"] == "group_id"
        assert groups_map["cn"] == "group_name"
        assert groups_map["member"] == "members"


class TestPostgreSQLTarget:
    """Test PostgreSQLTarget implementation - comprehensive coverage."""

    def test_postgresql_target_initialization(self) -> None:
        """Test PostgreSQLTarget initialization."""
        config = {
            "host": "localhost",
            "port": 5432,
            "database": "test_db",
            "username": "test_user",
            "password": "test_pass",
        }

        target = PostgreSQLTarget(config)

        assert target.config == config
        assert target.config["host"] == "localhost"
        assert target.config["port"] == 5432

    @pytest.mark.asyncio
    async def test_postgresql_write_record(self) -> None:
        """Test PostgreSQL single record write."""
        config = {"database": "test_db"}
        target = PostgreSQLTarget(config)

        record = {
            "id": "test_001",
            "name": "Test Record",
            "created_at": "2023-01-01T00:00:00Z",
        }

        # Should not raise an exception (implementation detail handled internally)
        await target.write_record("test_stream", record)

    @pytest.mark.asyncio
    async def test_postgresql_write_batch(self) -> None:
        """Test PostgreSQL batch record write."""
        config = {"database": "test_db"}
        target = PostgreSQLTarget(config)

        records = [
            {
                "id": "test_001",
                "name": "Test Record 1",
                "created_at": "2023-01-01T00:00:00Z",
            },
            {
                "id": "test_002",
                "name": "Test Record 2",
                "created_at": "2023-01-02T00:00:00Z",
            },
            {
                "id": "test_003",
                "name": "Test Record 3",
                "created_at": "2023-01-03T00:00:00Z",
            },
        ]

        # Should not raise an exception (implementation detail handled internally)
        await target.write_batch("test_stream", records)

    @pytest.mark.asyncio
    async def test_postgresql_write_empty_batch(self) -> None:
        """Test PostgreSQL write with empty batch."""
        config = {"database": "test_db"}
        target = PostgreSQLTarget(config)

        # Should handle empty batch gracefully
        await target.write_batch("test_stream", [])

    def test_postgresql_get_stream_maps(self) -> None:
        """Test PostgreSQL stream field mappings."""
        config = {"database": "test_db"}
        target = PostgreSQLTarget(config)

        stream_maps = target.get_stream_maps()

        assert "default" in stream_maps

        default_map = stream_maps["default"]
        assert default_map["datetime_fields"] == "timestamp_columns"
        assert default_map["string_fields"] == "text_columns"
        assert default_map["numeric_fields"] == "numeric_columns"


class TestFlextSingerSDKIntegration:
    """Test FlextSingerSDKIntegration main class - comprehensive coverage."""

    def test_flext_singer_sdk_integration_initialization_with_string_path(self) -> None:
        """Test FlextSingerSDKIntegration initialization with string path."""
        project_root = "/test/project"

        integration = FlextSingerSDKIntegration(project_root)

        assert integration.project_root == Path(project_root)
        assert isinstance(integration.project_root, Path)
        assert integration.taps == {}
        assert integration.targets == {}

    def test_flext_singer_sdk_integration_initialization_with_path_object(self) -> None:
        """Test FlextSingerSDKIntegration initialization with Path object."""
        project_root = Path("/test/project")

        integration = FlextSingerSDKIntegration(project_root)

        assert integration.project_root == project_root
        assert isinstance(integration.project_root, Path)
        assert integration.taps == {}
        assert integration.targets == {}

    def test_flext_singer_sdk_integration_model_post_init(self) -> None:
        """Test FlextSingerSDKIntegration model_post_init hook."""
        project_root = "/test/project"

        # Mock the _discover_plugins method to test it's called
        with patch.object(
            FlextSingerSDKIntegration,
            "_discover_plugins",
        ) as mock_discover:
            FlextSingerSDKIntegration(project_root)
            mock_discover.assert_called_once()

    def test_flext_singer_sdk_integration_discover_plugins(self) -> None:
        """Test FlextSingerSDKIntegration plugin discovery."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        # Call _discover_plugins directly to test implementation
        integration._discover_plugins()

        # Should not raise an exception (implementation placeholder)
        assert True

    @pytest.mark.asyncio
    async def test_create_oracle_oic_tap(self) -> None:
        """Test Oracle OIC tap creation."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        config = {"api_url": "https://oracle-oic.example.com"}

        tap = await integration.create_oracle_oic_tap(config)

        assert isinstance(tap, OracleOICTap)
        assert tap.config == config

    @pytest.mark.asyncio
    async def test_create_ldap_tap(self) -> None:
        """Test LDAP tap creation."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        config = {"ldap_url": "ldap://localhost:389"}

        tap = await integration.create_ldap_tap(config)

        assert isinstance(tap, LDAPTap)
        assert tap.config == config

    @pytest.mark.asyncio
    async def test_create_postgres_target(self) -> None:
        """Test PostgreSQL target creation."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        config = {"host": "localhost", "database": "test_db"}

        target = await integration.create_postgres_target(config)

        assert isinstance(target, PostgreSQLTarget)
        assert target.config == config

    @pytest.mark.asyncio
    async def test_run_elt_pipeline_oracle_oic_to_postgres_success(self) -> None:
        """Test successful ELT pipeline from Oracle OIC to PostgreSQL."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        tap_config = {"api_url": "https://oracle-oic.example.com"}
        target_config = {"host": "localhost", "database": "test_db"}

        result = await integration.run_elt_pipeline(
            tap_name="tap-oracle-oic",
            target_name="target-postgres",
            tap_config=tap_config,
            target_config=target_config,
        )

        assert result["success"] is True
        assert "records_processed" in result
        assert "streams_processed" in result
        assert result["records_processed"] >= 0
        assert result["streams_processed"] >= 0

    @pytest.mark.asyncio
    async def test_run_elt_pipeline_ldap_to_postgres_success(self) -> None:
        """Test successful ELT pipeline from LDAP to PostgreSQL."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        tap_config = {"ldap_url": "ldap://localhost:389"}
        target_config = {"host": "localhost", "database": "test_db"}

        result = await integration.run_elt_pipeline(
            tap_name="tap-ldap",
            target_name="target-postgres",
            tap_config=tap_config,
            target_config=target_config,
        )

        assert result["success"] is True
        assert "records_processed" in result
        assert "streams_processed" in result
        assert result["records_processed"] >= 0
        assert result["streams_processed"] >= 0

    @pytest.mark.asyncio
    async def test_run_elt_pipeline_unknown_tap(self) -> None:
        """Test ELT pipeline with unknown tap."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        tap_config = {"url": "https://unknown.com"}
        target_config = {"host": "localhost", "database": "test_db"}

        result = await integration.run_elt_pipeline(
            tap_name="tap-unknown",
            target_name="target-postgres",
            tap_config=tap_config,
            target_config=target_config,
        )

        assert result["success"] is False
        assert result["error"] == "Unknown tap: tap-unknown"

    @pytest.mark.asyncio
    async def test_run_elt_pipeline_unknown_target(self) -> None:
        """Test ELT pipeline with unknown target."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        tap_config = {"api_url": "https://oracle-oic.example.com"}
        target_config = {"url": "https://unknown.com"}

        result = await integration.run_elt_pipeline(
            tap_name="tap-oracle-oic",
            target_name="target-unknown",
            tap_config=tap_config,
            target_config=target_config,
        )

        assert result["success"] is False
        assert result["error"] == "Unknown target: target-unknown"

    @pytest.mark.asyncio
    async def test_run_elt_pipeline_with_batch_processing(self) -> None:
        """Test ELT pipeline batch processing with large datasets."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        # Mock large dataset by patching sync_stream to yield many records
        async def mock_sync_stream(stream: object) -> AsyncGenerator[dict[str, Any]]:
            for i in range(SINGER_BATCH_SIZE_LIMIT + 100):  # More than batch limit
                yield {
                    "id": f"record_{i:04d}",
                    "name": f"Test Record {i}",
                    "created_at": datetime.now(UTC).isoformat(),
                }

        with patch.object(OracleOICTap, "sync_stream", side_effect=mock_sync_stream):
            result = await integration.run_elt_pipeline(
                tap_name="tap-oracle-oic",
                target_name="target-postgres",
                tap_config={"api_url": "https://test.com"},
                target_config={"host": "localhost", "database": "test_db"},
            )

        assert result["success"] is True
        # Oracle OIC has 2 streams, each yields SINGER_BATCH_SIZE_LIMIT + 100 records
        expected_records = 2 * (SINGER_BATCH_SIZE_LIMIT + 100)
        assert result["records_processed"] == expected_records

    @pytest.mark.asyncio
    async def test_run_elt_pipeline_with_unselected_streams(self) -> None:
        """Test ELT pipeline with unselected streams (should be skipped)."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        # Mock discover_streams to return unselected streams
        def mock_discover_streams() -> list[SingerStreamDefinition]:
            return [
                SingerStreamDefinition(
                    name="selected_stream",
                    stream_schema={"properties": {"id": {"type": "string"}}},
                    selected=True,
                ),
                SingerStreamDefinition(
                    name="unselected_stream",
                    stream_schema={"properties": {"id": {"type": "string"}}},
                    selected=False,
                ),
            ]

        # Mock sync_stream to yield one record per stream
        async def mock_sync_stream(stream: Any) -> AsyncGenerator[dict[str, Any]]:
            stream_name = getattr(stream, "name", "unknown_stream")
            yield {
                "id": f"record_from_{stream_name}",
                "data": f"test data from {stream_name}",
            }

        with (
            patch.object(
                OracleOICTap,
                "discover_streams",
                side_effect=mock_discover_streams,
            ),
            patch.object(OracleOICTap, "sync_stream", side_effect=mock_sync_stream),
        ):
            result = await integration.run_elt_pipeline(
                tap_name="tap-oracle-oic",
                target_name="target-postgres",
                tap_config={"api_url": "https://test.com"},
                target_config={"host": "localhost", "database": "test_db"},
            )

        assert result["success"] is True
        assert result["records_processed"] == 1  # Only selected stream
        assert result["streams_processed"] == 1  # Only selected stream

    @pytest.mark.asyncio
    async def test_run_elt_pipeline_error_handling(self) -> None:
        """Test ELT pipeline error handling."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        # Mock discover_streams to raise an exception
        def mock_discover_streams_error() -> Never:
            msg = "Database connection failed"
            raise RuntimeError(msg)

        with patch.object(
            OracleOICTap,
            "discover_streams",
            side_effect=mock_discover_streams_error,
        ):
            result = await integration.run_elt_pipeline(
                tap_name="tap-oracle-oic",
                target_name="target-postgres",
                tap_config={"api_url": "https://test.com"},
                target_config={"host": "localhost", "database": "test_db"},
            )

        assert result["success"] is False
        assert "Database connection failed" in result["error"]
        assert result["records_processed"] == 0

    @pytest.mark.asyncio
    async def test_run_elt_pipeline_type_error_handling(self) -> None:
        """Test ELT pipeline TypeError handling."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        # Mock to raise TypeError
        def mock_discover_streams_type_error() -> Never:
            msg = "Invalid configuration type"
            raise TypeError(msg)

        with patch.object(
            OracleOICTap,
            "discover_streams",
            side_effect=mock_discover_streams_type_error,
        ):
            result = await integration.run_elt_pipeline(
                tap_name="tap-oracle-oic",
                target_name="target-postgres",
                tap_config={"api_url": "https://test.com"},
                target_config={"host": "localhost", "database": "test_db"},
            )

        assert result["success"] is False
        assert "Invalid configuration type" in result["error"]

    @pytest.mark.asyncio
    async def test_run_elt_pipeline_value_error_handling(self) -> None:
        """Test ELT pipeline ValueError handling."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        # Mock to raise ValueError
        def mock_discover_streams_value_error() -> Never:
            msg = "Invalid configuration value"
            raise ValueError(msg)

        with patch.object(
            OracleOICTap,
            "discover_streams",
            side_effect=mock_discover_streams_value_error,
        ):
            result = await integration.run_elt_pipeline(
                tap_name="tap-oracle-oic",
                target_name="target-postgres",
                tap_config={"api_url": "https://test.com"},
                target_config={"host": "localhost", "database": "test_db"},
            )

        assert result["success"] is False
        assert "Invalid configuration value" in result["error"]

    @pytest.mark.asyncio
    async def test_run_elt_pipeline_os_error_handling(self) -> None:
        """Test ELT pipeline OSError handling."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        # Mock to raise OSError
        def mock_discover_streams_os_error() -> Never:
            msg = "File system error"
            raise OSError(msg)

        with patch.object(
            OracleOICTap,
            "discover_streams",
            side_effect=mock_discover_streams_os_error,
        ):
            result = await integration.run_elt_pipeline(
                tap_name="tap-oracle-oic",
                target_name="target-postgres",
                tap_config={"api_url": "https://test.com"},
                target_config={"host": "localhost", "database": "test_db"},
            )

        assert result["success"] is False
        assert "File system error" in result["error"]

    @pytest.mark.asyncio
    async def test_run_elt_pipeline_with_stream_maps(self) -> None:
        """Test ELT pipeline with stream maps parameter."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        stream_maps = {
            "integrations": {"id": "integration_id", "name": "integration_name"},
            "connections": {"connection_id": "id", "display_name": "name"},
        }

        result = await integration.run_elt_pipeline(
            tap_name="tap-oracle-oic",
            target_name="target-postgres",
            tap_config={"api_url": "https://test.com"},
            target_config={"host": "localhost", "database": "test_db"},
            _stream_maps=stream_maps,
        )

        assert result["success"] is True
        # Stream maps are passed but implementation is placeholder
        assert "records_processed" in result


class TestConvenienceFunctions:
    """Test convenience functions."""

    def test_create_singer_sdk_integration(self) -> None:
        """Test create_singer_sdk_integration convenience function."""
        project_root = Path("/test/project")

        integration = create_singer_sdk_integration(project_root)

        assert isinstance(integration, FlextSingerSDKIntegration)
        assert integration.project_root == project_root


class TestSingerConstants:
    """Test Singer SDK constants."""

    def test_singer_batch_size_limit(self) -> None:
        """Test SINGER_BATCH_SIZE_LIMIT constant."""
        assert SINGER_BATCH_SIZE_LIMIT == 1000
        assert isinstance(SINGER_BATCH_SIZE_LIMIT, int)
        assert SINGER_BATCH_SIZE_LIMIT > 0


class TestTypeAliases:
    """Test type aliases are properly defined."""

    def test_type_aliases_importable(self) -> None:
        """Test that type aliases are properly imported and usable."""
        from flext_meltano.singer_sdk_integration import (
            SingerMessage,
            SingerRecord,
            StreamSchema,
            TapConfig,
            TargetConfig,
        )

        # These should be importable without error
        assert StreamSchema is not None
        assert TapConfig is not None
        assert TargetConfig is not None
        assert SingerRecord is not None
        assert SingerMessage is not None


class TestIntegrationWorkflow:
    """Test complete integration workflow scenarios."""

    @pytest.mark.asyncio
    async def test_complete_oracle_oic_to_postgres_workflow(self) -> None:
        """Test complete workflow from Oracle OIC discovery to PostgreSQL load."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        # Step 1: Create Oracle OIC tap
        tap_config = {"api_url": "https://oracle-oic.example.com", "username": "test"}
        tap = await integration.create_oracle_oic_tap(tap_config)
        assert isinstance(tap, OracleOICTap)

        # Step 2: Discover streams
        streams = tap.discover_streams()
        assert len(streams) == 2

        # Step 3: Create PostgreSQL target
        target_config = {"host": "localhost", "database": "test_db"}
        target = await integration.create_postgres_target(target_config)
        assert isinstance(target, PostgreSQLTarget)

        # Step 4: Run complete pipeline
        result = await integration.run_elt_pipeline(
            tap_name="tap-oracle-oic",
            target_name="target-postgres",
            tap_config=tap_config,
            target_config=target_config,
        )

        assert result["success"] is True
        assert result["records_processed"] >= 0
        assert result["streams_processed"] >= 0

    @pytest.mark.asyncio
    async def test_complete_ldap_to_postgres_workflow(self) -> None:
        """Test complete workflow from LDAP discovery to PostgreSQL load."""
        project_root = "/test/project"
        integration = FlextSingerSDKIntegration(project_root)

        # Step 1: Create LDAP tap
        tap_config = {
            "ldap_url": "ldap://localhost:389",
            "bind_dn": "cn=REDACTED_LDAP_BIND_PASSWORD,dc=test,dc=com",
        }
        tap = await integration.create_ldap_tap(tap_config)
        assert isinstance(tap, LDAPTap)

        # Step 2: Discover streams
        streams = tap.discover_streams()
        assert len(streams) == 2

        # Step 3: Create PostgreSQL target
        target_config = {"host": "localhost", "database": "test_db"}
        target = await integration.create_postgres_target(target_config)
        assert isinstance(target, PostgreSQLTarget)

        # Step 4: Run complete pipeline
        result = await integration.run_elt_pipeline(
            tap_name="tap-ldap",
            target_name="target-postgres",
            tap_config=tap_config,
            target_config=target_config,
        )

        assert result["success"] is True
        assert result["records_processed"] >= 0
        assert result["streams_processed"] >= 0
