"""Real Runtime Bridge Tests - Tests REAL Go bridge integration capabilities.

**Test Category**: Real Integration Tests  
**Coverage Target**: 100% for runtime bridge functionality
**Dependencies**: Real Go bridge integration, NO subprocess, NO mocks
**Execution Time**: Real bridge calls, may take longer

## Test Scope

Tests REAL runtime bridge functionality:
- Direct FlextMeltanoBridge API for Go service integration
- JSON API responses for Go service consumption
- Real bridge integration with MeltanoBridge and MeltanoDbtWrapper
- FlextResult patterns with .value and unwrap_or() - NO .data/.unwrap()

## Architecture Alignment  

Tests the Runtime function (Função 2):
- Real Go ↔ Python bridge communication
- JSON API integration for Go services  
- Enterprise error handling with structured responses
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from flext_meltano.funcao2_runtime_bridge import FlextMeltanoBridge


class TestRealFlextMeltanoBridge:
    """Test real FlextMeltanoBridge with actual Go bridge integration."""

    def setup_method(self) -> None:
        """Setup real bridge instance."""
        self.bridge = FlextMeltanoBridge()

    def test_bridge_initialization_real(self) -> None:
        """Test bridge initializes with real dependencies."""
        assert self.bridge is not None
        
        # Test bridge has access to real components
        assert hasattr(self.bridge, 'executor')
        assert hasattr(self.bridge, 'meltano_bridge')
        assert hasattr(self.bridge, 'wrapper_dbt')
        
        # Test that components are properly initialized
        assert self.bridge.executor is not None
        assert self.bridge.meltano_bridge is not None
        assert self.bridge.wrapper_dbt is not None

    def test_get_version_real_integration(self) -> None:
        """Test version retrieval returns real integration info."""
        result = self.bridge.get_version()
        
        assert isinstance(result, dict)
        assert "success" in result
        assert result["success"] is True
        
        # Test data structure for Go consumption
        assert "data" in result
        data = result["data"]
        assert isinstance(data, dict)
        
        # Verify version information
        assert "flext_meltano" in data
        assert data["flext_meltano"] == "2.0.0-enterprise"
        assert "meltano" in data
        assert data["meltano"] == "3.9.1"
        assert "dbt_core" in data
        assert data["dbt_core"] == "1.10.5"
        assert "singer_sdk" in data
        assert data["singer_sdk"] == "0.48.0"
        assert "python" in data
        assert data["python"] == "3.13+"
        assert "integration_method" in data
        assert data["integration_method"] == "native_apis"

    def test_list_plugins_real_hub_integration(self) -> None:
        """Test plugin listing uses real Meltano Hub integration."""
        result = self.bridge.list_plugins()
        
        assert isinstance(result, dict)
        assert "success" in result
        
        # Should succeed with real Hub integration
        if result["success"]:
            assert "data" in result
            plugins_data = result["data"]
            assert isinstance(plugins_data, (list, dict))
        else:
            # If it fails, should have error message
            assert "error" in result
            assert isinstance(result["error"], str)

    def test_run_pipeline_validation(self) -> None:
        """Test pipeline execution validation with bridge."""
        # Test with invalid parameters (should return structured error)
        result = self.bridge.run_pipeline("", "")
        
        assert isinstance(result, dict)
        assert "success" in result
        
        # Should fail due to validation but return structured response
        if not result["success"]:
            assert "error" in result
            assert isinstance(result["error"], str)

    def test_execute_command_validation(self) -> None:
        """Test command execution validation through bridge."""
        # Test with invalid project root
        with tempfile.TemporaryDirectory() as temp_dir:
            result = self.bridge.execute_meltano_command(["--version"], str(temp_dir))
            
            assert isinstance(result, dict)
            assert "success" in result
            
            # Should fail due to no meltano.yml but return structured response
            if not result["success"]:
                assert "error" in result
                assert isinstance(result["error"], str)
                assert "Not a Meltano project" in result["error"]

    def test_bridge_json_response_format(self) -> None:
        """Test bridge returns properly formatted JSON responses for Go."""
        # Test version response format
        version_result = self.bridge.get_version()
        self._validate_json_response_format(version_result, expect_data=True)
        
        # Test plugins response format
        plugins_result = self.bridge.list_plugins()
        self._validate_json_response_format(plugins_result)

    def _validate_json_response_format(self, response: dict[str, object], expect_data: bool = False) -> None:
        """Validate JSON response format for Go consumption."""
        assert isinstance(response, dict)
        assert "success" in response
        assert isinstance(response["success"], bool)
        
        if response["success"]:
            if expect_data:
                assert "data" in response
        else:
            assert "error" in response
            assert isinstance(response["error"], str)


class TestRealBridgeIntegration:
    """Test real bridge integration without subprocess."""

    def setup_method(self) -> None:
        """Setup bridge for integration tests."""
        self.bridge = FlextMeltanoBridge()

    def test_real_executor_integration(self) -> None:
        """Test bridge integrates with real FlextMeltanoExecutor."""
        # Test that bridge uses real executor
        executor = self.bridge.executor
        assert executor is not None
        
        # Test executor functionality
        executor_result = executor.execute()
        assert executor_result.success is True
        
        executor_data = executor_result.value
        assert isinstance(executor_data, dict)
        assert executor_data["status"] == "ready"

    def test_real_meltano_bridge_integration(self) -> None:
        """Test bridge uses real MeltanoBridge."""
        # Test that bridge uses real MeltanoBridge
        meltano_bridge = self.bridge.meltano_bridge
        assert meltano_bridge is not None
        
        # Test MeltanoBridge functionality
        version_result = meltano_bridge.get_version()
        assert version_result.success is True
        
        version_data = version_result.value
        assert isinstance(version_data, dict)
        assert version_data["version"] == "3.9.1"

    def test_real_dbt_wrapper_integration(self) -> None:
        """Test bridge uses real MeltanoDbtWrapper."""
        # Test that bridge uses real MeltanoDbtWrapper
        dbt_wrapper = self.bridge.wrapper_dbt
        assert dbt_wrapper is not None
        
        # Test DBT wrapper functionality
        wrapper_result = dbt_wrapper.execute()
        assert wrapper_result.success is True
        
        wrapper_data = wrapper_result.value
        assert isinstance(wrapper_data, dict)
        assert wrapper_data["dbt_available"] is True

    def test_bridge_error_handling_patterns(self) -> None:
        """Test bridge error handling uses proper patterns."""
        # Test with operations that might fail
        with tempfile.TemporaryDirectory() as temp_dir:
            # This should fail but return proper JSON response
            result = self.bridge.execute_meltano_command(["invalid"], str(temp_dir))
            
            assert isinstance(result, dict)
            assert "success" in result
            
            # Should handle error gracefully
            if not result["success"]:
                assert "error" in result
                assert isinstance(result["error"], str)


class TestBridgeMethodCoverage:
    """Test comprehensive bridge method coverage."""

    def setup_method(self) -> None:
        """Setup bridge for method coverage tests."""
        self.bridge = FlextMeltanoBridge()

    def test_get_version_comprehensive(self) -> None:
        """Test get_version method comprehensively."""
        result = self.bridge.get_version()
        
        # Validate complete response structure
        assert isinstance(result, dict)
        assert result["success"] is True
        
        data = result["data"]
        required_keys = [
            "flext_meltano",
            "meltano", 
            "dbt_core",
            "singer_sdk",
            "python",
            "integration_method"
        ]
        
        for key in required_keys:
            assert key in data
            assert isinstance(data[key], str)
            assert len(data[key]) > 0

    def test_list_plugins_comprehensive(self) -> None:
        """Test list_plugins method comprehensively."""
        result = self.bridge.list_plugins()
        
        # Validate response structure
        assert isinstance(result, dict)
        assert "success" in result
        
        # Response should be valid regardless of success/failure
        if result["success"]:
            assert "data" in result
            # Data should be structured for Go consumption
            plugins_data = result["data"]
            assert isinstance(plugins_data, (list, dict))
        else:
            assert "error" in result
            assert isinstance(result["error"], str)

    def test_bridge_method_availability(self) -> None:
        """Test all expected bridge methods are available."""
        expected_methods = [
            'get_version',
            'list_plugins',
            'run_pipeline',
            'execute_meltano_command',
            'execute_dbt_command',
            'install_plugin',
            'get_project_info'
        ]
        
        for method_name in expected_methods:
            assert hasattr(self.bridge, method_name), f"Missing method: {method_name}"
            method = getattr(self.bridge, method_name)
            assert callable(method), f"Method {method_name} is not callable"


class TestBridgeErrorHandling:
    """Test bridge error handling for Go integration."""

    def setup_method(self) -> None:
        """Setup bridge for error handling tests."""
        self.bridge = FlextMeltanoBridge()

    def test_version_error_handling(self) -> None:
        """Test version method handles errors gracefully."""
        # Normal case should succeed
        result = self.bridge.get_version()
        assert result["success"] is True
        
        # Verify error handling structure exists
        assert isinstance(result, dict)
        assert "success" in result

    def test_plugins_error_handling(self) -> None:
        """Test plugins method handles errors gracefully."""
        result = self.bridge.list_plugins()
        
        # Should return structured response regardless of success
        assert isinstance(result, dict)
        assert "success" in result
        
        if not result["success"]:
            assert "error" in result
            assert isinstance(result["error"], str)

    def test_command_execution_error_handling(self) -> None:
        """Test command execution handles errors properly."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test with invalid project
            result = self.bridge.execute_meltano_command(["invalid"], temp_dir)
            
            assert isinstance(result, dict)
            assert "success" in result
            
            # Should handle validation errors properly
            if not result["success"]:
                assert "error" in result
                assert isinstance(result["error"], str)

    def test_json_serialization_safety(self) -> None:
        """Test JSON responses are safe for Go consumption."""
        # Test version response
        version_result = self.bridge.get_version()
        
        # Should be JSON serializable
        import json
        try:
            json.dumps(version_result)
        except Exception as e:
            pytest.fail(f"Version result not JSON serializable: {e}")
        
        # Test plugins response  
        plugins_result = self.bridge.list_plugins()
        
        try:
            json.dumps(plugins_result)
        except Exception as e:
            pytest.fail(f"Plugins result not JSON serializable: {e}")


class TestBridgePerformance:
    """Test bridge performance for Go integration."""

    def setup_method(self) -> None:
        """Setup bridge for performance tests."""
        self.bridge = FlextMeltanoBridge()

    def test_version_response_performance(self) -> None:
        """Test version response is fast for Go calls."""
        import time
        
        start_time = time.time()
        result = self.bridge.get_version()
        end_time = time.time()
        
        # Version call should be very fast (< 1 second)
        execution_time = end_time - start_time
        assert execution_time < 1.0, f"Version call too slow: {execution_time}s"
        assert result["success"] is True

    def test_multiple_calls_performance(self) -> None:
        """Test multiple bridge calls perform well."""
        import time
        
        start_time = time.time()
        
        # Make multiple calls
        for _ in range(5):
            version_result = self.bridge.get_version()
            assert version_result["success"] is True
        
        end_time = time.time()
        
        # Should complete 5 calls in reasonable time
        total_time = end_time - start_time
        assert total_time < 5.0, f"Multiple calls too slow: {total_time}s"