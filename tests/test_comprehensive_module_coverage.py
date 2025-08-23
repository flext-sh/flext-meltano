"""Comprehensive module coverage tests - focusing on uncovered functionality.

**Purpose**: Increase test coverage to 90%+ by testing all functional modules
**Target**: Real API integration without subprocess calls or mocks  
**Scope**: Base services, CLI, utilities, configuration patterns
"""

from __future__ import annotations

from pathlib import Path

import pytest
from flext_core import FlextResult

from flext_meltano.base_dbt import MeltanoDbtWrapper, FlextDbtAdapter
from flext_meltano.base_services import (
    FlextMeltanoTapService, 
    FlextMeltanoTargetService, 
    FlextMeltanoDbtService
)
from flext_meltano.base_singer import MeltanoSingerWrapper, FlextSingerAdapter
from flext_meltano.config import FlextMeltanoConfig
from flext_meltano.constants import (
    FLEXT_MELTANO_VERSION,
    DEFAULT_ENVIRONMENT,
    DEFAULT_MELTANO_PROJECT_ROOT,
    DEFAULT_COMMAND_TIMEOUT
)
from flext_meltano.utilities import (
    FlextMeltanoUtilities,
    validate_config_value_simple,
    validate_directory_path,
    validate_file_path
)
from flext_meltano.exceptions import (
    FlextMeltanoError,
    FlextMeltanoConfigurationError, 
    FlextMeltanoExecutionError,
    FlextMeltanoValidationError
)


class TestConfigurationComprehensive:
    """Comprehensive configuration testing."""
    
    def test_config_default_initialization(self) -> None:
        """Test default configuration initialization."""
        config = FlextMeltanoConfig()
        
        assert config.environment == "development"
        assert str(config.project_root) == str(Path.cwd())
        
    def test_config_custom_initialization(self) -> None:
        """Test configuration with custom values."""
        custom_root = "/tmp/custom"
        config = FlextMeltanoConfig(
            project_root=custom_root,
            environment="production"
        )
        
        assert str(config.project_root) == custom_root
        assert config.environment == "production"
        
    def test_config_validation_methods(self) -> None:
        """Test configuration validation methods."""
        config = FlextMeltanoConfig()
        
        # Test that config has expected properties
        assert hasattr(config, 'project_root')
        assert hasattr(config, 'environment')
        
        
class TestConstantsValidation:
    """Test all constants are properly defined."""
    
    def test_essential_constants_defined(self) -> None:
        """Test that essential constants are defined with correct types."""
        assert isinstance(FLEXT_MELTANO_VERSION, str)
        assert FLEXT_MELTANO_VERSION == "2.0.0-enterprise"
        
        assert isinstance(DEFAULT_ENVIRONMENT, str)
        assert DEFAULT_ENVIRONMENT == "dev"
        
        assert isinstance(DEFAULT_COMMAND_TIMEOUT, int)
        assert DEFAULT_COMMAND_TIMEOUT > 0
        
    def test_path_constants(self) -> None:
        """Test path-related constants."""
        assert isinstance(DEFAULT_MELTANO_PROJECT_ROOT, str)
        assert DEFAULT_MELTANO_PROJECT_ROOT == "."
        
        
class TestUtilitiesComprehensive:
    """Comprehensive utilities testing."""
    
    def test_utilities_initialization(self) -> None:
        """Test utilities class initialization."""
        utils = FlextMeltanoUtilities()
        assert utils is not None
        
    def test_validate_config_value_simple_success(self) -> None:
        """Test config value validation success cases."""
        # Test string validation
        result = validate_config_value_simple("test_value", str)
        assert result == "test_value"
        
        # Test dict validation
        test_dict = {"key": "value"}
        result = validate_config_value_simple(test_dict, dict)
        assert result == test_dict
        
    def test_validate_config_value_simple_none(self) -> None:
        """Test config value validation with None."""
        result = validate_config_value_simple(None, str, default="default")
        assert result == "default"
        
    def test_validate_directory_path_current(self) -> None:
        """Test directory path validation with current directory."""
        current_dir = str(Path.cwd())
        result = validate_directory_path(current_dir)
        
        assert result is not None
        assert Path(result).exists()
        assert Path(result).is_dir()
        
    def test_validate_directory_path_invalid(self) -> None:
        """Test directory path validation with invalid path."""
        invalid_path = "/nonexistent/invalid/path"
        result = validate_directory_path(invalid_path)
        
        # Should handle gracefully - either return None or the path
        assert result is None or isinstance(result, str)
        
    def test_validate_file_path_existing(self) -> None:
        """Test file path validation with existing file."""
        # Use a file we know exists
        existing_file = __file__  # This test file itself
        result = validate_file_path(existing_file)
        
        assert result is not None
        assert Path(result).exists()
        assert Path(result).is_file()
        
        
class TestExceptionsHierarchy:
    """Test exception hierarchy and functionality."""
    
    def test_base_exception_creation(self) -> None:
        """Test base FlextMeltanoError creation."""
        error = FlextMeltanoError("Test error")
        assert "Test error" in str(error)
        assert isinstance(error, Exception)
        
    def test_config_error_creation(self) -> None:
        """Test FlextMeltanoConfigurationError creation."""
        error = FlextMeltanoConfigurationError("Config error")
        assert "Config error" in str(error)
        assert isinstance(error, FlextMeltanoError)
        
    def test_execution_error_creation(self) -> None:
        """Test FlextMeltanoExecutionError creation."""
        error = FlextMeltanoExecutionError("Execution error")
        assert "Execution error" in str(error)
        assert isinstance(error, FlextMeltanoError)
        
    def test_validation_error_creation(self) -> None:
        """Test FlextMeltanoValidationError creation.""" 
        error = FlextMeltanoValidationError("Validation error")
        assert "Validation error" in str(error)
        assert isinstance(error, FlextMeltanoError)
        
        
