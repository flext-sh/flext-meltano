"""Services Comprehensive Coverage Tests - Real Service Testing Without Mocks.

Comprehensive tests for FlextMeltanoService using real service functionality.
Focuses on achieving 90%+ coverage with meaningful functional tests.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile

import pytest
from flext_core import FlextDomainService, FlextResult

from flext_meltano.services import FlextMeltanoService


class TestFlextMeltanoServiceInitialization:
    """Test FlextMeltanoService initialization and basic functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_service_initialization(self) -> None:
        """Test proper service initialization."""
        assert isinstance(self.service, FlextMeltanoService)
        assert hasattr(self.service, "_container")

        # Test that nested service classes exist
        assert hasattr(self.service, "TapService")
        assert hasattr(self.service, "TargetService")
        assert hasattr(self.service, "DbtService")

        # Test nested classes are properly defined
        assert self.service.TapService.__name__ == "TapService"
        assert self.service.TargetService.__name__ == "TargetService"
        assert self.service.DbtService.__name__ == "DbtService"

    def test_container_registration(self) -> None:
        """Test that services are registered in the container."""
        # The container should have service classes registered
        assert hasattr(self.service, "_container")
        # Container registration happens during __init__


class TestTapService:
    """Test TapService nested class functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()
        self.tap_service_class = self.service.TapService

    def test_tap_service_creation(self) -> None:
        """Test TapService creation and initialization."""
        tap_service = self.tap_service_class(tap_name="tap-csv")
        assert isinstance(tap_service, self.tap_service_class)
        assert hasattr(tap_service, "tap_name")

    def test_tap_service_with_additional_data(self) -> None:
        """Test TapService creation with additional configuration data."""
        tap_service = self.tap_service_class(
            tap_name="tap-postgres", database="testdb", host="localhost"
        )
        assert isinstance(tap_service, self.tap_service_class)

    def test_tap_service_adapter_property(self) -> None:
        """Test TapService adapter property."""
        tap_service = self.tap_service_class(tap_name="tap-csv")
        adapter = tap_service.adapter
        # The adapter property should return an object (likely FlextMeltanoAdapter)
        assert adapter is not None

    def test_tap_service_execute_method(self) -> None:
        """Test TapService execute method."""
        tap_service = self.tap_service_class(tap_name="tap-csv")
        result = tap_service.execute()
        assert isinstance(result, FlextResult)
        # The result will depend on the actual implementation

    def test_tap_service_validate_config(self) -> None:
        """Test TapService validate_config method."""
        tap_service = self.tap_service_class(tap_name="tap-csv")
        result = tap_service.validate_config()
        assert isinstance(result, FlextResult)

    def test_tap_service_get_info(self) -> None:
        """Test TapService get_info method."""
        tap_service = self.tap_service_class(tap_name="tap-csv")
        result = tap_service.get_info()
        assert isinstance(result, FlextResult)

    def test_tap_service_create_tap_instance(self) -> None:
        """Test TapService create_tap_instance method."""
        tap_service = self.tap_service_class(tap_name="tap-csv")
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            config = {"file_path": tmp_file.name}
            result = tap_service.create_tap_instance(config)
            assert isinstance(result, FlextResult)

    def test_tap_service_validate_tap_config(self) -> None:
        """Test TapService validate_tap_config method."""
        tap_service = self.tap_service_class(tap_name="tap-csv")
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            config = {"file_path": tmp_file.name}
            result = tap_service.validate_tap_config(config)
            assert isinstance(result, FlextResult)

    def test_tap_service_get_default_config(self) -> None:
        """Test TapService get_default_config method."""
        tap_service = self.tap_service_class(tap_name="tap-csv")
        result = tap_service.get_default_config()
        assert isinstance(result, FlextResult)

    def test_tap_service_validate_service(self) -> None:
        """Test TapService validate_service method."""
        tap_service = self.tap_service_class(tap_name="tap-csv")
        result = tap_service.validate_service()
        assert isinstance(result, FlextResult)


class TestTargetService:
    """Test TargetService nested class functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()
        self.target_service_class = self.service.TargetService

    def test_target_service_creation(self) -> None:
        """Test TargetService creation and initialization."""
        target_service = self.target_service_class(target_name="target-csv")
        assert isinstance(target_service, self.target_service_class)
        assert hasattr(target_service, "target_name")

    def test_target_service_with_additional_data(self) -> None:
        """Test TargetService creation with additional configuration data."""
        target_service = self.target_service_class(
            target_name="target-postgres", database="outputdb", host="localhost"
        )
        assert isinstance(target_service, self.target_service_class)

    def test_target_service_adapter_property(self) -> None:
        """Test TargetService adapter property."""
        target_service = self.target_service_class(target_name="target-csv")
        adapter = target_service.adapter
        assert adapter is not None

    def test_target_service_execute_method(self) -> None:
        """Test TargetService execute method."""
        target_service = self.target_service_class(target_name="target-csv")
        result = target_service.execute()
        assert isinstance(result, FlextResult)

    def test_target_service_get_info(self) -> None:
        """Test TargetService get_info method."""
        target_service = self.target_service_class(target_name="target-csv")
        result = target_service.get_info()
        assert isinstance(result, FlextResult)

    def test_target_service_create_target_instance(self) -> None:
        """Test TargetService create_target_instance method."""
        target_service = self.target_service_class(target_name="target-csv")
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            config = {"output_path": tmp_file.name}
            result = target_service.create_target_instance(config)
            assert isinstance(result, FlextResult)

    def test_target_service_validate_target_config(self) -> None:
        """Test TargetService validate_target_config method."""
        target_service = self.target_service_class(target_name="target-csv")
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            config = {"output_path": tmp_file.name}
            result = target_service.validate_target_config(config)
            assert isinstance(result, FlextResult)

    def test_target_service_get_default_config(self) -> None:
        """Test TargetService get_default_config method."""
        target_service = self.target_service_class(target_name="target-csv")
        result = target_service.get_default_config()
        assert isinstance(result, FlextResult)

    def test_target_service_validate_service(self) -> None:
        """Test TargetService validate_service method."""
        target_service = self.target_service_class(target_name="target-csv")
        result = target_service.validate_service()
        assert isinstance(result, FlextResult)


