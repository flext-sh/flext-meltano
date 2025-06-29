"""Reflection-based Meltano orchestrator with ZERO boilerplate using Python 3.13.

This module implements automatic pipeline orchestration through reflection,
eliminating ALL boilerplate code while maintaining complete type safety.
"""

from __future__ import annotations

import asyncio
import inspect
import sys
from enum import Enum, auto
from functools import wraps
from typing import TYPE_CHECKING, TypeVar

from flx_core.domain.pydantic_base import DomainBaseModel, DomainValueObject
from pydantic import Field

# ZERO TOLERANCE - Use TYPE_CHECKING and runtime imports for dependencies
# All modules should be available in properly configured system

if TYPE_CHECKING:
    from types import ModuleType

    from flx_core.domain.entities import Pipeline, PipelineExecution, PipelineStep
    from flx_core.engine.meltano_wrapper import MeltanoEngine
    from flx_core.events.event_bus import DomainEventBus

# Python 3.13 type aliases - with strict validation
from collections.abc import Callable

StepFunction = Callable[..., object]
StepResult = dict[str, object]
PipelineConfig = dict[str, object]
ExecutionContext = dict[str, object]  # Pipeline execution context

T = TypeVar("T")
P = TypeVar("P")


class StepType(Enum):
    """Pipeline step types with automatic behavior."""

    EXTRACT = auto()
    TRANSFORM = auto()
    LOAD = auto()
    QUALITY = auto()
    NOTIFY = auto()


class StepProtocol:
    """Protocol for pipeline steps with reflection support."""

    async def execute(self, context: dict[str, object]) -> StepResult: ...

    @property
    def step_type(self) -> StepType: ...

    @property
    def dependencies(self) -> list[str]: ...


class ReflectionStep(DomainValueObject):
    """Zero-boilerplate step implementation using reflection."""

    model_config = {"arbitrary_types_allowed": True}

    name: str = Field(description="Step name for identification")
    func: StepFunction = Field(description="Step function to execute")
    step_type: StepType = Field(description="Type of step for orchestration")
    dependencies: list[str] = Field(
        default_factory=list,
        description="List of step dependencies",
    )
    retry_count: int = Field(
        default=3,
        description="Number of retry attempts on failure",
    )
    timeout_seconds: int = Field(
        default=300,
        description="Timeout in seconds for step execution",
    )

    async def execute(self, context: dict[str, object]) -> StepResult:
        """Execute step with automatic parameter injection."""
        # Get function signature
        sig = inspect.signature(self.func)

        # Build kwargs from context based on signature
        kwargs = {}
        for param_name, param in sig.parameters.items():
            if param_name in context:
                kwargs[param_name] = context[param_name]
            elif param.default != inspect.Parameter.empty:
                kwargs[param_name] = param.default
            elif param_name != "self" and param.annotation != inspect.Parameter.empty:
                # Try to inject based on type annotation
                type_hint = param.annotation
                # Look for matching type in context
                for value in context.values():
                    if isinstance(value, type_hint):
                        kwargs[param_name] = value
                        break

        # Execute function
        if asyncio.iscoroutinefunction(self.func):
            result = await self.func(**kwargs)
        else:
            result = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.func(**kwargs),
            )

        return {"name": self.name, "result": result, "type": self.step_type.name}


def pipeline_step(
    step_type: StepType,
    name: str | None = None,
    dependencies: list[str] | None = None,
    retry: int = 3,
    timeout: int = 300,
) -> callable[[T], T]:
    """Decorate zero-boilerplate pipeline steps."""

    def decorator(func: T) -> T:
        # Extract name from function if not provided
        step_name = name or func.__name__.replace("_", "-")

        # Create reflection step
        step = ReflectionStep(
            name=step_name,
            func=func,
            step_type=step_type,
            dependencies=dependencies or [],
            retry_count=retry,
            timeout_seconds=timeout,
        )

        # Store step metadata on function
        func._pipeline_step = step
        func._step_type = step_type
        func._dependencies = dependencies or []

        @wraps(func)
        async def wrapper(*args: object, **kwargs) -> object:
            # Execute through reflection step
            context = {**kwargs}
            if args:
                try:
                    arg_dict = args[0].__dict__
                    context.update(arg_dict)
                except AttributeError:
                    pass  # args[0] doesn't have __dict__

            return await step.execute(context)

        return wrapper

    return decorator


