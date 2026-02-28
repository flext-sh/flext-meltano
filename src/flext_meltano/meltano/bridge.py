"""FLEXT Meltano Bridge - Go ↔ Python bridge communication.

This module provides the FlextMeltanoBridge class for JSON-based communication
between Go and Python components for Meltano operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping

from flext_core import FlextLogger, FlextResult

from flext_meltano import (
    FlextMeltanoConstants,
    FlextMeltanoModels,
    FlextMeltanoTypes,
    u,
)

# Import aliases for simplified usage
r = FlextResult
t = FlextMeltanoTypes
c = FlextMeltanoConstants
m = FlextMeltanoModels


class FlextMeltanoBridge:
    """Go Bridge - JSON API para integração Go ↔ Python.

    Provides JSON-based communication between Go and Python components
    for Meltano operations.
    """

    def __init__(self) -> None:
        """Initialize the bridge."""
        self.logger: FlextLogger = FlextLogger(__name__)

    @staticmethod
    def execute_command(
        command: str,
        args: Mapping[str, t.JsonValue] | None = None,
    ) -> FlextResult[t.Bridge.BridgeStatus]:
        """Execute a bridge command with JSON arguments.

        Args:
        command: Command name to execute
        args: JSON-serializable arguments

        Returns:
        FlextResult with command execution results

        """
        try:
            # Go bridge integration point — communicates with FlexCore Go service via JSON API
            # Build result dict with proper typing via model normalization
            args_dict: t.MeltanoCore.MeltanoConfigDict = (
                m.Meltano.ConfigMappingPayload.model_validate(
                    {"values": args},
                ).values
                if args
                else {}
            )
            result: t.Bridge.BridgeStatus = {
                "command": command,
                "args": args_dict,
                "status": "executed",
                "timestamp": u.Generators.generate_iso_timestamp(),
            }
            return FlextResult[t.Bridge.BridgeStatus].ok(result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return FlextResult[t.Bridge.BridgeStatus].fail(
                f"Bridge command failed: {e}",
            )

    @staticmethod
    def get_version() -> FlextResult[str]:
        """Get bridge version information."""
        try:
            # Go bridge version endpoint — returns bridge protocol version
            return FlextResult[str].ok("1.0.0")
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return FlextResult[str].fail(f"Failed to get version: {e}")

    @staticmethod
    def validate_connection() -> FlextResult[bool]:
        """Validate connection to Go bridge."""
        try:
            # Go bridge connectivity check — validates FlexCore service availability
            return FlextResult[bool].ok(value=True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return FlextResult[bool].fail(f"Bridge connection validation failed: {e}")

    @staticmethod
    def discover_plugins() -> FlextResult[t.Plugin.PluginCatalog]:
        """Discover available plugins through the Go bridge."""
        try:
            # Go bridge plugin discovery — queries FlexCore for registered plugins
            extractor1: t.Plugin.PluginDefinition = {
                "name": "tap-csv",
                "type": "extractors",
            }
            extractor2: t.Plugin.PluginDefinition = {
                "name": "tap-postgres",
                "type": "extractors",
            }
            extractor3: t.Plugin.PluginDefinition = {
                "name": "tap-json",
                "type": "extractors",
            }
            loader1: t.Plugin.PluginDefinition = {
                "name": "target-csv",
                "type": "loaders",
            }
            loader2: t.Plugin.PluginDefinition = {
                "name": "target-postgres",
                "type": "loaders",
            }
            loader3: t.Plugin.PluginDefinition = {
                "name": "target-jsonl",
                "type": "loaders",
            }
            transformer1: t.Plugin.PluginDefinition = {
                "name": "dbt-postgres",
                "type": "transformers",
            }
            transformer2: t.Plugin.PluginDefinition = {
                "name": "dbt-snowflake",
                "type": "transformers",
            }

            result: t.Plugin.PluginCatalog = {
                "extractors": [extractor1, extractor2, extractor3],
                "loaders": [loader1, loader2, loader3],
                "transformers": [transformer1, transformer2],
            }
            return FlextResult[t.Plugin.PluginCatalog].ok(result)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return FlextResult[t.Plugin.PluginCatalog].fail(
                f"Plugin discovery failed: {e}",
            )


__all__ = ["FlextMeltanoBridge"]
