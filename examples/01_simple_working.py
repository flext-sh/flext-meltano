"""Simple working example using ONLY real FLEXT Meltano APIs.

This example demonstrates the actual working functionality that exists,
using only classes and functions that are actually exported from flext_meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from flext_core import FlextLogger

# Import ONLY what actually exists
from flext_meltano import (
    FlextMeltanoBridge,
    FlextMeltanoConfig,
    FlextMeltanoExecutor,
)

logger = FlextLogger(__name__)


def simple_bridge_example() -> None:
    """Example using real MeltanoBridge functionality."""
    # Create bridge using real API
    bridge = FlextMeltanoBridge()

    # Get version - this actually works
    version_result = bridge.get_version()
    if version_result.is_success:
        logger.info(f"Meltano version: {version_result.value}")

    # Discover available plugins - this actually works
    discovery_result = bridge.discover_plugins()
    if discovery_result.is_success:
        plugins = discovery_result.value
        logger.info(f"Found {len(plugins)} available plugins")


def simple_executor_example() -> None:
    """Example using real FlextMeltanoExecutor functionality."""
    # Create executor with proper config dict
    executor = FlextMeltanoExecutor(config={})

    # Execute with required command parameter (list of strings)
    result = executor.execute_command(["meltano", "version"])
    if result.is_success:
        logger.info(f"Executor result: {result.value}")


def simple_config_example() -> None:
    """Example using real FlextMeltanoConfig functionality."""
    # Create config using real API
    config = FlextMeltanoConfig()

    # Use actual existing method from FlextMeltanoConfig
    logger.info("Config created: %s", config)

    # Show environment value
    if config is not None:
        logger.info(f"Environment: {getattr(config, 'environment', 'unknown')}")
    else:
        logger.info("Environment: config is None")


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