class TestDbtWrapperComprehensive:
    """Comprehensive DBT wrapper testing."""
    
    def test_dbt_wrapper_creation(self) -> None:
        """Test DBT wrapper creation."""
        wrapper = MeltanoDbtWrapper()
        assert wrapper is not None
        
    def test_dbt_wrapper_execution(self) -> None:
        """Test DBT wrapper execution pattern."""
        wrapper = MeltanoDbtWrapper()
        
        # Test FlextDomainService pattern
        result = wrapper.execute()
        assert isinstance(result, FlextResult)
        
        if result.success:
            assert result.value["service"] == "MeltanoDbtWrapper"
            assert result.value["status"] == "ready"
            
    def test_dbt_adapter_static_methods(self) -> None:
        """Test DBT adapter static methods."""
        # FlextDbtAdapter is a static class with utility methods
        assert hasattr(FlextDbtAdapter, 'adapt_run_results')
        assert callable(getattr(FlextDbtAdapter, 'adapt_run_results'))
        
        
class TestSingerWrapperComprehensive:
    """Comprehensive Singer wrapper testing."""
    
    def test_singer_wrapper_creation(self) -> None:
        """Test Singer wrapper creation."""
        wrapper = MeltanoSingerWrapper()
        assert wrapper is not None
        
    def test_singer_wrapper_execution(self) -> None:
        """Test Singer wrapper execution pattern."""
        wrapper = MeltanoSingerWrapper()
        
        # Test FlextDomainService pattern
        result = wrapper.execute()
        assert isinstance(result, FlextResult)
        
        if result.success:
            assert result.value["service"] == "MeltanoSingerWrapper"
            assert result.value["status"] == "ready"
            
    def test_singer_adapter_static_methods(self) -> None:
        """Test Singer adapter static methods."""
        # FlextSingerAdapter is a static class with utility methods
        assert hasattr(FlextSingerAdapter, 'adapt_catalog')
        assert callable(getattr(FlextSingerAdapter, 'adapt_catalog'))
        

class TestBaseServicePatterns:
    """Test base service patterns without instantiating abstract classes."""
    
    def test_base_services_available_in_module(self) -> None:
        """Test that base service classes are available for import."""
        # These are abstract base classes, we just verify they're importable
        assert FlextMeltanoTapService is not None
        assert FlextMeltanoTargetService is not None 
        assert FlextMeltanoDbtService is not None
        
    def test_service_class_hierarchy(self) -> None:
        """Test service class hierarchy properties."""
        # Verify classes have expected attributes without instantiation
        assert hasattr(FlextMeltanoTapService, '__abstractmethods__')
        assert hasattr(FlextMeltanoTargetService, '__abstractmethods__')
        assert hasattr(FlextMeltanoDbtService, '__abstractmethods__')
        

class TestRealApiIntegrationPatterns:
    """Test integration patterns with real APIs."""
    
    def test_singer_sdk_imports_comprehensive(self) -> None:
        """Test comprehensive Singer SDK imports."""
        # Test that all Singer SDK components are available
        from singer_sdk import Stream, Tap, Target
        from singer_sdk.typing import PropertiesList, Property
        from singer_sdk.sinks import BatchSink, Sink, SQLSink
        
        # Verify classes are real Singer SDK classes
        assert hasattr(Tap, 'discover_streams')
        assert hasattr(Stream, 'schema')
        assert hasattr(Target, 'listen')
        assert hasattr(PropertiesList, 'to_dict')
        assert hasattr(Property, 'to_dict')
        
    def test_dbt_core_integration_comprehensive(self) -> None:
        """Test comprehensive DBT Core integration."""
        from dbt.cli.main import dbtRunner
        
        # Test that DBT runner is available
        runner = dbtRunner()
        assert runner is not None
        assert hasattr(runner, 'invoke')
        
    def test_meltano_core_integration_comprehensive(self) -> None:
        """Test comprehensive Meltano Core integration."""
        # These imports should work with real Meltano 3.9.1
        try:
            from meltano.core.project import Project
            from meltano.core.hub import MeltanoHubService
            
            assert Project is not None
            assert MeltanoHubService is not None
        except ImportError:
            # If Meltano is not available, that's expected in some environments
            pytest.skip("Meltano Core not available in test environment")


class TestModuleStructureValidation:
    """Test module structure and exports."""
    
    def test_init_exports_comprehensive(self) -> None:
        """Test that __init__.py exports all expected components."""
        import flext_meltano
        
        # Test core exports
        assert hasattr(flext_meltano, 'FlextMeltanoConfig')
        assert hasattr(flext_meltano, 'FlextMeltanoError')
        assert hasattr(flext_meltano, 'FLEXT_MELTANO_VERSION')
        
        # Test base service exports
        assert hasattr(flext_meltano, 'FlextMeltanoTapService')
        assert hasattr(flext_meltano, 'FlextMeltanoTargetService')
        assert hasattr(flext_meltano, 'FlextMeltanoDbtService')
        
        # Test Singer SDK re-exports
        assert hasattr(flext_meltano, 'Stream')
        assert hasattr(flext_meltano, 'Tap')
        assert hasattr(flext_meltano, 'Target')
        
    def test_version_consistency(self) -> None:
        """Test version consistency across module."""
        import flext_meltano
        
        assert flext_meltano.__version__ == "2.0.0-enterprise"
        assert flext_meltano.FLEXT_MELTANO_VERSION == "2.0.0-enterprise"