"""Simple working example using ONLY real FLEXT Meltano APIs.

This example demonstrates the actual working functionality that exists,
using only classes and functions that are actually exported from flext_meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from examples import c, u
from flext_meltano import FlextMeltanoSettings, meltano

logger = u.fetch_logger(__name__)


def simple_api_example() -> None:
    """Demonstrate the public Meltano facade."""
    version_result = meltano.fetch_version()
    if version_result.success:
        logger.info("Meltano version: %s", version_result.value)
    discovery_result = meltano.discover_installed_plugins()
    if discovery_result.success:
        logger.info("Found %s installed plugins", len(discovery_result.value))


def simple_component_example() -> None:
    """Demonstrate canonical component factories."""
    tap_result = meltano.tap("tap-csv")
    target_result = meltano.target("target-jsonl")
    dbt_result = meltano.dbt("analytics")
    if tap_result.success:
        logger.info(f"Tap source: {tap_result.value.source_name}")
    if target_result.success:
        logger.info(f"Target sink: {target_result.value.sink_name}")
    if dbt_result.success:
        logger.info(f"DBT transformation: {dbt_result.value.transformation_name}")


def simple_runtime_example() -> None:
    """Demonstrate the public runtime command surface."""
    result = meltano.execute_meltano_command([
        c.Meltano.CMD_BINARY,
        c.Meltano.ExecutorCommand.VERSION,
    ])
    if result.success:
        logger.info(
            "Runtime command result: %s", result.value.model_dump(mode="python")
        )


def simple_config_example() -> None:
    """Demonstrate typed settings through the public facade."""
    typed_settings = FlextMeltanoSettings.fetch_global()
    logger.info(
        "Config created: project_root=%s, config_dir=%s",
        typed_settings.Meltano.project_root,
        typed_settings.Meltano.config_dir,
    )
    logger.info("Environment: %s", typed_settings.Meltano.environment)


def run_examples() -> None:
    """Run all examples in display order."""
    simple_api_example()
    logger.info("")
    simple_component_example()
    logger.info("")
    simple_runtime_example()
    logger.info("")
    simple_config_example()


if __name__ == "__main__":
    logger.info("=== FLEXT Meltano Simple Working Examples ===")
    try:
        run_examples()
    except (ValueError, RuntimeError, OSError):
        logger.exception("Error executing examples")
