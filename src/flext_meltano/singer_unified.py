"""FLEXT Meltano Singer Unified Interface - Central Simplification Hub.

ARCHITECTURAL IMPROVEMENT: This module provides a unified interface that simplifies
the implementation of flext-tap-*, flext-target-*, and flext-singer-* projects.

As requested, this makes flext-meltano the central simplification point for all
Singer/Meltano operations across the FLEXT ecosystem without taking over the
responsibilities of individual projects.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union

from flext_core import FlextDomainService, FlextEntity, FlextResult, FlextValueObject
from singer_sdk import Stream, Tap, Target

from flext_meltano.singer_base import (
    FlextSingerError,
    FlextTapError,
    FlextTargetError,
)

if TYPE_CHECKING:
    from pathlib import Path


class FlextSingerUnifiedConfig:
    """Unified configuration for all Singer operations - eliminates duplication.
    
    SOLID SRP: Single configuration object supporting taps, targets, and transforms.
    This eliminates the need for separate config classes in each Singer project.  
    """
    
    def __init__(
        self,
        name: str,
        config: Dict[str, Any],
        catalog: Optional[Dict[str, Any]] = None,
        state: Optional[Dict[str, Any]] = None,
        environment: str = "dev",
        **extra_config: Any,
    ) -> None:
        """Initialize unified Singer configuration.
        
        Args:
            name: Singer plugin name (tap-oracle, target-csv, etc.)
            config: Plugin-specific configuration
            catalog: Singer catalog for schema definition
            state: Singer state for incremental processing
            environment: Execution environment
            **extra_config: Additional configuration options
        """
        self.name = name
        self.config = config
        self.catalog = catalog or {}
        self.state = state or {}
        self.environment = environment
        self.extra_config = extra_config
    
    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate unified Singer configuration domain rules.
        
        Returns:
            FlextResult indicating validation success/failure
        """
        if not self.name or not isinstance(self.name, str):
            return FlextResult.fail("Singer plugin name must be a non-empty string")
            
        if not self.config or not isinstance(self.config, dict):
            return FlextResult.fail("Singer config must be a non-empty dictionary")
            
        if not isinstance(self.catalog, dict):
            return FlextResult.fail("Singer catalog must be a dictionary")
            
        if not isinstance(self.state, dict):
            return FlextResult.fail("Singer state must be a dictionary")
            
        return FlextResult.ok(None)


