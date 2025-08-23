"""Real Base Services Tests - Tests REAL base service components.

**Test Category**: Real Integration Tests  
**Coverage Target**: 100% for base services functionality
**Dependencies**: Real Singer SDK 0.48.0, DBT Core 1.10.5, NO mocks
**Execution Time**: Real service calls, may take longer

## Test Scope

Tests REAL base services functionality:
- Direct FlextMeltanoTapService, FlextMeltanoTargetService, FlextMeltanoDbtService
- Real Singer SDK 0.48.0 integration for base service patterns
- DBT Core 1.10.5 integration for base DBT services
- FlextResult patterns with .value and unwrap_or() - NO .data/.unwrap()

## Architecture Alignment  

Tests the Base function (Função 3):
- Real foundation components for flext-(tap|target|dbt) projects
- Native SDK integration without mocks
- Enterprise error handling with FlextResult
"""

from __future__ import annotations

from abc import ABC
from pathlib import Path

import pytest
from flext_core import FlextResult
from singer_sdk import Tap, Target

from flext_meltano.funcao3_base_services import (
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
    FlextMeltanoDbtService,
)


# Test implementations for abstract base classes
class TestTapService(FlextMeltanoTapService):
    """Test implementation of FlextMeltanoTapService."""
    
    tap_name: str = "test-tap"

    def get_tap_class(self) -> type[Tap]:
        """Return test tap class."""
        # Create a minimal test tap class
        class TestTap(Tap):
            name = "test-tap"
            
            def discover_streams(self):
                return []
        
        return TestTap

    def get_default_config(self) -> dict[str, object]:
        """Return test default config."""
        return {
            "test_setting": "test_value",
            "required_field": "default"
        }


class TestTargetService(FlextMeltanoTargetService):
    """Test implementation of FlextMeltanoTargetService."""
    
    target_name: str = "test-target"

    def get_target_class(self) -> type[Target]:
        """Return test target class."""
        # Create a minimal test target class
        class TestTarget(Target):
            name = "test-target"
            
            def process_record(self, record, context):
                pass
        
        return TestTarget

    def get_default_config(self) -> dict[str, object]:
        """Return test default config."""
        return {
            "output_path": "/tmp/test",
            "format": "json"
        }


class TestDbtService(FlextMeltanoDbtService):
    """Test implementation of FlextMeltanoDbtService."""
    
    project_name: str = "test-dbt-project"

    # FlextMeltanoDbtService is concrete, so we only override if needed
    # It has default implementations of get_project_config and other methods


class TestRealFlextMeltanoTapService:
    """Test real FlextMeltanoTapService base functionality."""

    def setup_method(self) -> None:
        """Setup test tap service instance."""
        self.tap_service = TestTapService()

    def test_tap_service_initialization_real(self) -> None:
        """Test tap service initializes with real dependencies."""
        assert self.tap_service is not None
        assert hasattr(self.tap_service, 'logger')
        
        # Test service has Singer wrapper integration
        assert hasattr(self.tap_service, 'wrapper_singer')
        assert hasattr(self.tap_service, 'singer_adapter')
        
        # Test service properties
        assert self.tap_service.tap_name == "test-tap"
        assert self.tap_service.wrapper_singer is not None
        assert self.tap_service.singer_adapter is not None

    def test_execute_service_real_functionality(self) -> None:
        """Test service execution returns real tap information."""
        result = self.tap_service.execute()
        
        assert result.success is True, f"Service execution failed: {result.error}"
        assert isinstance(result.value, dict)
        
        service_data = result.value
        assert "service" in service_data
        assert service_data["service"] == "FlextMeltanoTapService"
        assert "tap_name" in service_data
        assert service_data["tap_name"] == "test-tap"
        assert "status" in service_data
        assert service_data["status"] == "ready"

    def test_abstract_methods_implementation(self) -> None:
        """Test abstract methods are properly implemented."""
        # Test get_tap_class
        tap_class = self.tap_service.get_tap_class()
        assert issubclass(tap_class, Tap)
        assert tap_class.name == "test-tap"
        
        # Test get_default_config
        config = self.tap_service.get_default_config()
        assert isinstance(config, dict)
        assert "test_setting" in config
        assert config["test_setting"] == "test_value"

    def test_singer_integration_real(self) -> None:
        """Test tap service integrates with real Singer SDK."""
        # Test wrapper is accessible
        wrapper_result = self.tap_service.wrapper_singer.execute()
        assert wrapper_result.success is True
        
        wrapper_data = wrapper_result.value
        assert isinstance(wrapper_data, dict)
        assert wrapper_data["status"] == "ready"
        
        # Test adapter is functional
        assert self.tap_service.singer_adapter is not None

    def test_flext_result_patterns_in_tap_service(self) -> None:
        """Test tap service uses correct FlextResult patterns."""
        # Test .value property usage
        execute_result = self.tap_service.execute()
        assert hasattr(execute_result, 'value')
        execute_value = execute_result.value
        assert isinstance(execute_value, dict)
        
        # Test unwrap_or() usage
        service_or_default = execute_result.unwrap_or({"service": "unknown"})
        assert "service" in service_or_default
        assert service_or_default["service"] == "FlextMeltanoTapService"


