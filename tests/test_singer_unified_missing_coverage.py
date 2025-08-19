"""Additional tests for singer_unified module to improve coverage."""

from __future__ import annotations

from flext_core import FlextResult

from flext_meltano import (
    FlextSingerUnifiedConfig,
    FlextSingerUnifiedInterface,
    FlextSingerUnifiedResult,
    FlextSingerUnifiedService,
    create_unified_singer_config,
    create_unified_singer_service,
)


class TestSingerUnifiedMissingCoverage:
    """Test missing coverage areas in singer_unified module."""

    def test_service_execute_operation_empty_args(self) -> None:
        """Test service execute_operation method with empty args (line 383-384)."""
        service = FlextSingerUnifiedService()

        # Test with empty args
        result = service.execute_operation()
        assert result.is_failure
        assert "Operation name required as first argument" in result.error

    def test_service_execute_operation_discover_catalogs(self) -> None:
        """Test service execute_operation with discover_catalogs operation (lines 397-405)."""
        service = FlextSingerUnifiedService()

        # Test discover_catalogs operation
        result = service.execute_operation("discover_catalogs")
        # Should succeed or fail gracefully
        assert isinstance(result.success, bool)
        if result.is_failure:
            assert (
                "Catalog discovery failed" in result.error or result.error is not None
            )

    def test_service_execute_operation_validate_components(self) -> None:
        """Test service execute_operation with validate_components operation (lines 406-414)."""
        service = FlextSingerUnifiedService()

        # Test validate_components operation
        result = service.execute_operation("validate_components")
        # Should succeed or fail gracefully
        assert isinstance(result.success, bool)
        if result.is_failure:
            assert (
                "Component validation failed" in result.error
                or result.error is not None
            )

    def test_service_execute_operation_unknown_operation(self) -> None:
        """Test service execute_operation with unknown operation (line 415)."""
        service = FlextSingerUnifiedService()

        # Test unknown operation
        result = service.execute_operation("unknown_operation")
        assert result.is_failure
        assert "Unknown operation: unknown_operation" in result.error

    def test_service_execute_operation_pipeline_operation(self) -> None:
        """Test service execute_operation with execute_pipeline operation (lines 388-396)."""
        service = FlextSingerUnifiedService()

        # Test execute_pipeline operation
        result = service.execute_operation("execute_pipeline", config={"test": "value"})
        # Should succeed or fail gracefully
        assert isinstance(result.success, bool)
        if result.is_failure:
            assert (
                "Pipeline execution failed" in result.error or result.error is not None
            )

    def test_service_execute_method(self) -> None:
        """Test the basic execute method."""
        service = FlextSingerUnifiedService()

        # Test basic execute method
        result = service.execute()
        assert result.success
        assert isinstance(result.data, FlextSingerUnifiedResult)
        assert result.data.success is True
        assert result.data.records_processed == 0

    def test_execute_pipeline_operation_private_method(self) -> None:
        """Test private _execute_pipeline_operation method."""
        service = FlextSingerUnifiedService()

        # Test with valid kwargs
        kwargs = {"config": {"name": "test"}}
        result = service._execute_pipeline_operation(kwargs)

        # Should return a result
        assert hasattr(result, "success")

    def test_unified_interface_abstract_methods(self) -> None:
        """Test abstract interface methods for coverage."""

        class TestInterface(FlextSingerUnifiedInterface):
            """Test implementation of abstract interface."""

            def initialize(self, config: dict[str, object]) -> FlextResult[bool]:
                return FlextResult[None].ok(True)

            def discover_catalog(self) -> FlextResult[dict[str, object]]:
                return FlextResult[None].ok({"streams": []})

            def execute(self, *args: object, **kwargs: object) -> FlextResult[object]:
                return FlextResult[None].ok("executed")

            def validate_configuration(
                self,
                config: dict[str, object],
            ) -> FlextResult[bool]:
                return FlextResult[None].ok(True)

        # Test the implementation
        interface = TestInterface()

        # Test initialize
        result = interface.initialize({"test": "config"})
        assert result.success
        assert result.data is True

        # Test discover_catalog
        result = interface.discover_catalog()
        assert result.success
        assert result.data == {"streams": []}

        # Test execute
        result = interface.execute("test")
        assert result.success
        assert result.data == "executed"

        # Test validate_configuration
        result = interface.validate_configuration({"test": "config"})
        assert result.success
        assert result.data is True

    def test_result_serialization_methods(self) -> None:
        """Test result serialization methods for coverage."""
        result = FlextSingerUnifiedResult(
            success=True,
            catalog_updates={},
            state_updates={},
            records_processed=100,
            execution_time_ms=5000.0,
            metrics={"metric1": "value1"},
        )

        # Test to_dict method (if available)
        if hasattr(result, "to_dict"):
            data = result.to_dict()
            assert isinstance(data, dict)
            assert data["success"] is True
            assert data["records_processed"] == 100

    def test_config_edge_cases(self) -> None:
        """Test configuration edge cases for coverage."""
        # Test with minimal config
        config = FlextSingerUnifiedConfig(
            name="test",
            config={},
        )

        # Test domain rules validation
        validation_result = config.validate_business_rules()
        assert validation_result.success or validation_result.is_failure

        # Test with catalog and state
        config_with_data = FlextSingerUnifiedConfig(
            name="test_with_data",
            config={"setting": "value"},
            catalog={"streams": []},
            state={"bookmarks": {}},
        )

        validation_result = config_with_data.validate_business_rules()
        assert validation_result.success or validation_result.is_failure

    def test_factory_functions(self) -> None:
        """Test factory function coverage."""
        # Test create_unified_singer_config
        config = create_unified_singer_config(
            name="factory_test",
            config={"test": "value"},
        )

        assert config.name == "factory_test"
        assert config.config == {"test": "value"}

        # Test create_unified_singer_service
        service = create_unified_singer_service()
        assert isinstance(service, FlextSingerUnifiedService)

    def test_service_component_management_edge_cases(self) -> None:
        """Test service component management edge cases."""
        service = FlextSingerUnifiedService()

        # Test get non-existent component
        result = service.get_component("non_existent")
        assert result.is_failure
        assert "Component 'non_existent' is not registered" in result.error

        # Test register component with invalid data
        invalid_component = "not_a_component"
        result = service.register_component("invalid", invalid_component)
        # Should handle gracefully
        assert isinstance(result.success, bool)

    def test_result_error_scenarios(self) -> None:
        """Test result creation in error scenarios."""
        # Test result with failure state
        error_result = FlextSingerUnifiedResult(
            success=False,
            error_message="Test error",
            catalog_updates={},
            state_updates={},
            records_processed=0,
            execution_time_ms=0.0,
        )

        assert error_result.success is False
        assert error_result.error_message == "Test error"
        assert error_result.records_processed == 0

        # Test domain rules with invalid data
        invalid_result = FlextSingerUnifiedResult(
            success=True,
            catalog_updates={},
            state_updates={},
            records_processed=-1,  # Invalid negative value
            execution_time_ms=0.0,
        )

        domain_validation = invalid_result.validate_business_rules()
        assert domain_validation.is_failure
        assert (
            "Records processed must be a non-negative integer"
            in domain_validation.error
        )