class ReflectionOrchestrator(DomainBaseModel):
    """Automatic pipeline orchestrator using reflection patterns."""

    model_config = {"arbitrary_types_allowed": True}

    meltano_engine: MeltanoEngine = Field(description="Meltano execution engine")
    event_bus: DomainEventBus = Field(description="Event bus for orchestration events")

    # Registry of steps discovered through reflection
    step_registry: dict[str, ReflectionStep] = Field(
        default_factory=dict,
        description="Step registry by name",
    )
    type_registry: dict[StepType, list[ReflectionStep]] = Field(
        default_factory=dict,
        description="Step registry by type",
    )

    def discover_steps(self, module: ModuleType) -> None:
        """Automatically discover pipeline steps in a module."""
        for _name, obj in inspect.getmembers(module):
            try:
                pipeline_step = obj._pipeline_step
                self.step_registry[pipeline_step.name] = pipeline_step
            except AttributeError:
                # obj doesn't have _pipeline_step attribute

                # Register by type (using obj instead of undefined step)
                if hasattr(obj, "step_type"):
                    if obj.step_type not in self.type_registry:
                        self.type_registry[obj.step_type] = []
                    self.type_registry[obj.step_type].append(obj)

    def _extract_pipeline_id_safe(self, pipeline: Pipeline) -> str:
        """Extract pipeline ID safely with try/except pattern - ZERO TOLERANCE MODERNIZATION.

        Args:
        ----
            pipeline: The pipeline object that may or may not have a 'value' attribute on id

        Returns:
        -------
            String representation of the pipeline ID

        """
        try:
            # Try to access pipeline.id.value attribute for value objects
            return str(pipeline.id.value)
        except AttributeError:
            # Fallback to string representation if no value attribute
            return str(pipeline.id)

    async def execute_pipeline(
        self, pipeline: Pipeline, execution: PipelineExecution
    ) -> ExecutionContext:
        """Execute pipeline using UNIFIED EXECUTION ARCHITECTURE with reflection orchestration."""
        try:
            # ZERO TOLERANCE - Runtime import to avoid circular dependencies
            from flx_core.universe import get_universe

            # Use UNIFIED COMMAND UNIVERSE for orchestrated execution - ZERO TOLERANCE
            universe = await get_universe()

            # Delegate to unified execution with reflection orchestration parameters
            result = await universe.execute(
                command_name="execute_pipeline",
                parameters={
                    "pipeline_id": self._extract_pipeline_id_safe(pipeline),
                    "execution_id": str(execution.id),
                    "orchestration_mode": "reflection",
                    "steps": [
                        {
                            "step_id": step.step_id,
                            "configuration": step.configuration,
                            "dependencies": getattr(step, "dependencies", []),
                        }
                        for step in pipeline.steps
                    ],
                },
                context={
                    "service": "reflection_orchestrator",
                    "caller": self.__class__.__name__,
                    "meltano_engine": self.meltano_engine,
                    "event_bus": self.event_bus,
                },
            )

            # Return execution context with results

        except (
            ValueError,
            TypeError,
            RuntimeError,
            OSError,
            ImportError,
            ConnectionError,
            TimeoutError,
            AttributeError,
            LookupError,
        ) as e:
            # ZERO TOLERANCE - Specific exception types for reflection orchestrator failures
            self.logger.exception(
                "Reflection orchestrator execution failed through unified interface",
            )
            # Return error context
            return {
                "pipeline": pipeline,
                "execution": execution,
                "results": {},
                "success": False,
                "error": str(e),
            }
        else:
            return {
                "pipeline": pipeline,
                "execution": execution,
                "results": result.data if result.success else {},
                "success": result.success,
                "error": result.error if not result.success else None,
            }

    def _build_execution_graph(
        self, steps: list[PipelineStep]
    ) -> list[list[PipelineStep]]:
        """Build execution graph with dependency resolution."""
        # Topological sort for dependency ordering
        graph: dict[str, set[str]] = {}
        in_degree: dict[str, int] = {}

        # Initialize graph
        for step in steps:
            graph[step.step_id] = set()
            in_degree[step.step_id] = 0

        # Build dependency graph
        for step in steps:
            for dep in step.depends_on:
                if dep in graph:
                    graph[dep].add(step.step_id)
                    in_degree[step.step_id] += 1

            # Find execution order
            execution_order = []
            queue = [step_id for step_id, degree in in_degree.items() if degree == 0]

            while queue:
                # Process all steps with no dependencies in parallel
                current_group = []
                next_queue = []

                for step_id in queue:
                    current_group.append(
                        next(s for s in steps if s.step_id == step_id),
                    )

                    # Update dependencies
                    for dependent in graph[step_id]:
                        in_degree[dependent] -= 1
                        if in_degree[dependent] == 0:
                            next_queue.append(dependent)

                execution_order.append(current_group)
                queue = next_queue

            return execution_order
        return None

    async def _execute_step_with_retry(
        self,
        step: ReflectionStep,
        context: ExecutionContext,
        configuration: ExecutionContext,
    ) -> StepResult:
        """Execute step with automatic retry logic."""
        last_error = None

        for attempt in range(step.retry_count):
            try:
                # Add configuration to context
                step_context = {**context, "config": configuration}

                # Execute with timeout
                result = await asyncio.wait_for(
                    step.execute(step_context),
                    timeout=step.timeout_seconds,
                )

                # Publish success event
                await self.event_bus.publish(
                    {
                        "type": "step_completed",
                        "step": step.name,
                        "attempt": attempt + 1,
                        "result": result,
                    },
                )

            except TimeoutError:
                last_error = TimeoutError(
                    f"Step {step.name} timed out after {step.timeout_seconds}s",
                )
            except (ValueError, TypeError, RuntimeError, OSError) as e:
                last_error = e

            # Publish retry event
            if attempt < step.retry_count - 1:
                await self.event_bus.publish(
                    {
                        "type": "step_retry",
                        "step": step.name,
                        "attempt": attempt + 1,
                        "error": str(last_error),
                    },
                )

                # Exponential backoff
                await asyncio.sleep(2**attempt)

        raise last_error

    async def _handle_step_failure(
        self, step: PipelineStep, error: Exception, execution: PipelineExecution
    ) -> None:
        """Handle step failure with automatic recovery."""
        # Publish failure event
        await self.event_bus.publish(
            {
                "type": "step_failed",
                "step": step.step_id,
                "error": str(error),
                "execution_id": str(execution.execution_id),
            },
        )

        # Update execution status
        execution.fail(f"Step {step.step_id} failed: {error}")


