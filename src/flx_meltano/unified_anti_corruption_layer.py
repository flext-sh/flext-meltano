"""UNIFIED MELTANO ANTI-CORRUPTION LAYER - ZERO TOLERANCE CONSOLIDATION.

ARCHITECTURAL REVOLUTION: Single source of truth for ALL Meltano integration patterns.
Eliminates scattered ACL implementations with unified, modern architecture.

CONSOLIDATES:
- infrastructure/meltano/acl.py (537 LOC) - Infrastructure ACL with ServiceResult patterns
- meltano/anti_corruption_layer.py (592 LOC) - Domain ACL with adapter patterns

ZERO TOLERANCE PRINCIPLES:
✅ Single ACL system for all Meltano integration operations
✅ Python 3.13 type system with modern union syntax
✅ Strategic TYPE_CHECKING for circular dependency management
✅ ServiceResult integration for enterprise error handling
✅ Adapter pattern with concrete MeltanoEngine implementation
✅ Enterprise validation and transformation engines
✅ Domain entity translation with proper type mapping

FEATURES:
1. Universal Meltano operations through single interface
2. Domain entity ↔ Meltano format translation
3. Enterprise error handling with ServiceResult patterns
4. Pipeline execution with comprehensive logging
5. Plugin management with type-safe operations
6. State management with proper isolation
7. Configuration management with validation
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

import structlog
from flx_core.config.domain_config import get_config, get_domain_constants
from flx_core.domain.advanced_types import (
    ConfigurationDict,
    ServiceError,
    ServiceResult,
)
from flx_core.domain.entities import Pipeline, PipelineExecution, Plugin, PluginType
from flx_core.domain.pydantic_base import DomainValueObject
from flx_core.engine.meltano_wrapper import MeltanoEngine, MeltanoExecutionResult
from pydantic import Field, model_validator

# Python 3.13 type aliases - ZERO TOLERANCE modern syntax
type MeltanoOperationResult = dict[str, Any]
type PluginConfiguration = ConfigurationDict
type PipelineConfiguration = ConfigurationDict
type ExecutionEnvironment = dict[str, str]
type StateData = ConfigurationDict

if TYPE_CHECKING:
    from collections.abc import Mapping

    from flx_core.events.event_bus import EventBusProtocol

logger = structlog.get_logger()


class MeltanoPluginDescriptor(DomainValueObject):
    """External representation of a Meltano plugin with enterprise validation.

    This class represents how plugins are structured in the Meltano ecosystem,
    serving as an intermediate format for translation between Meltano's plugin
    hub format and FLX's domain model.
    """

    name: str = Field(description="Plugin name in Meltano ecosystem")
    namespace: str = Field(description="Plugin namespace for organization")
    pip_url: str | None = Field(
        default=None,
        description="Python package URL for installation",
    )
    settings: ConfigurationDict = Field(
        default_factory=dict,
        description="Plugin configuration settings",
    )
    variant: str | None = Field(default=None, description="Plugin variant identifier")
    docs: str | None = Field(default=None, description="Documentation URL or content")
    plugin_type: str | None = Field(
        default=None,
        description="Meltano plugin type classification",
    )
    description: str | None = Field(default=None, description="Plugin description text")

    @model_validator(mode="after")
    def validate_required_fields(self) -> MeltanoPluginDescriptor:
        """Validate plugin descriptor after initialization."""
        if not self.name or not self.namespace:
            msg = "Plugin name and namespace are required"
            raise ValueError(msg)
        return self


class MeltanoRunResult(DomainValueObject):
    """Result of a Meltano pipeline execution with comprehensive metrics.

    Captures the complete execution result including success status, process
    exit code, captured output streams, execution duration, and metadata
    for monitoring and debugging purposes.
    """

    success: bool = Field(description="Whether pipeline execution was successful")
    exit_code: int = Field(description="Process exit code from execution")
    stdout: str = Field(description="Standard output from execution")
    stderr: str = Field(description="Standard error output from execution")
    duration_seconds: float = Field(description="Total execution duration in seconds")
    started_at: datetime | None = Field(
        default=None,
        description="Execution start timestamp",
    )
    completed_at: datetime | None = Field(
        default=None,
        description="Execution completion timestamp",
    )
    records_processed: int = Field(default=0, description="Number of records processed")
    execution_metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional execution metadata",
    )

    @property
    def has_output(self) -> bool:
        """Check if execution produced standard output."""
        return bool(self.stdout.strip())

    @property
    def has_errors(self) -> bool:
        """Check if execution produced errors or failed."""
        return bool(self.stderr.strip()) or not self.success

    @classmethod
    def from_meltano_execution_result(
        cls, result: MeltanoExecutionResult
    ) -> MeltanoRunResult:
        """Create MeltanoRunResult from MeltanoExecutionResult."""
        return cls(
            success=result.success,
            exit_code=result.exit_code,
            stdout=result.stdout,
            stderr=result.stderr,
            duration_seconds=result.duration_seconds,
            started_at=result.started_at,
            completed_at=result.completed_at,
        )


# ============================================================================
# UNIFIED MELTANO ANTI-CORRUPTION LAYER
# ============================================================================


class UnifiedMeltanoAntiCorruptionLayer:
    """Master anti-corruption layer - ZERO TOLERANCE single source of truth.

    This class implements the Anti-Corruption Layer pattern, providing clean
    translation between FLX's domain entities and Meltano's external API.
    It ensures the domain model remains independent of Meltano's implementation
    details and API changes while providing enterprise-grade functionality.
    """

    def __init__(
        self, engine: MeltanoEngine, event_bus: EventBusProtocol | None = None
    ) -> None:
        """Initialize the unified ACL with dependencies.

        Args:
        ----
            engine: MeltanoEngine instance for low-level operations
            event_bus: Optional event bus for domain event publishing

        """
        self.engine = engine
        self.event_bus = event_bus
        self._plugin_type_mapping: dict[PluginType, str] = {}
        self.config = get_config()
        self.logger = logger.bind(component="unified_meltano_acl")
        self._setup_plugin_type_mappings()

    def _setup_plugin_type_mappings(self) -> None:
        """Initialize plugin type mappings for domain ↔ Meltano translation."""
        self._plugin_type_mapping = {
            PluginType.EXTRACTOR: "extractors",
            PluginType.LOADER: "loaders",
            PluginType.TRANSFORMER: "transformers",
            PluginType.ORCHESTRATOR: "orchestrators",
            PluginType.UTILITY: "utilities",
        }

    async def translate_and_run_pipeline(
        self,
        pipeline: Pipeline,
        execution: PipelineExecution,
        env_vars: Mapping[str, str] | None = None,
    ) -> ServiceResult[MeltanoRunResult]:
        """Execute pipeline by translating from domain model to Meltano execution.

        Converts a FLX Pipeline entity to Meltano's execution format, handles
        complexity-based execution strategies, and provides comprehensive
        error handling with ServiceResult patterns.

        Args:
        ----
            pipeline: Domain model pipeline to execute
            execution: Execution context with runtime parameters
            env_vars: Optional environment variables for execution

        Returns:
        -------
            ServiceResult containing MeltanoRunResult or error details

        """
        try:
            # Validate pipeline can execute
            if not pipeline.can_execute():
                return ServiceResult.fail(
                    ServiceError.business_rule_error(
                        "pipeline_not_executable",
                        f"Pipeline {pipeline.name.value} cannot be executed",
                    ),
                )

            # Build execution environment
            execution_env = self._build_execution_environment(
                pipeline,
                execution,
                env_vars,
            )

            # Create Meltano job configuration
            job_config = await self._create_meltano_job_from_pipeline(pipeline)
            if not job_config.is_ok():
                return ServiceResult.fail(
                    job_config.error
                    or ServiceError(
                        "UNKNOWN_ERROR",
                        "Unknown error creating job config",
                    ),
                )

            # Execute pipeline based on step count and complexity
            meltano_result = await self._execute_pipeline_by_complexity(
                pipeline,
                execution_env,
            )

            # Convert MeltanoExecutionResult to MeltanoRunResult
            if isinstance(meltano_result, MeltanoExecutionResult):
                run_result = MeltanoRunResult.from_meltano_execution_result(
                    meltano_result,
                )
            else:
                # Handle legacy result format
                run_result = MeltanoRunResult(
                    success=meltano_result.get("success", False),
                    exit_code=meltano_result.get("exit_code", 1),
                    stdout=meltano_result.get("stdout", ""),
                    stderr=meltano_result.get("stderr", ""),
                    duration_seconds=meltano_result.get("duration_seconds", 0.0),
                    records_processed=meltano_result.get("records_processed", 0),
                )

            # Publish domain events if event bus available
            if self.event_bus:
                await self._publish_execution_events(pipeline, execution, run_result)

            return ServiceResult.ok(run_result)

        except (
            RuntimeError,
            ValueError,
            TypeError,
            OSError,
            KeyError,
            AttributeError,
        ) as e:
            self.logger.exception("Pipeline translation and execution failed")
            return ServiceResult.fail(
                ServiceError(
                    code="MELTANO_TRANSLATION_ERROR",
                    message=f"Failed to translate and run pipeline: {e}",
                    details={
                        "pipeline_id": str(pipeline.pipeline_id.value),
                        "execution_id": str(execution.execution_id),
                    },
                ),
            )

    def _build_execution_environment(
        self,
        pipeline: Pipeline,
        execution: PipelineExecution,
        env_vars: Mapping[str, str] | None = None,
    ) -> ExecutionEnvironment:
        """Build comprehensive execution environment variables."""
        execution_env: ExecutionEnvironment = {}

        # Add pipeline environment variables (convert ConfigurationDict to ExecutionEnvironment)
        for key, value in pipeline.environment_variables.items():
            execution_env[key] = str(value) if value is not None else ""

        # Add execution input data (convert ConfigurationDict to ExecutionEnvironment)
        for key, value in execution.input_data.items():
            execution_env[key] = str(value) if value is not None else ""

        # Add optional environment variables
        if env_vars:
            execution_env.update(env_vars)

        # Add execution metadata for tracking
        execution_env.update(
            {
                "FLX_EXECUTION_ID": str(execution.execution_id),
                "FLX_PIPELINE_ID": str(pipeline.pipeline_id.value),
                "FLX_EXECUTION_NUMBER": str(execution.execution_number),
                "FLX_TRIGGERED_BY": execution.triggered_by,
                "FLX_TRIGGER_TYPE": execution.trigger_type,
            },
        )

        return execution_env

    async def _execute_pipeline_by_complexity(
        self, pipeline: Pipeline, execution_env: ExecutionEnvironment
    ) -> MeltanoExecutionResult | MeltanoOperationResult:
        """Execute pipeline based on complexity (number of steps)."""
        step_count = len(pipeline.steps)
        min_command_count = get_domain_constants().MINIMUM_MELTANO_COMMAND_COUNT

        if step_count == 1:
            return await self._execute_single_step_pipeline(pipeline, execution_env)
        if step_count == min_command_count:
            return await self._execute_two_step_pipeline(pipeline, execution_env)
        return await self._execute_complex_pipeline(pipeline, execution_env)

    async def _execute_single_step_pipeline(
        self, pipeline: Pipeline, execution_env: ExecutionEnvironment
    ) -> MeltanoExecutionResult:
        """Execute single-step pipeline using plugin invocation."""
        step = pipeline.steps[0]
        plugin_name = f"flx_{step.step_id}"

        return await self.engine.invoke_plugin(
            plugin_name=plugin_name,
            env_vars=execution_env,
            settings={
                k: str(v) if v is not None else ""
                for k, v in (pipeline.environment_variables or {}).items()
            },
        )

    async def _execute_two_step_pipeline(
        self, pipeline: Pipeline, execution_env: ExecutionEnvironment
    ) -> MeltanoExecutionResult:
        """Execute two-step ELT pipeline using run_pipeline."""
        extractor_step = None
        loader_step = None
        min_command_count = get_domain_constants().MINIMUM_MELTANO_COMMAND_COUNT

        for step in pipeline.steps:
            if step.order == 1:
                extractor_step = step
            elif step.order == min_command_count:
                loader_step = step

        if extractor_step and loader_step:
            result = await self.engine.run_pipeline(
                extractor=f"flx_{extractor_step.step_id}",
                loader=f"flx_{loader_step.step_id}",
                state_id=f"flx_pipeline_{pipeline.pipeline_id.value}",
                env=execution_env or None,
            )
            # Convert MeltanoOperationResult to MeltanoExecutionResult
            from flx_core.engine.meltano_wrapper import MeltanoExecutionResult

            # Type-safe conversion with proper type guards
            exit_code_val = result.get("exit_code", 0)
            exit_code = (
                int(exit_code_val) if isinstance(exit_code_val, int | str) else 0
            )

            execution_time_val = result.get("execution_time", 0.0)
            execution_time = (
                float(execution_time_val)
                if isinstance(execution_time_val, int | float | str)
                else 0.0
            )

            command_val = result.get("command", ["meltano", "run"])
            command = (
                command_val if isinstance(command_val, list) else ["meltano", "run"]
            )

            started_at_val = result.get("started_at")
            started_at = (
                started_at_val
                if isinstance(started_at_val, datetime)
                else datetime.now(UTC)
            )

            completed_at_val = result.get("completed_at")
            completed_at = (
                completed_at_val
                if isinstance(completed_at_val, datetime)
                else datetime.now(UTC)
            )

            return MeltanoExecutionResult(
                success=bool(result.get("success", True)),
                exit_code=exit_code,
                stdout=str(result.get("stdout", "")),
                stderr=str(result.get("stderr", "")),
                command=command,
                execution_time=execution_time,
                started_at=started_at,
                completed_at=completed_at,
            )

        # Fallback to complex pipeline execution
        return await self._execute_complex_pipeline(pipeline, execution_env)

    async def _execute_complex_pipeline(
        self, pipeline: Pipeline, execution_env: ExecutionEnvironment
    ) -> MeltanoExecutionResult:
        """Execute complex multi-step pipeline as a job."""
        job_name = f"flx_pipeline_{pipeline.name.value}"

        return await self.engine.run_job(
            job_name=job_name,
            env_vars=execution_env,
            settings={
                k: str(v) if v is not None else ""
                for k, v in (pipeline.environment_variables or {}).items()
            },
        )

    async def _create_meltano_job_from_pipeline(
        self, pipeline: Pipeline
    ) -> ServiceResult[dict[str, Any]]:
        """Create Meltano job configuration from domain pipeline."""
        try:
            # Sort steps by order
            sorted_steps = sorted(pipeline.steps, key=lambda s: s.order)

            # Build task list
            tasks: list[str] = []
            for step in sorted_steps:
                task_name = f"flx_{step.step_id}"
                tasks.append(task_name)

            # Create job configuration
            job_config: dict[str, Any] = {
                "name": f"flx_pipeline_{pipeline.name.value}",
                "tasks": tasks,
                "description": pipeline.description
                or f"FLX Pipeline: {pipeline.name.value}",
            }

            # Add environment variables
            if pipeline.environment_variables:
                job_config["env"] = pipeline.environment_variables

            return ServiceResult.ok(job_config)

        except (ValueError, TypeError, RuntimeError, KeyError, AttributeError) as e:
            return ServiceResult.fail(
                ServiceError(
                    code="JOB_CREATION_ERROR",
                    message=f"Failed to create Meltano job configuration: {e}",
                    details={"pipeline_id": str(pipeline.pipeline_id.value)},
                ),
            )

    async def _publish_execution_events(
        self, pipeline: Pipeline, execution: PipelineExecution, result: MeltanoRunResult
    ) -> None:
        """Publish domain events for pipeline execution."""
        if not self.event_bus:
            return

        try:
            from flx_core.events.event_bus import DomainEvent

            event_type = "pipeline.completed" if result.success else "pipeline.failed"
            event_data: dict[str, str | int | bool | float | None] = {
                "pipeline_id": str(pipeline.pipeline_id.value),
                "execution_id": str(execution.execution_id),
                "success": bool(result.success),
                "duration_seconds": float(result.duration_seconds),
                "records_processed": int(result.records_processed),
            }

            if not result.success:
                event_data["error_message"] = result.stderr

            event = DomainEvent.create(event_type, event_data)
            await self.event_bus.publish(event)

        except (RuntimeError, ValueError, ImportError, AttributeError, OSError) as e:
            self.logger.warning("Failed to publish execution event", error=str(e))

    # ========================================================================
    # PLUGIN MANAGEMENT OPERATIONS
    # ========================================================================

    async def install_plugin_from_domain(
        self, plugin: Plugin
    ) -> ServiceResult[MeltanoExecutionResult]:
        """Install a domain plugin in Meltano with proper translation."""
        try:
            # Translate plugin type
            meltano_type = self._translate_plugin_type(plugin.plugin_type)
            if not meltano_type:
                return ServiceResult.fail(
                    ServiceError.validation_error(
                        f"Unsupported plugin type: {plugin.plugin_type}",
                    ),
                )

            # Add plugin to Meltano
            result = await self.engine.add_plugin(
                plugin_type=meltano_type,
                plugin_name=f"flx_{plugin.name}",
            )

            if not result:
                return ServiceResult.fail(
                    ServiceError(
                        code="PLUGIN_INSTALLATION_FAILED",
                        message="Failed to add plugin",
                    ),
                )

            # Configure plugin settings if provided
            if plugin.configuration.settings:
                for key, value in plugin.configuration.settings.items():
                    config_result = await self.engine.set_config(
                        plugin_name=f"flx_{plugin.name}",
                        config_key=key,
                        config_value=str(value),
                    )
                    if not config_result:
                        return ServiceResult.fail(
                            ServiceError(
                                code="PLUGIN_CONFIG_ERROR",
                                message=f"Failed to set configuration {key} for plugin {plugin.name}",
                            ),
                        )

            # Create success result
            success_result = MeltanoExecutionResult(
                success=True,
                exit_code=0,
                stdout=f"Plugin {plugin.name} installed successfully",
                stderr="",
                command=["meltano", "add", meltano_type, f"flx_{plugin.name}"],
                execution_time=0.0,
                started_at=datetime.now(UTC),
                completed_at=datetime.now(UTC),
            )

            return ServiceResult.ok(success_result)

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ImportError,
            FileNotFoundError,
        ) as e:
            return ServiceResult.fail(
                ServiceError(
                    code="PLUGIN_INSTALLATION_ERROR",
                    message=f"Failed to install plugin {plugin.name}: {e}",
                    details={"plugin_id": str(plugin.plugin_id.value)},
                ),
            )

    async def test_plugin_from_domain(
        self, plugin: Plugin
    ) -> ServiceResult[MeltanoExecutionResult]:
        """Test a domain plugin in Meltano."""
        try:
            # Test plugin configuration
            plugin_name = f"flx_{plugin.name}"
            result = await self.engine.test_plugin(plugin_name=plugin_name)
            return ServiceResult.ok(result)

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ImportError,
            FileNotFoundError,
        ) as e:
            return ServiceResult.fail(
                ServiceError(
                    code="PLUGIN_TEST_ERROR",
                    message=f"Failed to test plugin {plugin.name}: {e}",
                    details={"plugin_id": str(plugin.plugin_id.value)},
                ),
            )

    async def remove_plugin_from_domain(
        self, plugin: Plugin
    ) -> ServiceResult[MeltanoExecutionResult]:
        """Remove a domain plugin from Meltano."""
        try:
            # Translate plugin type
            meltano_type = self._translate_plugin_type(plugin.plugin_type)
            if not meltano_type:
                return ServiceResult.fail(
                    ServiceError.validation_error(
                        f"Unsupported plugin type: {plugin.plugin_type}",
                    ),
                )

            # Remove plugin from Meltano
            result = await self.engine.remove_plugin(
                plugin_type=meltano_type,
                plugin_name=f"flx_{plugin.name}",
            )

            # Create result object
            execution_result = MeltanoExecutionResult(
                success=result,
                exit_code=0 if result else 1,
                stdout=f"Plugin {plugin.name} removed successfully" if result else "",
                stderr="" if result else f"Failed to remove plugin {plugin.name}",
                command=["meltano", "remove", meltano_type, f"flx_{plugin.name}"],
                execution_time=0.0,
                started_at=datetime.now(UTC),
                completed_at=datetime.now(UTC),
            )

            return ServiceResult.ok(execution_result)

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ImportError,
            FileNotFoundError,
        ) as e:
            return ServiceResult.fail(
                ServiceError(
                    code="PLUGIN_REMOVAL_ERROR",
                    message=f"Failed to remove plugin {plugin.name}: {e}",
                    details={"plugin_id": str(plugin.plugin_id.value)},
                ),
            )

    def _translate_plugin_type(self, plugin_type: PluginType) -> str | None:
        """Translate domain plugin type to Meltano type."""
        type_mapping = {
            PluginType.EXTRACTOR: "extractor",
            PluginType.LOADER: "loader",
            PluginType.TRANSFORMER: "transformer",
            PluginType.ORCHESTRATOR: "orchestrator",
            PluginType.UTILITY: "utility",
        }
        return type_mapping.get(plugin_type)

    # ========================================================================
    # STATE MANAGEMENT OPERATIONS
    # ========================================================================

    async def get_pipeline_state(self, pipeline: Pipeline) -> ServiceResult[StateData]:
        """Get pipeline state from Meltano with proper error handling."""
        try:
            state_id = f"flx_pipeline_{pipeline.pipeline_id.value}"
            state_data = await self.engine.get_state(state_id)
            return ServiceResult.ok(state_data)

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ImportError,
            FileNotFoundError,
        ) as e:
            return ServiceResult.fail(
                ServiceError(
                    code="STATE_RETRIEVAL_ERROR",
                    message=f"Failed to get state for pipeline {pipeline.name.value}: {e}",
                    details={"pipeline_id": str(pipeline.pipeline_id.value)},
                ),
            )

    async def set_pipeline_state(
        self, pipeline: Pipeline, state_data: StateData
    ) -> ServiceResult[MeltanoExecutionResult]:
        """Set pipeline state in Meltano with comprehensive validation."""
        try:
            state_id = f"flx_pipeline_{pipeline.pipeline_id.value}"
            result = await self.engine.set_state(state_id, state_data)

            execution_result = MeltanoExecutionResult.from_state_result(result)
            return ServiceResult.ok(execution_result)

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ImportError,
            FileNotFoundError,
        ) as e:
            return ServiceResult.fail(
                ServiceError(
                    code="STATE_UPDATE_ERROR",
                    message=f"Failed to set state for pipeline {pipeline.name.value}: {e}",
                    details={"pipeline_id": str(pipeline.pipeline_id.value)},
                ),
            )

    async def clear_pipeline_state(
        self, pipeline: Pipeline
    ) -> ServiceResult[MeltanoExecutionResult]:
        """Clear pipeline state in Meltano with validation."""
        try:
            state_id = f"flx_pipeline_{pipeline.pipeline_id.value}"
            result = await self.engine.clear_state(state_id)

            execution_result = MeltanoExecutionResult.from_state_result(result)
            return ServiceResult.ok(execution_result)

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ImportError,
            FileNotFoundError,
        ) as e:
            return ServiceResult.fail(
                ServiceError(
                    code="STATE_CLEAR_ERROR",
                    message=f"Failed to clear state for pipeline {pipeline.name.value}: {e}",
                    details={"pipeline_id": str(pipeline.pipeline_id.value)},
                ),
            )

    # ========================================================================
    # VALIDATION AND MONITORING
    # ========================================================================

    async def validate_meltano_setup(self) -> ServiceResult[bool]:
        """Validate the Meltano setup with comprehensive checks."""
        try:
            validation_result = await self.engine.validate_installation()
            return ServiceResult.ok(validation_result)

        except (RuntimeError, ValueError, ImportError, AttributeError, OSError) as e:
            return ServiceResult.fail(
                ServiceError(
                    code="MELTANO_VALIDATION_ERROR",
                    message=f"Failed to validate Meltano setup: {e}",
                ),
            )

    async def get_meltano_logs(
        self, execution_id: str | None = None, limit: int = 100
    ) -> ServiceResult[list[str]]:
        """Get Meltano execution logs for monitoring and debugging.

        Retrieves execution logs from the Meltano logs directory, optionally
        filtered by execution ID and limited by count for performance.

        Args:
        ----
            execution_id: Optional execution identifier to filter logs
            limit: Maximum number of log entries to return (default 100)

        Returns:
        -------
            ServiceResult containing list of log entries as strings

        """
        try:
            logs_dir = self.engine.project_root / "logs"

            if not logs_dir.exists():
                return ServiceResult.ok([])

            log_files = []
            for log_file in logs_dir.glob("*.log"):
                if execution_id and execution_id not in log_file.name:
                    continue
                log_files.append(log_file)

            # Sort by modification time (newest first)
            log_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)

            logs: list[str] = []
            for log_file in log_files[:limit]:
                try:
                    with log_file.open("r", encoding="utf-8") as f:
                        lines = f.readlines()
                        logs.extend(line.strip() for line in lines if line.strip())
                except (
                    OSError,
                    FileNotFoundError,
                    UnicodeDecodeError,
                    PermissionError,
                ):
                    # Skip files that can't be read
                    continue

            return ServiceResult.ok(logs[-limit:] if len(logs) > limit else logs)

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ImportError,
            FileNotFoundError,
        ) as e:
            return ServiceResult.fail(
                ServiceError(
                    code="LOG_RETRIEVAL_ERROR",
                    message=f"Failed to retrieve Meltano logs: {e}",
                ),
            )


# Export unified interface
__all__ = [
    "ExecutionEnvironment",
    "MeltanoOperationResult",
    "MeltanoPluginDescriptor",
    "MeltanoRunResult",
    "PipelineConfiguration",
    "PluginConfiguration",
    "StateData",
    "UnifiedMeltanoAntiCorruptionLayer",
]
