"""FLEXT Meltano environment manager."""

from __future__ import annotations

from typing import Any

from flext_core import FlextResult

from flext_meltano.environment.models import (
    EnvironmentType,
    FlextMeltanoEnvironment,
)


class FlextMeltanoEnvironmentManager:
    """Manager for FLEXT Meltano environments."""

    def __init__(self) -> None:
        """Initialize environment manager."""
        self._environments: dict[str, FlextMeltanoEnvironment] = {}

    def create_environment(
        self,
        name: str,
        env_type: EnvironmentType,
        config: dict[str, Any] | None = None,
        variables: dict[str, str] | None = None,
    ) -> FlextResult[FlextMeltanoEnvironment]:
        """Create a new environment.

        Args:
            name: Environment name
            env_type: Environment type
            config: Environment configuration
            variables: Environment variables

        Returns:
            FlextResult with created environment

        """
        try:
            if name in self._environments:
                return FlextResult.fail(f"Environment '{name}' already exists")

            environment = FlextMeltanoEnvironment(
                name=name,
                type=env_type,
                config=config or {},
                variables=variables or {},
            )
            self._environments[name] = environment
            return FlextResult.ok(environment)

        except Exception as e:
            return FlextResult.fail(f"Failed to create environment: {e}")

    def get_environment(self, name: str) -> FlextResult[FlextMeltanoEnvironment]:
        """Get environment by name.

        Args:
            name: Environment name

        Returns:
            FlextResult with environment

        """
        if name not in self._environments:
            return FlextResult.fail(f"Environment '{name}' not found")
        return FlextResult.ok(self._environments[name])

    def list_environments(self) -> FlextResult[list[FlextMeltanoEnvironment]]:
        """List all environments.

        Returns:
            FlextResult with list of environments

        """
        return FlextResult.ok(list(self._environments.values()))

    def delete_environment(self, name: str) -> FlextResult[bool]:
        """Delete environment.

        Args:
            name: Environment name

        Returns:
            FlextResult with success status

        """
        if name not in self._environments:
            return FlextResult.fail(f"Environment '{name}' not found")

        del self._environments[name]
        return FlextResult.ok(True)
