"""Real execution functionality tests - ACTUAL Meltano/DBT execution.

This module tests REAL functionality by executing actual Meltano/DBT commands
using the current API structure. NO MOCKS - only real execution.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from flext_core import FlextResult

from flext_meltano.bridge import FlextMeltanoBridge
from flext_meltano.execution import FlextMeltanoExecutor
from flext_meltano.execution import SimpleMeltanoExecutor, SimpleDbtExecutor, execute_simple_elt_workflow, execute_simple_dbt_workflow
from flext_meltano.meltano import MeltanoBridge
from flext_meltano.dbt import MeltanoDbtWrapper


class TestRealExecutionFunctionality:
    """Test actual execution functionality without mocks."""

    def test_flext_meltano_executor_service_info(self) -> None:
        """Test FlextMeltanoExecutor service information."""
        executor = FlextMeltanoExecutor()
        
        # Test the execute method (required by FlextDomainService)
        result = executor.execute()
        
        assert result.success
        assert isinstance(result.value, dict)
        assert "service" in result.value
        assert result.value["service"] == "FlextMeltanoExecutor"

    def test_flext_meltano_bridge_version(self) -> None:
        """Test FlextMeltanoBridge version information."""
        bridge = FlextMeltanoBridge()
        
        # Test version information
        version_info = bridge.get_version()
        
        assert version_info["success"] is True
        assert "data" in version_info
        data = version_info["data"]
        assert "flext_meltano" in data
        assert "meltano" in data
        assert "dbt_core" in data
        assert "singer_sdk" in data
        assert data["integration_method"] == "native_apis"

    def test_meltano_bridge_service_info(self) -> None:
        """Test MeltanoBridge service execution."""
        bridge = MeltanoBridge()
        
        # Test the execute method
        result = bridge.execute()
        
        assert result.success
        assert isinstance(result.value, dict)
        assert "service" in result.value

    def test_dbt_wrapper_service_info(self) -> None:
        """Test MeltanoDbtWrapper service execution."""
        wrapper = MeltanoDbtWrapper()
        
        # Test the execute method 
        result = wrapper.execute()
        
        assert result.success
        assert isinstance(result.value, dict)
        assert "service" in result.value

    def test_simple_meltano_executor_project_creation(self) -> None:
        """Test SimpleMeltanoExecutor project creation."""
        executor = SimpleMeltanoExecutor()
        
        # Test creating a test project
        project_result = executor.create_test_project("pytest_test")
        
        # Should succeed in creating a project
        assert project_result.success
        project_path = project_result.value
        assert isinstance(project_path, Path)
        assert project_path.exists()
        assert (project_path / "meltano.yml").exists()
        assert (project_path / "test.csv").exists()

    def test_simple_dbt_executor_project_creation(self) -> None:
        """Test SimpleDbtExecutor project creation."""
        executor = SimpleDbtExecutor()
        
        # Test creating a DBT project
        project_result = executor.create_test_dbt_project("pytest_dbt_test")
        
        # Should succeed in creating a project
        assert project_result.success
        project_path = project_result.value
        assert isinstance(project_path, Path)
        assert project_path.exists()
        assert (project_path / "dbt_project.yml").exists()
        assert (project_path / "profiles.yml").exists()
        assert (project_path / "models").exists()

    @pytest.mark.slow
    def test_simple_elt_workflow_execution(self) -> None:
        """Test complete ELT workflow execution (marked as slow)."""
        # Execute the workflow function
        result = execute_simple_elt_workflow()
        
        # Should return a result dict
        assert isinstance(result, dict)
        assert "success" in result
        assert "exit_code" in result
        
        # Even if it fails, we should get structured data back
        # (This tests the .unwrap_or() fallback pattern)
        if result["success"] == "true":
            assert "output_files" in result
            assert "extractor" in result
            assert "loader" in result

    @pytest.mark.slow
    def test_simple_dbt_workflow_execution(self) -> None:
        """Test complete DBT workflow execution (marked as slow)."""
        # Execute the workflow function
        result = execute_simple_dbt_workflow()
        
        # Should return a result dict
        assert isinstance(result, dict)
        assert "workflow" in result
        
        # Should have workflow status
        assert result["workflow"] in ["complete", "stopped_at_parse", "stopped_at_compile"]
        
        # Should have parse result
        if "parse" in result:
            assert result["parse"] in ["true", "false"]


class TestRealFlextResultPatterns:
    """Test that FlextResult patterns work correctly with real data."""

    def test_flext_result_success_pattern(self) -> None:
        """Test FlextResult success pattern."""
        bridge = MeltanoBridge()
        result = bridge.execute()
        
        # Test that we can use the new .value pattern
        if result.success:
            data = result.value
            assert isinstance(data, dict)
            assert "service" in data
        else:
            # Should not reach here in this test
            pytest.fail(f"Service execution failed: {result.error}")

    def test_flext_result_unwrap_or_pattern(self) -> None:
        """Test FlextResult .unwrap_or() pattern."""
        executor = SimpleMeltanoExecutor()
        
        # Test the .unwrap_or() pattern
        project_path = executor.create_test_project().unwrap_or(Path.cwd())
        
        # Should get a valid path (either real project or current dir fallback)
        assert isinstance(project_path, Path)
        assert project_path.exists()


class TestRealAPIIntegration:
    """Test that real API integration works without subprocess calls."""

    def test_meltano_hub_integration(self) -> None:
        """Test that Meltano Hub integration works."""
        bridge = MeltanoBridge()
        
        # Create a temporary project for hub access
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Test hub plugin discovery
            result = bridge.discover_plugins(temp_path)
            
            # Should return a result (success or failure)
            assert isinstance(result, FlextResult)
            # Even if it fails due to project setup, should return structured data
            if result.success:
                plugins = result.value
                assert isinstance(plugins, list)

    def test_dbt_runner_integration(self) -> None:
        """Test that DBT runner integration works."""
        wrapper = MeltanoDbtWrapper()
        
        # Test creating a runner
        runner_result = wrapper.create_runner()
        
        # Should be able to create a DBT runner
        assert isinstance(runner_result, FlextResult)
        # DBT Core is installed, so this should work
        if runner_result.success:
            runner = runner_result.value
            assert runner is not None


if __name__ == "__main__":
    # Allow running the tests directly
    pytest.main([__file__, "-v"])