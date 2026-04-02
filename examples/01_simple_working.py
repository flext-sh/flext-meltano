"""Simple working example using ONLY real FLEXT Meltano APIs.

This example demonstrates the actual working functionality that exists,
using only classes and functions that are actually exported from flext_meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextLogger

from flext_meltano import FlextMeltanoBridge, FlextMeltanoExecutor, FlextMeltanoSettings

logger = FlextLogger(__name__)


def simple_bridge_example() -> None:
    """Example using real MeltanoBridge functionality."""
    bridge = FlextMeltanoBridge()
    version_result = bridge.get_version()
    if version_result.is_success:
        logger.info(f"Meltano version: {version_result.value}")
    discovery_result = bridge.discover_installed_plugins()
    if discovery_result.is_success:
        plugins = discovery_result.value
        logger.info(f"Found {len(plugins)} installed plugins")


def simple_executor_example() -> None:
    """Example using real FlextMeltanoExecutor functionality."""
    executor = FlextMeltanoExecutor(config_overrides={})
    result = executor.execute_meltano_command(["meltano", "version"])
    if result.is_success:
        logger.info(f"Executor result: {result.value}")


def simple_config_example() -> None:
    """Example using real FlextMeltanoSettings functionality."""
    config = FlextMeltanoSettings()
    logger.info("Config created: %s", config)
    logger.info(f"Environment: {getattr(config, 'environment', 'unknown')}")


if __name__ == "__main__":
    logger.info("=== FLEXT Meltano Simple Working Examples ===")
    try:
        simple_bridge_example()
        logger.info("")
        simple_executor_example()
        logger.info("")
        simple_config_example()
    except (ValueError, RuntimeError, OSError):
        logger.exception("Error executing examples")