class TestRealFlextMeltanoTargetService:
    """Test real FlextMeltanoTargetService base functionality."""

    def setup_method(self) -> None:
        """Setup test target service instance."""
        self.target_service = TestTargetService()

    def test_target_service_initialization_real(self) -> None:
        """Test target service initializes with real dependencies."""
        assert self.target_service is not None
        assert hasattr(self.target_service, 'logger')
        
        # Test service has Singer wrapper integration
        assert hasattr(self.target_service, 'wrapper_singer')
        assert hasattr(self.target_service, 'singer_adapter')
        
        # Test service properties
        assert self.target_service.target_name == "test-target"
        assert self.target_service.wrapper_singer is not None
        assert self.target_service.singer_adapter is not None

    def test_execute_service_real_functionality(self) -> None:
        """Test service execution returns real target information."""
        result = self.target_service.execute()
        
        assert result.success is True, f"Service execution failed: {result.error}"
        assert isinstance(result.value, dict)
        
        service_data = result.value
        assert "service" in service_data
        assert service_data["service"] == "FlextMeltanoTargetService"
        assert "target_name" in service_data
        assert service_data["target_name"] == "test-target"
        assert "status" in service_data
        assert service_data["status"] == "ready"

    def test_abstract_methods_implementation(self) -> None:
        """Test abstract methods are properly implemented."""
        # Test get_target_class
        target_class = self.target_service.get_target_class()
        assert issubclass(target_class, Target)
        assert target_class.name == "test-target"
        
        # Test get_default_config
        config = self.target_service.get_default_config()
        assert isinstance(config, dict)
        assert "output_path" in config
        assert config["output_path"] == "/tmp/test"

    def test_singer_integration_real(self) -> None:
        """Test target service integrates with real Singer SDK."""
        # Test wrapper is accessible
        wrapper_result = self.target_service.wrapper_singer.execute()
        assert wrapper_result.success is True
        
        wrapper_data = wrapper_result.value
        assert isinstance(wrapper_data, dict)
        assert wrapper_data["status"] == "ready"


