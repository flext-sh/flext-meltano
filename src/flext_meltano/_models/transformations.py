"""FLEXT Meltano models - Transformation models."""

from __future__ import annotations

from typing import Annotated, Self

from flext_cli import m, u

from flext_meltano import c, t


class FlextMeltanoModelsTransformations:
    """Transformation project and execution models."""

    class TransformationProjectModel(m.Entity):
        """Generic transformation project configuration with validation."""

        name: Annotated[t.NonEmptyStr, u.Field(description="Project name")]
        transformation_version: Annotated[str, u.Field(description="Project version")]
        profile: Annotated[str, u.Field(description="Profile name")]
        model_paths: Annotated[
            t.StrSequence,
            u.Field(description="Model paths"),
        ] = u.Field(
            default_factory=lambda: [c.Meltano.DbtPathName.MODELS],
            description="Model paths",
        )
        analysis_paths: Annotated[
            t.StrSequence,
            u.Field(description="Analysis paths"),
        ] = u.Field(
            default_factory=lambda: [c.Meltano.DbtPathName.ANALYSIS],
            description="Analysis paths",
        )
        test_paths: Annotated[
            t.StrSequence,
            u.Field(description="Test paths"),
        ] = u.Field(
            default_factory=lambda: [c.Meltano.DbtPathName.TESTS],
            description="Test paths",
        )
        seed_paths: Annotated[
            t.StrSequence,
            u.Field(description="Seed paths"),
        ] = u.Field(
            default_factory=lambda: [c.Meltano.DbtPathName.SEEDS],
            description="Seed paths",
        )
        macro_paths: Annotated[
            t.StrSequence,
            u.Field(description="Macro paths"),
        ] = u.Field(
            default_factory=lambda: [c.Meltano.DbtPathName.MACROS],
            description="Macro paths",
        )

        @u.computed_field()
        @property
        def has_custom_paths(self) -> bool:
            """Check if project has custom paths."""
            all_paths = {
                *self.model_paths,
                *self.analysis_paths,
                *self.test_paths,
                *self.seed_paths,
                *self.macro_paths,
            }
            return bool(all_paths - c.Meltano.DBT_DEFAULT_PATHS)

        @u.computed_field()
        @property
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
                return str(c.Meltano.ProjectStructureComplexity.SIMPLE)
            if total_path_count <= c.Meltano.VALIDATION_STRUCTURE_MODERATE_MAX_PATHS:
                return str(c.Meltano.ProjectStructureComplexity.MODERATE)
            return str(c.Meltano.ProjectStructureComplexity.COMPLEX)

        @u.computed_field()
        @property
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

        @u.model_validator(mode="after")
        def validate_project_consistency(self) -> Self:
            """Validate project consistency."""
            if not self.model_paths:
                msg = "Project must have at least one model path"
                raise ValueError(msg)

            return self
