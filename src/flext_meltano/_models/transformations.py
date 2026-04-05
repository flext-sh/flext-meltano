"""FLEXT Meltano models - Transformation models."""

from __future__ import annotations

from typing import Annotated, Self

from flext_cli import FlextCliModels, u
from pydantic import Field, computed_field, model_validator

from flext_meltano import c, t


class FlextMeltanoModelsTransformations:
    """Transformation project and execution models."""

    class DbtProjectModel(FlextCliModels.Entity):
        """Generic DBT project configuration with validation."""

        name: Annotated[str, Field(description="DBT project name")]
        profile: Annotated[str, Field(description="DBT profile name")]
        dbt_version: Annotated[
            str, Field(default="1.0.0", description="DBT project version")
        ] = "1.0.0"
        config: Annotated[
            t.ContainerMapping, Field(description="DBT project configuration")
        ] = Field(default_factory=dict, description="DBT project configuration")
        models: Annotated[
            t.ContainerMapping, Field(description="DBT models configuration")
        ] = Field(default_factory=dict, description="DBT models configuration")
        sources: Annotated[
            t.ContainerMapping, Field(description="DBT sources configuration")
        ] = Field(default_factory=dict, description="DBT sources configuration")
        tests: Annotated[
            t.ContainerMapping, Field(description="DBT tests configuration")
        ] = Field(default_factory=dict, description="DBT tests configuration")

        @model_validator(mode="after")
        def validate_dbt_project(self) -> Self:
            """Validate DBT project configuration consistency."""
            if not self.name or not self.name.strip():
                msg = "name cannot be empty"
                raise ValueError(msg)

            if not self.profile or not self.profile.strip():
                msg = "profile cannot be empty"
                raise ValueError(msg)

            return self

    class TransformationProjectModel(FlextCliModels.Entity):
        """Generic transformation project configuration with validation."""

        name: Annotated[t.NonEmptyStr, Field(description="Project name")]
        transformation_version: Annotated[str, Field(description="Project version")]
        profile: Annotated[str, Field(description="Profile name")]
        model_paths: Annotated[
            t.StrSequence,
            Field(default=["models"], description="Model paths"),
        ] = Field(default=["models"], description="Model paths")
        analysis_paths: Annotated[
            t.StrSequence,
            Field(default=["analysis"], description="Analysis paths"),
        ] = Field(default=["analysis"], description="Analysis paths")
        test_paths: Annotated[
            t.StrSequence,
            Field(default=["tests"], description="Test paths"),
        ] = Field(default=["tests"], description="Test paths")
        seed_paths: Annotated[
            t.StrSequence,
            Field(default=["seeds"], description="Seed paths"),
        ] = Field(default=["seeds"], description="Seed paths")
        macro_paths: Annotated[
            t.StrSequence,
            Field(default=["macros"], description="Macro paths"),
        ] = Field(default=["macros"], description="Macro paths")

        @computed_field
        def has_custom_paths(self) -> bool:
            """Check if project has custom paths."""
            default_paths = {"models", "analysis", "tests", "seeds", "macros"}
            all_paths = {
                *self.model_paths,
                *self.analysis_paths,
                *self.test_paths,
                *self.seed_paths,
                *self.macro_paths,
            }
            return bool(all_paths - default_paths)

        @computed_field
        def project_structure_complexity(self) -> str:
            """Project structure complexity."""
            # Use u.count() for unified counting (DSL pattern)
            total_path_count = (
                u.count(self.model_paths)
                + u.count(self.analysis_paths)
                + u.count(self.test_paths)
                + u.count(self.seed_paths)
                + u.count(self.macro_paths)
            )
            if total_path_count <= c.Meltano.VALIDATION_STRUCTURE_SIMPLE_MAX_PATHS:
                return "simple"
            if total_path_count <= c.Meltano.VALIDATION_STRUCTURE_MODERATE_MAX_PATHS:
                return "moderate"
            return "complex"

        @computed_field
        def total_path_count(self) -> int:
            """Total number of configured paths."""
            # Use u.count() for unified counting (DSL pattern)
            return (
                u.count(self.model_paths)
                + u.count(self.analysis_paths)
                + u.count(self.test_paths)
                + u.count(self.seed_paths)
                + u.count(self.macro_paths)
            )

        @model_validator(mode="after")
        def validate_project_consistency(self) -> Self:
            """Validate project consistency."""
            if not self.model_paths:
                msg = "Project must have at least one model path"
                raise ValueError(msg)

            return self

    class TransformationExecutionModel(FlextCliModels.Entity):
        """Generic transformation execution configuration with validation."""

        command: Annotated[str, Field(description="Command to execute")]
        models: Annotated[
            t.StrSequence,
            Field(description="Models to execute"),
        ] = Field(default_factory=list, description="Models to execute")
        exclude: Annotated[
            t.StrSequence,
            Field(description="Models to exclude"),
        ] = Field(default_factory=list, description="Models to exclude")
        full_refresh: Annotated[
            bool,
            Field(default=False, description="Full refresh execution"),
        ] = False
        fail_fast: Annotated[
            bool,
            Field(default=True, description="Fail fast on first error"),
        ] = True
        threads: Annotated[
            t.WorkerCount,
            Field(default=1, description="Number of threads to use"),
        ] = 1

        @computed_field
        def exclude_count(self) -> int:
            """Number of models to exclude."""
            return len(self.exclude)

        @computed_field
        def execution_complexity(self) -> str:
            """Execution complexity assessment."""
            total_scope = len(self.models) + len(self.exclude)
            if total_scope == 0:
                return "full_project"
            if total_scope <= c.Meltano.VALIDATION_DBT_SIMPLE_EXECUTION_THRESHOLD:
                return "simple"
            if total_scope <= c.Meltano.VALIDATION_MAX_WORKERS_THRESHOLD:
                return "moderate"
            return "complex"

        @computed_field
        def is_parallel_execution(self) -> bool:
            """Check if execution uses multiple threads."""
            return self.threads > 1

        @computed_field
        def model_count(self) -> int:
            """Number of models to execute."""
            return len(self.models)

        @model_validator(mode="after")
        def validate_execution_consistency(self) -> Self:
            """Validate execution consistency."""
            max_threads = (
                c.Meltano.VALIDATION_MAX_WORKERS_THRESHOLD // 3
            )  # ~33, reasonable thread limit
            if self.threads > max_threads:
                msg = f"Thread count cannot exceed {max_threads}"
                raise ValueError(msg)

            model_set = set(self.models)
            exclude_set = set(self.exclude)
            overlap = model_set & exclude_set
            if overlap:
                msg = f"Models cannot be both included and excluded: {overlap}"
                raise ValueError(msg)

            return self
