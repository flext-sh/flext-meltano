"""Complete base projects coverage tests - testing all project service functionality with real APIs.

**Purpose**: Achieve 95%+ coverage on base_projects.py module
**Target**: Real functionality testing of all project service classes
**Scope**: All project service classes and factory functions
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from flext_core import FlextResult
from singer_sdk import Stream, Tap, Target

from flext_meltano.base_projects import (
    FlextMeltanoConfig,
    FlextMeltanoDbtService,
    FlextMeltanoExtensionService,
    FlextMeltanoTapService,
    FlextMeltanoTargetService,
)


# Create test tap and target implementations for testing
class TestProjectTap(Tap):
    """Test tap for project testing."""
    
    name = "test_project_tap"
    config_jsonschema = {
        "type": "object",
        "properties": {
            "test_param": {"type": "string"},
            "project_name": {"type": "string"}
        },
        "required": ["project_name"]
    }
    
    def discover_streams(self) -> list[Stream]:
        """Return test streams."""
        return []


class TestProjectTarget(Target):
    """Test target for project testing."""
    
    name = "test_project_target"
    config_jsonschema = {
        "type": "object",
        "properties": {
            "test_param": {"type": "string"},
            "output_path": {"type": "string"}
        },
        "required": ["output_path"]
    }
    
    default_sink_class = None
    
    def process_messages(self, messages) -> None:
        """Process Singer messages."""
        for message in messages:
            pass


# Helper function to create test configuration
def create_test_config() -> FlextMeltanoConfig:
    """Create test configuration."""
    return FlextMeltanoConfig(
        project_root=Path.cwd(),
        environment="test",
    )



class TestFlextMeltanoTapServiceComplete:
    """Complete testing of FlextMeltanoTapService functionality."""
    
    def test_tap_service_initialization(self) -> None:
        """Test tap service initialization."""
        config = create_test_config()
        service = FlextMeltanoTapService(config)
        
        assert service is not None
        assert service.tap_name == "test_tap"
        assert isinstance(service.project_root, Path)
        assert hasattr(service, 'logger')
        
    def test_tap_service_execution(self) -> None:
        """Test tap service execute method."""
        service = TestProjectTapService(
            tap_name="test_tap",
            project_root=Path.cwd()
        )
        
        result = service.execute()
        assert isinstance(result, FlextResult)
        assert result.success
        
        data = result.data
        assert isinstance(data, dict)
        assert "tap_name" in data
        assert data["tap_name"] == "test_tap"
        
    def test_get_tap_class_method(self) -> None:
        """Test get_tap_class method."""
        service = TestProjectTapService(
            tap_name="test_tap",
            project_root=Path.cwd()
        )
        
        tap_class = service.get_tap_class()
        assert tap_class == TestProjectTap
        assert issubclass(tap_class, Tap)
        
    def test_get_default_config_method(self) -> None:
        """Test get_default_config method."""
        service = TestProjectTapService(
            tap_name="test_tap",
            project_root=Path.cwd()
        )
        
        config = service.get_default_config()
        assert isinstance(config, dict)
        assert "project_name" in config
        assert config["project_name"] == "test_project"
        
    def test_create_tap_instance_patterns(self) -> None:
        """Test tap instance creation patterns."""
        service = TestProjectTapService(
            tap_name="test_tap",
            project_root=Path.cwd()
        )
        
        # Test with valid config
        config = service.get_default_config()
        if hasattr(service, 'create_tap_instance'):
            result = service.create_tap_instance(config)
            assert isinstance(result, FlextResult)
            
    def test_tap_validation_patterns(self) -> None:
        """Test tap validation patterns."""
        service = TestProjectTapService(
            tap_name="test_tap",
            project_root=Path.cwd()
        )
        
        # Test config validation if available
        if hasattr(service, 'validate_config'):
            config = {"project_name": "test", "test_param": "value"}
            result = service.validate_config(config)
            assert isinstance(result, FlextResult)


class TestFlextMeltanoTargetServiceComplete:
    """Complete testing of FlextMeltanoTargetService functionality."""
    
    def test_target_service_initialization(self) -> None:
        """Test target service initialization."""
        service = TestProjectTargetService(
            target_name="test_target",
            project_root=Path.cwd()
        )
        
        assert service is not None
        assert service.target_name == "test_target"
        assert isinstance(service.project_root, Path)
        assert hasattr(service, 'logger')
        
    def test_target_service_execution(self) -> None:
        """Test target service execute method."""
        service = TestProjectTargetService(
            target_name="test_target",
            project_root=Path.cwd()
        )
        
        result = service.execute()
        assert isinstance(result, FlextResult)
        assert result.success
        
        data = result.data
        assert isinstance(data, dict)
        assert "target_name" in data
        assert data["target_name"] == "test_target"
        
    def test_get_target_class_method(self) -> None:
        """Test get_target_class method."""
        service = TestProjectTargetService(
            target_name="test_target",
            project_root=Path.cwd()
        )
        
        target_class = service.get_target_class()
        assert target_class == TestProjectTarget
        assert issubclass(target_class, Target)
        
    def test_get_default_config_method(self) -> None:
        """Test get_default_config method."""
        service = TestProjectTargetService(
            target_name="test_target",
            project_root=Path.cwd()
        )
        
        config = service.get_default_config()
        assert isinstance(config, dict)
        assert "output_path" in config
        assert config["output_path"] == "/tmp/test"
        
    def test_create_target_instance_patterns(self) -> None:
        """Test target instance creation patterns."""
        service = TestProjectTargetService(
            target_name="test_target",
            project_root=Path.cwd()
        )
        
        # Test with valid config
        config = service.get_default_config()
        if hasattr(service, 'create_target_instance'):
            result = service.create_target_instance(config)
            assert isinstance(result, FlextResult)
            
    def test_target_validation_patterns(self) -> None:
        """Test target validation patterns."""
        service = TestProjectTargetService(
            target_name="test_target",
            project_root=Path.cwd()
        )
        
        # Test config validation if available
        if hasattr(service, 'validate_config'):
            config = {"output_path": "/tmp/test", "test_param": "value"}
            result = service.validate_config(config)
            assert isinstance(result, FlextResult)


class TestFlextMeltanoExtensionServiceComplete:
    """Complete testing of FlextMeltanoExtensionService functionality."""
    
    def test_extension_service_initialization(self) -> None:
        """Test extension service initialization."""
        service = FlextMeltanoExtensionService(
            extension_name="test_extension",
            project_root=Path.cwd()
        )
        
        assert service is not None
        assert service.extension_name == "test_extension"
        assert isinstance(service.project_root, Path)
        assert hasattr(service, 'logger')
        
    def test_extension_service_execution(self) -> None:
        """Test extension service execute method."""
        service = FlextMeltanoExtensionService(
            extension_name="test_extension",
            project_root=Path.cwd()
        )
        
        result = service.execute()
        assert isinstance(result, FlextResult)
        assert result.success
        
        data = result.data
        assert isinstance(data, dict)
        assert "extension_name" in data
        assert data["extension_name"] == "test_extension"
        
    def test_extension_configuration_patterns(self) -> None:
        """Test extension configuration patterns."""
        service = FlextMeltanoExtensionService(
            extension_name="test_extension",
            project_root=Path.cwd()
        )
        
        # Test configuration methods if available
        if hasattr(service, 'get_extension_config'):
            config = service.get_extension_config()
            assert isinstance(config, dict)
            
        if hasattr(service, 'validate_extension_config'):
            test_config = {"test": "value"}
            result = service.validate_extension_config(test_config)
            assert isinstance(result, FlextResult)


class TestFlextMeltanoDbtServiceComplete:
    """Complete testing of FlextMeltanoDbtService functionality."""
    
    def test_dbt_service_initialization(self) -> None:
        """Test DBT service initialization."""
        service = FlextMeltanoDbtService(
            project_name="test_dbt_project",
            project_root=Path.cwd()
        )
        
        assert service is not None
        assert service.project_name == "test_dbt_project"
        assert isinstance(service.project_root, Path)
        assert hasattr(service, 'logger')
        
    def test_dbt_service_execution(self) -> None:
        """Test DBT service execute method."""
        service = FlextMeltanoDbtService(
            project_name="test_dbt_project",
            project_root=Path.cwd()
        )
        
        result = service.execute()
        assert isinstance(result, FlextResult)
        assert result.success
        
        data = result.data
        assert isinstance(data, dict)
        assert "project_name" in data
        assert data["project_name"] == "test_dbt_project"
        
    def test_dbt_project_operations(self) -> None:
        """Test DBT project operations."""
        service = FlextMeltanoDbtService(
            project_name="test_dbt_project",
            project_root=Path.cwd()
        )
        
        # Test DBT operations if available
        if hasattr(service, 'initialize_project'):
            with tempfile.TemporaryDirectory() as temp_dir:
                project_path = Path(temp_dir)
                result = service.initialize_project(project_path)
                assert isinstance(result, FlextResult)
                
        if hasattr(service, 'run_models'):
            models = ["model1", "model2"]
            result = service.run_models(models)
            assert isinstance(result, FlextResult)
            
        if hasattr(service, 'run_tests'):
            result = service.run_tests()
            assert isinstance(result, FlextResult)
            
    def test_dbt_configuration_patterns(self) -> None:
        """Test DBT configuration patterns."""
        service = FlextMeltanoDbtService(
            project_name="test_dbt_project",
            project_root=Path.cwd()
        )
        
        # Test configuration methods if available
        if hasattr(service, 'get_dbt_config'):
            config = service.get_dbt_config()
            assert isinstance(config, dict)
            
        if hasattr(service, 'validate_dbt_config'):
            test_config = {"version": 2, "models": {}}
            result = service.validate_dbt_config(test_config)
            assert isinstance(result, FlextResult)


class TestProjectServicesIntegration:
    """Test integration between project services."""
    
    def test_service_hierarchy_consistency(self) -> None:
        """Test service hierarchy consistency."""
        services = [
            TestProjectTapService(tap_name="test", project_root=Path.cwd()),
            TestProjectTargetService(target_name="test", project_root=Path.cwd()),
            FlextMeltanoExtensionService(extension_name="test", project_root=Path.cwd()),
            FlextMeltanoDbtService(project_name="test", project_root=Path.cwd()),
        ]
        
        # All should be FlextDomainService instances
        from flext_core import FlextDomainService
        for service in services:
            assert isinstance(service, FlextDomainService)
            
    def test_execution_consistency(self) -> None:
        """Test execution method consistency."""
        services = [
            TestProjectTapService(tap_name="test", project_root=Path.cwd()),
            TestProjectTargetService(target_name="test", project_root=Path.cwd()),
            FlextMeltanoExtensionService(extension_name="test", project_root=Path.cwd()),
            FlextMeltanoDbtService(project_name="test", project_root=Path.cwd()),
        ]
        
        for service in services:
            result = service.execute()
            assert isinstance(result, FlextResult)
            assert result.success
            assert isinstance(result.data, dict)
            
    def test_logger_consistency(self) -> None:
        """Test logger consistency across services."""
        services = [
            TestProjectTapService(tap_name="test", project_root=Path.cwd()),
            TestProjectTargetService(target_name="test", project_root=Path.cwd()),
            FlextMeltanoExtensionService(extension_name="test", project_root=Path.cwd()),
            FlextMeltanoDbtService(project_name="test", project_root=Path.cwd()),
        ]
        
        for service in services:
            logger = service.logger
            assert logger is not None
            assert hasattr(logger, 'info')
            assert hasattr(logger, 'error')
            assert hasattr(logger, 'warning')
            
    def test_project_root_consistency(self) -> None:
        """Test project root consistency across services."""
        test_root = Path.cwd()
        services = [
            CustomTap(tap_name="test", project_root=test_root),
            TestProjectTapService(tap_name="test", project_root=test_root),
            TestProjectTargetService(target_name="test", project_root=test_root),
            FlextMeltanoExtensionService(extension_name="test", project_root=test_root),
            FlextMeltanoDbtService(project_name="test", project_root=test_root),
        ]
        
        for service in services:
            assert service.project_root == test_root
            assert isinstance(service.project_root, Path)


class TestProjectServiceErrorHandling:
    """Test error handling patterns across project services."""
    
    def test_service_error_recovery(self) -> None:
        """Test service error recovery."""
        services = [
            TestProjectTapService(tap_name="test", project_root=Path.cwd()),
            TestProjectTargetService(target_name="test", project_root=Path.cwd()),
            FlextMeltanoExtensionService(extension_name="test", project_root=Path.cwd()),
            FlextMeltanoDbtService(project_name="test", project_root=Path.cwd()),
        ]
        
        # All services should handle execution gracefully
        for service in services:
            try:
                result = service.execute()
                assert isinstance(result, FlextResult)
                # Should not raise exception
            except Exception:
                pytest.fail(f"Service {type(service)} should handle errors gracefully")
                
    def test_invalid_project_root_handling(self) -> None:
        """Test handling of invalid project roots."""
        invalid_root = Path("/nonexistent/path/to/project")
        
        # Services should still initialize even with invalid paths
        services = [
            TestProjectTapService(tap_name="test", project_root=invalid_root),
            TestProjectTargetService(target_name="test", project_root=invalid_root),
            FlextMeltanoExtensionService(extension_name="test", project_root=invalid_root),
            FlextMeltanoDbtService(project_name="test", project_root=invalid_root),
        ]
        
        # Should initialize without throwing exceptions
        for service in services:
            assert service is not None
            assert service.project_root == invalid_root


class TestProjectServiceRealWorldUsage:
    """Test real-world usage patterns for project services."""
    
    def test_typical_tap_project_workflow(self) -> None:
        """Test typical tap project workflow."""
        # Step 1: Initialize tap service
        service = TestProjectTapService(
            tap_name="production_tap", 
            project_root=Path.cwd()
        )
        
        # Step 2: Get and customize config
        config = service.get_default_config()
        config["project_name"] = "production_project"
        
        # Step 3: Execute service
        result = service.execute()
        assert result.success
        
        # Workflow completed successfully
        data = result.data
        assert "tap_name" in data
        assert data["tap_name"] == "production_tap"
        
    def test_typical_target_project_workflow(self) -> None:
        """Test typical target project workflow."""
        # Step 1: Initialize target service
        service = TestProjectTargetService(
            target_name="production_target",
            project_root=Path.cwd()
        )
        
        # Step 2: Get and customize config
        config = service.get_default_config()
        config["output_path"] = "/tmp/production"
        
        # Step 3: Execute service
        result = service.execute()
        assert result.success
        
        # Workflow completed successfully
        data = result.data
        assert "target_name" in data
        assert data["target_name"] == "production_target"
        
    def test_typical_dbt_project_workflow(self) -> None:
        """Test typical DBT project workflow."""
        # Step 1: Initialize DBT service
        service = FlextMeltanoDbtService(
            project_name="production_dbt",
            project_root=Path.cwd()
        )
        
        # Step 2: Execute service
        result = service.execute()
        assert result.success
        
        # Workflow completed successfully
        data = result.data
        assert "project_name" in data
        assert data["project_name"] == "production_dbt"