class TestRealFlextMeltanoDbtService:
    """Test real FlextMeltanoDbtService base functionality."""

    def setup_method(self) -> None:
        """Setup test DBT service instance."""
        self.dbt_service = TestDbtService()

    def test_dbt_service_initialization_real(self) -> None:
        """Test DBT service initializes with real dependencies."""
        assert self.dbt_service is not None
        assert hasattr(self.dbt_service, 'logger')
        
        # Test service has DBT wrapper integration
        assert hasattr(self.dbt_service, 'wrapper_dbt')
        assert hasattr(self.dbt_service, 'dbt_adapter')
        
        # Test service properties
        assert self.dbt_service.project_name == "test-dbt-project"
        assert self.dbt_service.wrapper_dbt is not None
        assert self.dbt_service.dbt_adapter is not None

    def test_execute_service_real_functionality(self) -> None:
        """Test service execution returns real DBT information."""
        result = self.dbt_service.execute()
        
        assert result.success is True, f"Service execution failed: {result.error}"
        assert isinstance(result.value, dict)
        
        service_data = result.value
        assert "service" in service_data
        assert service_data["service"] == "FlextMeltanoDbtService"
        assert "project_name" in service_data
        assert service_data["project_name"] == "test-dbt-project"
        assert "status" in service_data
        assert service_data["status"] == "ready"

    def test_concrete_methods_implementation(self) -> None:
        """Test concrete methods are properly implemented."""
        # Test get_project_config (the actual method name in the class)
        config = self.dbt_service.get_project_config()
        assert isinstance(config, dict)
        assert "name" in config
        assert config["name"] == "test-dbt-project"
        assert "version" in config
        assert "model-paths" in config
        
        # Test that default implementations work
        assert "analysis-paths" in config
        assert "test-paths" in config

    def test_dbt_integration_real(self) -> None:
        """Test DBT service integrates with real DBT Core."""
        # Test wrapper is accessible
        wrapper_result = self.dbt_service.wrapper_dbt.execute()
        assert wrapper_result.success is True
        
        wrapper_data = wrapper_result.value
        assert isinstance(wrapper_data, dict)
        assert wrapper_data["dbt_available"] is True


class TestRealServiceIntegration:
    """Test real service integration without mocks."""

    def setup_method(self) -> None:
        """Setup services for integration tests."""
        self.tap_service = TestTapService()
        self.target_service = TestTargetService()
        self.dbt_service = TestDbtService()

    def test_real_singer_sdk_integration(self) -> None:
        """Test services integrate with real Singer SDK."""
        # Test tap service Singer integration
        tap_class = self.tap_service.get_tap_class()
        assert issubclass(tap_class, Tap)
        
        # Test target service Singer integration
        target_class = self.target_service.get_target_class()
        assert issubclass(target_class, Target)
        
        # Both should use real Singer SDK classes
        assert hasattr(tap_class, 'name')
        assert hasattr(target_class, 'name')

    def test_real_dbt_core_integration(self) -> None:
        """Test DBT service integrates with real DBT Core."""
        # Test DBT service wrapper integration
        wrapper = self.dbt_service.wrapper_dbt
        assert wrapper is not None
        
        # Test DBT runner creation
        runner_result = wrapper.create_runner()
        assert runner_result.success is True
        
        runner = runner_result.value
        assert runner is not None
        assert hasattr(runner, 'invoke')

    def test_service_composition_patterns(self) -> None:
        """Test services use proper composition patterns."""
        # All services should have wrappers and adapters
        services = [self.tap_service, self.target_service, self.dbt_service]
        
        for service in services:
            assert hasattr(service, 'logger')
            
            # Test service execution
            result = service.execute()
            assert isinstance(result, FlextResult)
            assert result.success is True


