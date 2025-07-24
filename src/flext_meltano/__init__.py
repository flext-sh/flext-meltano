"""FLEXT Meltano - Unified Data Integration Platform.

Modern enterprise-grade library that unifies:
- Meltano (data integration orchestration)
- Singer SDK (tap/target development)
- dbt (data transformation)
- Meltano EDK (extension development)
- FlexCore Go runtime integration

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

# Core FlextCore patterns (PRIORIDADE 2: using root namespace)
from flext_core import FlextConstants, FlextContainer, FlextResult

# Application services (import from main services.py file)
from flext_meltano.application.services import (
    FlextMeltanoJobService,
    FlextMeltanoPluginService,
    FlextMeltanoProjectService,
    FlextMeltanoStateService,
)
from flext_meltano.config.loader import FlextMeltanoConfigLoader

# Configuration and settings
from flext_meltano.config.settings import FlextMeltanoSettings

# Core executor and config - FlextMeltanoConfig and FlextMeltanoExecutor removed (unused)
# Unified Meltano platform classes
from flext_meltano.core.platform import FlextMeltanoPlatform
from flext_meltano.core.runtime import FlextMeltanoRuntime
from flext_meltano.dbt.models import FlextMeltanoDbtModel

# dbt integration
from flext_meltano.dbt.project import FlextMeltanoDbtProject
from flext_meltano.dbt.runner import FlextMeltanoDbtRunner

# Meltano EDK integration
from flext_meltano.edk.extension import FlextMeltanoExtension
from flext_meltano.edk.manager import FlextMeltanoExtensionManager
from flext_meltano.environment.manager import FlextMeltanoEnvironmentManager
from flext_meltano.environment.models import FlextMeltanoEnvironment
from flext_meltano.extensions import (
    FlextMeltanoExtensionCommand,
    FlextMeltanoExtensionConfig,
    FlextMeltanoExtensionDiscovery,
    FlextMeltanoExtensionResult,
    FlextMeltanoExtensionStatus,
    FlextMeltanoExtensionType,
)

# Helpers and utilities
from flext_meltano.helpers.cli import flext_meltano_run_command
from flext_meltano.helpers.config import flext_meltano_load_config
from flext_meltano.helpers.discovery import flext_meltano_discover_plugins
from flext_meltano.helpers.execution import flext_meltano_execute_job
from flext_meltano.helpers.installation import flext_meltano_install_plugin
from flext_meltano.helpers.validation import flext_meltano_validate_project
from flext_meltano.jobs.executor import FlextMeltanoJobExecutor

# Job and execution management
from flext_meltano.jobs.manager import FlextMeltanoJobManager
from flext_meltano.jobs.models import FlextMeltanoJob

# Orchestrator classes and enums (with aliases to avoid conflicts)
from flext_meltano.orchestrator import (
    FlextMeltanoEngine,
    FlextMeltanoJob as FlextMeltanoOrchestratorJob,
    FlextMeltanoJobProtocol,
    FlextMeltanoLocalExecutionStatus,
    FlextMeltanoOrchestrationMode,
    FlextMeltanoOrchestrator,
    FlextMeltanoPayload,
    FlextMeltanoPayloadProtocol,
    FlextMeltanoProject as FlextMeltanoOrchestratorProject,
    FlextMeltanoProjectProtocol,
    FlextMeltanoRunMode,
    FlextMeltanoState as FlextMeltanoOrchestratorState,
    FlextMeltanoStateProtocol,
)

# Plugin management
from flext_meltano.plugins.manager import FlextMeltanoPluginManager
from flext_meltano.plugins.models import FlextMeltanoPlugin

# Project and environment management
# Enhanced project manager - now using main implementation
from flext_meltano.project.manager import (
    FlextMeltanoProjectManager,
    FlextMeltanoProjectManager as FlextMeltanoProjectManagerCore,
)
from flext_meltano.project.models import FlextMeltanoProject

# Reflection orchestrator
from flext_meltano.reflection_orchestrator import (
    FlextMeltanoReflectionOrchestrator,
    FlextMeltanoReflectionStep,
)

# Simple API helpers - flext_create_basic_config removed (unused)
from flext_meltano.singer.catalog import FlextMeltanoCatalog
from flext_meltano.singer.stream import FlextMeltanoStream

# Singer SDK integration
from flext_meltano.singer.tap import FlextMeltanoTap
from flext_meltano.singer.target import FlextMeltanoTarget

# Singer direct integration
from flext_meltano.singer_direct import FlextMeltanoSingerDirectRunner

# State management
from flext_meltano.state.manager import FlextMeltanoStateManager
from flext_meltano.state.models import FlextMeltanoState

# Anti-corruption layer
from flext_meltano.unified_anti_corruption_layer import (
    FlextMeltanoUnifiedAntiCorruptionLayer,
)

# Service aliases for backward compatibility
MeltanoJobService = FlextMeltanoJobService
MeltanoPluginService = FlextMeltanoPluginService
MeltanoProjectService = FlextMeltanoProjectService
MeltanoStateService = FlextMeltanoStateService

# Anti-corruption layer aliases
UnifiedMeltanoAntiCorruptionLayer = FlextMeltanoUnifiedAntiCorruptionLayer

# Short aliases for convenience
JobService = FlextMeltanoJobService
PluginService = FlextMeltanoPluginService
ProjectService = FlextMeltanoProjectService
StateService = FlextMeltanoStateService

# Manager aliases for backward compatibility
MeltanoProjectManager = FlextMeltanoProjectManager
MeltanoJobManager = FlextMeltanoJobManager
MeltanoPluginManager = FlextMeltanoPluginManager
MeltanoStateManager = FlextMeltanoStateManager
# MeltanoExtensionManager already imported from flext_meltano.extensions (line 59)

__version__ = "0.7.0"


# Main platform instance factory
def create_flext_meltano_platform(
    config: dict[str, object] | None = None,
) -> FlextMeltanoPlatform:
    """Create unified FLEXT Meltano platform instance.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured FlextMeltanoPlatform instance

    """
    return FlextMeltanoPlatform(config or {})


__all__ = [
    # FlextCore patterns
    "FlextConstants",
    "FlextContainer",
    "FlextMeltanoCatalog",
    "FlextMeltanoConfigLoader",
    "FlextMeltanoDbtModel",
    # dbt integration
    "FlextMeltanoDbtProject",
    "FlextMeltanoDbtRunner",
    # Orchestrator classes
    "FlextMeltanoEngine",
    # Environment management
    "FlextMeltanoEnvironment",
    "FlextMeltanoEnvironmentManager",
    # Extensions (FLEXT Meltano EDK)
    "FlextMeltanoExtension",
    "FlextMeltanoExtensionCommand",
    "FlextMeltanoExtensionConfig",
    "FlextMeltanoExtensionDiscovery",
    "FlextMeltanoExtensionManager",
    "FlextMeltanoExtensionResult",
    "FlextMeltanoExtensionStatus",
    "FlextMeltanoExtensionType",
    # Job management
    "FlextMeltanoJob",
    "FlextMeltanoJobExecutor",
    "FlextMeltanoJobManager",
    "FlextMeltanoJobProtocol",
    "FlextMeltanoLocalExecutionStatus",
    "FlextMeltanoOrchestrationMode",
    "FlextMeltanoOrchestrator",
    "FlextMeltanoOrchestratorJob",
    "FlextMeltanoOrchestratorProject",
    "FlextMeltanoOrchestratorState",
    "FlextMeltanoPayload",
    "FlextMeltanoPayloadProtocol",
    # Core platform
    "FlextMeltanoPlatform",
    # Plugin management
    "FlextMeltanoPlugin",
    "FlextMeltanoPluginManager",
    # Project management
    "FlextMeltanoProject",
    "FlextMeltanoProjectManager",
    "FlextMeltanoProjectManagerCore",
    "FlextMeltanoProjectProtocol",
    # Reflection orchestrator
    "FlextMeltanoReflectionOrchestrator",
    "FlextMeltanoReflectionStep",
    "FlextMeltanoRunMode",
    "FlextMeltanoRuntime",
    # Configuration
    "FlextMeltanoSettings",
    # Singer direct integration
    "FlextMeltanoSingerDirectRunner",
    # State management
    "FlextMeltanoState",
    "FlextMeltanoStateManager",
    "FlextMeltanoStateProtocol",
    "FlextMeltanoStream",
    # Singer SDK
    "FlextMeltanoTap",
    "FlextMeltanoTarget",
    "FlextMeltanoUnifiedAntiCorruptionLayer",
    "FlextResult",
    # Service aliases
    "JobService",
    "MeltanoExtension",
    "MeltanoExtensionManager",
    "MeltanoJobManager",
    "MeltanoJobService",
    "MeltanoPluginManager",
    "MeltanoPluginService",
    "MeltanoProjectManager",
    "MeltanoProjectService",
    "MeltanoStateManager",
    "MeltanoStateService",
    "PluginService",
    "ProjectService",
    "StateService",
    "UnifiedMeltanoAntiCorruptionLayer",
    # Metadata
    "__version__",
    "create_flext_meltano_platform",
    "flext_meltano_discover_plugins",
    "flext_meltano_execute_job",
    "flext_meltano_install_plugin",
    "flext_meltano_load_config",
    # Helpers
    "flext_meltano_run_command",
    "flext_meltano_validate_project",
]
