"""Test module for flext-meltano."""

from __future__ import annotations

import tempfile

import pytest

from flext_meltano import FlextMeltanoService, r, s


class TestFlextMeltanoServiceInitialization:
    """Test FlextMeltanoService initialization and basic functionality."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_service_initialization(self) -> None:
        """Test proper service initialization."""
        assert isinstance(self.service, FlextMeltanoService)
        assert self.service.service_name == "flext_meltano_service"
        assert self.service.version == "0.9.9"
        assert hasattr(self.service, "create_tap_service")
        assert hasattr(self.service, "create_target_service")
        assert hasattr(self.service, "create_dbt_service")
        assert callable(FlextMeltanoService)

    def test_container_registration(self) -> None:
        """Test that services are registered in the container."""
        assert hasattr(self.service, "_container")


class TestTapService:
    """Test TapService functionality using unified architecture."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()
        self.create_tap_service = self.service.create_tap_service

    def test_tap_service_creation(self) -> None:
        """Test TapService creation and initialization."""
        service_result = self.create_tap_service("tap-csv")
        assert service_result.is_success
        tap_service = service_result.value
        assert isinstance(tap_service, FlextMeltanoService)
        assert hasattr(tap_service, "source_name")

    def test_tap_service_with_additional_data(self) -> None:
        """Test TapService creation with additional configuration data."""
        service_result = self.create_tap_service(
            "tap-postgres", database="testdb", host="localhost"
        )
        assert service_result.is_success
        tap_service = service_result.value
        assert isinstance(tap_service, FlextMeltanoService)

    def test_tap_service_adapter_property(self) -> None:
        """Test TapService has container for dependency injection."""
        service_result = self.create_tap_service("tap-csv")
        assert service_result.is_success
        tap_service = service_result.value
        assert hasattr(tap_service, "_container")
        assert tap_service._container is not None

    def test_tap_service_execute_method(self) -> None:
        """Test TapService execute method."""
        service_result = self.create_tap_service("tap-csv")
        assert service_result.is_success
        tap_service = service_result.value
        result = tap_service.execute()
        assert isinstance(result, r)

    def test_tap_service_validate_config(self) -> None:
        """Test TapService validate_config method."""
        service_result = self.create_tap_service("tap-csv")
        assert service_result.is_success
        tap_service = service_result.value
        result = tap_service.validate_config()
        assert isinstance(result, r)

    def test_tap_service_get_info(self) -> None:
        """Test TapService get_info method."""
        service_result = self.create_tap_service("tap-csv")
        assert service_result.is_success
        tap_service = service_result.value
        result = tap_service.get_info()
        assert isinstance(result, r)

    def test_tap_service_create_tap_instance(self) -> None:
        """Test TapService create_tap_instance method."""
        service_result = self.create_tap_service("tap-csv")
        assert service_result.is_success
        tap_service = service_result.value
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            config: dict[str, object] = {"file_path": tmp_file.name}
            try:
                result = tap_service.create_instance(config)
            except TypeError:
                pytest.skip(
                    "create_instance(config) not available (use PYTHONPATH=src)"
                )
            assert isinstance(result, r)

    def test_tap_service_validate_tap_config(self) -> None:
        """Test TapService validate_tap_config method."""
        service_result = self.create_tap_service("tap-csv")
        assert service_result.is_success
        tap_service = service_result.value
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            config: dict[str, object] = {"file_path": tmp_file.name}
            result = tap_service.validate_service_config(config)
            assert isinstance(result, r)

    def test_tap_service_get_default_config(self) -> None:
        """Test TapService get_default_config method."""
        service_result = self.create_tap_service("tap-csv")
        assert service_result.is_success
        tap_service = service_result.value
        result = tap_service.get_default_config()
        assert isinstance(result, r)

    def test_tap_service_validate_service(self) -> None:
        """Test TapService validate_service method."""
        service_result = self.create_tap_service("tap-csv")
        assert service_result.is_success
        tap_service = service_result.value
        result = tap_service.validate_service()
        assert isinstance(result, r)


