"""Simple working example using ONLY real FLEXT Meltano APIs.

This example demonstrates the actual working functionality that exists,
using only classes and functions that are actually exported from flext_meltano.
"""

from pathlib import Path

from flext_core import FlextLogger

# Import ONLY what actually exists
from flext_meltano import (
    FlextMeltanoConfig,
    FlextMeltanoExecutor,
    FlextMeltanoBridge,
)

logger = FlextLogger(__name__)


def simple_bridge_example() -> None:
    """Example using real MeltanoBridge functionality."""
    # Create bridge using real API
    bridge = FlextMeltanoBridge()

    # Get version - this actually works
    version_result = bridge.get_version()
    if version_result.success:
        logger.info(f"Meltano version: {version_result.value}")

    # Discover available plugins - this actually works
    discovery_result = bridge.discover_plugins()
    if discovery_result.success:
        plugins = discovery_result.value
        logger.info(f"Found {len(plugins)} available plugins")


def simple_executor_example() -> None:
    """Example using real FlextMeltanoExecutor functionality."""
    # Create executor with proper Path argument
    executor = FlextMeltanoExecutor(Path.cwd())

    # Execute with required command parameter (string, not list)
    result = executor.execute("version")
    if result.success:
        logger.info(f"Executor result: {result.value}")


def simple_config_example() -> None:
    """Example using real FlextMeltanoConfig functionality."""
    # Create config using real API
    config = FlextMeltanoConfig()

    # Use actual existing method from FlextMeltanoConfig
    logger.info(f"Config created: {config}")

    # Show environment value
    logger.info(f"Environment: {config.environment}")


if __name__ == "__main__":
    logger.info("=== FLEXT Meltano Simple Working Examples ===")

    try:
        simple_bridge_example()
        logger.info("")

        simple_executor_example()
        logger.info("")

        simple_config_example()

    except Exception:
        logger.exception("Error executing examples")
