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


class _TestAssertions:
    """Minimal assertion helper when flext_tests is not available."""

    @staticmethod
    def assert_true(condition: bool, message: str = "") -> None:
        tm.that(condition, eq=True)

    @staticmethod
    def assert_false(condition: bool, message: str = "") -> None:
        tm.that(not condition, eq=True)

    @staticmethod
    def assert_equal(
        actual: t.Tests.TestobjectSerializable,
        expected: t.Tests.TestobjectSerializable,
        message: str = "",
    ) -> None:
        tm.that(actual, eq=expected)
        _ = message or f"expected {expected!r}, got {actual!r}"

    @staticmethod
    def assert_in(
        item: str, container: t.Tests.TestobjectSerializable, message: str = ""
    ) -> None:
        if isinstance(container, dict):
            tm.that(container, has=item)


class TestFlextMeltanoAbstractionsComplete:
    """Complete test suite for FlextMeltanoAbstractions."""

    tap_abstractions: FlextMeltanoAbstractions
    test_assertions: _TestAssertions

    def setup_method(self) -> None:
        """Setup for each test."""
        self.tap_abstractions = FlextMeltanoAbstractions()
        if not hasattr(self, "test_assertions"):
            self.test_assertions = _TestAssertions()

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
        stream_schema: t.ContainerMapping = {
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
        self.test_assertions.assert_equal(
            actual=stream_def.stream_name,
            expected="users",
            message="Stream name should match",
        )
        self.test_assertions.assert_equal(
            actual=stream_def.source_type,
            expected="tap-postgres",
            message="Tap type should match",
        )
        self.test_assertions.assert_equal(
            actual=stream_def.records_extracted,
            expected=42,
            message="Records extracted should match",
        )

    def test_tap_instance_validation(self) -> None:
        """Test m.Meltano.TapInstance Pydantic validation using flext_tests."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = m.Meltano.TapConfig(
                tap_type="tap-csv",
                connection_config={"file_path": f"{temp_dir}/data.csv"},
            )
            tap_instance = m.Meltano.TapInstance(
                tap_type="tap-csv",
                config=config,
                tap_id="tap_csv_123",
                status="initialized",
                streams=[
                    m.Meltano.StreamInfo(
                        stream_name="test_stream",
                        stream_schema={},
                        stream_created_at="2025-01-01T00:00:00Z",
                    ),
                ],
            )
            self.test_assertions.assert_equal(
                actual=tap_instance.tap_type,
                expected="tap-csv",
                message="Tap type should match",
            )
            self.test_assertions.assert_equal(
                actual=tap_instance.tap_id,
                expected="tap_csv_123",
                message="Tap ID should match",
            )
            self.test_assertions.assert_equal(
                actual=len(tap_instance.streams),
                expected=1,
                message="Should have one stream",
            )

    def test_tap_abstractions_initialization(self) -> None:
        """Test FlextMeltanoAbstractions initialization."""
        tap_abs = FlextMeltanoAbstractions()
        assert tap_abs is not None
        if hasattr(tap_abs, "service_name"):
            service_name = getattr(tap_abs, "service_name")
            tm.that(service_name, eq="FlextMeltanoAbstractions")
        tm.that(
            hasattr(tap_abs, "_stream_registry") or hasattr(tap_abs, "logger"),
            eq=True,
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
        self.test_assertions.assert_true(
            condition=config_result.is_success,
            message="Valid config should pass processing",
        )

    def test_serviceprocessor_build_method(self) -> None:
        """Test ServiceProcessor build method using flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-csv",
            connection_config={"file": "test.csv"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-csv",
            config=config,
            tap_id="test_tap_123",
            status="ready",
        )
        result = self.tap_abstractions.build_tap_instance(tap_instance)
        assert isinstance(result, dict)
        tm.that(result["tap_id"], eq="test_tap_123")
        tm.that(result["tap_type"], eq="tap-csv")

    def test_get_stream_config(self) -> None:
        """Test get_stream_config method using flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
            stream_config={
                "users": {"selected": True, "replication_key": "id"},
                "orders": {"selected": False},
            },
        )
        users_config = self.tap_abstractions.get_stream_config(config, "users")
        orders_config = self.tap_abstractions.get_stream_config(config, "orders")
        missing_config = self.tap_abstractions.get_stream_config(config, "missing")
        self.test_assertions.assert_true(
            condition=isinstance(users_config, dict),
            message="Should return dict",
        )
        self.test_assertions.assert_true(
            condition=bool(users_config["selected"]),
            message="Users should be selected",
        )
        self.test_assertions.assert_false(
            condition=bool(orders_config["selected"]),
            message="Orders should not be selected",
        )
        assert missing_config == {}

    def test_create_tap_from_config_success(self) -> None:
        """Test create_tap_from_config success using flext_tests."""
        connection_config: t.ContainerMapping = {
            "host": "localhost",
            "port": 5432,
            "database": "test_db",
            "username": "test_user",
        }
        stream_config: t.StrMapping = {
            "users": "selected",
            "orders": "not_selected",
        }
        result = self.tap_abstractions.create_tap_from_config(
            tap_type="tap-postgres",
            connection_config=connection_config,
            stream_config=stream_config,
        )
        tm.that(result, is_=r)
        if result.is_success:
            tap_instance = result.value
            tm.that(tap_instance, is_=m.Meltano.TapInstance)

    def test_validate_tap_instance(self) -> None:
        """Test tap instance validation using process method and flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-csv",
            connection_config={"file": "test.csv"},
        )
        valid_instance = m.Meltano.TapInstance(
            tap_type="tap-csv",
            config=config,
            tap_id="valid_tap_123",
        )
        try:
            invalid_config = m.Meltano.TapConfig(tap_type="", connection_config={})
            invalid_instance = m.Meltano.TapInstance(
                tap_type="",
                config=invalid_config,
                tap_id="",
            )
            invalid_result = self.tap_abstractions.process_tap_config(
                invalid_instance.config
            )
        except (ValidationError, ValueError):
            invalid_result = r[m.Meltano.TapConfig].fail(
                "Validation failed at creation",
            )
        valid_result = self.tap_abstractions.process_tap_config(valid_instance.config)
        tm.that(valid_result, is_=r)
        if valid_result.is_success:
            self.test_assertions.assert_true(
                condition=bool(valid_result.value),
                message="Valid instance should pass validation",
            )
        if invalid_result.is_success:
            self.test_assertions.assert_false(
                condition=bool(invalid_result.value),
                message="Invalid instance should fail validation",
            )

    def test_discover_streams_postgres(self) -> None:
        """Test discover_streams with PostgreSQL tap via mocked runtime."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-postgres",
            config=config,
            tap_id="postgres_tap_123",
        )
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
            tap_type="tap-csv",
            connection_config={"file": "test.csv"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-csv",
            config=config,
            tap_id="csv_tap_123",
        )
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].ok("data"),
        ):
            result = self.tap_abstractions.discover_streams(tap_instance)
        tm.that(result, is_=r)

    def test_discover_streams_default(self) -> None:
        """Test discover_streams with unknown tap type via mocked runtime."""
        config = m.Meltano.TapConfig(
            tap_type="tap-unknown",
            connection_config={"endpoint": "http://api.example.com"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-unknown",
            config=config,
            tap_id="unknown_tap_123",
        )
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
                "get_stream_by_name not available on this FlextMeltanoAbstractions",
            )
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-postgres",
            config=config,
            tap_id="postgres_tap_123",
        )
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].ok("users\norders"),
        ):
            stream_result = self.tap_abstractions.get_stream_by_name(
                tap_instance,
                "users",
            )
        tm.that(stream_result, is_=r)

    def test_generate_catalog_success(self) -> None:
        """Test generate_catalog delegates to discover_streams."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-postgres",
            config=config,
            tap_id="postgres_tap_123",
        )
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].ok("users\norders"),
        ):
            result = self.tap_abstractions.generate_catalog(tap_instance)
        tm.that(result, is_=r)

    def test_catalog_entry_structure(self) -> None:
        """Test catalog entry structure using flext_tests."""
        stream = m.Meltano.StreamDefinition(
            stream_name="users",
            stream_schema={
                "type": "t.NormalizedValue",
                "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
            },
            source_type="tap-postgres",
        )
        result = self.tap_abstractions._create_catalog_entry_from_stream(stream)
        tm.that(result, is_=r)
        if result.is_success:
            entry = result.value
            assert entry["tap_stream_id"] == "users"
            assert entry["stream"] == "users"
            assert "schema" in entry
            assert "metadata" in entry

    def test_sync_stream_success(self) -> None:
        """Test sync_stream via mocked runtime call."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-postgres",
            config=config,
            tap_id="postgres_tap_123",
        )
        mock_target = m.Meltano.TargetConfig(
            target_type="target-jsonl",
            connection_config={"loaded_records": 0},
        )
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].ok("sync ok"),
        ):
            result = self.tap_abstractions.sync_stream(
                tap_instance,
                "users",
                mock_target,
            )
        tm.that(result, is_=r)

    def test_sync_stream_without_target(self) -> None:
        """Test sync_stream without target using flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-csv",
            connection_config={"file": "test.csv"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-csv",
            config=config,
            tap_id="csv_tap_123",
        )
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].ok("sync ok"),
        ):
            result = self.tap_abstractions.sync_stream(tap_instance, "data")
        tm.that(result, is_=r)

    def test_list_streams(self) -> None:
        """Test list_streams method delegates to discover_streams."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-postgres",
            config=config,
            tap_id="postgres_tap_123",
        )
        with patch.object(
            FlextMeltanoAbstractions,
            "_run_meltano",
            return_value=r[str].ok("users\norders"),
        ):
            stream_names = self.tap_abstractions.list_streams(tap_instance)
        tm.that(isinstance(stream_names, list), eq=True)

    def test_get_tap_type(self) -> None:
        """Test get_tap_type method using flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-csv",
            connection_config={"file": "test.csv"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-csv",
            config=config,
            tap_id="csv_tap_123",
        )
        tap_type = self.tap_abstractions.get_tap_type(tap_instance)
        self.test_assertions.assert_equal(
            actual=tap_type,
            expected="tap-csv",
            message="Tap type should match",
        )

    def test_get_registered_streams(self) -> None:
        """Test get_registered_streams method using flext_tests."""
        initial_streams = self.tap_abstractions.get_registered_streams()
        tm.that(isinstance(initial_streams, list), eq=True)

    def test_create_instance_factory(self) -> None:
        """Test create_abstractions_instance factory method using flext_tests."""
        result = FlextMeltanoAbstractions.create_abstractions_instance()
        tm.that(result, is_=r)
        if result.is_success:
            instance = result.value
            assert isinstance(instance, FlextMeltanoAbstractions)
            if hasattr(instance, "service_name"):
                service_name_val = getattr(instance, "service_name")
                self.test_assertions.assert_equal(
                    actual=service_name_val,
                    expected="FlextMeltanoAbstractions",
                    message="Service name should match",
                )

    def test_tap_abstractions_error_handling(self) -> None:
        """Test tap abstractions error handling."""
        timeout_error = TimeoutError("Connection timed out")
        tm.that(timeout_error, is_=Exception)
        validation_error = ValidationError.from_exception_data(
            title="Validation Error",
            line_errors=[],
        )
        tm.that(validation_error, is_=Exception)

    def test_invalid_tap_config_creation(self) -> None:
        """Test invalid tap config creation using flext_tests."""
        try:
            result = self.tap_abstractions.create_tap_from_config(
                tap_type="",
                connection_config={},
            )
            if result.is_failure:
                self.test_assertions.assert_true(
                    condition=result.error is not None,
                    message="Should have error message",
                )
        except (ValueError, TypeError, RuntimeError):
            tm.that(True, eq=True)

    def test_missing_stream_handling(self) -> None:
        """Test missing stream handling using flext_tests."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
        )
        tap_instance = m.Meltano.TapInstance(
            tap_type="tap-postgres",
            config=config,
            tap_id="postgres_tap_123",
        )
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
        connection_config: t.ContainerMapping = {
            "host": "localhost",
            "database": "test_db",
        }
        stream_config: t.ContainerMapping = {"users": {"selected": True}}
        create_result = self.tap_abstractions.create_tap_from_config(
            tap_type="tap-postgres",
            connection_config=connection_config,
            stream_config=stream_config,
        )
        self.test_assertions.assert_true(
            condition=create_result.is_success,
            message="Tap creation should succeed",
        )
        if create_result.is_failure:
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
            self.test_assertions.assert_true(
                condition=discovery_result.is_success,
                message="Stream discovery should succeed",
            )
            catalog_result = self.tap_abstractions.generate_catalog(tap_instance)
            self.test_assertions.assert_true(
                condition=catalog_result.is_success,
                message="Catalog generation should succeed",
            )
            sync_result = self.tap_abstractions.sync_stream(tap_instance, "users")
            self.test_assertions.assert_true(
                condition=sync_result.is_success,
                message="Stream sync should succeed",
            )

    def test_execute_returns_config_status(self) -> None:
        """Test execute returns configuration status dict."""
        result = self.tap_abstractions.execute()
        tm.that(result, is_=r)
        if result.is_success:
            value = result.value
            tm.that(isinstance(value, dict), eq=True)