class TestTargetService:
    """Test TargetService functionality using unified architecture."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()
        self.create_target_service = self.service.create_target_service

    def test_target_service_creation(self) -> None:
        """Test TargetService creation and initialization."""
        service_result = self.create_target_service("target-csv")
        assert service_result.is_success
        target_service = service_result.value
        assert isinstance(target_service, FlextMeltanoService)
        assert hasattr(target_service, "sink_name")

    def test_target_service_with_additional_data(self) -> None:
        """Test TargetService creation with additional configuration data."""
        service_result = self.create_target_service(
            "target-postgres", database="outputdb", host="localhost"
        )
        assert service_result.is_success
        target_service = service_result.value
        assert isinstance(target_service, FlextMeltanoService)

    def test_target_service_has_container(self) -> None:
        """Test TargetService has container for dependency injection."""
        service_result = self.create_target_service("target-csv")
        assert service_result.is_success
        target_service = service_result.value
        assert hasattr(target_service, "_container")
        assert target_service._container is not None

    def test_target_service_execute_method(self) -> None:
        """Test TargetService execute method."""
        service_result = self.create_target_service("target-csv")
        assert service_result.is_success
        target_service = service_result.value
        result = target_service.execute()
        assert isinstance(result, r)

    def test_target_service_get_info(self) -> None:
        """Test TargetService get_info method."""
        service_result = self.create_target_service("target-csv")
        assert service_result.is_success
        target_service = service_result.value
        result = target_service.get_info()
        assert isinstance(result, r)

    def test_target_service_create_target_instance(self) -> None:
        """Test TargetService create_target_instance method."""
        service_result = self.create_target_service("target-csv")
        assert service_result.is_success
        target_service = service_result.value
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            config: dict[str, object] = {"output_path": tmp_file.name}
            try:
                result = target_service.create_instance(config)
            except TypeError:
                pytest.skip(
                    "create_instance(config) not available (use PYTHONPATH=src)"
                )
            assert isinstance(result, r)

    def test_target_service_validate_target_config(self) -> None:
        """Test TargetService validate_target_config method."""
        service_result = self.create_target_service("target-csv")
        assert service_result.is_success
        target_service = service_result.value
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as tmp_file:
            config: dict[str, object] = {"output_path": tmp_file.name}
            result = target_service.validate_service_config(config)
            assert isinstance(result, r)

    def test_target_service_get_default_config(self) -> None:
        """Test TargetService get_default_config method."""
        service_result = self.create_target_service("target-csv")
        assert service_result.is_success
        target_service = service_result.value
        result = target_service.get_default_config()
        assert isinstance(result, r)

    def test_target_service_validate_service(self) -> None:
        """Test TargetService validate_service method."""
        service_result = self.create_target_service("target-csv")
        assert service_result.is_success
        target_service = service_result.value
        result = target_service.validate_service()
        assert isinstance(result, r)


class TestDbtService:
    """Test DbtService functionality using unified architecture."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()
        self.create_dbt_service = self.service.create_dbt_service

    def test_dbt_service_creation(self) -> None:
        """Test DbtService creation and initialization."""
        service_result = self.create_dbt_service("my_dbt_project")
        assert service_result.is_success
        dbt_service = service_result.value
        assert isinstance(dbt_service, FlextMeltanoService)
        assert hasattr(dbt_service, "transformation_name")

    def test_dbt_service_with_additional_data(self) -> None:
        """Test DbtService creation with additional configuration data."""
        service_result = self.create_dbt_service(
            "analytics_project", profile_name="dev", target="dev"
        )
        assert service_result.is_success
        dbt_service = service_result.value
        assert isinstance(dbt_service, FlextMeltanoService)

    def test_dbt_service_has_container(self) -> None:
        """Test DbtService has container for dependency injection."""
        service_result = self.create_dbt_service("my_dbt_project")
        assert service_result.is_success
        dbt_service = service_result.value
        assert hasattr(dbt_service, "_container")
        assert dbt_service._container is not None

    def test_dbt_service_execute_method(self) -> None:
        """Test DbtService execute method."""
        service_result = self.create_dbt_service("my_dbt_project")
        assert service_result.is_success
        dbt_service = service_result.value
        result = dbt_service.execute()
        assert isinstance(result, r)

    def test_dbt_service_get_info(self) -> None:
        """Test DbtService get_info method."""
        service_result = self.create_dbt_service("my_dbt_project")
        assert service_result.is_success
        dbt_service = service_result.value
        result = dbt_service.get_info()
        assert isinstance(result, r)

    def test_dbt_service_get_profiles_config(self) -> None:
        """Test DbtService get_profiles_config method."""
        service_result = self.create_dbt_service("my_dbt_project")
        assert service_result.is_success
        dbt_service = service_result.value
        result = dbt_service.get_profiles_config()
        assert isinstance(result, r)


