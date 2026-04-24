"""FLEXT Meltano models - Project configuration models."""

from __future__ import annotations

from collections.abc import (
    Mapping,
    Sequence,
)
from pathlib import Path
from types import MappingProxyType
from typing import Annotated, Self

from flext_cli import m, u

from flext_meltano import c, t


class FlextMeltanoModelsProjects:
    """Project configuration models."""

    class DbtManifestNode(m.FlexibleModel):
        """Parsed dbt manifest node with typed fields."""

        name: Annotated[str | None, u.Field(default=None, description="Node name")]
        path: Annotated[str | None, u.Field(default=None, description="Node path")]
        description: Annotated[
            str | None, u.Field(default=None, description="Node description")
        ] = None
        fqn: t.StrSequence = u.Field(
            default_factory=tuple,
            description="Fully qualified dbt node path segments",
        )
        resource_type: Annotated[
            str,
            u.Field(default="", description="Node resource type (model, test, etc.)"),
        ] = ""

        @u.computed_field()
        @property
        def fqn_string(self) -> str:
            """Fully qualified name as dot-separated string."""
            return ".".join(self.fqn) if self.fqn else ""

    class DbtManifest(m.FlexibleModel):
        """Parsed dbt manifest with typed nodes."""

        nodes: Mapping[str, FlextMeltanoModelsProjects.DbtManifestNode] = u.Field(
            default_factory=lambda: MappingProxyType({}),
            description="dbt manifest nodes keyed by unique node id",
        )

    class MeltanoProjectModel(m.Entity):
        """Generic Meltano project configuration with validation."""

        project_id: Annotated[str, u.Field(description="Unique project identifier")]
        project_version: Annotated[
            str, u.Field(default="1", description="Project version")
        ] = "1"
        default_environment: Annotated[
            c.Meltano.ProjectEnvironment,
            u.Field(
                default=c.Meltano.METADATA_DEFAULT_ENVIRONMENTS[0],
                description="Default environment name",
            ),
        ] = c.Meltano.METADATA_DEFAULT_ENVIRONMENTS[0]
        plugins: t.JsonMapping = u.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Configured Meltano plugins grouped by plugin category",
        )
        environments: t.JsonMapping = u.Field(
            default_factory=lambda: MappingProxyType({}),
            description="Meltano environment definitions keyed by environment name",
        )

        @u.model_validator(mode="after")
        def validate_meltano_project(self) -> Self:
            """Validate Meltano project configuration consistency."""
            if not self.project_id or not self.project_id.strip():
                msg = "project_id cannot be empty"
                raise ValueError(msg)
            return self

    class PipelineProjectModel(m.Entity):
        """Generic pipeline project configuration with validation."""

        schema_version: Annotated[
            int,
            u.Field(
                default=1,
                ge=1,
                le=1,
                description="Pipeline schema version (only version 1 supported)",
            ),
        ] = 1
        project_id: Annotated[str, u.Field(description="Project ID required")]
        default_environment: Annotated[
            c.Meltano.ProjectEnvironment,
            u.Field(
                default=c.Meltano.METADATA_DEFAULT_ENVIRONMENTS[0],
                description="Default environment",
            ),
        ] = c.Meltano.METADATA_DEFAULT_ENVIRONMENTS[0]
        project_root: Path = u.Field(
            default_factory=Path.cwd, description="Project root directory"
        )
        environments: Sequence[c.Meltano.ProjectEnvironment] = u.Field(
            default_factory=lambda: c.Meltano.METADATA_DEFAULT_ENVIRONMENTS,
            description="Available environments",
        )

        @u.computed_field()
        @property
        def environment_count(self) -> int:
            """Number of environments."""
            return u.count(self.environments)

        @u.computed_field()
        @property
        def has_production_environment(self) -> bool:
            """Check if production environment exists."""
            normalized_envs = [
                u.normalize(env, case="lower") for env in self.environments
            ]
            prod_envs_list: t.StrSequence = list(
                c.Meltano.PRODUCTION_ENVIRONMENT_MARKERS
            )
            return any(u.in_(env, prod_envs_list) for env in normalized_envs)

        @u.computed_field()
        @property
        def project_maturity(self) -> str:
            """Project maturity assessment."""
            normalized_envs = [
                u.normalize(env, case="lower") for env in self.environments
            ]
            prod_envs_list: t.StrSequence = list(
                c.Meltano.PRODUCTION_ENVIRONMENT_MARKERS
            )
            has_prod = any(u.in_(env, prod_envs_list) for env in normalized_envs)
            env_count = u.count(self.environments)
            if has_prod and env_count >= c.Meltano.VALIDATION_MATURITY_MATURE_ENV_COUNT:
                return str(c.Meltano.ProjectMaturity.MATURE)
            if env_count >= c.Meltano.VALIDATION_MATURITY_DEVELOPING_ENV_COUNT:
                return str(c.Meltano.ProjectMaturity.DEVELOPING)
            return str(c.Meltano.ProjectMaturity.BASIC)

        @u.model_validator(mode="after")
        def validate_project_consistency(self) -> Self:
            """Validate project consistency."""
            if self.default_environment not in self.environments:
                msg = (
                    f"Default environment '{self.default_environment}' "
                    f"not in environments list"
                )
                raise ValueError(msg)
            if not self.project_root.exists():
                msg = f"Project root directory does not exist: {self.project_root}"
                raise ValueError(msg)
            return self
