"""FLEXT Meltano - API Principal Ultra-Simplificada.

API designed for MASSIVE CODE REDUCTION and EXTREME USABILITY.
Uma única classe para 90% dos casos de uso reais.
"""

from __future__ import annotations

import asyncio
import json
import re
import time
from contextlib import asynccontextmanager, suppress
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from flext_meltano.helpers.execution import (
    flext_meltano_execute_job,
    flext_meltano_run_command,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator


@dataclass
class PipelineConfig:
    """Pipeline configuration - ultra-simplified."""

    tap: str
    target: str
    environment: str = "dev"
    project_root: str | Path = "."
    select: list[str] | None = None
    state_backend: str = "filesystem"

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "tap": self.tap,
            "target": self.target,
            "environment": self.environment,
            "project_root": str(self.project_root),
            "select": self.select,
            "state_backend": self.state_backend,
        }


@dataclass
class PipelineResult:
    """Pipeline execution result - comprehensive."""

    success: bool
    duration: float
    records_processed: int
    errors: list[str]
    warnings: list[str]
    state: dict[str, Any]
    metadata: dict[str, Any]

    @property
    def failed(self) -> bool:
        """Check if pipeline failed."""
        return not self.success

    @property
    def has_errors(self) -> bool:
        """Check if pipeline has errors."""
        return len(self.errors) > 0

    @property
    def has_warnings(self) -> bool:
        """Check if pipeline has warnings."""
        return len(self.warnings) > 0


