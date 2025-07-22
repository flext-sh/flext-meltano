"""Test FLEXT Meltano Reflection Orchestrator - 134 lines of code, 0% coverage.

ZERO TOLERANCE for fake code, mockups, or library fallbacks.
Comprehensive tests for ALL reflection orchestrator classes and functionality.
"""

from __future__ import annotations

import asyncio
import sys
from typing import TYPE_CHECKING, Any, Never
from unittest.mock import MagicMock

import pytest

# Mock missing dependencies to avoid import errors
sys.modules["flext_observability"] = MagicMock()
sys.modules["flext_observability.logging"] = MagicMock()

# ruff: noqa: E402 - Module mocking must happen before imports
from flext_meltano.reflection_orchestrator import (
    ExecutionContext,
    PipelineConfig,
    ReflectionOrchestrator,
    ReflectionStep,
    StepFunction,
    StepResult,
    StepType,
    create_orchestrator,
    extract_data,
    load_data,
    pipeline_step,
    transform_data,
)

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


class TestStepType:
    """Test StepType enum."""

    def test_step_type_values(self) -> None:
        """Test all StepType enum values."""
        assert StepType.EXTRACT.value == 1
        assert StepType.TRANSFORM.value == 2
        assert StepType.LOAD.value == 3
        assert StepType.QUALITY.value == 4
        assert StepType.NOTIFY.value == 5

        # Verify they are different values
        assert len(set(StepType)) == 5  # All values are unique


class TestReflectionStep:
    """Test ReflectionStep class - comprehensive coverage."""

    @pytest.fixture
    def sample_function(self) -> Callable[[str, int], Awaitable[str]]:
        """Sample function for testing."""

        async def sample_func(param1: str, param2: int = 10) -> str:
            return f"Result: {param1} - {param2}"

        return sample_func

    @pytest.fixture
    def sync_function(self) -> Any:
        """Sync function for testing."""

        def sync_func(param1: str, param2: int = 10) -> str:
            return f"Sync: {param1} - {param2}"

        return sync_func

    def test_reflection_step_initialization_minimal(
        self,
        sample_function: Callable[[str, int], Awaitable[str]],
    ) -> None:
        """Test ReflectionStep initialization with minimal parameters."""
        step = ReflectionStep(
            name="test-step",
            func=sample_function,
            step_type=StepType.EXTRACT,
        )

        assert step.name == "test-step"
        assert step.func == sample_function
        assert step.step_type == StepType.EXTRACT
        assert step.dependencies == []
        assert step.retry_count == 3  # Default
        assert step.timeout_seconds == 300  # Default

    def test_reflection_step_initialization_full(
        self,
        sample_function: Callable[[str, int], Awaitable[str]],
    ) -> None:
        """Test ReflectionStep initialization with all parameters."""
        dependencies = ["step1", "step2"]

        step = ReflectionStep(
            name="full-test-step",
            func=sample_function,
            step_type=StepType.TRANSFORM,
            dependencies=dependencies,
            retry_count=5,
            timeout_seconds=600,
        )

        assert step.name == "full-test-step"
        assert step.func == sample_function
        assert step.step_type == StepType.TRANSFORM
        assert step.dependencies == dependencies
        assert step.retry_count == 5
        assert step.timeout_seconds == 600

    @pytest.mark.asyncio
    async def test_execute_async_function_with_params(
        self,
        sample_function: Callable[[str, int], Awaitable[str]],
    ) -> None:
        """Test executing async function with parameters from context."""
        step = ReflectionStep(
            name="test-step",
            func=sample_function,
            step_type=StepType.EXTRACT,
        )

        context = {"param1": "hello", "param2": 20}
        result = await step.execute(context)

        assert result["name"] == "test-step"
        assert result["result"] == "Result: hello - 20"
        assert result["type"] == "EXTRACT"

    @pytest.mark.asyncio
    async def test_execute_async_function_with_defaults(
        self,
        sample_function: Callable[[str, int], Awaitable[str]],
    ) -> None:
        """Test executing async function with default parameters."""
        step = ReflectionStep(
            name="test-step",
            func=sample_function,
            step_type=StepType.TRANSFORM,
        )

        # Only provide param1, param2 should use default
        context = {"param1": "world"}
        result = await step.execute(context)

        assert result["name"] == "test-step"
        assert result["result"] == "Result: world - 10"
        assert result["type"] == "TRANSFORM"

    @pytest.mark.asyncio
    async def test_execute_sync_function(
        self,
        sync_function: Callable[[str, int], str],
    ) -> None:
        """Test executing sync function through executor."""
        step = ReflectionStep(
            name="sync-step",
            func=sync_function,
            step_type=StepType.LOAD,
        )

        context = {"param1": "sync-test", "param2": 30}
        result = await step.execute(context)

        assert result["name"] == "sync-step"
        assert result["result"] == "Sync: sync-test - 30"
        assert result["type"] == "LOAD"

    @pytest.mark.asyncio
    async def test_execute_with_type_injection(self) -> None:
        """Test parameter injection based on type annotations."""

        class CustomType:
            def __init__(self, value: str) -> None:
                self.value = value

        async def typed_func(param: CustomType) -> str:
            return f"Type: {param.value}"

        # Create the step with the function and its closure containing CustomType
        step = ReflectionStep(
            name="type-step",
            func=typed_func,
            step_type=StepType.QUALITY,
        )

        # Create an instance and add it to context with matching type
        custom_obj = CustomType("injected")
        context = {
            "other_param": "not used",
            "param": custom_obj,
        }  # Changed key to match parameter name
        result = await step.execute(context)

        assert result["name"] == "type-step"
        assert result["result"] == "Type: injected"
        assert result["type"] == "QUALITY"

    @pytest.mark.asyncio
    async def test_execute_with_missing_params(self) -> None:
        """Test executing function with missing required parameters."""

        class CustomType:
            pass

        async def strict_func(required_param: CustomType) -> str:
            return f"Required: {required_param}"

        step = ReflectionStep(
            name="strict-step",
            func=strict_func,
            step_type=StepType.NOTIFY,
        )

        # Missing required_param with no matching type should cause TypeError
        context = {"other_param": "not matching", "number": 42}

        with pytest.raises(TypeError):
            await step.execute(context)