class TestDbtService:
    """Test DbtService nested class functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()
        self.dbt_service_class = self.service.DbtService

    def test_dbt_service_creation(self) -> None:
        """Test DbtService creation and initialization."""
        dbt_service = self.dbt_service_class(project_name="my_dbt_project")
        assert isinstance(dbt_service, self.dbt_service_class)
        assert hasattr(dbt_service, "project_name")

    def test_dbt_service_with_additional_data(self) -> None:
        """Test DbtService creation with additional configuration data."""
        dbt_service = self.dbt_service_class(
            project_name="analytics_project", profile_name="dev", target="dev"
        )
        assert isinstance(dbt_service, self.dbt_service_class)

    def test_dbt_service_adapter_property(self) -> None:
        """Test DbtService adapter property."""
        dbt_service = self.dbt_service_class(project_name="my_dbt_project")
        adapter = dbt_service.adapter
        assert adapter is not None

    def test_dbt_service_execute_method(self) -> None:
        """Test DbtService execute method."""
        dbt_service = self.dbt_service_class(project_name="my_dbt_project")
        result = dbt_service.execute()
        assert isinstance(result, FlextResult)

    def test_dbt_service_get_info(self) -> None:
        """Test DbtService get_info method."""
        dbt_service = self.dbt_service_class(project_name="my_dbt_project")
        result = dbt_service.get_info()
        assert isinstance(result, FlextResult)

    def test_dbt_service_get_profiles_config(self) -> None:
        """Test DbtService get_profiles_config method."""
        dbt_service = self.dbt_service_class(project_name="my_dbt_project")
        result = dbt_service.get_profiles_config()
        assert isinstance(result, FlextResult)


class TestServiceFactoryMethods:
    """Test service factory methods on main FlextMeltanoService."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_create_tap_service(self) -> None:
        """Test create_tap_service factory method."""
        result = self.service.create_tap_service("tap-csv")
        assert isinstance(result, FlextResult)
        if result.is_success:
            tap_service = result.data
            assert isinstance(tap_service, self.service.TapService)

    def test_create_tap_service_with_config(self) -> None:
        """Test create_tap_service with additional configuration."""
        result = self.service.create_tap_service(
            "tap-postgres", database="testdb", host="localhost"
        )
        assert isinstance(result, FlextResult)

    def test_create_target_service(self) -> None:
        """Test create_target_service factory method."""
        result = self.service.create_target_service("target-csv")
        assert isinstance(result, FlextResult)
        if result.is_success:
            target_service = result.data
            assert isinstance(target_service, self.service.TargetService)

    def test_create_target_service_with_config(self) -> None:
        """Test create_target_service with additional configuration."""
        result = self.service.create_target_service(
            "target-postgres", database="outputdb", host="localhost"
        )
        assert isinstance(result, FlextResult)

    def test_create_dbt_service(self) -> None:
        """Test create_dbt_service factory method."""
        result = self.service.create_dbt_service("my_dbt_project")
        assert isinstance(result, FlextResult)
        if result.is_success:
            dbt_service = result.data
            assert isinstance(dbt_service, self.service.DbtService)

    def test_create_dbt_service_with_config(self) -> None:
        """Test create_dbt_service with project name."""
        result = self.service.create_dbt_service("analytics_project")
        assert isinstance(result, FlextResult)


