"""Reflection-based Meltano orchestrator with ZERO boilerplate using Python 3.13.

This module implements automatic pipeline orchestration through reflection,
eliminating ALL boilerplate code while maintaining complete type safety.
"""

from __future__ import annotations

import asyncio
import contextlib
import inspect
import sys
from collections.abc import Callable
from enum import Enum
from enum import auto
from functools import wraps
from typing import TYPE_CHECKING
from typing import Any
from typing import ClassVar
from typing import Protocol
from typing import TypeVar

from flext_core.domain.pydantic_base import BaseModel
from flext_core.domain.pydantic_base import DomainValueObject
from flext_core.domain.pydantic_base import Field

if TYPE_CHECKING:
    from types import ModuleType

    from flext_core.domain.entities import Pipeline
    from flext_core.domain.entities import PipelineExecution


# Type aliases for clean interface
StepFunction = Callable[..., Any]
StepResult = dict[str, Any]
PipelineConfig = dict[str, Any]
ExecutionContext = dict[str, Any]

T = TypeVar("T")
P = TypeVar("P")


class StepType(Enum):
    """Pipeline step types with automatic behavior."""

    EXTRACT = auto()
    TRANSFORM = auto()
    LOAD = auto()
    QUALITY = auto()
    NOTIFY = auto()


class StepProtocol(Protocol):
    """Protocol for pipeline steps with reflection support."""

    async def execute(self, context: dict[str, Any]) -> StepResult:
        """Execute the step with the given context."""
        ...

    @property
    def step_type(self) -> StepType:
        """Return the step type."""
        ...

    @property
    def dependencies(self) -> list[str]:
        """Return the list of step dependencies."""
        ...


class ReflectionStep(DomainValueObject):
    """Zero-boilerplate step implementation using reflection."""

    model_config: ClassVar = {"arbitrary_types_allowed": True}

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

    async def execute(self, context: dict[str, Any]) -> StepResult:
        """Execute the step function with dependency injection from context."""
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
) -> Callable[[T], T]:
    """Decorator to mark a function as a pipeline step."""

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
        async def wrapper(*args: object, **kwargs: object) -> Any:
            # Execute through reflection step
            context = {**kwargs}
            if args:
                # Safely extract context from first argument if it has __dict__
                with contextlib.suppress(AttributeError):
                    if hasattr(args[0], "__dict__"):
                        context.update(args[0].__dict__)

            return await step.execute(context)

        return wrapper

    return decorator


class ReflectionOrchestrator(BaseModel):
    """Automatic pipeline orchestrator using reflection patterns."""

    model_config: ClassVar = {"arbitrary_types_allowed": True}

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
        """Discover pipeline steps in a module through reflection."""
        for _name, obj in inspect.getmembers(module):
            # Check if object has pipeline step metadata
            if hasattr(obj, "_pipeline_step"):
                try:
                    pipeline_step = obj._pipeline_step
                    self.step_registry[pipeline_step.name] = pipeline_step
                except (AttributeError, TypeError):
                    continue

            # Register by type for objects with step_type
            elif hasattr(obj, "step_type"):
                try:
                    if obj.step_type not in self.type_registry:
                        self.type_registry[obj.step_type] = []
                    self.type_registry[obj.step_type].append(obj)
                except (AttributeError, TypeError):
                    continue

    async def execute_pipeline(
        self,
        pipeline: Pipeline,
        execution: PipelineExecution,
    ) -> ExecutionContext:
        """Execute a pipeline using reflection orchestration."""
        try:
            # Build execution context
            context = {
                "pipeline": pipeline,
                "execution": execution,
                "orchestrator": self,
            }

            # Execute all steps
            results = {}
            for step in pipeline.steps:
                if step.step_id in self.step_registry:
                    reflection_step = self.step_registry[step.step_id]
                    step_result = await self._execute_step_with_retry(
                        reflection_step,
                        context,
                        step.configuration,
                    )
                    results[step.step_id] = step_result

            return {
                "pipeline": pipeline,
                "execution": execution,
                "results": results,
                "success": True,
                "error": None,
            }

        except (ValueError, TypeError, RuntimeError, OSError) as e:
            return {
                "pipeline": pipeline,
                "execution": execution,
                "results": {},
                "success": False,
                "error": str(e),
            }

    async def _execute_step_with_retry(
        self,
        step: ReflectionStep,
        context: ExecutionContext,
        configuration: dict[str, Any],
    ) -> StepResult:
        """Execute a step with retry logic."""
        last_error = None

        for attempt in range(step.retry_count):
            try:
                # Add configuration to context
                step_context = {**context, "config": configuration}

                # Execute with timeout
                return await asyncio.wait_for(
                    step.execute(step_context),
                    timeout=step.timeout_seconds,
                )

            except (TimeoutError, ValueError, TypeError, RuntimeError, OSError) as e:
                last_error = e

                # Exponential backoff if retrying
                if attempt < step.retry_count - 1:
                    await asyncio.sleep(2**attempt)

        if last_error:
            raise last_error
        msg = f"Step {step.name} failed after {step.retry_count} attempts"
        raise RuntimeError(msg)


# Example step implementations using the decorator
@pipeline_step(StepType.EXTRACT, name="simple-extract")
async def extract_data(source: str, config: dict[str, Any]) -> dict[str, Any]:
    """Simple data extraction step."""
    return {"source": source, "data": f"extracted from {source}"}


@pipeline_step(StepType.TRANSFORM, name="simple-transform")
async def transform_data(
    data: dict[str, Any], config: dict[str, Any],
) -> dict[str, Any]:
    """Simple data transformation step."""
    return {"transformed": True, "original": data}


@pipeline_step(StepType.LOAD, name="simple-load")
async def load_data(
    data: dict[str, Any], target: str, config: dict[str, Any],
) -> dict[str, Any]:
    """Simple data loading step."""
    return {"target": target, "loaded": True, "data": data}


def create_orchestrator() -> ReflectionOrchestrator:
    """Create a reflection orchestrator with discovered steps."""
    orchestrator = ReflectionOrchestrator()

    # Discover steps in current module
    orchestrator.discover_steps(sys.modules[__name__])

    return orchestrator