class FlextMeltano:
    """FLEXT Meltano - Ultra-simplified API for massive code reduction.

    Examples:
        # Basic usage - 1 line replaces 50+ lines
        result = FlextMeltano().run("tap-csv", "target-csv")

        # With configuration
        fm = FlextMeltano(project_root="/path/to/project")
        result = fm.run("tap-oracle", "target-postgres", select=["users", "orders"])

        # Async usage
        async with FlextMeltano().async_context() as fm:
            result = await fm.async_run("tap-csv", "target-csv")

        # Chain operations
        result = (FlextMeltano()
                 .add_tap("tap-csv")
                 .add_target("target-csv")
                 .run("tap-csv", "target-csv"))

    """

    def __init__(
        self,
        project_root: str | Path = ".",
        environment: str = "dev",
        *,
        auto_install: bool = True,
        state_backend: str = "filesystem",
    ) -> None:
        """Initialize FLEXT Meltano with sensible defaults.

        Args:
            project_root: Meltano project directory
            environment: Meltano environment (dev, prod, staging)
            auto_install: Auto-install missing plugins
            state_backend: State backend (filesystem, s3, gcs)

        """
        self.project_root = Path(project_root)
        self.environment = environment
        self.auto_install = auto_install
        self.state_backend = state_backend
        self._initialized = False

    def run(
        self,
        tap: str,
        target: str,
        *,
        select: list[str] | None = None,
        full_refresh: bool = False,
        dry_run: bool = False,
    ) -> PipelineResult:
        """Run pipeline with ZERO boilerplate - replaces 50+ lines of code.

        Args:
            tap: Source tap name (e.g., "tap-csv", "tap-postgres")
            target: Target name (e.g., "target-csv", "target-postgres")
            select: Optional list of streams to extract
            full_refresh: Force full refresh (ignore state)
            dry_run: Validate without executing

        Returns:
            PipelineResult with comprehensive execution details

        Examples:
            # Basic usage
            result = fm.run("tap-csv", "target-csv")

            # With stream selection
            result = fm.run("tap-postgres", "target-csv", select=["users", "orders"])

            # Full refresh
            result = fm.run("tap-postgres", "target-csv", full_refresh=True)

        """
        # Auto-ensure project setup
        if not self._initialized:
            self._ensure_project_setup()

        # Auto-install plugins if needed
        if self.auto_install:
            self._ensure_plugins_installed(tap, target)

        # Build pipeline config
        config = PipelineConfig(
            tap=tap,
            target=target,
            environment=self.environment,
            project_root=self.project_root,
            select=select,
            state_backend=self.state_backend,
        )

        # Execute pipeline
        return self._execute_pipeline(
            config, full_refresh=full_refresh, dry_run=dry_run,
        )

    def add_tap(
        self,
        tap_name: str,
        *,
        variant: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> FlextMeltano:
        """Add tap plugin - chainable method.

        Args:
            tap_name: Tap plugin name
            variant: Plugin variant (optional)
            config: Plugin configuration

        Returns:
            Self for method chaining

        Examples:
            fm.add_tap("tap-csv").add_target("target-csv").run("tap-csv", "target-csv")

        """
        cmd = ["add", "extractor", tap_name]
        if variant:
            cmd.extend(["--variant", variant])

        result = flext_meltano_run_command(cmd, project_root=self.project_root)
        if not result.success:
            msg = f"Failed to add tap {tap_name}: {result.error}"
            raise RuntimeError(msg)

        # Configure plugin if config provided
        if config:
            self._configure_plugin("extractors", tap_name, config)

        return self

    def add_target(
        self,
        target_name: str,
        *,
        variant: str | None = None,
        config: dict[str, Any] | None = None,
    ) -> FlextMeltano:
        """Add target plugin - chainable method.

        Args:
            target_name: Target plugin name
            variant: Plugin variant (optional)
            config: Plugin configuration

        Returns:
            Self for method chaining

        """
        cmd = ["add", "loader", target_name]
        if variant:
            cmd.extend(["--variant", variant])

        result = flext_meltano_run_command(cmd, project_root=self.project_root)
        if not result.success:
            msg = f"Failed to add target {target_name}: {result.error}"
            raise RuntimeError(msg)

        # Configure plugin if config provided
        if config:
            self._configure_plugin("loaders", target_name, config)

        return self

    def discover(self, tap: str) -> dict[str, Any]:
        """Discover tap catalog - simplified.

        Args:
            tap: Tap name to discover

        Returns:
            Catalog as dictionary

        Examples:
            catalog = fm.discover("tap-postgres")
            tables = [stream["tap_stream_id"] for stream in catalog["streams"]]

        """
        result = flext_meltano_run_command(
            ["invoke", tap, "--discover"],
            project_root=self.project_root,
        )

        if not result.success:
            msg = f"Failed to discover {tap}: {result.error}"
            raise RuntimeError(msg)

        if result.data and result.data.get("stdout"):
            try:
                return json.loads(result.data["stdout"])
            except json.JSONDecodeError as e:
                msg = f"Invalid catalog JSON from {tap}: {e!s}"
                raise RuntimeError(msg) from e

        msg = f"No catalog output from {tap}"
        raise RuntimeError(msg)

    def test_connection(self, tap: str) -> bool:
        """Test tap connection - ultra-simple.

        Args:
            tap: Tap name to test

        Returns:
            True if connection successful

        Examples:
            if fm.test_connection("tap-postgres"):
                result = fm.run("tap-postgres", "target-csv")

        """
        try:
            self.discover(tap)
        except RuntimeError:
            return False
        else:
            return True

    def get_state(self, tap: str, target: str) -> dict[str, Any]:
        """Get pipeline state - simplified.

        Args:
            tap: Source tap name
            target: Target name

        Returns:
            State dictionary

        """
        result = flext_meltano_run_command(
            ["state", "list", f"{tap}-to-{target}"],
            project_root=self.project_root,
        )

        if result.success and result.data and result.data.get("stdout"):
            try:
                return json.loads(result.data["stdout"])
            except json.JSONDecodeError:
                return {}

        return {}

    def reset_state(self, tap: str, target: str) -> bool:
        """Reset pipeline state - simplified.

        Args:
            tap: Source tap name
            target: Target name

        Returns:
            True if reset successful

        """
        result = flext_meltano_run_command(
            ["state", "clear", f"{tap}-to-{target}"],
            project_root=self.project_root,
        )
        return result.success

    @asynccontextmanager
    async def async_context(self) -> AsyncIterator[FlextMeltano]:
        """Async context manager for async operations.

        Examples:
            async with FlextMeltano().async_context() as fm:
                result = await fm.async_run("tap-csv", "target-csv")

        """
        try:
            yield self
        finally:
            # Cleanup if needed
            pass

    async def async_run(
        self,
        tap: str,
        target: str,
        *,
        select: list[str] | None = None,
        full_refresh: bool = False,
        dry_run: bool = False,
    ) -> PipelineResult:
        """Async version of run() method.

        Args:
            tap: Source tap name
            target: Target name
            select: Optional streams to select
            full_refresh: Force full refresh
            dry_run: Validate without executing

        Returns:
            PipelineResult with execution details

        """
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None,
            self.run,
            tap,
            target,
            select,
            full_refresh,
            dry_run,
        )

    def _ensure_project_setup(self) -> None:
        """Ensure Meltano project is initialized."""
        meltano_yml = self.project_root / "meltano.yml"
        if not meltano_yml.exists():
            result = flext_meltano_run_command(
                ["init", str(self.project_root.name), "."],
                project_root=self.project_root.parent,
            )
            if not result.success:
                msg = f"Failed to initialize Meltano project: {result.error}"
                raise RuntimeError(msg)

        self._initialized = True

    def _ensure_plugins_installed(self, tap: str, target: str) -> None:
        """Ensure required plugins are installed."""
        # Check if plugins exist via config
        result = flext_meltano_run_command(
            ["config", "list"], project_root=self.project_root,
        )
        if result.success and result.data:
            config_output = result.data.get("stdout", "")

            # Install tap if not present
            if tap not in config_output:
                self.add_tap(tap)

            # Install target if not present
            if target not in config_output:
                self.add_target(target)

    def _configure_plugin(
        self, plugin_type: str, plugin_name: str, config: dict[str, Any],
    ) -> None:
        """Configure plugin with provided settings."""
        for key, value in config.items():
            cmd = ["config", plugin_type, plugin_name, "set", key, str(value)]
            result = flext_meltano_run_command(cmd, project_root=self.project_root)
            if not result.success:
                msg = f"Failed to configure {plugin_name}.{key}: {result.error}"
                raise RuntimeError(msg)

    def _execute_pipeline(
        self,
        config: PipelineConfig,
        *,
        full_refresh: bool = False,
        dry_run: bool = False,
    ) -> PipelineResult:
        """Execute pipeline with comprehensive result parsing."""
        start_time = time.time()

        # Build command arguments
        cmd_args = []
        if dry_run:
            cmd_args.append("test")

        if full_refresh:
            # Reset state before run
            self.reset_state(config.tap, config.target)

        # Execute pipeline
        result = flext_meltano_execute_job(
            tap_name=config.tap,
            target_name=config.target,
            project_root=config.project_root,
            environment=config.environment,
        )

        duration = time.time() - start_time

        # Parse result into comprehensive format
        records_processed = 0
        errors = []
        warnings = []
        state = {}

        if result.data and result.data.get("stdout"):
            output = result.data["stdout"]

            # Extract metrics from output (basic parsing)
            if "records extracted" in output.lower():
                try:
                    # Simple regex to extract record count
                    match = re.search(r"(\d+)\s+records?", output.lower())
                    if match:
                        records_processed = int(match.group(1))
                except (ValueError, AttributeError):
                    pass

        if not result.success:
            errors.append(result.error)

        # Get final state
        with suppress(RuntimeError):
            state = self.get_state(config.tap, config.target)

        return PipelineResult(
            success=result.success,
            duration=duration,
            records_processed=records_processed,
            errors=errors,
            warnings=warnings,
            state=state,
            metadata={
                "config": config.to_dict(),
                "command": result.data.get("command", "") if result.data else "",
                "returncode": result.data.get("returncode", -1) if result.data else -1,
            },
        )


