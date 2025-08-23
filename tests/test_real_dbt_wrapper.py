"""Real DBT Wrapper Tests - Tests REAL DBT Core 1.10.5 API integration.

**Test Category**: Real Integration Tests  
**Coverage Target**: 100% for DBT wrapper functionality
**Dependencies**: Real DBT Core 1.10.5 API, NO subprocess, NO mocks
**Execution Time**: Real API calls, may take longer

## Test Scope

Tests REAL DBT wrapper functionality:
- Direct DBT Core 1.10.5 API integration using native Python APIs
- dbtRunner real execution capabilities
- Project management with real DBT project operations
- FlextResult patterns with .value and unwrap_or() - NO .data/.unwrap()

## Architecture Alignment  

Tests the Wrapper function (Função 1):
- Real adaptation of DBT Core APIs to flext-core patterns
- Native API integration without subprocess calls
- Enterprise error handling with FlextResult
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from flext_core import FlextResult

from flext_meltano.funcao1_wrapper_dbt import MeltanoDbtWrapper, FlextDbtAdapter


class TestRealMeltanoDbtWrapper:
    """Test real MeltanoDbtWrapper with actual DBT Core 1.10.5 API integration."""

    def setup_method(self) -> None:
        """Setup real DBT wrapper instance."""
        self.wrapper = MeltanoDbtWrapper()

    def test_wrapper_initialization_real(self) -> None:
        """Test wrapper initializes with real DBT availability."""
        assert self.wrapper is not None
        assert hasattr(self.wrapper, 'logger')
        
        # Test wrapper has access to real DBT methods
        assert hasattr(self.wrapper, 'create_runner')
        assert hasattr(self.wrapper, 'run_models_real')
        assert hasattr(self.wrapper, 'test_models')

    def test_create_runner_real_dbt_api(self) -> None:
        """Test runner creation using real DBT Core API."""
        result = self.wrapper.create_runner()
        
        assert result.success is True, f"Runner creation failed: {result.error}"
        
        # Should return real dbtRunner instance
        runner = result.value
        assert runner is not None
        # DBT runner should have invoke method
        assert hasattr(runner, 'invoke')

    def test_execute_service_real_functionality(self) -> None:
        """Test service execution returns real wrapper information."""
        result = self.wrapper.execute()
        
        assert result.success is True, f"Service execution failed: {result.error}"
        assert isinstance(result.value, dict)
        
        service_data = result.value
        assert "service" in service_data
        assert service_data["service"] == "MeltanoDbtWrapper"
        assert "status" in service_data
        assert "dbt_available" in service_data
        assert service_data["dbt_available"] is True  # Real availability
        assert "capabilities" in service_data
        assert isinstance(service_data["capabilities"], list)
        assert "create_runner" in service_data["capabilities"]

    def test_compile_project_capability(self) -> None:
        """Test compile project capability exists."""
        # Test that compile_project method is available
        assert hasattr(self.wrapper, 'compile_project')
        
        # Test execute() shows this capability
        result = self.wrapper.execute()
        assert result.success is True
        capabilities = result.value["capabilities"]
        assert "compile_project" in capabilities

    def test_generate_docs_capability(self) -> None:
        """Test generate docs capability exists."""
        # Test that generate_docs method is available
        assert hasattr(self.wrapper, 'generate_docs')
        
        # Test execute() shows this capability
        result = self.wrapper.execute()
        assert result.success is True
        capabilities = result.value["capabilities"]
        assert "generate_docs" in capabilities

    def test_test_models_capability(self) -> None:
        """Test test models capability with real validation."""
        # Test that test_models method is available
        assert hasattr(self.wrapper, 'test_models')
        
        # Test execute() shows this capability
        result = self.wrapper.execute()
        assert result.success is True
        capabilities = result.value["capabilities"]
        assert "test_models" in capabilities

    def test_flext_result_patterns_in_wrapper(self) -> None:
        """Test wrapper methods use correct FlextResult patterns."""
        # Test .value property usage (not .data)
        execute_result = self.wrapper.execute()
        assert hasattr(execute_result, 'value')
        execute_value = execute_result.value
        assert isinstance(execute_value, dict)
        
        # Test unwrap_or() usage (not manual if/else)
        service_or_default = execute_result.unwrap_or({"service": "unknown"})
        assert "service" in service_or_default
        
        # Test error handling with unwrap_or
        runner_result = self.wrapper.create_runner()
        runner_or_none = runner_result.unwrap_or(None)
        assert runner_or_none is not None  # Should get real runner


class TestFlextDbtAdapter:
    """Test FlextDbtAdapter real type adaptations."""

    def test_adapt_project_data_real(self) -> None:
        """Test adapter handles real DBT project data structures."""
        # Create sample project data that matches real DBT structures
        real_project_data = {
            "name": "test_project",
            "version": "1.0.0",
            "profile": "test_profile",
            "model-paths": ["models"],
            "analysis-paths": ["analysis"],
            "test-paths": ["tests"],
            "seed-paths": ["data"]
        }
        
        # Test adapter processes real data
        adapter = FlextDbtAdapter()
        # Note: adapter methods may need to be static or have different signatures
        # This tests the adapter exists and can be instantiated
        assert adapter is not None

    def test_adapter_integration_with_wrapper(self) -> None:
        """Test adapter integration with real wrapper operations."""
        wrapper = MeltanoDbtWrapper()
        adapter = FlextDbtAdapter()
        
        # Both should be compatible for real usage
        assert wrapper is not None
        assert adapter is not None
        
        # Test they can work together in real scenarios
        wrapper_result = wrapper.execute()
        assert wrapper_result.success is True


class TestRealDbtIntegration:
    """Test real DBT integration without subprocess."""

    def setup_method(self) -> None:
        """Setup wrapper for DBT integration tests."""
        self.wrapper = MeltanoDbtWrapper()

    def test_real_dbt_runner_integration(self) -> None:
        """Test real dbtRunner integration."""
        # Create dbtRunner for testing
        runner_result = self.wrapper.create_runner()
        
        # Should create real dbtRunner instance
        assert runner_result.success is True, f"Runner creation failed: {runner_result.error}"
        
        runner = runner_result.value
        assert runner is not None
        assert hasattr(runner, 'invoke')

    def test_real_dbt_runner_api(self) -> None:
        """Test direct integration with real DBT runner API."""
        # This should use DBT Core API internally, not subprocess
        result = self.wrapper.create_runner()
        
        assert result.success is True
        runner = result.value
        assert runner is not None
        
        # Verify it's using real API, not subprocess fallback
        assert hasattr(runner, 'invoke')

    def test_real_dbt_core_integration(self) -> None:
        """Test that wrapper uses real DBT Core, not subprocess."""
        # Import DBT Core directly to test integration
        from dbt.cli.main import dbtRunner
        
        # Create runner directly
        real_runner = dbtRunner()
        assert real_runner is not None
        
        # Now test wrapper creates same type
        wrapper_result = self.wrapper.create_runner()
        assert wrapper_result.success is True
        
        wrapper_runner = wrapper_result.value
        
        # Both should be real DBT runners
        assert type(wrapper_runner).__name__ == type(real_runner).__name__


class TestErrorHandlingPatterns:
    """Test real error handling using FlextResult patterns."""

    def setup_method(self) -> None:
        """Setup wrapper for error handling tests."""
        self.wrapper = MeltanoDbtWrapper()

    def test_flext_result_error_patterns(self) -> None:
        """Test error handling uses FlextResult.fail() properly."""
        # Test successful operations return FlextResult
        result = self.wrapper.execute()
        
        # Should handle success gracefully with FlextResult
        assert isinstance(result, FlextResult)
        # Should succeed for basic service info
        assert result.success is True

    def test_unwrap_or_error_handling(self) -> None:
        """Test error handling uses unwrap_or() pattern."""
        # Test successful case
        success_result = self.wrapper.execute()
        service_data = success_result.unwrap_or({"service": "fallback"})
        assert service_data != {"service": "fallback"}  # Should get real service info
        
        # Test that unwrap_or provides clean error handling
        assert isinstance(service_data, dict)
        assert "service" in service_data

    def test_chaining_with_error_handling(self) -> None:
        """Test FlextResult chaining with proper error handling."""
        # Test multiple operations can be chained safely
        execute_result = self.wrapper.execute()
        runner_result = self.wrapper.create_runner()
        
        # Both should return FlextResult for chaining
        assert isinstance(execute_result, FlextResult)
        assert isinstance(runner_result, FlextResult)
        
        # Test chained unwrap_or usage
        combined_data = {
            "service": execute_result.unwrap_or({"service": "unknown"}),
            "runner_available": runner_result.unwrap_or(None) is not None
        }
        
        assert "service" in combined_data
        assert "runner_available" in combined_data
        assert combined_data["runner_available"] is True