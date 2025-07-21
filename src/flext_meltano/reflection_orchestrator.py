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
from enum import Enum, auto
from functools import wraps
from typing import TYPE_CHECKING, Any, ClassVar, Protocol, TypeVar

from flext_core.domain.pydantic_base import (
    DomainBaseModel as BaseModel,
    DomainValueObject,
    Field,
)

if TYPE_CHECKING:
    from types import ModuleType

    from flext_core.domain.pipeline import Pipeline, PipelineExecution


# Type aliases for clean interface
StepFunction = Callable[..., Any]
StepResult = dict[str, Any]
PipelineConfig = dict[str, Any]
ExecutionContext = dict[str, Any]

T = TypeVar("T", bound=Callable[..., Any])
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
        # Build kwargs from context based on function signature
        kwargs = self._build_kwargs_from_context(context)

        # Execute function
        result = await self._execute_function(kwargs)

        # Build and return result
        return self._build_step_result(result)

    def _build_kwargs_from_context(self, context: dict[str, Any]) -> dict[str, Any]:
        """Build kwargs from context based on function signature."""
        sig = inspect.signature(self.func)
        kwargs = {}

        for param_name, param in sig.parameters.items():
            if param_name in context:
                kwargs[param_name] = context[param_name]
            elif param.default != inspect.Parameter.empty:
                kwargs[param_name] = param.default
            elif param_name != "self" and param.annotation != inspect.Parameter.empty:
                # Try to inject based on type annotation
                self._inject_by_type(param_name, param.annotation, context, kwargs)

        return kwargs

    def _inject_by_type(
        self,
        param_name: str,
        type_hint: Any,
        context: dict[str, Any],
        kwargs: dict[str, Any],
    ) -> None:
        """Inject parameter value based on type annotation."""
        try:
            # Handle both regular types and parameterized generics
            for value in context.values():
                if hasattr(type_hint, "__origin__"):
                    # Parameterized generic like dict[str, Any]
                    origin_type = type_hint.__origin__
                    if isinstance(value, origin_type):
                        kwargs[param_name] = value
                        break
                # Regular type
                elif isinstance(value, type_hint):
                    kwargs[param_name] = value
                    break
        except TypeError:
            # Skip problematic type annotations
            pass

    async def _execute_function(self, kwargs: dict[str, Any]) -> Any:
        """Execute the function with provided kwargs."""
        if asyncio.iscoroutinefunction(self.func):
            return await self.func(**kwargs)
        return await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self.func(**kwargs),
        )

    def _build_step_result(self, result: Any) -> StepResult:
        """Build step result with proper type name handling."""
        # Handle both enum and value cases
        step_type_name = (
            self.step_type.name
            if hasattr(self.step_type, "name")
            else StepType(self.step_type).name
        )
        return {"name": self.name, "result": result, "type": step_type_name}


def pipeline_step(
    step_type: StepType,
    name: str | None = None,
    dependencies: list[str] | None = None,
    retry: int = 3,
    timeout: int = 300,
) -> Callable[[T], Any]:
    """Decorator to mark a function as a pipeline step."""

    def decorator(func: T) -> Any:
        # Extract name from function if not provided
        step_name = name or getattr(func, "__name__", "unknown_step").replace("_", "-")

        # Create reflection step
        step = ReflectionStep(
            name=step_name,
            func=func,
            step_type=step_type,
            dependencies=dependencies or [],
            retry_count=retry,
            timeout_seconds=timeout,
        )

        # Store step metadata on function - intentional dynamic attributes
        func._pipeline_step = step  # noqa: SLF001
        func._step_type = step_type  # noqa: SLF001
        func._dependencies = dependencies or []  # noqa: SLF001

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
            try:
                pipeline_step = obj._pipeline_step  # noqa: SLF001
                self.step_registry[pipeline_step.name] = pipeline_step
            except (AttributeError, TypeError):
                continue

            # Register by type for objects with step_type
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
        try:
            # Build execution context
            context = {
                "pipeline": pipeline,
                "execution": execution,
                "orchestrator": self,
            }

            # Execute steps based on pipeline configuration
            results = {}

            # Check if pipeline has steps defined
            if hasattr(pipeline, "steps") and pipeline.steps:
                # Execute pipeline steps with their configurations
                for step_config in pipeline.steps:
                    step_id = step_config.step_id
                    configuration = step_config.configuration

                    if step_id in self.step_registry:
                        reflection_step = self.step_registry[step_id]
                        step_result = await self._execute_step_with_retry(
                            reflection_step,
                            context,
                            configuration,
                        )
                        results[step_id] = step_result
            else:
                # Fallback: Execute all steps from step registry with empty config
                for step_name, reflection_step in self.step_registry.items():
                    step_result = await self._execute_step_with_retry(
                        reflection_step,
                        context,
                        {},  # Default empty configuration
                    )
                    results[step_name] = step_result

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
                # Add configuration to context (both as config and spread individual keys)
                step_context = {**context, "config": configuration, **configuration}

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
        msg = "Step execution failed"
        raise RuntimeError(msg)


# Example step implementations using the decorator
@pipeline_step(StepType.EXTRACT, name="simple-extract")
async def extract_data(source: str, config: dict[str, Any]) -> dict[str, Any]:
    """Simple data extraction step."""
    return {"source": source, "data": f"extracted from {source}"}


@pipeline_step(StepType.TRANSFORM, name="simple-transform")
async def transform_data(
    data: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    """Simple data transformation step."""
    return {"transformed": True, "original": data}


@pipeline_step(StepType.LOAD, name="simple-load")
async def load_data(
    data: dict[str, Any],
    target: str,
    config: dict[str, Any],
) -> dict[str, Any]:
    """Simple data loading step."""
    return {"target": target, "loaded": True, "data": data}


def create_orchestrator() -> ReflectionOrchestrator:
    """Create a reflection orchestrator with discovered steps."""
    orchestrator = ReflectionOrchestrator()

    # Discover steps in current module
    orchestrator.discover_steps(sys.modules[__name__])

    return orchestrator
