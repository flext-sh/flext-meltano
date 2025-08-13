"""DBT Model Registry for FLEXT Ecosystem.

Provides a central registry for reusable DBT models, macros, and seeds
across the FLEXT ecosystem.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path

from flext_core import FlextResult, get_logger
from jinja2 import Environment

logger = get_logger(__name__)


@dataclass
class FlextDbtModel:
    """Represents a reusable DBT model.

    Attributes:
        name: Model name (e.g., 'stg_ldap_users')
        package: Source package (e.g., 'flext-dbt-ldap')
        sql: SQL template with Jinja2 placeholders
        description: Model description
        columns: Column definitions
        tags: Model tags for categorization
        config: DBT model configuration
        dependencies: Other models this depends on

    """

    name: str
    package: str
    sql: str
    description: str = ""
    columns: dict[str, dict[str, object]] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    config: dict[str, object] = field(default_factory=dict)
    dependencies: list[str] = field(default_factory=list)

    @property
    def model_id(self) -> str:
        """Generate unique model ID."""
        return f"{self.package}.{self.name}"

    @property
    def checksum(self) -> str:
        """Calculate model checksum for change detection."""
        content = f"{self.sql}{json.dumps(self.columns, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()

    def to_dict(self) -> dict[str, object]:
        """Convert model to dictionary."""
        return {
            "name": self.name,
            "package": self.package,
            "sql": self.sql,
            "description": self.description,
            "columns": self.columns,
            "tags": self.tags,
            "config": self.config,
            "dependencies": self.dependencies,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> FlextDbtModel:
        """Create model from dictionary."""
        name = str(data.get("name", ""))
        package = str(data.get("package", ""))
        sql = str(data.get("sql", ""))
        description = str(data.get("description", ""))
        columns = data.get("columns", {})
        tags = data.get("tags", [])
        config = data.get("config", {})
        dependencies = data.get("dependencies", [])

        return cls(
            name=name,
            package=package,
            sql=sql,
            description=description,
            columns=columns if isinstance(columns, dict) else {},
            tags=[str(t) for t in tags] if isinstance(tags, list) else [],
            config=config if isinstance(config, dict) else {},
            dependencies=[str(d) for d in dependencies]
            if isinstance(dependencies, list)
            else [],
        )


class FlextDbtModelRegistry:
    """Registry for reusable DBT models.

    Manages a catalog of DBT models that can be reused across
    different FLEXT projects.
    """

    def __init__(self, registry_path: Path | None = None) -> None:
        """Initialize model registry.

        Args:
            registry_path: Path to model registry file

        """
        self.registry_path = registry_path or Path.home() / ".flext" / "dbt_models.json"
        self.models: dict[str, FlextDbtModel] = {}
        self.jinja_env = Environment(autoescape=True)
        self._load_registry()

    def _load_registry(self) -> None:
        """Load model registry from disk."""
        if self.registry_path.exists():
            try:
                with self.registry_path.open() as f:
                    data = json.load(f)
                    for model_data in data.get("models", []):
                        model = FlextDbtModel.from_dict(model_data)
                        self.models[model.model_id] = model
                logger.info(f"Loaded {len(self.models)} models from registry")
            except Exception:
                logger.exception("Failed to load model registry")

    def _save_registry(self) -> FlextResult[None]:
        """Save model registry to disk."""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "models": [model.to_dict() for model in self.models.values()],
            }
            with self.registry_path.open("w") as f:
                json.dump(data, f, indent=2)
            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Failed to save model registry: {e}")

    def register_model(self, model: FlextDbtModel) -> FlextResult[None]:
        """Register a reusable DBT model.

        Args:
            model: Model to register

        Returns:
            FlextResult indicating success or failure

        """
        try:
            model_id = model.model_id

            # Check for changes
            if model_id in self.models:
                existing = self.models[model_id]
                if existing.checksum != model.checksum:
                    logger.warning(
                        f"Model {model_id} has changed, updating registry",
                    )

            self.models[model_id] = model
            logger.info(f"Registered model: {model_id}")

            # Save registry
            return self._save_registry()

        except Exception as e:
            return FlextResult.fail(f"Failed to register model: {e}")

    def get_model(self, name: str) -> FlextResult[FlextDbtModel]:
        """Get a model from the registry.

        Args:
            name: Model name or model_id

        Returns:
            FlextResult with model if found

        """
        # Try direct lookup
        if name in self.models:
            return FlextResult.ok(self.models[name])

        # Try by name only
        for model in self.models.values():
            if model.name == name:
                return FlextResult.ok(model)

        return FlextResult.fail(f"Model {name} not found")

    def compile_model(
        self,
        model: FlextDbtModel,
        context: dict[str, object],
    ) -> FlextResult[str]:
        """Compile a model with given context.

        Args:
            model: Model to compile
            context: Jinja2 context for rendering

        Returns:
            FlextResult with compiled SQL

        """
        try:
            template = self.jinja_env.from_string(model.sql)
            compiled_sql = template.render(**context)

            logger.debug(f"Compiled model {model.model_id}")
            return FlextResult.ok(compiled_sql)

        except Exception as e:
            return FlextResult.fail(f"Failed to compile model: {e}")

    def search_models(
        self,
        package: str | None = None,
        tags: list[str] | None = None,
    ) -> list[FlextDbtModel]:
        """Search for models by criteria.

        Args:
            package: Filter by package name
            tags: Filter by tags (models must have all specified tags)

        Returns:
            List of matching models

        """
        results = []

        for model in self.models.values():
            # Filter by package
            if package and model.package != package:
                continue

            # Filter by tags
            if tags and not all(tag in model.tags for tag in tags):
                continue

            results.append(model)

        logger.info(f"Found {len(results)} models matching criteria")
        return results

    def get_model_dependencies(
        self,
        model_name: str,
    ) -> FlextResult[list[FlextDbtModel]]:
        """Get all dependencies for a model.

        Args:
            model_name: Model name or ID

        Returns:
            FlextResult with ordered list of dependencies

        """
        try:
            # Get the model
            model_result = self.get_model(model_name)
            if not model_result.success:
                error_msg = model_result.error or f"Model {model_name} not found"
                return FlextResult.fail(error_msg)

            model = model_result.data
            if not model:
                return FlextResult.fail(f"Model {model_name} data is None")
            resolved: list[FlextDbtModel] = []
            visited: set[str] = set()

            def _resolve(dep_name: str) -> None:
                if dep_name in visited:
                    return
                visited.add(dep_name)

                dep_result = self.get_model(dep_name)
                if dep_result.success and dep_result.data:
                    dep_model = dep_result.data
                    for sub_dep in dep_model.dependencies:
                        _resolve(sub_dep)
                    resolved.append(dep_model)

            for dep in model.dependencies:
                _resolve(dep)

            return FlextResult.ok(resolved)

        except Exception as e:
            return FlextResult.fail(f"Failed to get dependencies: {e}")

    def list_models(self) -> list[FlextDbtModel]:
        """List all registered models.

        Returns:
            List of all models

        """
        return list(self.models.values())


def create_model_registry(
    registry_path: Path | None = None,
) -> FlextDbtModelRegistry:
    """Create a new model registry instance.

    Args:
        registry_path: Optional path to registry file

    Returns:
        FlextDbtModelRegistry instance

    """
    return FlextDbtModelRegistry(registry_path)