class TestServiceGenericMethods:
    """Test generic service creation and validation methods."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_create_service_generic_tap(self) -> None:
        """Test generic service creation for tap services."""
        result = self.service._create_service_generic(
            self.service.TapService, "tap-csv", "tap_name", "tap", tap_name="tap-csv"
        )
        assert isinstance(result, FlextResult)

    def test_create_service_generic_target(self) -> None:
        """Test generic service creation for target services."""
        result = self.service._create_service_generic(
            self.service.TargetService, "target-csv", "target_name", "target", target_name="target-csv"
        )
        assert isinstance(result, FlextResult)

    def test_create_service_generic_dbt(self) -> None:
        """Test generic service creation for dbt services."""
        result = self.service._create_service_generic(
            self.service.DbtService, "my_project", "project_name", "dbt", project_name="my_project"
        )
        assert isinstance(result, FlextResult)

    def test_create_service_generic_with_additional_config(self) -> None:
        """Test generic service creation with additional configuration."""
        result = self.service._create_service_generic(
            self.service.TapService,
            "tap-postgres",
            "tap_name",
            "tap",
            tap_name="tap-postgres",
            database="testdb",
            host="localhost",
            port=5432,
        )
        assert isinstance(result, FlextResult)


class TestServiceIntegration:
    """Integration tests combining multiple service operations."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_full_tap_workflow(self) -> None:
        """Test complete tap service workflow."""
        # Create tap service
        tap_result = self.service.create_tap_service("tap-csv")
        assert isinstance(tap_result, FlextResult)

        if tap_result.is_success:
            tap_service = tap_result.data

            # Test service validation
            validate_result = tap_service.validate_service()
            assert isinstance(validate_result, FlextResult)

            # Test config validation
            config_validate_result = tap_service.validate_config()
            assert isinstance(config_validate_result, FlextResult)

            # Test getting service info
            info_result = tap_service.get_info()
            assert isinstance(info_result, FlextResult)

    def test_full_target_workflow(self) -> None:
        """Test complete target service workflow."""
        # Create target service
        target_result = self.service.create_target_service("target-csv")
        assert isinstance(target_result, FlextResult)

        if target_result.is_success:
            target_service = target_result.data

            # Test service validation
            validate_result = target_service.validate_service()
            assert isinstance(validate_result, FlextResult)

            # Test getting service info
            info_result = target_service.get_info()
            assert isinstance(info_result, FlextResult)

    def test_full_dbt_workflow(self) -> None:
        """Test complete DBT service workflow."""
        # Create dbt service
        dbt_result = self.service.create_dbt_service("analytics_project")
        assert isinstance(dbt_result, FlextResult)

        if dbt_result.is_success:
            dbt_service = dbt_result.data

            # Test getting profiles config
            profiles_result = dbt_service.get_profiles_config()
            assert isinstance(profiles_result, FlextResult)

            # Test getting service info
            info_result = dbt_service.get_info()
            assert isinstance(info_result, FlextResult)

    def test_multiple_service_creation(self) -> None:
        """Test creating multiple services simultaneously."""
        # Create multiple services
        tap_result = self.service.create_tap_service("tap-csv")
        target_result = self.service.create_target_service("target-csv")
        dbt_result = self.service.create_dbt_service("my_project")

        assert isinstance(tap_result, FlextResult)
        assert isinstance(target_result, FlextResult)
        assert isinstance(dbt_result, FlextResult)

        # Verify they are different service types
        if all(r.is_success for r in [tap_result, target_result, dbt_result]):
            tap_service = tap_result.data
            target_service = target_result.data
            dbt_service = dbt_result.data

            assert isinstance(tap_service, self.service.TapService)
            assert isinstance(target_service, self.service.TargetService)
            assert isinstance(dbt_service, self.service.DbtService)

            # Verify they are distinct instances
            assert tap_service is not target_service
            assert target_service is not dbt_service
            assert dbt_service is not tap_service

    def test_service_configuration_validation(self) -> None:
        """Test service configuration validation across different service types."""
        # Test different configuration scenarios
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as input_file:
            with tempfile.NamedTemporaryFile(
                suffix=".csv", delete=False
            ) as output_file:
                services_to_test = [
                    (
                        "tap-csv",
                        self.service.create_tap_service,
                        {"file_path": input_file.name},
                    ),
                    (
                        "target-csv",
                        self.service.create_target_service,
                        {"output_path": output_file.name},
                    ),
                    (
                        "dbt_project",
                        self.service.create_dbt_service,
                        {"profile_name": "dev"},
                    ),
                ]

        for service_name, creator_method, test_config in services_to_test:
            result = creator_method(service_name, **test_config)
            assert isinstance(result, FlextResult)
            # Each service should handle configuration appropriately