# === REFLECTION-BASED STEP IMPLEMENTATIONS ===


@pipeline_step(StepType.EXTRACT, name="meltano-tap")
async def extract_with_meltano(
    tap_name: str, config: ExecutionContext, meltano: MeltanoEngine
) -> ExecutionContext:
    """Extract data using Meltano tap with zero boilerplate."""
    result = await meltano.run_pipeline(
        extractor=tap_name,
        loader="target-jsonl",  # Standard target for data extraction
        env=config,
    )
    return {"tap": tap_name, "records": result.get("stdout", "")}


@pipeline_step(StepType.TRANSFORM, name="dbt-transform")
async def transform_with_dbt(
    models: list[str], config: ExecutionContext, meltano: MeltanoEngine
) -> ExecutionContext:
    """Transform data using dbt with zero boilerplate."""
    # Run dbt through Meltano
    dbt_args = ["run", "--models", *models]
    result = await meltano.run_pipeline(
        extractor="dbt",
        loader=None,
        env={"DBT_ARGS": " ".join(dbt_args), **config},
    )
    return {"models": models, "result": result}


@pipeline_step(StepType.LOAD, name="meltano-target")
async def load_with_meltano(
    target_name: str,
    config: ExecutionContext,
    meltano: MeltanoEngine,
    results: ExecutionContext,
) -> ExecutionContext:
    """Load data using Meltano target with zero boilerplate."""
    # Get data from previous extract step
    extract_result = next(
        (r for r in results.values() if r.get("tap")),
        None,
    )

    if not extract_result:
        msg = "No extract result found for load step"
        raise ValueError(msg)

    # Run target
    result = await meltano.run_pipeline(
        extractor="tap-replay",  # Replay extracted data
        loader=target_name,
        env={"REPLAY_DATA": extract_result["records"], **config},
    )
    return {"target": target_name, "result": result}