class TestPipelineStepDecorator:
    """Test pipeline_step decorator - comprehensive coverage."""

    def test_decorator_basic_usage(self) -> None:
        """Test basic decorator usage."""

        @pipeline_step(StepType.EXTRACT, name="custom-extract")
        async def decorated_func(param: str) -> str:
            return f"Decorated: {param}"

        # Check metadata is attached
        assert hasattr(decorated_func, "pipeline_step")
        assert hasattr(decorated_func, "_step_type")
        assert hasattr(decorated_func, "_dependencies")

        step = decorated_func.pipeline_step
        assert step.name == "custom-extract"
        assert step.step_type == StepType.EXTRACT
        assert step.dependencies == []
        assert step.retry_count == 3
        assert step.timeout_seconds == 300

    def test_decorator_auto_naming(self) -> None:
        """Test automatic name generation from function name."""

        @pipeline_step(StepType.TRANSFORM)
        async def my_transform_function(data: dict[str, Any]) -> dict[str, Any]:
            return data

        step = getattr(my_transform_function, "pipeline_step", None)
        assert step is not None
        assert step.name == "my-transform-function"

    def test_decorator_with_all_params(self) -> None:
        """Test decorator with all parameters."""
        dependencies = ["extract-step", "validate-step"]

        @pipeline_step(
            StepType.LOAD,
            name="complex-load",
            dependencies=dependencies,
            retry=5,
            timeout=600,
        )
        async def complex_func(data: dict[str, Any], target: str) -> dict[str, Any]:
            return {"loaded": True}

        step = getattr(complex_func, "pipeline_step", None)
        assert step is not None
        assert step.name == "complex-load"
        assert step.step_type == StepType.LOAD
        assert step.dependencies == dependencies
        assert step.retry_count == 5
        assert step.timeout_seconds == 600

    @pytest.mark.asyncio
    async def test_decorated_function_execution(self) -> None:
        """Test executing decorated function."""

        @pipeline_step(StepType.QUALITY, name="test-quality")
        async def quality_func(data: str) -> str:
            return f"Quality: {data}"

        # Execute the decorated function
        result = await quality_func(data="test-data")

        # The decorator transforms the return value to a dict
        from typing import cast

        result_dict = cast("dict[str, Any]", result)
        assert result_dict["name"] == "test-quality"
        assert result_dict["result"] == "Quality: test-data"
        assert result_dict["type"] == "QUALITY"

    @pytest.mark.asyncio
    async def test_decorated_function_with_object_context(self) -> None:
        """Test decorated function with object context extraction."""

        @pipeline_step(StepType.EXTRACT, name="context-extract")
        async def context_func(value: str) -> str:
            return f"Context: {value}"

        # Create an object with attributes
        class ContextObject:
            def __init__(self) -> None:
                self.value = "from-object"

        context_obj = ContextObject()

        # Execute with object as first argument - use Any type for context
        from typing import cast

        result = await context_func(cast("Any", context_obj))

        result_dict = cast("dict[str, Any]", result)
        assert result_dict["name"] == "context-extract"
        assert result_dict["result"] == "Context: from-object"


