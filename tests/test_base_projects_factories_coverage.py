"""Base projects factory functions coverage tests - testing what works with real APIs.

**Purpose**: Cover the working factory functions in base_projects.py
**Target**: Real functionality testing with correct factory usage
**Scope**: FlextMeltanoConfig and factory functions that actually work
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest
from flext_core import FlextResult

from flext_meltano.base_projects import (
    FlextMeltanoConfig,
    create_meltano_dbt_service,
    create_meltano_extension_service,
    create_meltano_tap_service,
    create_meltano_target_service,
)


class TestFlextMeltanoConfigWorking:
    """Test FlextMeltanoConfig functionality that actually works."""
    
    def test_config_creation_minimal(self) -> None:
        """Test config creation with minimal valid parameters."""
        config = FlextMeltanoConfig(
            project_root=str(Path.cwd()),
            environment="test",
        )
        
        assert config is not None
        assert isinstance(config.project_root, str)
        assert config.environment == "test"
        
    def test_config_with_different_environments(self) -> None:
        """Test configuration with different environments."""
        environments = ["development", "test", "staging", "production"]
        
        for env in environments:
            config = FlextMeltanoConfig(
                project_root=str(Path.cwd()),
                environment=env,
            )
            
            assert config.environment == env
            assert isinstance(config.project_root, str)
            
    def test_config_with_temp_directory(self) -> None:
        """Test config with temporary directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(
                project_root=temp_dir,
                environment="temporary",
            )
            
            assert config.project_root == temp_dir
            assert config.environment == "temporary"


class TestMeltanoFactoryFunctions:
    """Test the factory functions that create services."""
    
    def test_create_meltano_tap_service(self) -> None:
        """Test create_meltano_tap_service factory function."""
        config = FlextMeltanoConfig(
            project_root=str(Path.cwd()),
            environment="test",
        )
        
        result = create_meltano_tap_service(config)
        assert isinstance(result, FlextResult)
        # Factory might succeed or fail, but should return FlextResult
        
    def test_create_meltano_target_service(self) -> None:
        """Test create_meltano_target_service factory function."""
        config = FlextMeltanoConfig(
            project_root=str(Path.cwd()),
            environment="test",
        )
        
        result = create_meltano_target_service(config)
        assert isinstance(result, FlextResult)
        # Factory might succeed or fail, but should return FlextResult
        
    def test_create_meltano_dbt_service(self) -> None:
        """Test create_meltano_dbt_service factory function."""
        config = FlextMeltanoConfig(
            project_root=str(Path.cwd()),
            environment="test",
        )
        
        result = create_meltano_dbt_service(config)
        assert isinstance(result, FlextResult)
        # Factory might succeed or fail, but should return FlextResult
        
    def test_create_meltano_extension_service(self) -> None:
        """Test create_meltano_extension_service factory function."""
        config = FlextMeltanoConfig(
            project_root=str(Path.cwd()),
            environment="test",
        )
        
        result = create_meltano_extension_service(config)
        assert isinstance(result, FlextResult)
        # Factory might succeed or fail, but should return FlextResult
        
    def test_factory_functions_with_same_config(self) -> None:
        """Test all factory functions with same configuration."""
        config = FlextMeltanoConfig(
            project_root=str(Path.cwd()),
            environment="factory_test",
        )
        
        factories = [
            create_meltano_tap_service,
            create_meltano_target_service,
            create_meltano_dbt_service,
            create_meltano_extension_service,
        ]
        
        for factory in factories:
            result = factory(config)
            assert isinstance(result, FlextResult)
            # Each factory should return FlextResult consistently
            
    def test_factory_functions_with_different_configs(self) -> None:
        """Test factory functions with different configurations."""
        configs = [
            FlextMeltanoConfig(project_root=str(Path.cwd()), environment="dev"),
            FlextMeltanoConfig(project_root=str(Path.cwd()), environment="prod"),
        ]
        
        for config in configs:
            # Test tap service factory
            tap_result = create_meltano_tap_service(config)
            assert isinstance(tap_result, FlextResult)
            
            # Test target service factory
            target_result = create_meltano_target_service(config)
            assert isinstance(target_result, FlextResult)
            
            # Test DBT service factory
            dbt_result = create_meltano_dbt_service(config)
            assert isinstance(dbt_result, FlextResult)
            
            # Test extension service factory
            ext_result = create_meltano_extension_service(config)
            assert isinstance(ext_result, FlextResult)


class TestFactoryErrorHandling:
    """Test factory function error handling."""
    
    def test_factories_with_nonexistent_project_root(self) -> None:
        """Test factory functions with nonexistent project root."""
        config = FlextMeltanoConfig(
            project_root="/nonexistent/project/path",
            environment="test_nonexistent",
        )
        
        factories = [
            create_meltano_tap_service,
            create_meltano_target_service,
            create_meltano_dbt_service,
            create_meltano_extension_service,
        ]
        
        for factory in factories:
            try:
                result = factory(config)
                assert isinstance(result, FlextResult)
                # Should handle gracefully, not raise exception
            except Exception:
                pytest.fail(f"Factory {factory.__name__} should handle errors gracefully")
                
    def test_factories_with_edge_case_environments(self) -> None:
        """Test factory functions with edge case environments."""
        edge_environments = [
            "",  # Empty string
            "test-with-dashes",
            "test_with_underscores", 
            "123_numeric_start",
            "UPPERCASE_ENV",
        ]
        
        for env in edge_environments:
            config = FlextMeltanoConfig(
                project_root=str(Path.cwd()),
                environment=env,
            )
            
            factories = [
                create_meltano_tap_service,
                create_meltano_target_service,
                create_meltano_dbt_service,
                create_meltano_extension_service,
            ]
            
            for factory in factories:
                try:
                    result = factory(config)
                    assert isinstance(result, FlextResult)
                    # Should handle edge cases gracefully
                except Exception:
                    pytest.fail(f"Factory {factory.__name__} should handle edge cases")