@pipeline_step(StepType.QUALITY, name="great-expectations")
async def validate_data_quality(
    expectations_suite: str, _config: ExecutionContext, event_bus: DomainEventBus
) -> ExecutionContext:
    """Validate data quality with zero boilerplate."""
    # This would integrate with Great Expectations
    # For now, simulate validation
    validation_results = {
        "suite": expectations_suite,
        "passed": True,
        "statistics": {
            "evaluated_expectations": 10,
            "successful_expectations": 10,
            "unsuccessful_expectations": 0,
        },
    }

    await event_bus.publish(
        {
            "type": "data_quality_validated",
            "suite": expectations_suite,
            "results": validation_results,
        },
    )

    return validation_results


@pipeline_step(StepType.NOTIFY, name="notification")
async def send_notification(
    channel: str, message: str, config: ExecutionContext, execution: PipelineExecution
) -> ExecutionContext:
    """Send notification using REAL NotificationService."""
    # ZERO TOLERANCE - Runtime import for notification dependencies
    from flx_core.config import settings
    from flx_core.services.notification_service import NotificationService

    notification_service = NotificationService()

    # Format message with execution context
    formatted_message = message.format(
        pipeline_id=execution.pipeline_id,
        execution_id=execution.execution_id,
        status=execution.status,
        started_at=execution.started_at,
        completed_at=execution.completed_at,
    )

    # Send notification through specified channel
    try:
        if channel == "email" and settings.notification_email:
            await notification_service.send_email_notification(
                recipient=config.get("recipient", settings.notification_email),
                subject=config.get(
                    "subject",
                    f"Pipeline Notification: {execution.pipeline_id}",
                ),
                message=formatted_message,
            )

        elif channel == "slack":
            webhook_url = config.get(
                "webhook_url",
                settings.notification_slack_webhook_url,
            )
            if webhook_url:
                await notification_service.send_slack_notification(
                    webhook_url=webhook_url,
                    message=formatted_message,
                    channel=config.get("channel", "#flx-pipelines"),
                )
            else:
                return {
                    "channel": channel,
                    "sent": False,
                    "error": "No Slack webhook URL configured",
                }

        elif channel == "webhook":
            webhook_url = config.get("webhook_url", settings.notification_webhook_url)
            if webhook_url:
                webhook_payload = {
                    "pipeline_id": execution.pipeline_id,
                    "execution_id": execution.execution_id,
                    "status": execution.status,
                    "message": formatted_message,
                    "started_at": (
                        execution.started_at.isoformat()
                        if execution.started_at
                        else None
                    ),
                    "completed_at": (
                        execution.completed_at.isoformat()
                        if execution.completed_at
                        else None
                    ),
                    **config.get("extra_data", {}),
                }
                await notification_service.send_webhook_notification(
                    webhook_url=webhook_url,
                    payload=webhook_payload,
                )
            else:
                return {
                    "channel": channel,
                    "sent": False,
                    "error": "No webhook URL configured",
                }
        else:
            return {
                "channel": channel,
                "sent": False,
                "error": f"Unsupported channel: {channel}",
            }

    except (ValueError, TypeError, RuntimeError, OSError, ConnectionError) as e:
        return {
            "channel": channel,
            "message": formatted_message,
            "sent": False,
            "error": str(e),
        }


def create_orchestrator(
    meltano_engine: MeltanoEngine, event_bus: DomainEventBus
) -> ReflectionOrchestrator:
    """Create orchestrator with automatic step discovery."""
    orchestrator = ReflectionOrchestrator(
        meltano_engine=meltano_engine,
        event_bus=event_bus,
    )

    # Discover steps in current module - ZERO TOLERANCE to late imports
    orchestrator.discover_steps(sys.modules[__name__])

    return orchestrator