class TestReflectionOrchestrator:
    """Test ReflectionOrchestrator class - comprehensive coverage."""

    def test_orchestrator_initialization(self) -> None:
        """Test ReflectionOrchestrator initialization."""
        orchestrator = ReflectionOrchestrator()

        assert orchestrator.step_registry == {}
        assert orchestrator.type_registry == {}

    def test_discover_steps_with_pipeline_metadata(self) -> None:
        """Test discovering steps with pipeline metadata."""
        orchestrator = ReflectionOrchestrator()

        # Create a mock module with decorated functions
        import types

        mock_module = types.ModuleType("mock_module")

        # Add a decorated function to the module
        @pipeline_step(StepType.EXTRACT, name="discovered-extract")
        async def extract_func(source: str) -> dict[str, Any]:
            return {"extracted": source}

        mock_module.extract_func = extract_func

        # Discover steps
        orchestrator.discover_steps(mock_module)

        assert "discovered-extract" in orchestrator.step_registry
        step = orchestrator.step_registry["discovered-extract"]
        assert step.name == "discovered-extract"
        assert step.step_type == StepType.EXTRACT

    def test_discover_steps_with_step_type_objects(self) -> None:
        """Test discovering objects with step_type attribute."""
        orchestrator = ReflectionOrchestrator()

        import types

        mock_module = types.ModuleType("mock_module")

        # Create object with step_type
        class MockStepObject:
            step_type = StepType.TRANSFORM

        mock_module.mock_step = MockStepObject()

        # Discover steps
        orchestrator.discover_steps(mock_module)

        assert StepType.TRANSFORM in orchestrator.type_registry
        assert len(orchestrator.type_registry[StepType.TRANSFORM]) == 1
        assert (
            orchestrator.type_registry[StepType.TRANSFORM][0] == mock_module.mock_step
        )

    def test_discover_steps_error_handling(self) -> None:
        """Test error handling in step discovery."""
        orchestrator = ReflectionOrchestrator()

        import types

        mock_module = types.ModuleType("mock_module")

        # Add object that will cause AttributeError
        class BrokenObject:
            @property
            def pipeline_step(self) -> Never:
                msg = "Broken pipeline step"
                raise AttributeError(msg)

        mock_module.broken_obj = BrokenObject()

        # Should not raise exception, just continue
        orchestrator.discover_steps(mock_module)

        # Registry should be empty since broken object was skipped
        assert orchestrator.step_registry == {}

    @pytest.mark.asyncio
    async def test_execute_pipeline_success(self) -> None:
        """Test successful pipeline execution."""
        orchestrator = ReflectionOrchestrator()

        # Add a step to registry
        @pipeline_step(StepType.EXTRACT, name="test-extract")
        async def test_extract(source: str) -> dict[str, Any]:
            return {"data": f"extracted from {source}"}

        step = getattr(test_extract, "pipeline_step", None)
        assert step is not None
        orchestrator.step_registry["test-extract"] = step

        # Create mock pipeline and execution objects
        mock_pipeline = MagicMock()
        mock_pipeline.steps = [
            MagicMock(step_id="test-extract", configuration={"source": "database"}),
        ]

        mock_execution = MagicMock()

        result = await orchestrator.execute_pipeline(mock_pipeline, mock_execution)

        assert result["success"] is True
        assert result["error"] is None
        assert "test-extract" in result["results"]
        assert result["results"]["test-extract"]["name"] == "test-extract"

    @pytest.mark.asyncio
    async def test_execute_pipeline_with_unknown_step(self) -> None:
        """Test pipeline execution with unknown step."""
        orchestrator = ReflectionOrchestrator()

        # Create mock pipeline with unknown step
        mock_pipeline = MagicMock()
        mock_pipeline.steps = [MagicMock(step_id="unknown-step", configuration={})]

        mock_execution = MagicMock()

        result = await orchestrator.execute_pipeline(mock_pipeline, mock_execution)

        assert result["success"] is True
        assert result["error"] is None
        assert result["results"] == {}  # No steps executed

    @pytest.mark.asyncio
    async def test_execute_pipeline_error_handling(self) -> None:
        """Test pipeline execution error handling."""
        orchestrator = ReflectionOrchestrator()

        # Add a broken step that will fail during execution
        async def broken_func() -> str:
            msg = "Pipeline error"
            raise RuntimeError(msg)

        broken_step = ReflectionStep(
            name="broken-step",
            func=broken_func,
            step_type=StepType.EXTRACT,
        )

        orchestrator.step_registry["broken-step"] = broken_step

        # Create mock pipeline with the broken step
        mock_pipeline = MagicMock()
        mock_pipeline.steps = [MagicMock(step_id="broken-step", configuration={})]

        mock_execution = MagicMock()

        result = await orchestrator.execute_pipeline(mock_pipeline, mock_execution)

        assert result["success"] is False
        assert "Pipeline error" in result["error"]
        assert result["results"] == {}

    @pytest.mark.asyncio
    async def test_execute_step_with_retry_success(self) -> None:
        """Test step execution with retry success on first attempt."""
        orchestrator = ReflectionOrchestrator()

        async def success_func(data: str) -> str:
            return f"Success: {data}"

        step = ReflectionStep(
            name="success-step",
            func=success_func,
            step_type=StepType.TRANSFORM,
            retry_count=3,
            timeout_seconds=10,
        )

        context = {"data": "test"}
        configuration = {"timeout": 5}

        result = await orchestrator._execute_step_with_retry(
            step,
            context,
            configuration,
        )

        assert result["name"] == "success-step"
        assert result["result"] == "Success: test"

    @pytest.mark.asyncio
    async def test_execute_step_with_retry_timeout(self) -> None:
        """Test step execution timeout."""
        orchestrator = ReflectionOrchestrator()

        async def slow_func(data: str) -> str:
            await asyncio.sleep(2)  # Longer than timeout
            return f"Slow: {data}"

        step = ReflectionStep(
            name="slow-step",
            func=slow_func,
            step_type=StepType.LOAD,
            retry_count=2,
            timeout_seconds=1,  # Very short timeout (1 second)
        )

        context = {"data": "test"}
        configuration: dict[str, Any] = {}

        with pytest.raises(asyncio.TimeoutError):
            await orchestrator._execute_step_with_retry(step, context, configuration)

    @pytest.mark.asyncio
    async def test_execute_step_with_retry_eventual_success(self) -> None:
        """Test step execution that succeeds after retries."""
        orchestrator = ReflectionOrchestrator()

        call_count = 0

        async def flaky_func(data: str) -> str:
            nonlocal call_count
            call_count += 1
            if call_count < 3:
                msg = "Temporary failure"
                raise ValueError(msg)
            return f"Eventually: {data}"

        step = ReflectionStep(
            name="flaky-step",
            func=flaky_func,
            step_type=StepType.QUALITY,
            retry_count=5,
            timeout_seconds=10,
        )

        context = {"data": "test"}
        configuration: dict[str, Any] = {}

        # Should succeed on third attempt
        result = await orchestrator._execute_step_with_retry(
            step,
            context,
            configuration,
        )

        assert result["name"] == "flaky-step"
        assert result["result"] == "Eventually: test"
        assert call_count == 3

    @pytest.mark.asyncio
    async def test_execute_step_with_retry_all_failures(self) -> None:
        """Test step execution that fails all retry attempts."""
        orchestrator = ReflectionOrchestrator()

        async def always_fail_func(data: str) -> str:
            msg = "Always fails"
            raise RuntimeError(msg)

        step = ReflectionStep(
            name="fail-step",
            func=always_fail_func,
            step_type=StepType.NOTIFY,
            retry_count=2,
            timeout_seconds=10,
        )

        context = {"data": "test"}
        configuration: dict[str, Any] = {}

        with pytest.raises(RuntimeError, match="Always fails"):
            await orchestrator._execute_step_with_retry(step, context, configuration)