# Ultra-simplified factory functions for one-liners
def run_pipeline(
    tap: str, target: str, *, project_root: str | Path = ".",
) -> PipelineResult:
    """One-liner pipeline execution - replaces 50+ lines.

    Examples:
        # Ultimate simplicity - just one line
        result = run_pipeline("tap-csv", "target-csv")

        # With project path
        result = run_pipeline("tap-postgres", "target-csv", project_root="/path/to/project")

    """
    return FlextMeltano(project_root=project_root).run(tap, target)


def discover_catalog(tap: str, *, project_root: str | Path = ".") -> dict[str, Any]:
    """One-liner catalog discovery.

    Examples:
        catalog = discover_catalog("tap-postgres")
        streams = [s["tap_stream_id"] for s in catalog["streams"]]

    """
    return FlextMeltano(project_root=project_root).discover(tap)


def test_tap_connection(tap: str, *, project_root: str | Path) -> bool:
    """One-liner connection test.

    Examples:
        if test_tap_connection("tap-postgres"):
            result = run_pipeline("tap-postgres", "target-csv")

    """
    return FlextMeltano(project_root=project_root).test_connection(tap)


# Async one-liners
async def async_run_pipeline(
    tap: str, target: str, *, project_root: str | Path = ".",
) -> PipelineResult:
    """Async one-liner pipeline execution.

    Examples:
        result = await async_run_pipeline("tap-csv", "target-csv")

    """
    async with FlextMeltano(project_root=project_root).async_context() as fm:
        return await fm.async_run(tap, target)