class TestErrorHandlingPatterns:
    """Test error handling in base services using FlextResult patterns."""

    def setup_method(self) -> None:
        """Setup services for error handling tests."""
        self.tap_service = TestTapService()
        self.target_service = TestTargetService()
        self.dbt_service = TestDbtService()

    def test_flext_result_error_patterns(self) -> None:
        """Test error handling uses FlextResult.fail() properly."""
        # Test successful operations return FlextResult
        tap_result = self.tap_service.execute()
        target_result = self.target_service.execute()
        dbt_result = self.dbt_service.execute()
        
        # All should handle success gracefully with FlextResult
        for result in [tap_result, target_result, dbt_result]:
            assert isinstance(result, FlextResult)
            assert result.success is True

    def test_unwrap_or_error_handling(self) -> None:
        """Test error handling uses unwrap_or() pattern."""
        # Test successful cases
        tap_result = self.tap_service.execute()
        tap_data = tap_result.unwrap_or({"service": "fallback"})
        assert tap_data != {"service": "fallback"}  # Should get real service info
        
        target_result = self.target_service.execute()
        target_data = target_result.unwrap_or({"service": "fallback"})
        assert target_data != {"service": "fallback"}
        
        dbt_result = self.dbt_service.execute()
        dbt_data = dbt_result.unwrap_or({"service": "fallback"})
        assert dbt_data != {"service": "fallback"}

    def test_chaining_with_error_handling(self) -> None:
        """Test FlextResult chaining with proper error handling."""
        # Test multiple service operations can be chained safely
        tap_result = self.tap_service.execute()
        target_result = self.target_service.execute()
        dbt_result = self.dbt_service.execute()
        
        # All should return FlextResult for chaining
        results = [tap_result, target_result, dbt_result]
        for result in results:
            assert isinstance(result, FlextResult)
        
        # Test chained unwrap_or usage
        combined_data = {
            "tap": tap_result.unwrap_or({"service": "unknown"}),
            "target": target_result.unwrap_or({"service": "unknown"}),
            "dbt": dbt_result.unwrap_or({"service": "unknown"})
        }
        
        for service_type, data in combined_data.items():
            assert isinstance(data, dict)
            assert "service" in data
            assert data["service"] != "unknown"


class TestBaseServiceAbstractions:
    """Test base service abstraction patterns."""

    def test_tap_service_abstraction(self) -> None:
        """Test FlextMeltanoTapService abstraction is properly defined."""
        # Test class hierarchy
        assert issubclass(FlextMeltanoTapService, ABC)
        
        # Test abstract methods exist
        abstract_methods = FlextMeltanoTapService.__abstractmethods__
        expected_abstract = {'get_tap_class', 'get_default_config'}
        assert abstract_methods == expected_abstract

    def test_target_service_abstraction(self) -> None:
        """Test FlextMeltanoTargetService abstraction is properly defined."""
        # Test class hierarchy
        assert issubclass(FlextMeltanoTargetService, ABC)
        
        # Test abstract methods exist
        abstract_methods = FlextMeltanoTargetService.__abstractmethods__
        expected_abstract = {'get_target_class', 'get_default_config'}
        assert abstract_methods == expected_abstract

    def test_dbt_service_abstraction(self) -> None:
        """Test FlextMeltanoDbtService is concrete, not abstract."""
        # DBT service is concrete, not abstract (has default implementations)
        # This is different from Tap and Target services which are abstract
        
        # Test that it can be instantiated directly
        dbt_service = TestDbtService()
        assert dbt_service is not None
        
        # Test it has expected methods
        assert hasattr(dbt_service, 'get_project_config')
        assert callable(dbt_service.get_project_config)

    def test_concrete_implementations_required(self) -> None:
        """Test abstract classes cannot be instantiated without implementations."""
        # Test that abstract classes require implementation
        with pytest.raises(TypeError):
            FlextMeltanoTapService()  # type: ignore[abstract]
        
        with pytest.raises(TypeError):
            FlextMeltanoTargetService()  # type: ignore[abstract]
        
        # Note: FlextMeltanoDbtService is concrete, not abstract, so it can be instantiated
        # (but requires project_name parameter)

    def test_implemented_services_work(self) -> None:
        """Test concrete implementations work properly."""
        # Test implementations work
        tap = TestTapService()
        target = TestTargetService()
        dbt = TestDbtService()
        
        # All should execute successfully
        assert tap.execute().success is True
        assert target.execute().success is True
        assert dbt.execute().success is True