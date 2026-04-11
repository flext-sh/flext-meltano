"""Simple working example using ONLY real FLEXT Meltano APIs.

This example demonstrates the actual working functionality that exists,
using only classes and functions that are actually exported from flext_meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from examples import c, u
from flext_meltano import meltano

logger = u.fetch_logger(__name__)


def simple_api_example() -> None:
    """Example using the public Meltano facade."""
    version_result = meltano.get_version()
    if version_result.success:
        logger.info("Meltano version: %s", version_result.value)
    discovery_result = meltano.discover_installed_plugins()
    if discovery_result.success:
        logger.info(
            "Found %s installed plugins",
            len(discovery_result.value),
        )


def simple_component_example() -> None:
    """Example using canonical component factories."""
    tap_result = meltano.Tap("tap-csv")
    target_result = meltano.Target("target-jsonl")
    dbt_result = meltano.Dbt("analytics")
    if tap_result.success:
        logger.info("Tap source: %s", tap_result.value.source_name)
    if target_result.success:
        logger.info("Target sink: %s", target_result.value.sink_name)
    if dbt_result.success:
        logger.info("DBT transformation: %s", dbt_result.value.transformation_name)


def simple_runtime_example() -> None:
    """Example using the public runtime command surface."""
    result = meltano.execute_meltano_command([
        c.Meltano.CMD_BINARY,
        c.Meltano.ExecutorCommand.VERSION,
    ])
    if result.success:
        logger.info("Runtime command result: %s", result.value)


def simple_config_example() -> None:
    """Example using typed settings through the public facade."""
    logger.info("Config created: %s", meltano.settings)
    logger.info("Environment: %s", meltano.settings.environment)


if __name__ == "__main__":
    logger.info("=== FLEXT Meltano Simple Working Examples ===")
    try:
        simple_api_example()
        logger.info("")
        simple_component_example()
        logger.info("")
        simple_runtime_example()
        logger.info("")
        simple_config_example()
    except (ValueError, RuntimeError, OSError):
        logger.exception("Error executing examples")
