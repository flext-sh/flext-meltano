"""FLEXT Meltano models - Project configuration models."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Annotated, Self

from flext_cli import m, u

from flext_meltano import c, t


class FlextMeltanoModelsProjects:
    """Project configuration models."""

    class DbtManifestNode(m.FlexibleModel):
        """Parsed dbt manifest node with typed fields."""

        name: Annotated[str | None, m.Field(default=None, description="Node name")]
        path: Annotated[str | None, m.Field(default=None, description="Node path")]
        description: Annotated[
            str | None, m.Field(default=None, description="Node description")
        ] = None
        fqn: t.StrSequence = m.Field(
            default_factory=list, description="Fully qualified name parts"
        )
        resource_type: Annotated[
            str, m.Field(default="", description="Node resource type (model, test, etc.)")
        ] = ""

        @m.computed_field
        def fqn_string(self) -> str:
            """Fully qualified name as dot-separated string."""
            return ".".join(self.fqn) if self.fqn else ""

    class DbtManifest(m.FlexibleModel):
        """Parsed dbt manifest with typed nodes."""

        nodes: Mapping[str, FlextMeltanoModelsProjects.DbtManifestNode] = m.Field(
            default_factory=dict, description="Manifest nodes keyed by node_id"
        )

        def get_nodes_by_type(
            self, resource_type: str
        ) -> Sequence[FlextMeltanoModelsProjects.DbtManifestNode]:
            """Get all nodes of a specific resource type."""
            return [
                node
                for node in self.nodes.values()
                if node.resource_type == resource_type
            ]

    class MeltanoProjectModel(m.Entity):
        """Generic Meltano project configuration with validation."""

        project_id: Annotated[str, m.Field(description="Unique project identifier")]
        project_version: Annotated[
            str, m.Field(default="1", description="Project version")
        ] = "1"
        default_environment: Annotated[
            str, m.Field(default="dev", description="Default environment name")
        ] = "dev"
        plugins: t.FlatContainerMapping = m.Field(
            default_factory=dict, description="Plugin configurations"
        )
        environments: t.FlatContainerMapping = m.Field(
            default_factory=dict, description="Environment configurations"
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
            m.Field(
                default=1,
                ge=1,
                le=1,
                description="Pipeline schema version (only version 1 supported)",
            ),
        ] = 1
        project_id: Annotated[str, m.Field(description="Project ID required")]
        default_environment: Annotated[
            str, m.Field(default="dev", description="Default environment")
        ] = "dev"
        project_root: Path = m.Field(
            default_factory=Path.cwd, description="Project root directory"
        )
        environments: t.StrSequence = m.Field(
            default_factory=lambda: ["dev", "staging", "prod"],
            description="Available environments",
        )

        @m.computed_field
        def environment_count(self) -> int:
            """Number of environments."""
            return u.count(self.environments)

        @m.computed_field
        def has_production_environment(self) -> bool:
            """Check if production environment exists."""
            prod_environments = {"prod", "production", "live"}
            normalized_envs = [
                u.normalize(env, case="lower") for env in self.environments
            ]
            prod_envs_list: t.StrSequence = list(prod_environments)
            return any(u.in_(env, prod_envs_list) for env in normalized_envs)

        @m.computed_field
        def project_maturity(self) -> str:
            """Project maturity assessment."""
            prod_envs = {"prod", "production", "live"}
            normalized_envs = [
                u.normalize(env, case="lower") for env in self.environments
            ]
            prod_envs_list: t.StrSequence = list(prod_envs)
            has_prod = any(u.in_(env, prod_envs_list) for env in normalized_envs)
            env_count = u.count(self.environments)
            if has_prod and env_count >= c.Meltano.VALIDATION_MATURITY_MATURE_ENV_COUNT:
                return "mature"
            if env_count >= c.Meltano.VALIDATION_MATURITY_DEVELOPING_ENV_COUNT:
                return "developing"
            return "basic"

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