class TestServiceFactoryMethods:
    """Test service factory methods on main FlextMeltanoService."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_create_tap_service(self) -> None:
        """Test create_tap_service factory method."""
        result = self.service.create_tap_service("tap-csv")
        assert isinstance(result, r)
        if result.is_success:
            tap_service = result.value
            assert isinstance(tap_service, FlextMeltanoService)

    def test_create_tap_service_with_config(self) -> None:
        """Test create_tap_service with additional configuration."""
        result = self.service.create_tap_service(
            "tap-postgres", database="testdb", host="localhost"
        )
        assert isinstance(result, r)

    def test_create_target_service(self) -> None:
        """Test create_target_service factory method."""
        result = self.service.create_target_service("target-csv")
        assert isinstance(result, r)
        if result.is_success:
            target_service = result.value
            assert isinstance(target_service, FlextMeltanoService)

    def test_create_target_service_with_config(self) -> None:
        """Test create_target_service with additional configuration."""
        result = self.service.create_target_service(
            "target-postgres", database="outputdb", host="localhost"
        )
        assert isinstance(result, r)

    def test_create_dbt_service(self) -> None:
        """Test create_dbt_service factory method."""
        result = self.service.create_dbt_service("my_dbt_project")
        assert isinstance(result, r)
        if result.is_success:
            dbt_service = result.value
            assert isinstance(dbt_service, FlextMeltanoService)

    def test_create_dbt_service_with_config(self) -> None:
        """Test create_dbt_service with project name."""
        result = self.service.create_dbt_service("analytics_project")
        assert isinstance(result, r)


class TestServiceGenericMethods:
    """Test generic service creation and validation methods."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_create_service_generic_tap(self) -> None:
        """Test generic service creation for tap services."""
        tap_service = FlextMeltanoService(service_name="test-tap-service")
        assert tap_service is not None
        assert tap_service.service_name == "test-tap-service"

    def test_create_service_generic_target(self) -> None:
        """Test generic service creation for target services."""
        target_service = FlextMeltanoService(service_name="test-target-service")
        assert target_service is not None
        assert target_service.service_name == "test-target-service"

    def test_create_service_generic_dbt(self) -> None:
        """Test generic service creation for dbt services."""
        dbt_service = FlextMeltanoService(service_name="test-dbt-service")
        assert dbt_service is not None
        assert dbt_service.service_name == "test-dbt-service"

    def test_create_service_generic_with_additional_config(self) -> None:
        """Test generic service creation with additional configuration."""
        service = FlextMeltanoService(
            service_name="test-config-service", source_name="tap-postgres"
        )
        assert service is not None
        assert service.service_name == "test-config-service"
        assert service.source_name == "tap-postgres"


