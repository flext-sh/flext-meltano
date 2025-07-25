"""FLEXT Meltano Plugin Installation Helpers.

Plugin installation utilities following Clean Architecture patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_meltano.helpers.cli import flext_run_meltano_command
from flext_meltano.helpers.execution import FlextMeltanoResult

if TYPE_CHECKING:
    from pathlib import Path


def flext_meltano_install_plugin(
    plugin_type: str,
    plugin_name: str,
    variant: str | None = None,
    project_root: Path | None = None,
) -> FlextMeltanoResult:
    """Install a Meltano plugin with comprehensive validation.

    Args:
        plugin_type: Type of plugin (extractor, loader, etc.)
        plugin_name: Name of the plugin to install
        variant: Optional plugin variant
        project_root: Meltano project root directory

    Returns:
        FlextMeltanoResult with installation status

    """
    try:
        # Build installation command
        args = ["add", plugin_type, plugin_name]
        if variant:
            args.extend(["--variant", variant])

        result = flext_run_meltano_command(
            args=args,
            project_root=project_root or ".",
        )

        if not result.success:
            return FlextMeltanoResult.fail(
                f"Failed to install plugin {plugin_name}: {result.error}",
            )

        return FlextMeltanoResult.ok(
            {
                "plugin_type": plugin_type,
                "plugin_name": plugin_name,
                "variant": variant or "original",
                "status": "installed",
                "command_output": result.data,
            },
        )

    except (ValueError, TypeError, RuntimeError, OSError) as e:
        return FlextMeltanoResult.fail(f"Plugin installation failed: {e}")