class FlextSingerUnifiedResult:
    """Unified result object for all Singer operations - consistent interface.
    
    SOLID ISP: Interface segregation with optional result components.
    This provides a consistent result interface across all Singer operations.
    """
    
    def __init__(
        self,
        success: bool,
        records_processed: int = 0,
        schemas_discovered: Optional[List[str]] = None,
        state_updates: Optional[Dict[str, Any]] = None,
        catalog_updates: Optional[Dict[str, Any]] = None,
        execution_time_ms: float = 0.0,
        error_message: Optional[str] = None,
        **metrics: Any,
    ) -> None:
        """Initialize unified Singer result.
        
        Args:
            success: Whether the operation succeeded
            records_processed: Number of records processed
            schemas_discovered: List of discovered schema names
            state_updates: Singer state updates
            catalog_updates: Catalog modifications
            execution_time_ms: Execution time in milliseconds
            error_message: Error message if operation failed
            **metrics: Additional operation metrics
        """
        self.success = success
        self.records_processed = records_processed
        self.schemas_discovered = schemas_discovered or []
        self.state_updates = state_updates or {}
        self.catalog_updates = catalog_updates or {}
        self.execution_time_ms = execution_time_ms
        self.error_message = error_message
        self.metrics = metrics
    
    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate unified Singer result domain rules.
        
        Returns:
            FlextResult indicating validation success/failure
        """
        if not isinstance(self.success, bool):
            return FlextResult.fail("Success flag must be a boolean")
            
        if not isinstance(self.records_processed, int) or self.records_processed < 0:
            return FlextResult.fail("Records processed must be a non-negative integer")
            
        if not isinstance(self.execution_time_ms, (int, float)) or self.execution_time_ms < 0:
            return FlextResult.fail("Execution time must be a non-negative number")
            
        return FlextResult.ok(None)


class FlextSingerUnifiedInterface(ABC):
    """Abstract interface for unified Singer operations - foundation for all projects.
    
    SOLID DIP: Dependency inversion principle providing abstract interface
    that all Singer projects can implement without tight coupling to flext-meltano.
    
    This interface supports taps, targets, and transforms in a unified way.
    """
    
    @abstractmethod
    def initialize(self, config: FlextSingerUnifiedConfig) -> FlextResult[None]:
        """Initialize the Singer component with unified configuration.
        
        Args:
            config: Unified configuration object
            
        Returns:
            FlextResult indicating initialization success/failure
        """
        
    @abstractmethod
    def discover_catalog(self) -> FlextResult[Dict[str, Any]]:
        """Discover available schemas and generate Singer catalog.
        
        Returns:
            FlextResult containing Singer catalog or error
        """
        
    @abstractmethod
    def execute(
        self, 
        input_data: Optional[Any] = None
    ) -> FlextResult[FlextSingerUnifiedResult]:
        """Execute the Singer operation (extract, load, transform).
        
        Args:
            input_data: Optional input data for the operation
            
        Returns:
            FlextResult containing unified operation result
        """
        
    @abstractmethod
    def validate_configuration(self) -> FlextResult[None]:
        """Validate the current configuration.
        
        Returns:
            FlextResult indicating validation success/failure
        """


class FlextSingerUnifiedService(FlextDomainService):
    """Unified service orchestrating all Singer operations - central orchestration.
    
    SOLID SRP: Single responsibility for orchestrating Singer operations
    across taps, targets, and transforms. This is the main entry point that
    Singer projects use to leverage flext-meltano functionality.
    """
    
    def __init__(self) -> None:
        """Initialize the unified Singer service."""
        super().__init__()
        self._registered_components: Dict[str, FlextSingerUnifiedInterface] = {}
    
    def execute(self, *args: Any, **kwargs: Any) -> FlextResult[Any]:
        """Execute unified Singer service operations.
        
        SOLID SRP: Single entry point for all Singer service operations.
        Delegates to specific methods based on operation type.
        
        Args:
            *args: Operation arguments (first arg should be operation name)
            **kwargs: Operation parameters
            
        Returns:
            FlextResult with operation result
        """
        if not args:
            return FlextResult.fail("Operation name required as first argument")
            
        operation = args[0]
        
        if operation == "execute_pipeline":
            return self._execute_pipeline_operation(kwargs)
        elif operation == "discover_catalogs": 
            return self.discover_all_catalogs()
        elif operation == "validate_components":
            return self.validate_all_components()
        else:
            return FlextResult.fail(f"Unknown operation: {operation}")
    
    def _execute_pipeline_operation(self, kwargs: Dict[str, Any]) -> FlextResult[Any]:
        """Execute pipeline operation from service execute method.
        
        Args:
            kwargs: Pipeline parameters
            
        Returns:
            FlextResult with pipeline execution result
        """
        required_params = ["tap_name", "target_name", "tap_config", "target_config"]
        for param in required_params:
            if param not in kwargs:
                return FlextResult.fail(f"Missing required parameter: {param}")
        
        return self.execute_pipeline(
            tap_name=kwargs["tap_name"],
            target_name=kwargs["target_name"],
            tap_config=kwargs["tap_config"],
            target_config=kwargs["target_config"],
            catalog=kwargs.get("catalog"),
            state=kwargs.get("state"),
        )
        
    def register_component(
        self, 
        name: str, 
        component: FlextSingerUnifiedInterface
    ) -> FlextResult[None]:
        """Register a Singer component (tap, target, transform) with the service.
        
        SOLID OCP: Open/closed principle - service is open for extension
        by registering new components without modifying existing code.
        
        Args:
            name: Unique component name
            component: Singer component implementing unified interface
            
        Returns:
            FlextResult indicating registration success/failure
        """
        try:
            if name in self._registered_components:
                return FlextResult.fail(f"Component '{name}' is already registered")
                
            self._registered_components[name] = component
            return FlextResult.ok(None)
            
        except Exception as e:
            return FlextResult.fail(f"Failed to register component '{name}': {e}")
    
    def get_component(self, name: str) -> FlextResult[FlextSingerUnifiedInterface]:
        """Get a registered Singer component by name.
        
        Args:
            name: Component name
            
        Returns:
            FlextResult containing the component or error
        """
        try:
            if name not in self._registered_components:
                return FlextResult.fail(f"Component '{name}' is not registered")
                
            return FlextResult.ok(self._registered_components[name])
            
        except Exception as e:
            return FlextResult.fail(f"Failed to get component '{name}': {e}")
    
    def execute_pipeline(
        self,
        tap_name: str,
        target_name: str,
        tap_config: Dict[str, Any],
        target_config: Dict[str, Any],
        catalog: Optional[Dict[str, Any]] = None,
        state: Optional[Dict[str, Any]] = None,
    ) -> FlextResult[FlextSingerUnifiedResult]:
        """Execute a complete Singer pipeline (tap -> target).
        
        SOLID SRP: Single responsibility for end-to-end pipeline execution.
        This orchestrates the complete flow without implementing tap/target logic.
        
        Args:
            tap_name: Name of registered tap component
            target_name: Name of registered target component  
            tap_config: Tap configuration
            target_config: Target configuration
            catalog: Optional Singer catalog
            state: Optional Singer state
            
        Returns:
            FlextResult containing pipeline execution result
        """
        try:
            # Get components
            tap_result = self.get_component(tap_name)
            if tap_result.is_failure:
                return FlextResult.fail(f"Tap error: {tap_result.error}")
                
            target_result = self.get_component(target_name)
            if target_result.is_failure:
                return FlextResult.fail(f"Target error: {target_result.error}")
                
            tap = tap_result.data
            target = target_result.data
            
            # Initialize components
            tap_unified_config = FlextSingerUnifiedConfig(
                name=tap_name,
                config=tap_config,
                catalog=catalog,
                state=state,
            )
            
            target_unified_config = FlextSingerUnifiedConfig(
                name=target_name,
                config=target_config,
                catalog=catalog,
            )
            
            # Initialize tap
            tap_init_result = tap.initialize(tap_unified_config)
            if tap_init_result.is_failure:
                return FlextResult.fail(f"Tap initialization failed: {tap_init_result.error}")
                
            # Initialize target
            target_init_result = target.initialize(target_unified_config)
            if target_init_result.is_failure:
                return FlextResult.fail(f"Target initialization failed: {target_init_result.error}")
            
            # Execute pipeline
            # 1. Extract data from tap
            extract_result = tap.execute()
            if extract_result.is_failure:
                return FlextResult.fail(f"Extract failed: {extract_result.error}")
                
            # 2. Load data to target (using extracted data)
            load_result = target.execute(extract_result.data)
            if load_result.is_failure:
                return FlextResult.fail(f"Load failed: {load_result.error}")
            
            # 3. Combine results
            combined_result = FlextSingerUnifiedResult(
                success=True,
                records_processed=extract_result.data.records_processed,
                schemas_discovered=extract_result.data.schemas_discovered,
                state_updates=extract_result.data.state_updates,
                execution_time_ms=extract_result.data.execution_time_ms + load_result.data.execution_time_ms,
            )
            
            return FlextResult.ok(combined_result)
            
        except Exception as e:
            return FlextResult.fail(f"Pipeline execution failed: {e}")
    
    def discover_all_catalogs(self) -> FlextResult[Dict[str, Dict[str, Any]]]:
        """Discover catalogs from all registered components.
        
        Returns:
            FlextResult containing dictionary of component catalogs
        """
        try:
            catalogs = {}
            
            for name, component in self._registered_components.items():
                catalog_result = component.discover_catalog()
                if catalog_result.is_success:
                    catalogs[name] = catalog_result.data
                    
            return FlextResult.ok(catalogs)
            
        except Exception as e:
            return FlextResult.fail(f"Catalog discovery failed: {e}")
    
    def validate_all_components(self) -> FlextResult[Dict[str, bool]]:
        """Validate configuration of all registered components.
        
        Returns:
            FlextResult containing validation status for each component
        """
        try:
            validation_results = {}
            
            for name, component in self._registered_components.items():
                validation_result = component.validate_configuration()
                validation_results[name] = validation_result.is_success
                
            return FlextResult.ok(validation_results)
            
        except Exception as e:
            return FlextResult.fail(f"Component validation failed: {e}")


# Factory functions for easy instantiation

def create_unified_singer_service() -> FlextSingerUnifiedService:
    """Factory function to create unified Singer service.
    
    Returns:
        Configured FlextSingerUnifiedService instance
    """
    return FlextSingerUnifiedService()


def create_unified_singer_config(
    name: str,
    config: Dict[str, Any],
    **kwargs: Any,
) -> FlextSingerUnifiedConfig:
    """Factory function to create unified Singer configuration.
    
    Args:
        name: Singer plugin name
        config: Plugin configuration
        **kwargs: Additional configuration options
        
    Returns:
        Configured FlextSingerUnifiedConfig instance
    """
    return FlextSingerUnifiedConfig(name=name, config=config, **kwargs)


__all__ = [
    "FlextSingerUnifiedConfig",
    "FlextSingerUnifiedResult", 
    "FlextSingerUnifiedInterface",
    "FlextSingerUnifiedService",
    "create_unified_singer_service",
    "create_unified_singer_config",
]