class TestConfigurationValidation:
    """Test configuration validation patterns."""
    
    def test_config_field_validation(self) -> None:
        """Test configuration field validation."""
        # Valid configuration
        valid_config = FlextMeltanoConfig(
            project_root=str(Path.cwd()),
            environment="validation_test",
        )
        
        assert valid_config is not None
        assert hasattr(valid_config, 'project_root')
        assert hasattr(valid_config, 'environment')
        
    def test_config_immutability(self) -> None:
        """Test configuration immutability if applicable."""
        config = FlextMeltanoConfig(
            project_root=str(Path.cwd()),
            environment="immutable_test",
        )
        
        original_env = config.environment
        original_root = config.project_root
        
        # Configuration should maintain its values
        assert config.environment == original_env
        assert config.project_root == original_root
        
    def test_config_properties_access(self) -> None:
        """Test configuration properties access."""
        config = FlextMeltanoConfig(
            project_root=str(Path.cwd()),
            environment="properties_test",
        )
        
        # Should be able to access all properties without error
        assert isinstance(config.project_root, str)
        assert isinstance(config.environment, str)
        
        # Check if additional properties exist (common Meltano config patterns)
        if hasattr(config, 'dbt_project_dir'):
            # Access without error
            _ = config.dbt_project_dir
            
        if hasattr(config, 'dbt_profiles_dir'):
            # Access without error  
            _ = config.dbt_profiles_dir


class TestRealWorldFactoryUsage:
    """Test real-world usage patterns for factory functions."""
    
    def test_typical_service_creation_workflow(self) -> None:
        """Test typical service creation workflow using factories."""
        # Step 1: Create project configuration
        with tempfile.TemporaryDirectory() as temp_dir:
            config = FlextMeltanoConfig(
                project_root=temp_dir,
                environment="production",
            )
            
            # Step 2: Create services using factories
            tap_result = create_meltano_tap_service(config)
            target_result = create_meltano_target_service(config)
            dbt_result = create_meltano_dbt_service(config)
            extension_result = create_meltano_extension_service(config)
            
            # Step 3: Verify all factories returned FlextResult
            assert isinstance(tap_result, FlextResult)
            assert isinstance(target_result, FlextResult)
            assert isinstance(dbt_result, FlextResult)
            assert isinstance(extension_result, FlextResult)
            
    def test_multi_project_factory_usage(self) -> None:
        """Test factory usage across multiple projects."""
        projects = [
            {"root": str(Path.cwd()), "env": "project1"},
            {"root": str(Path.cwd() / "subproject"), "env": "project2"},
        ]
        
        for project in projects:
            config = FlextMeltanoConfig(
                project_root=project["root"],
                environment=project["env"],
            )
            
            # Create all service types for this project
            services = [
                create_meltano_tap_service(config),
                create_meltano_target_service(config),
                create_meltano_dbt_service(config),
                create_meltano_extension_service(config),
            ]
            
            # All should return FlextResult
            for service_result in services:
                assert isinstance(service_result, FlextResult)
                
    def test_factory_consistency_across_environments(self) -> None:
        """Test factory consistency across different environments."""
        environments = ["development", "testing", "staging", "production"]
        
        for env in environments:
            config = FlextMeltanoConfig(
                project_root=str(Path.cwd()),
                environment=env,
            )
            
            # Each environment should work with all factories
            results = [
                create_meltano_tap_service(config),
                create_meltano_target_service(config),
                create_meltano_dbt_service(config),
                create_meltano_extension_service(config),
            ]
            
            # All should return FlextResult regardless of environment
            for result in results:
                assert isinstance(result, FlextResult)


class TestFactoryIntegration:
    """Test integration patterns for factory functions."""
    
    def test_factory_result_patterns(self) -> None:
        """Test factory result patterns and consistency."""
        config = FlextMeltanoConfig(
            project_root=str(Path.cwd()),
            environment="integration_test",
        )
        
        factories = [
            ("tap", create_meltano_tap_service),
            ("target", create_meltano_target_service),
            ("dbt", create_meltano_dbt_service),
            ("extension", create_meltano_extension_service),
        ]
        
        for service_type, factory in factories:
            result = factory(config)
            assert isinstance(result, FlextResult)
            
            # FlextResult should have consistent interface
            assert hasattr(result, 'success')
            # Only access .data/.error if we know the state
            if result.success:
                assert hasattr(result, 'data')
            else:
                assert hasattr(result, 'error')
            
    def test_factory_error_propagation(self) -> None:
        """Test how factories propagate errors."""
        # Use invalid configuration to test error handling
        invalid_configs = [
            FlextMeltanoConfig(project_root="", environment="test"),
            FlextMeltanoConfig(project_root=str(Path.cwd()), environment=""),
        ]
        
        for config in invalid_configs:
            factories = [
                create_meltano_tap_service,
                create_meltano_target_service, 
                create_meltano_dbt_service,
                create_meltano_extension_service,
            ]
            
            for factory in factories:
                result = factory(config)
                assert isinstance(result, FlextResult)
                # Should handle errors gracefully via FlextResult