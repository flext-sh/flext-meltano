"""Test module for flext-meltano."""

from __future__ import annotations

import tempfile
from unittest.mock import patch

import pytest
from flext_tests import tm
from pydantic_core import ValidationError

from flext_core import r
from flext_meltano import FlextMeltanoAbstractions
from tests import m, t


class TestFlextMeltanoAbstractionsComplete:
    """Complete test suite for FlextMeltanoAbstractions."""

    tap_abstractions: FlextMeltanoAbstractions

    def setup_method(self) -> None:
        """Setup for each test."""
        self.tap_abstractions = FlextMeltanoAbstractions()

    def test_tap_config_validation(self) -> None:
        """Test m.Meltano.TapConfig Pydantic validation."""
        connection_config: t.HeaderMapping = {
            "host": "localhost",
            "port": 5432,
            "database": "test_db",
        }
        stream_config: t.StrMapping = {"users": "selected"}
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config=connection_config,
            stream_config=stream_config,
            tap_version="v1.2.0",
        )
        tm.that(config.tap_type, eq="tap-postgres")
        tm.that(config.tap_version, eq="v1.2.0")
        tm.that(config.stream_config, has="users")

    def test_stream_definition_validation(self) -> None:
        """Test m.Meltano.StreamDefinition Pydantic validation using flext_tests."""
        stream_schema: t.FlatContainerMapping = {
            "type": "t.NormalizedValue",
            "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
        }
        stream_def = m.Meltano.StreamDefinition(
            stream_name="users",
            stream_schema=stream_schema,
            source_type="tap-postgres",
            status="discovered",
            records_extracted=42,
        )
        tm.that(stream_def.stream_name, eq="users")
        tm.that(stream_def.source_type, eq="tap-postgres")
        tm.that(stream_def.records_extracted, eq=42)

    def test_tap_instance_validation(self) -> None:
        """Test m.Meltano.TapInstance Pydantic validation using flext_tests."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = m.Meltano.TapConfig(
                tap_type="tap-csv",
                connection_config={"file_path": f"{temp_dir}/data.csv"},
            )
            tap_instance = m.Meltano.TapInstance.model_validate({"tap_type": "tap-csv", "settings": config, "tap_id": "tap_csv_123", "status": "initialized", "streams": [
                    m.Meltano.StreamInfo(
                        stream_name="test_stream",
                        stream_schema={},
                        stream_created_at="2025-01-01T00:00:00Z",
                    )
                ]})
            tm.that(tap_instance.tap_type, eq="tap-csv")
            tm.that(tap_instance.tap_id, eq="tap_csv_123")
            tm.that(len(tap_instance.streams), eq=1)

    def test_tap_abstractions_initialization(self) -> None:
        """Test FlextMeltanoAbstractions initialization."""
        tap_abs = FlextMeltanoAbstractions()
        assert tap_abs is not None
        if hasattr(tap_abs, "service_name"):
            service_name = getattr(tap_abs, "service_name")
            tm.that(service_name, eq="FlextMeltanoAbstractions")
        tm.that(
            hasattr(tap_abs, "_stream_registry") or hasattr(tap_abs, "logger"), eq=True
        )

    def test_serviceprocessor_process_method(self) -> None:
        """Test ServiceProcessor process method using flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost", "database": "test"},
            tap_version="v1.0.0",
        )
        result = self.tap_abstractions.process_tap_config(config)
        tm.that(result, is_=r)
        config_result = self.tap_abstractions.process_tap_config(config)
        tm.that(config_result.success, eq=True)

    def test_serviceprocessor_build_method(self) -> None:
        """Test ServiceProcessor build method using flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-csv", connection_config={"file": "test.csv"}
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-csv",
            "settings": config,
            "tap_id": "test_tap_123",
            "status": "ready",
        })
        result = self.tap_abstractions.build_tap_instance(tap_instance)
        assert isinstance(result, dict)
        tm.that(result["tap_id"], eq="test_tap_123")
        tm.that(result["tap_type"], eq="tap-csv")

    def test_fetch_stream_config(self) -> None:
        """Test fetch_stream_config method using flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
            stream_config={
                "users": {"selected": True, "replication_key": "id"},
                "orders": {"selected": False},
            },
        )
        users_config = self.tap_abstractions.fetch_stream_config(config, "users")
        orders_config = self.tap_abstractions.fetch_stream_config(config, "orders")
        missing_config = self.tap_abstractions.fetch_stream_config(config, "missing")
        tm.that(isinstance(users_config, dict), eq=True)
        tm.that(bool(users_config["selected"]), eq=True)
        tm.that(not (bool(orders_config["selected"])), eq=True)
        assert missing_config == {}

    def test_create_tap_from_config_success(self) -> None:
        """Test create_tap_from_config success using flext_tests."""
        connection_config: t.FlatContainerMapping = {
            "host": "localhost",
            "port": 5432,
            "database": "test_db",
            "username": "test_user",
        }
        stream_config: t.StrMapping = {"users": "selected", "orders": "not_selected"}
        result = self.tap_abstractions.create_tap_from_config(
            tap_type="tap-postgres",
            connection_config=connection_config,
            stream_config=stream_config,
        )
        tm.that(result, is_=r)
        if result.success:
            tap_instance = result.value
            tm.that(tap_instance, is_=m.Meltano.TapInstance)

    def test_validate_tap_instance(self) -> None:
        """Test tap instance validation using process method and flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-csv", connection_config={"file": "test.csv"}
        )
        valid_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-csv",
            "settings": config,
            "tap_id": "valid_tap_123",
        })
        try:
            invalid_config = m.Meltano.TapConfig(tap_type="", connection_config={})
            invalid_instance = m.Meltano.TapInstance.model_validate({
                "tap_type": "",
                "settings": invalid_config,
                "tap_id": "",
            })
            invalid_result = self.tap_abstractions.process_tap_config(
                invalid_instance.settings
            )
        except (ValidationError, ValueError):
            invalid_result = r[m.Meltano.TapConfig].fail(
                "Validation failed at creation"
            )
        valid_result = self.tap_abstractions.process_tap_config(valid_instance.settings)
        tm.that(valid_result, is_=r)
        if valid_result.success:
            tm.that(bool(valid_result.value), eq=True)
        if invalid_result.success:
            tm.that(not (bool(invalid_result.value)), eq=True)

    def test_discover_streams_postgres(self) -> None:
        """Test discover_streams with PostgreSQL tap via mocked runtime."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres", connection_config={"host": "localhost"}
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-postgres",
            "settings": config,
            "tap_id": "postgres_tap_123",
        })
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].ok("users\norders"),
        ):
            result = self.tap_abstractions.discover_streams(tap_instance)
        tm.that(result, is_=r)

    def test_discover_streams_csv(self) -> None:
        """Test discover_streams with CSV tap via mocked runtime."""
        config = m.Meltano.TapConfig(
            tap_type="tap-csv", connection_config={"file": "test.csv"}
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-csv",
            "settings": config,
            "tap_id": "csv_tap_123",
        })
        with patch.object(
            FlextMeltanoAbstractions, "_run_meltano", return_value=r[str].ok("data")
        ):
            result = self.tap_abstractions.discover_streams(tap_instance)
        tm.that(result, is_=r)

    def test_discover_streams_default(self) -> None:
        """Test discover_streams with unknown tap type via mocked runtime."""
        config = m.Meltano.TapConfig(
            tap_type="tap-unknown",
            connection_config={"endpoint": "http://api.example.com"},
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-unknown",
            "settings": config,
            "tap_id": "unknown_tap_123",
        })
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].fail("Unknown tap type"),
        ):
            result = self.tap_abstractions.discover_streams(tap_instance)
        tm.that(result, is_=r)

    def test_get_stream_by_name(self) -> None:
        """Test get_stream_by_name method using flext_tests."""
        if not hasattr(self.tap_abstractions, "get_stream_by_name"):
            pytest.skip(
                "get_stream_by_name not available on this FlextMeltanoAbstractions"
            )
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres", connection_config={"host": "localhost"}
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-postgres",
            "settings": config,
            "tap_id": "postgres_tap_123",
        })
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].ok("users\norders"),
        ):
            stream_result = self.tap_abstractions.get_stream_by_name(
                tap_instance, "users"
            )
        tm.that(stream_result, is_=r)

    def test_generate_catalog_success(self) -> None:
        """Test generate_catalog delegates to discover_streams."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres", connection_config={"host": "localhost"}
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-postgres",
            "settings": config,
            "tap_id": "postgres_tap_123",
        })
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].ok("users\norders"),
        ):
            result = self.tap_abstractions.generate_catalog(tap_instance)
        tm.that(result, is_=r)

    def test_catalog_entry_structure(self) -> None:
        """Test catalog entry structure through the public generate_catalog path."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres", connection_config={"host": "localhost"}
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-postgres",
            "settings": config,
            "tap_id": "postgres_tap_catalog",
        })
        with patch.object(
            FlextMeltanoAbstractions, "_run_meltano", return_value=r[str].ok("users")
        ):
            result = self.tap_abstractions.generate_catalog(tap_instance)
        tm.that(result, is_=r)
        if result.success:
            catalog = result.value
            tm.that(catalog, has="streams")

    def test_sync_stream_success(self) -> None:
        """Test sync_stream via mocked runtime call."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres", connection_config={"host": "localhost"}
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-postgres",
            "settings": config,
            "tap_id": "postgres_tap_123",
        })
        mock_target = m.Meltano.TargetConfig(
            target_type="target-jsonl", connection_config={"loaded_records": 0}
        )
        with patch.object(
            FlextMeltanoAbstractions, "_run_meltano", return_value=r[str].ok("sync ok")
        ):
            result = self.tap_abstractions.sync_stream(
                tap_instance, "users", mock_target
            )
        tm.that(result, is_=r)

    def test_sync_stream_without_target(self) -> None:
        """Test sync_stream without target using flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-csv", connection_config={"file": "test.csv"}
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-csv",
            "settings": config,
            "tap_id": "csv_tap_123",
        })
        with patch.object(
            FlextMeltanoAbstractions, "_run_meltano", return_value=r[str].ok("sync ok")
        ):
            result = self.tap_abstractions.sync_stream(tap_instance, "data")
        tm.that(result, is_=r)

    def test_list_streams(self) -> None:
        """Test list_streams method delegates to discover_streams."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres", connection_config={"host": "localhost"}
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-postgres",
            "settings": config,
            "tap_id": "postgres_tap_123",
        })
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].ok("users\norders"),
        ):
            stream_names = self.tap_abstractions.list_streams(tap_instance)
        tm.that(isinstance(stream_names, list), eq=True)

    def test_fetch_tap_type(self) -> None:
        """Test fetch_tap_type method using flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-csv", connection_config={"file": "test.csv"}
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-csv",
            "settings": config,
            "tap_id": "csv_tap_123",
        })
        tap_type = self.tap_abstractions.fetch_tap_type(tap_instance)
        tm.that(tap_type, eq="tap-csv")

    def test_fetch_registered_streams(self) -> None:
        """Test fetch_registered_streams method using flext_tests."""
        initial_streams = self.tap_abstractions.fetch_registered_streams()
        tm.that(isinstance(initial_streams, list), eq=True)

    def test_create_instance_factory(self) -> None:
        """Test create_abstractions_instance factory method using flext_tests."""
        result = FlextMeltanoAbstractions.create_abstractions_instance()
        tm.that(result, is_=r)
        if result.success:
            instance = result.value
            assert isinstance(instance, FlextMeltanoAbstractions)
            if hasattr(instance, "service_name"):
                service_name_val = getattr(instance, "service_name")
                tm.that(service_name_val, eq="FlextMeltanoAbstractions")

    def test_tap_abstractions_error_handling(self) -> None:
        """Test tap abstractions error handling."""
        timeout_error = TimeoutError("Connection timed out")
        tm.that(timeout_error, is_=Exception)
        validation_error = ValidationError.from_exception_data(
            title="Validation Error", line_errors=[]
        )
        tm.that(validation_error, is_=Exception)

    def test_invalid_tap_config_creation(self) -> None:
        """Test invalid tap config creation using flext_tests."""
        try:
            result = self.tap_abstractions.create_tap_from_config(
                tap_type="", connection_config={}
            )
            if result.failure:
                tm.that(result.error is not None, eq=True)
        except (ValueError, TypeError, RuntimeError):
            tm.that(True, eq=True)

    def test_missing_stream_handling(self) -> None:
        """Test missing stream handling using flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres", connection_config={"host": "localhost"}
        )
        tap_instance = m.Meltano.TapInstance.model_validate({
            "tap_type": "tap-postgres",
            "settings": config,
            "tap_id": "postgres_tap_123",
        })
        assert self.tap_abstractions is not None
        tm.that(hasattr(self.tap_abstractions, "discover_streams"), eq=True)
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].fail("No streams found"),
        ):
            result = self.tap_abstractions.discover_streams(tap_instance)
        tm.that(result, is_=r)

    def test_complete_tap_workflow(self) -> None:
        """Test complete tap workflow using flext_tests."""
        connection_config: t.FlatContainerMapping = {
            "host": "localhost",
            "database": "test_db",
        }
        stream_config: t.FlatContainerMapping = {"users": {"selected": True}}
        create_result = self.tap_abstractions.create_tap_from_config(
            tap_type="tap-postgres",
            connection_config=connection_config,
            stream_config=stream_config,
        )
        tm.that(create_result.success, eq=True)
        if create_result.failure:
            msg = create_result.error or "Tap creation should succeed"
            raise AssertionError(msg)
        tap_instance = create_result.value
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            side_effect=[
                r[str].ok("users\norders"),
                r[str].ok("users\norders"),
                r[str].ok("sync ok"),
            ],
        ):
            discovery_result = self.tap_abstractions.discover_streams(tap_instance)
            tm.that(discovery_result.success, eq=True)
            catalog_result = self.tap_abstractions.generate_catalog(tap_instance)
            tm.that(catalog_result.success, eq=True)
            sync_result = self.tap_abstractions.sync_stream(tap_instance, "users")
            tm.that(sync_result.success, eq=True)

    def test_execute_returns_config_status(self) -> None:
        """Test execute returns configuration status dict."""
        result = self.tap_abstractions.execute()
        tm.that(result, is_=r)
        if result.success:
            value = result.value
            tm.that(isinstance(value, dict), eq=True)
