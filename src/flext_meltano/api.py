"""FLEXT Meltano API - Unified Interface.

Clean API using flext-core patterns.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from flext_core import FlextCommonResult, FlextValueObject

from flext_meltano.constants import FlextMeltanoConstants


class FlextMeltanoPipelineConfig(FlextValueObject):
    """Pipeline configuration."""

    tap_name: str
    target_name: str
    project_root: str = "."
    environment: str = "dev"
    config: dict[str, Any] = {}


class FlextMeltanoPipelineResult(FlextValueObject):
    """Pipeline execution result."""

    success: bool
    data: dict[str, Any] | None = None
    error: str | None = None


class FlextMeltanoAPI:
    """FLEXT Meltano API."""

    def __init__(self, project_root: str = ".") -> None:
        """Initialize API.

        Args:
            project_root: Path to Meltano project root

        """
        self.project_root = Path(project_root)

    def run_pipeline(
        self,
        tap_name: str,
        target_name: str,
        config: dict[str, Any] | None = None,
    ) -> FlextCommonResult[FlextMeltanoPipelineResult]:
        """Run a Meltano pipeline.

        Args:
            tap_name: Name of the tap to run
            target_name: Name of the target to run
            config: Optional configuration overrides

        Returns:
            FlextCommonResult containing pipeline result

        """
        try:
            # Ensure project is set up
            setup_result = self._ensure_project_setup()
            if not setup_result.success:
                return FlextCommonResult.fail(setup_result.error or "Setup failed")

            # Build command
            cmd = [
                "meltano",
                "run",
                tap_name,
                target_name,
            ]

            # Add config if provided
            if config:
                for key, value in config.items():
                    cmd.extend(["--config", f"{key}={value}"])

            # Execute pipeline
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.PIPELINE_TIMEOUT,
            )

            if result.returncode == 0:
                return FlextCommonResult.ok(
                    FlextMeltanoPipelineResult(
                        success=True,
                        data={
                            "output": result.stdout,
                            "tap": tap_name,
                            "target": target_name,
                        },
                    ),
                )
            return FlextCommonResult.ok(
                FlextMeltanoPipelineResult(
                    success=False,
                    error=result.stderr or "Pipeline execution failed",
                    data={"output": result.stdout, "stderr": result.stderr},
                ),
            )

        except subprocess.TimeoutExpired:
            return FlextCommonResult.fail("Pipeline execution timed out")
        except Exception as e:
            return FlextCommonResult.fail(f"Pipeline execution failed: {e}")

    def discover_catalog(
        self,
        tap_name: str,
        config: dict[str, Any] | None = None,
    ) -> FlextCommonResult[dict[str, Any]]:
        """Discover catalog for a tap.

        Args:
            tap_name: Name of the tap
            config: Optional configuration overrides

        Returns:
            FlextCommonResult containing catalog data

        """
        try:
            # Ensure project is set up
            setup_result = self._ensure_project_setup()
            if not setup_result.success:
                return FlextCommonResult.fail(setup_result.error or "Setup failed")

            # Build command
            cmd = ["meltano", "invoke", tap_name, "--discover"]

            # Add config if provided
            if config:
                for key, value in config.items():
                    cmd.extend(["--config", f"{key}={value}"])

            # Execute discovery
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.DISCOVERY_TIMEOUT,
            )

            if result.returncode == 0:
                return FlextCommonResult.ok({"catalog": result.stdout})
            return FlextCommonResult.fail(
                result.stderr or "Catalog discovery failed",
            )

        except subprocess.TimeoutExpired:
            return FlextCommonResult.fail("Catalog discovery timed out")
        except Exception as e:
            return FlextCommonResult.fail(f"Catalog discovery failed: {e}")

    def test_connection(
        self,
        tap_name: str,
        config: dict[str, Any] | None = None,
    ) -> FlextCommonResult[dict[str, Any]]:
        """Test connection for a tap.

        Args:
            tap_name: Name of the tap
            config: Optional configuration overrides

        Returns:
            FlextCommonResult containing test result

        """
        try:
            # Ensure project is set up
            setup_result = self._ensure_project_setup()
            if not setup_result.success:
                return FlextCommonResult.fail(setup_result.error or "Setup failed")

            # Build command
            cmd = ["meltano", "invoke", tap_name, "--test"]

            # Add config if provided
            if config:
                for key, value in config.items():
                    cmd.extend(["--config", f"{key}={value}"])

            # Execute test
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
            )

            if result.returncode == 0:
                return FlextCommonResult.ok({"test_result": result.stdout})
            return FlextCommonResult.fail(
                result.stderr or "Connection test failed",
            )

        except subprocess.TimeoutExpired:
            return FlextCommonResult.fail("Connection test timed out")
        except Exception as e:
            return FlextCommonResult.fail(f"Connection test failed: {e}")

    def install_plugin(
        self,
        plugin_type: str,
        plugin_name: str,
    ) -> FlextCommonResult[dict[str, Any]]:
        """Install a Meltano plugin.

        Args:
            plugin_type: Type of plugin (extractor, loader, etc.)
            plugin_name: Name of the plugin

        Returns:
            FlextCommonResult containing installation result

        """
        try:
            cmd = ["meltano", "add", plugin_type, plugin_name]
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
            )

            if result.returncode == 0:
                return FlextCommonResult.ok({"installed": plugin_name})
            return FlextCommonResult.fail(
                result.stderr or "Plugin installation failed",
            )

        except subprocess.TimeoutExpired:
            return FlextCommonResult.fail("Plugin installation timed out")
        except Exception as e:
            return FlextCommonResult.fail(f"Plugin installation failed: {e}")

    def configure_plugin(
        self,
        plugin_name: str,
        config: dict[str, Any],
    ) -> FlextCommonResult[dict[str, Any]]:
        """Configure a Meltano plugin.

        Args:
            plugin_name: Name of the plugin
            config: Configuration to apply

        Returns:
            FlextCommonResult containing configuration result

        """
        try:
            cmd = ["meltano", "config", plugin_name, "set"]
            for key, value in config.items():
                cmd.extend([key, str(value)])

            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
            )

            if result.returncode == 0:
                return FlextCommonResult.ok({"configured": plugin_name})
            return FlextCommonResult.fail(
                result.stderr or "Plugin configuration failed",
            )

        except subprocess.TimeoutExpired:
            return FlextCommonResult.fail("Plugin configuration timed out")
        except Exception as e:
            return FlextCommonResult.fail(f"Plugin configuration failed: {e}")

    def get_pipeline_state(
        self,
        tap_name: str,
    ) -> FlextCommonResult[dict[str, Any]]:
        """Get pipeline state for a tap.

        Args:
            tap_name: Name of the tap

        Returns:
            FlextCommonResult containing state data

        """
        try:
            cmd = ["meltano", "state", "list", tap_name]
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
            )

            if result.returncode == 0:
                return FlextCommonResult.ok({"state": result.stdout})
            return FlextCommonResult.fail(
                result.stderr or "Failed to get pipeline state",
            )

        except subprocess.TimeoutExpired:
            return FlextCommonResult.fail("Get state timed out")
        except Exception as e:
            return FlextCommonResult.fail(f"Failed to get pipeline state: {e}")

    def reset_pipeline_state(
        self,
        tap_name: str,
    ) -> FlextCommonResult[dict[str, Any]]:
        """Reset pipeline state for a tap.

        Args:
            tap_name: Name of the tap

        Returns:
            FlextCommonResult containing reset result

        """
        try:
            cmd = ["meltano", "state", "clear", tap_name]
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
            )

            if result.returncode == 0:
                return FlextCommonResult.ok({"reset": tap_name})
            return FlextCommonResult.fail(
                result.stderr or "Failed to reset pipeline state",
            )

        except subprocess.TimeoutExpired:
            return FlextCommonResult.fail("Reset state timed out")
        except Exception as e:
            return FlextCommonResult.fail(f"Failed to reset pipeline state: {e}")

    def list_plugins(self) -> FlextCommonResult[dict[str, Any]]:
        """List installed plugins.

        Returns:
            FlextCommonResult containing plugin list

        """
        try:
            cmd = ["meltano", "list"]
            result = subprocess.run(
                cmd,
                check=False,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=FlextMeltanoConstants.COMMAND_TIMEOUT,
            )

            if result.returncode == 0:
                return FlextCommonResult.ok({"plugins": result.stdout})
            return FlextCommonResult.fail(
                result.stderr or "Failed to list plugins",
            )

        except subprocess.TimeoutExpired:
            return FlextCommonResult.fail("List plugins timed out")
        except Exception as e:
            return FlextCommonResult.fail(f"Failed to list plugins: {e}")

    def _ensure_project_setup(self) -> FlextCommonResult[None]:
        """Ensure project is properly set up.

        Returns:
            FlextCommonResult indicating setup status

        """
        try:
            meltano_yml = self.project_root / "meltano.yml"
            if not meltano_yml.exists():
                return FlextCommonResult.fail(
                    f"No meltano.yml found in {self.project_root}",
                )
            return FlextCommonResult.ok(None)
        except Exception as e:
            return FlextCommonResult.fail(f"Project setup check failed: {e}")


# One-liner functions for simplified usage
def run_pipeline(
    tap_name: str,
    target_name: str,
    project_root: str = ".",
    config: dict[str, Any] | None = None,
) -> FlextCommonResult[FlextMeltanoPipelineResult]:
    """Run a Meltano pipeline.

    Args:
        tap_name: Name of the tap to run
        target_name: Name of the target to run
        project_root: Path to Meltano project root
        config: Optional configuration overrides

    Returns:
        FlextCommonResult containing pipeline result

    """
    api = FlextMeltanoAPI(project_root)
    return api.run_pipeline(tap_name, target_name, config)


def discover_catalog(
    tap_name: str,
    project_root: str = ".",
    config: dict[str, Any] | None = None,
) -> FlextCommonResult[dict[str, Any]]:
    """Discover catalog for a tap.

    Args:
        tap_name: Name of the tap
        project_root: Path to Meltano project root
        config: Optional configuration overrides

    Returns:
        FlextCommonResult containing catalog data

    """
    api = FlextMeltanoAPI(project_root)
    return api.discover_catalog(tap_name, config)


def test_connection(
    tap_name: str,
    project_root: str = ".",
    config: dict[str, Any] | None = None,
) -> FlextCommonResult[dict[str, Any]]:
    """Test connection for a tap.

    Args:
        tap_name: Name of the tap
        project_root: Path to Meltano project root
        config: Optional configuration overrides

    Returns:
        FlextCommonResult containing test result

    """
    api = FlextMeltanoAPI(project_root)
    return api.test_connection(tap_name, config)


__all__ = [
    "FlextMeltanoAPI",
    "FlextMeltanoPipelineConfig",
    "FlextMeltanoPipelineResult",
    "discover_catalog",
    "run_pipeline",
    "test_connection",
]