class TestServiceIntegration:
    """Integration tests combining multiple service operations."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_full_tap_workflow(self) -> None:
        """Test complete tap service workflow."""
        tap_result = self.service.create_tap_service("tap-csv")
        assert isinstance(tap_result, r)
        if tap_result.is_success:
            tap_service = tap_result.value
            assert tap_service is not None
            validate_result = tap_service.validate_service()
            assert isinstance(validate_result, r)
            config_validate_result = tap_service.validate_config()
            assert isinstance(config_validate_result, r)
            info_result = tap_service.get_info()
            assert isinstance(info_result, r)

    def test_full_target_workflow(self) -> None:
        """Test complete target service workflow."""
        target_result = self.service.create_target_service("target-csv")
        assert isinstance(target_result, r)
        if target_result.is_success:
            target_service = target_result.value
            assert target_service is not None
            validate_result = target_service.validate_service()
            assert isinstance(validate_result, r)
            info_result = target_service.get_info()
            assert isinstance(info_result, r)

    def test_full_dbt_workflow(self) -> None:
        """Test complete DBT service workflow."""
        dbt_result = self.service.create_dbt_service("analytics_project")
        assert isinstance(dbt_result, r)
        if dbt_result.is_success:
            dbt_service = dbt_result.value
            assert dbt_service is not None
            profiles_result = dbt_service.get_profiles_config()
            assert isinstance(profiles_result, r)
            info_result = dbt_service.get_info()
            assert isinstance(info_result, r)

    def test_multiple_service_creation(self) -> None:
        """Test creating multiple services simultaneously."""
        tap_result = self.service.create_tap_service("tap-csv")
        target_result = self.service.create_target_service("target-csv")
        dbt_result = self.service.create_dbt_service("my_project")
        assert isinstance(tap_result, r)
        assert isinstance(target_result, r)
        assert isinstance(dbt_result, r)
        if all(r.is_success for r in [tap_result, target_result, dbt_result]):
            tap_service = tap_result.value
            target_service = target_result.value
            dbt_service = dbt_result.value
            assert tap_service is not None
            assert target_service is not None
            assert dbt_service is not None
            assert tap_service is not target_service
            assert target_service is not dbt_service
            assert dbt_service is not tap_service

    def test_service_configuration_validation(self) -> None:
        """Test service configuration validation across different service types."""
        with (
            tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as input_file,
            tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as output_file,
        ):
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
            assert isinstance(result, r)


class TestServiceErrorHandling:
    """Test error handling and edge cases in service operations."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_empty_service_names(self) -> None:
        """Test service creation with empty names."""
        tap_result = self.service.create_tap_service("")
        target_result = self.service.create_target_service("")
        dbt_result = self.service.create_dbt_service("")
        assert isinstance(tap_result, r)
        assert isinstance(target_result, r)
        assert isinstance(dbt_result, r)

    def test_invalid_service_configurations(self) -> None:
        """Test service creation with potentially invalid configurations."""
        tap_result = self.service.create_tap_service("tap-test", invalid_param=None)
        assert isinstance(tap_result, r)
        target_result = self.service.create_target_service(
            "target-test", empty_config={}
        )
        assert isinstance(target_result, r)

    def test_service_method_error_handling(self) -> None:
        """Test error handling in service methods."""
        tap_result = self.service.create_tap_service("tap-test")
        if tap_result.is_success:
            tap_service = tap_result.value
            assert tap_service is not None
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
                    assert isinstance(result, r)
                except Exception:
                    pytest.fail(
                        f"Method {method.__name__} raised exception instead of returning r"
                    )


class TestServiceArchitecture:
    """Test service architecture and patterns."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextMeltanoService()

    def test_service_inheritance_hierarchy(self) -> None:
        """Test that unified service properly inherits from s."""
        assert issubclass(FlextMeltanoService, s)
        tap_service = FlextMeltanoService(service_type="tap", tap_name="test")
        target_service = FlextMeltanoService(service_type="target", target_name="test")
        dbt_service = FlextMeltanoService(service_type="dbt", project_name="test")
        assert isinstance(tap_service, s)
        assert isinstance(target_service, s)
        assert isinstance(dbt_service, s)

    def test_service_type_annotations(self) -> None:
        """Test service type annotations and generics."""
        tap_service = FlextMeltanoService(service_type="tap", tap_name="test")
        target_service = FlextMeltanoService(service_type="target", target_name="test")
        dbt_service = FlextMeltanoService(service_type="dbt", project_name="test")
        assert isinstance(tap_service, FlextMeltanoService)
        assert isinstance(target_service, FlextMeltanoService)
        assert isinstance(dbt_service, FlextMeltanoService)
        assert tap_service._service_type == "tap"
        assert target_service._service_type == "target"
        assert dbt_service._service_type == "dbt"

    def test_dependency_injection_container(self) -> None:
        """Test dependency injection container usage."""
        assert hasattr(self.service, "_container")
        assert self.service._container is not None

    def test_unified_service_container_pattern(self) -> None:
        """Test that unified services implement the container pattern."""
        services = [
            FlextMeltanoService(service_type="tap", tap_name="test"),
            FlextMeltanoService(service_type="target", target_name="test"),
            FlextMeltanoService(service_type="dbt", project_name="test"),
        ]
        for service in services:
            assert hasattr(service, "_container")
            container = service._container
            assert container is not None
            assert hasattr(container, "register")
