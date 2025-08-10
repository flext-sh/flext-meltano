"""DBT Package Manager for FLEXT Ecosystem.

Manages DBT packages across the FLEXT ecosystem, providing package
registration, dependency resolution, and version management.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from flext_core import FlextResult, get_logger

logger = get_logger(__name__)


@dataclass
class FlextDbtPackage:
    """Represents a DBT package in the FLEXT ecosystem.

    Attributes:
        name: Package name (e.g., 'flext-dbt-ldap')
        version: Semantic version (e.g., '1.0.0')
        models: List of model paths in the package
        macros: List of macro names provided
        seeds: List of seed data files
        dependencies: Other packages this depends on
        metadata: Additional package metadata

    """

    name: str
    version: str
    models: list[str] = field(default_factory=list)
    macros: list[str] = field(default_factory=list)
    seeds: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    metadata: dict[str, object] = field(default_factory=dict)

    def to_dict(self) -> dict[str, object]:
        """Convert package to dictionary representation."""
        return {
            "name": self.name,
            "version": self.version,
            "models": self.models,
            "macros": self.macros,
            "seeds": self.seeds,
            "dependencies": self.dependencies,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, object]) -> FlextDbtPackage:
        """Create package from dictionary."""
        name = str(data.get("name", ""))
        version = str(data.get("version", ""))
        models = data.get("models", [])
        macros = data.get("macros", [])
        seeds = data.get("seeds", [])
        dependencies = data.get("dependencies", [])
        metadata = data.get("metadata", {})

        return cls(
            name=name,
            version=version,
            models=[str(m) for m in models] if isinstance(models, list) else [],
            macros=[str(m) for m in macros] if isinstance(macros, list) else [],
            seeds=[str(s) for s in seeds] if isinstance(seeds, list) else [],
            dependencies=[str(d) for d in dependencies] if isinstance(dependencies, list) else [],
            metadata=metadata if isinstance(metadata, dict) else {},
        )


class FlextDbtPackageManager:
    """Manages DBT packages in the FLEXT ecosystem.

    Provides functionality for package registration, dependency resolution,
    and version management across flext-dbt-* projects.
    """

    def __init__(self, registry_path: Path | None = None) -> None:
        """Initialize package manager.

        Args:
            registry_path: Path to package registry file

        """
        self.registry_path = registry_path or Path.home() / ".flext" / "dbt_packages.json"
        self.packages: dict[str, FlextDbtPackage] = {}
        self._load_registry()

    def _load_registry(self) -> None:
        """Load package registry from disk."""
        if self.registry_path.exists():
            try:
                with self.registry_path.open() as f:
                    data = json.load(f)
                    for pkg_data in data.get("packages", []):
                        pkg = FlextDbtPackage.from_dict(pkg_data)
                        self.packages[pkg.name] = pkg
                logger.info(f"Loaded {len(self.packages)} packages from registry")
            except Exception:
                logger.exception("Failed to load registry")

    def _save_registry(self) -> FlextResult[None]:
        """Save package registry to disk."""
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            data = {
                "packages": [pkg.to_dict() for pkg in self.packages.values()],
            }
            with self.registry_path.open("w") as f:
                json.dump(data, f, indent=2)
            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Failed to save registry: {e}")

    def register_package(self, package: FlextDbtPackage) -> FlextResult[None]:
        """Register a new DBT package.

        Args:
            package: Package to register

        Returns:
            FlextResult indicating success or failure

        """
        try:
            # Check for version conflicts
            if package.name in self.packages:
                existing = self.packages[package.name]
                if existing.version != package.version:
                    logger.warning(
                        f"Updating package {package.name} from "
                        f"v{existing.version} to v{package.version}",
                    )

            self.packages[package.name] = package
            logger.info(f"Registered package: {package.name} v{package.version}")

            # Save to registry
            return self._save_registry()

        except Exception as e:
            return FlextResult.fail(f"Failed to register package: {e}")

    def resolve_dependencies(
        self, project: str,
    ) -> FlextResult[list[FlextDbtPackage]]:
        """Resolve dependencies for a project.

        Args:
            project: Project name to resolve dependencies for

        Returns:
            FlextResult with ordered list of packages (dependencies first)

        """
        try:
            if project not in self.packages:
                return FlextResult.fail(f"Package {project} not found")

            resolved: list[FlextDbtPackage] = []
            visited: set[str] = set()

            def _resolve(pkg_name: str) -> None:
                if pkg_name in visited:
                    return
                visited.add(pkg_name)

                if pkg_name not in self.packages:
                    logger.warning(f"Dependency {pkg_name} not found")
                    return

                pkg = self.packages[pkg_name]
                for dep in pkg.dependencies:
                    _resolve(dep)

                resolved.append(pkg)

            _resolve(project)

            logger.info(
                f"Resolved {len(resolved)} packages for {project}: "
                f"{[p.name for p in resolved]}",
            )

            return FlextResult.ok(resolved)

        except Exception as e:
            return FlextResult.fail(f"Failed to resolve dependencies: {e}")

    def install_package(
        self, package: str, version: str,
    ) -> FlextResult[FlextDbtPackage]:
        """Install a DBT package.

        Args:
            package: Package name to install
            version: Version to install

        Returns:
            FlextResult with installed package

        """
        try:
            # For now, we'll create a placeholder package
            # In production, this would download from a registry
            pkg = FlextDbtPackage(
                name=package,
                version=version,
                models=[],
                macros=[],
                seeds=[],
                dependencies=[],
                metadata={"installed": True},
            )

            # Register the package
            result = self.register_package(pkg)
            if not result.success:
                error_msg = result.error or "Failed to register package"
                return FlextResult.fail(error_msg)

            logger.info(f"Installed package: {package} v{version}")
            return FlextResult.ok(pkg)

        except Exception as e:
            return FlextResult.fail(f"Failed to install package: {e}")

    def get_package(self, name: str) -> FlextResult[FlextDbtPackage]:
        """Get a package by name.

        Args:
            name: Package name

        Returns:
            FlextResult with package if found

        """
        if name in self.packages:
            return FlextResult.ok(self.packages[name])
        return FlextResult.fail(f"Package {name} not found")

    def list_packages(self) -> list[FlextDbtPackage]:
        """List all registered packages.

        Returns:
            List of all packages

        """
        return list(self.packages.values())


def create_package_manager(
    registry_path: Path | None = None,
) -> FlextDbtPackageManager:
    """Create a new package manager instance.

    Args:
        registry_path: Optional path to registry file

    Returns:
        FlextDbtPackageManager instance

    """
    return FlextDbtPackageManager(registry_path)