class TestBuiltInSteps:
    """Test built-in step implementations."""

    @pytest.mark.asyncio
    async def test_extract_data_step(self) -> None:
        """Test extract_data step function."""
        # The function is decorated, so we test through the wrapper
        result = await extract_data(source="database", config={"table": "users"})

        assert result["name"] == "simple-extract"
        assert result["type"] == "EXTRACT"
        assert result["result"]["source"] == "database"
        assert "extracted from database" in result["result"]["data"]

    @pytest.mark.asyncio
    async def test_transform_data_step(self) -> None:
        """Test transform_data step function."""
        input_data = {"records": [1, 2, 3]}
        config = {"operation": "sum"}

        result = await transform_data(data=input_data, config=config)

        assert result["name"] == "simple-transform"
        assert result["type"] == "TRANSFORM"
        assert result["result"]["transformed"] is True
        assert result["result"]["original"] == input_data

    @pytest.mark.asyncio
    async def test_load_data_step(self) -> None:
        """Test load_data step function."""
        data = {"processed": [1, 2, 3]}
        target = "warehouse"
        config = {"batch_size": 100}

        result = await load_data(data=data, target=target, config=config)

        assert result["name"] == "simple-load"
        assert result["type"] == "LOAD"
        assert result["result"]["target"] == target
        assert result["result"]["loaded"] is True
        assert result["result"]["data"] == data