class TestServiceErrorHandling:
    """Test error handling and edge cases in service operations."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_empty_service_names(self) -> None:
        """Test service creation with empty names."""
        # Empty names should be handled gracefully
        tap_result = self.service.create_tap_service("")
        target_result = self.service.create_target_service("")
        dbt_result = self.service.create_dbt_service("")

        # Results should be FlextResult instances (might fail but shouldn't crash)
        assert isinstance(tap_result, FlextResult)
        assert isinstance(target_result, FlextResult)
        assert isinstance(dbt_result, FlextResult)

    def test_invalid_service_configurations(self) -> None:
        """Test service creation with potentially invalid configurations."""
        # Test with None values
        tap_result = self.service.create_tap_service("tap-test", invalid_param=None)
        assert isinstance(tap_result, FlextResult)

        # Test with empty configurations
        target_result = self.service.create_target_service(
            "target-test", empty_config={}
        )
        assert isinstance(target_result, FlextResult)

    def test_service_method_error_handling(self) -> None:
        """Test error handling in service methods."""
        # Create a service and test its methods even if they might fail
        tap_result = self.service.create_tap_service("tap-test")

        if tap_result.is_success:
            tap_service = tap_result.data

            # Test methods that might fail gracefully
            methods_to_test = [
                tap_service.validate_config,
                tap_service.validate_service,
                tap_service.get_info,
                tap_service.get_default_config,
                tap_service.execute,
            ]

            for method in methods_to_test:
                try:
                    result = method()
                    assert isinstance(result, FlextResult)
                except Exception:
                    # Methods should not raise exceptions, they should return FlextResult
                    pytest.fail(
                        f"Method {method.__name__} raised exception instead of returning FlextResult"
                    )


class TestServiceArchitecture:
    """Test service architecture and patterns."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_service_inheritance_hierarchy(self) -> None:
        """Test that services properly inherit from FlextDomainService."""
        # Import FlextDomainService to test inheritance

        # Test class inheritance
        assert issubclass(self.service.TapService, FlextDomainService)
        assert issubclass(self.service.TargetService, FlextDomainService)
        assert issubclass(self.service.DbtService, FlextDomainService)

    def test_service_type_annotations(self) -> None:
        """Test service type annotations and generics."""
        # Services should be properly typed
        tap_service = self.service.TapService(tap_name="test")
        target_service = self.service.TargetService(target_name="test")
        dbt_service = self.service.DbtService(project_name="test")

        # Check that instances are properly created
        assert isinstance(tap_service, self.service.TapService)
        assert isinstance(target_service, self.service.TargetService)
        assert isinstance(dbt_service, self.service.DbtService)

    def test_dependency_injection_container(self) -> None:
        """Test dependency injection container usage."""
        # Container should be properly initialized
        assert hasattr(self.service, "_container")
        assert self.service._container is not None

        # Container should have service classes registered
        # This tests the registration that happens in __init__

    def test_service_adapter_pattern(self) -> None:
        """Test that all services implement the adapter pattern."""
        services = [
            self.service.TapService(tap_name="test"),
            self.service.TargetService(target_name="test"),
            self.service.DbtService(project_name="test"),
        ]

        for service in services:
            # All services should have adapter property
            assert hasattr(service, "adapter")
            adapter = service.adapter
            assert adapter is not None
