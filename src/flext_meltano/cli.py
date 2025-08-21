"""CLI Interface - Command line interface for FLEXT Meltano.

FUNÇÃO 2: Runtime CLI interface
- FlextMeltanoCli: CLI wrapper for Go services
"""

from __future__ import annotations

import sys

from flext_core import get_logger

from .runtime import FlextMeltanoExecutor
from .go_bridge import FlextMeltanoBridge

logger = get_logger(__name__)


class FlextMeltanoCli:
    """CLI interface for FLEXT Meltano operations."""

    def __init__(self) -> None:
        self.bridge = FlextMeltanoBridge()
        self.executor = FlextMeltanoExecutor()

    def run_command(self, args: list[str]) -> int:
        """Run CLI command and return exit code."""
        if not args:
            self._print_help()
            return 1

        command = args[0]

        try:
            if command == "version":
                result = self.bridge.get_version()
                if result["success"]:
                    print(f"FLEXT Meltano v{result['data']['flext_meltano']}")
                    return 0
                else:
                    print(f"Error: {result['error']}", file=sys.stderr)
                    return 1

            elif command == "plugins":
                result = self.bridge.list_plugins()
                if result["success"]:
                    plugins = result["data"]
                    print(f"Available plugins: {len(plugins)}")
                    for plugin in plugins[:5]:  # Show first 5
                        print(f"  - {plugin['name']} ({plugin['type']})")
                    return 0
                else:
                    print(f"Error: {result['error']}", file=sys.stderr)
                    return 1

            elif command == "run" and len(args) >= 3:
                tap_name, target_name = args[1], args[2]
                project_root = args[3] if len(args) > 3 else "."

                result = self.bridge.run_pipeline(tap_name, target_name, project_root)
                if result["success"]:
                    print(
                        f"Pipeline {tap_name} -> {target_name} completed successfully"
                    )
                    return 0
                else:
                    print(f"Error: {result['error']}", file=sys.stderr)
                    return 1

            else:
                self._print_help()
                return 1

        except Exception as e:
            print(f"CLI Error: {e}", file=sys.stderr)
            return 1

    def _print_help(self) -> None:
        """Print CLI help."""
        print("FLEXT Meltano CLI")
        print()
        print("Commands:")
        print("  version                    - Show version information")
        print("  plugins                    - List available plugins")
        print("  run <tap> <target> [dir]   - Run ELT pipeline")


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["FlextMeltanoCli"]