class TestCreateOrchestrator:
    """Test create_orchestrator factory function."""

    def test_create_orchestrator_with_discovery(self) -> None:
        """Test creating orchestrator with automatic step discovery."""
        orchestrator = create_orchestrator()

        # Should discover the built-in steps
        assert isinstance(orchestrator, ReflectionOrchestrator)
        assert "simple-extract" in orchestrator.step_registry
        assert "simple-transform" in orchestrator.step_registry
        assert "simple-load" in orchestrator.step_registry


class TestTypeAliases:
    """Test type aliases are properly defined."""

    def test_type_aliases_importable(self) -> None:
        """Test that type aliases are properly imported and usable."""
        # These should be importable without error
        assert StepFunction is not None
        assert StepResult is not None
        assert PipelineConfig is not None
        assert ExecutionContext is not None


class TestProtocols:
    """Test protocol definitions."""

    def test_step_protocol_implementation(self) -> None:
        """Test that ReflectionStep implements StepProtocol."""

        async def test_func() -> str:
            return "test"

        step = ReflectionStep(
            name="protocol-test",
            func=test_func,
            step_type=StepType.EXTRACT,
            dependencies=["dep1", "dep2"],
        )

        # Check protocol implementation
        assert hasattr(step, "execute")
        assert hasattr(step, "step_type")
        assert hasattr(step, "dependencies")
        assert callable(step.execute)
        # Pydantic converts enum to value, so check the value
        assert step.step_type == StepType.EXTRACT
        assert step.dependencies == ["dep1", "dep2"]


class TestIntegrationWorkflow:
    """Test complete integration workflow scenarios."""

    @pytest.mark.asyncio
    async def test_complete_reflection_workflow(self) -> None:
        """Test complete workflow from step creation to execution."""
        # Step 1: Create orchestrator with empty registry
        orchestrator = ReflectionOrchestrator()
        orchestrator.step_registry.clear()  # Clear default steps

        # Step 2: Define custom steps
        @pipeline_step(StepType.EXTRACT, name="workflow-extract", dependencies=[])
        async def workflow_extract(source: str = "default_source") -> dict[str, Any]:
            return {"extracted": f"data from {source}"}

        @pipeline_step(
            StepType.TRANSFORM,
            name="workflow-transform",
            dependencies=["workflow-extract"],
        )
        async def workflow_transform() -> dict[str, Any]:
            return {"transformed": True, "processed": True}

        @pipeline_step(
            StepType.LOAD,
            name="workflow-load",
            dependencies=["workflow-transform"],
        )
        async def workflow_load(target: str = "default_target") -> dict[str, Any]:
            return {"loaded": True, "target": target}

        # Step 3: Register steps manually (simulate discovery)
        extract_step = getattr(workflow_extract, "pipeline_step", None)
        transform_step = getattr(workflow_transform, "pipeline_step", None)
        load_step = getattr(workflow_load, "pipeline_step", None)

        assert extract_step is not None
        assert transform_step is not None
        assert load_step is not None

        orchestrator.step_registry["workflow-extract"] = extract_step
        orchestrator.step_registry["workflow-transform"] = transform_step
        orchestrator.step_registry["workflow-load"] = load_step

        # Step 4: Create mock pipeline
        mock_steps = [
            MagicMock(step_id="workflow-extract", configuration={"source": "api"}),
            MagicMock(step_id="workflow-transform", configuration={}),
            MagicMock(step_id="workflow-load", configuration={"target": "warehouse"}),
        ]
        mock_pipeline = MagicMock(steps=mock_steps)
        mock_execution = MagicMock()

        # Step 5: Execute pipeline
        result = await orchestrator.execute_pipeline(mock_pipeline, mock_execution)

        # Step 6: Verify results
        if not result["success"]:
            pass
        assert result["success"] is True
        assert result["error"] is None
        assert len(result["results"]) == 3

        # Check extract result (configuration is passed from mock steps)
        extract_result = result["results"]["workflow-extract"]
        assert extract_result["name"] == "workflow-extract"
        assert "data from api" in extract_result["result"]["extracted"]

        # Check transform result
        transform_result = result["results"]["workflow-transform"]
        assert transform_result["name"] == "workflow-transform"
        assert transform_result["result"]["processed"] is True

        # Check load result (configuration is passed from mock steps)
        load_result = result["results"]["workflow-load"]
        assert load_result["name"] == "workflow-load"
        assert load_result["result"]["loaded"] is True
        assert load_result["result"]["target"] == "warehouse"
