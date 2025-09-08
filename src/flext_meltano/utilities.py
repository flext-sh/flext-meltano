"""FLEXT Meltano Utilities - Extending FlextUtilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import cast

import yaml
from flext_core import (
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)

from flext_meltano.typings import FlextMeltanoTypes

logger = FlextLogger(__name__)


class FlextMeltanoUtilities:
    """FLEXT Meltano Utilities using FlextUtilities composition with Meltano-specific functionality."""

    @classmethod
    def create_temp_directory(cls, prefix: str = "flext_meltano_") -> FlextResult[Path]:
        """Create Meltano temp directory usando FlextUtilities + Meltano specifics with FlextResult."""
        try:
            # Use FlextUtilities for safe string handling
            safe_prefix = FlextUtilities.TextProcessor.safe_string(
                prefix, "flext_meltano_"
            )

            # Use FlextUtilities for basic temp directory creation pattern
            temp_dir = Path(tempfile.mkdtemp(prefix=safe_prefix))

            # Add Meltano-specific directory structure
            meltano_dirs = [".meltano", "extract", "load", "transform"]
            for dir_name in meltano_dirs:
                (temp_dir / dir_name).mkdir(exist_ok=True)

            logger.info(f"Created Meltano temp directory: {temp_dir}")
            return FlextResult[Path].ok(temp_dir)
        except Exception as e:
            error_msg = f"Failed to create Meltano temp directory: {e}"
            logger.exception(error_msg)
            return FlextResult[Path].fail(error_msg)

    @classmethod
    def create_meltano_config_dict(
        cls, project_id: str, project_name: str = ""
    ) -> FlextResult[FlextMeltanoTypes.DBT.ProjectConfig]:
        """Create complete Meltano configuration dictionary.

        Returns:
            FlextResult[FlextMeltanoTypes.DBT.ProjectConfig]: Project configuration result.

        """
        try:
            # Use FlextUtilities.TextProcessor.safe_string() for safe string handling
            safe_project_id = FlextUtilities.TextProcessor.safe_string(
                project_id, "flext-meltano-project"
            )
            safe_project_name = FlextUtilities.TextProcessor.safe_string(
                project_name, safe_project_id
            )

            config_dict = {
                "version": 1,
                "project_id": safe_project_id,
                "project_name": safe_project_name,
                "environments": [
                    {"name": "dev"},
                    {"name": "staging"},
                    {"name": "prod"},
                ],
                "plugins": {
                    "extractors": [],
                    "loaders": [],
                    "transformers": [],
                    "orchestrators": [],
                },
                "metadata": {
                    "created_by": "flext-meltano",
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                    "flext_version": "2.0.0-enterprise",
                },
            }
            return FlextResult[FlextMeltanoTypes.DBT.ProjectConfig].ok(
                cast("FlextMeltanoTypes.DBT.ProjectConfig", config_dict)
            )
        except Exception as e:
            error_msg = f"Failed to create Meltano config dict: {e}"
            logger.exception(error_msg)
            return FlextResult[FlextMeltanoTypes.DBT.ProjectConfig].fail(error_msg)

    @classmethod
    def write_meltano_yml(
        cls, config: FlextMeltanoTypes.DBT.ProjectConfig, target_path: Path
    ) -> FlextResult[bool]:
        """Write Meltano YAML configuration safely."""
        try:
            # Config is typed as ConfigDict so isinstance check is unnecessary
            with target_path.open("w", encoding="utf-8") as f:
                yaml.dump(config, f, default_flow_style=False, indent=2)

            return FlextResult.ok(data=True)

        except Exception as e:
            error_msg = f"Failed to write meltano.yml: {e}"
            logger.exception(error_msg)
            return FlextResult.fail(error_msg)

    @classmethod
    def create_plugin_config_dict(
        cls,
        name: str,
        plugin_type: str = "extractor",
        namespace: str = "",
        pip_url: str = "",
        executable: str = "",
    ) -> FlextResult[FlextMeltanoTypes.Plugin.Config]:
        """Create plugin configuration dictionary."""
        try:
            safe_name = FlextUtilities.TextProcessor.safe_string(name, "unknown-plugin")
            safe_namespace = FlextUtilities.TextProcessor.safe_string(
                namespace, f"tap_{safe_name}"
            )
            safe_pip_url = FlextUtilities.TextProcessor.safe_string(
                pip_url, f"tap-{safe_name}"
            )
            safe_executable = FlextUtilities.TextProcessor.safe_string(
                executable, f"tap-{safe_name}"
            )

            config_dict = {
                "name": safe_name,
                "namespace": safe_namespace,
                "pip_url": safe_pip_url,
                "executable": safe_executable,
                "type": FlextUtilities.TextProcessor.safe_string(
                    plugin_type, "extractor"
                ),
                "settings": {},
                "config": {},
                "metadata": {
                    "created_by": "flext-meltano",
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),
                },
            }
            return FlextResult[FlextMeltanoTypes.Plugin.Config].ok(
                cast("FlextMeltanoTypes.Plugin.Config", config_dict)
            )
        except Exception as e:
            error_msg = f"Failed to create plugin config dict: {e}"
            logger.exception(error_msg)
            return FlextResult[FlextMeltanoTypes.Plugin.Config].fail(error_msg)

    @classmethod
    def format_meltano_command_result(
        cls, *, success: bool, data: FlextTypes.Core.JsonValue | None = None
    ) -> FlextResult[FlextMeltanoTypes.CLI.ProcessResult]:
        """Format Meltano command result for bridge communication."""
        try:
            # Use FlextUtilities for safe boolean and timestamp handling
            response: FlextMeltanoTypes.CLI.ProcessResult = {
                "success": FlextUtilities.Conversions.safe_bool(success),
                "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
            }

            if data and isinstance(data, dict):
                response["data"] = data

            return FlextResult[FlextMeltanoTypes.CLI.ProcessResult].ok(response)
        except Exception as e:
            error_msg = f"Failed to format Meltano command result: {e}"
            logger.exception(error_msg)
            return FlextResult[FlextMeltanoTypes.CLI.ProcessResult].fail(error_msg)

    @classmethod
    def parse_meltano_output_safe(
        cls, output: str
    ) -> FlextResult[FlextMeltanoTypes.CLI.ProcessResult]:
        """Parse Meltano command output safely."""
        # Check if output is non-empty
        if not output or not output.strip():
            return FlextResult.ok({"output": "", "lines": []})

        try:
            # Clean output - normalize whitespace
            clean_output = output.strip()
            lines = clean_output.split("\n")

            # Try JSON parsing first using FlextUtilities.safe_json_parse
            try:
                parsed_json = FlextUtilities.safe_json_parse(clean_output, None)
                if parsed_json is not None:  # Safe parse succeeded
                    return FlextResult.ok(
                        {
                            "output": clean_output,
                            "lines": cast("FlextTypes.Core.JsonValue", lines),
                            "parsed_json": cast(
                                "FlextTypes.Core.JsonValue", parsed_json
                            ),
                        }
                    )
            except Exception as e:
                logger.debug(f"JSON parsing failed for Meltano output: {e}")

            # Fall through to text parsing
            return FlextResult.ok(
                {
                    "output": clean_output,
                    "lines": cast("FlextTypes.Core.JsonValue", lines),
                    "line_count": len(lines),
                }
            )

        except Exception as e:
            error_msg = f"Failed to parse Meltano output: {e}"
            logger.exception(error_msg)
            return FlextResult.fail(error_msg)

    @classmethod
    def adapt_meltano_plugin(
        cls, plugin_data: FlextMeltanoTypes.Plugin.PluginInfo
    ) -> FlextResult[FlextMeltanoTypes.Plugin.PluginInfo]:
        """Adapt Meltano plugin data for unified processing."""
        try:
            # plugin_data is typed as PluginInfo so isinstance check is unnecessary
            name = plugin_data.get("name", "unknown")
            plugin_type = plugin_data.get("type", "unknown")

            adapted_data: FlextTypes.Core.Dict = {
                "id": name,
                "name": name,
                "type": plugin_type,
                "status": "adapted",
                "namespace": plugin_data.get("namespace", f"{plugin_type}_{name}"),
                "version": plugin_data.get("version", "1.0.0"),
                "metadata": {
                    "adapted_by": "flext-meltano",
                    "adapted_at": FlextUtilities.Generators.generate_iso_timestamp(),
                },
            }
            # Cast to expected type - we know the structure matches PluginInfo
            typed_data = cast("FlextMeltanoTypes.Plugin.PluginInfo", adapted_data)
            return FlextResult[FlextMeltanoTypes.Plugin.PluginInfo].ok(typed_data)
        except Exception as e:
            error_msg = f"Failed to adapt Meltano plugin: {e}"
            logger.exception(error_msg)
            return FlextResult[FlextMeltanoTypes.Plugin.PluginInfo].fail(error_msg)

    @classmethod
    def create_bridge_response(
        cls, *, success: bool, data: FlextMeltanoTypes.CLI.ProcessResult | None = None
    ) -> FlextTypes.Core.Headers:
        """Create bridge response for Go communication."""
        response: FlextTypes.Core.Headers = {
            "success": FlextUtilities.TextProcessor.safe_string(str(success)),
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
        }

        if data and isinstance(data, dict):
            response["data"] = FlextUtilities.ProcessingUtils.safe_json_stringify(data)

        return response

    @classmethod
    def format_command_result(
        cls, exit_code: int, output: str, command: str
    ) -> FlextTypes.Core.Headers:
        """Format command execution result."""
        return {
            "exit_code": FlextUtilities.TextProcessor.safe_string(str(exit_code)),
            "success": FlextUtilities.TextProcessor.safe_string(str(exit_code == 0)),
            "output": FlextUtilities.TextProcessor.safe_string(output),
            "command": FlextUtilities.TextProcessor.safe_string(command),
            "timestamp": FlextUtilities.Generators.generate_iso_timestamp(),
        }

    # Legacy method aliases for backward compatibility using proper lambda syntax
    @classmethod
    def normalize_plugin_name(
        cls, name: str, plugin_type: str = "tap"
    ) -> FlextResult[str]:
        """Normalize plugin name with type prefix using FlextResult patterns."""
        try:
            # Validate inputs using FlextUtilities
            safe_name = (
                FlextUtilities.TextProcessor.safe_string(name, "unknown")
                .lower()
                .replace(" ", "-")
            )
            safe_plugin_type = FlextUtilities.TextProcessor.safe_string(
                plugin_type, "tap"
            )

            # Apply type-specific prefixes
            if safe_plugin_type in {"tap", "extractor"} and not safe_name.startswith(
                "tap-"
            ):
                normalized_name = f"tap-{safe_name}"
            elif safe_plugin_type in {"target", "loader"} and not safe_name.startswith(
                "target-"
            ):
                normalized_name = f"target-{safe_name}"
            else:
                normalized_name = safe_name

            return FlextResult[str].ok(normalized_name)
        except Exception as e:
            return FlextResult[str].fail(f"Failed to normalize plugin name: {e}")

    @classmethod
    def sanitize_plugin_name(cls, name: str) -> FlextResult[str]:
        """Sanitize plugin name to safe format using FlextResult patterns."""
        try:
            sanitized_name = (
                FlextUtilities.TextProcessor.safe_string(name, "unknown")
                .lower()
                .replace(" ", "_")
                .replace("-", "_")
            )
            return FlextResult[str].ok(sanitized_name)
        except Exception as e:
            return FlextResult[str].fail(f"Failed to sanitize plugin name: {e}")

    @classmethod
    def load_yaml_config(
        cls, path: Path
    ) -> FlextResult[FlextMeltanoTypes.DBT.ProjectConfig]:
        """Load YAML config safely.

        Returns:
            FlextResult[FlextMeltanoTypes.DBT.ProjectConfig]: Configuration loading result.

        """
        try:
            with path.open("r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            return FlextResult.ok(data if isinstance(data, dict) else {})
        except Exception as e:
            return FlextResult.fail(f"Failed to load YAML: {e}")

    @classmethod
    def setup_project_structure(
        cls, project_root: Path, project_name: str
    ) -> FlextResult[FlextMeltanoTypes.CLI.ProcessResult]:
        """Setup complete project structure using chain-of-operations pattern."""
        try:
            project_root.mkdir(parents=True, exist_ok=True)

            # Create directories
            for directory in ["extract", "load", "transform", "transform/models"]:
                (project_root / directory).mkdir(parents=True, exist_ok=True)

            # Create config files
            meltano_yml = project_root / "meltano.yml"
            dbt_yml = project_root / "transform" / "dbt_project.yml"

            # Chain operations using bind for railway-oriented programming
            def setup_operation(_: None) -> FlextResult[tuple[Path, Path]]:
                """Setup operation chain using FlextResult.bind() pattern."""
                # Create configs
                meltano_config_result = cls.create_meltano_config_dict(
                    project_name, project_name
                )
                if not meltano_config_result.success:
                    return FlextResult.fail(
                        meltano_config_result.error or "Failed to create Meltano config"
                    )

                dbt_config_result = cls.create_dbt_config(project_name, project_name)
                if not dbt_config_result.success:
                    return FlextResult.fail(
                        dbt_config_result.error or "Failed to create DBT config"
                    )

                # Write configs
                write_meltano_result = cls.write_meltano_yml(
                    meltano_config_result.value, meltano_yml
                )
                if not write_meltano_result.success:
                    return FlextResult.fail(
                        write_meltano_result.error or "Failed to write meltano.yml"
                    )

                write_dbt_result = cls.write_meltano_yml(
                    dbt_config_result.value, dbt_yml
                )
                if not write_dbt_result.success:
                    return FlextResult.fail(
                        write_dbt_result.error or "Failed to write dbt_project.yml"
                    )

                return FlextResult.ok((meltano_yml, dbt_yml))

            # Execute operation chain
            operation_result = setup_operation(None)
            if not operation_result.success:
                return FlextResult.fail(
                    operation_result.error or "Setup operation failed"
                )

            # Single success return point
            return FlextResult.ok(
                {
                    "project_root": str(project_root),
                    "meltano_yml": str(meltano_yml),
                    "dbt_yml": str(dbt_yml),
                }
            )
        except Exception as e:
            return FlextResult.fail(f"Failed to setup project structure: {e}")

    @classmethod
    def create_singer_tap_config(
        cls, name: str, namespace: str, pip_url: str, executable: str
    ) -> FlextResult[FlextMeltanoTypes.Singer.TapConfig]:
        """Create Singer tap configuration.

        Returns:
            FlextResult[FlextMeltanoTypes.Singer.TapConfig]: Singer tap config creation result.

        """
        try:
            config_result = cls.create_plugin_config_dict(
                name, "extractor", namespace, pip_url, executable
            )
            if not config_result.success:
                return FlextResult[FlextMeltanoTypes.Singer.TapConfig].fail(
                    config_result.error or "Failed to create plugin config"
                )

            config = config_result.value
            config["capabilities"] = ["discover", "properties", "catalog", "schema"]
            config["settings"] = {}
            return FlextResult[FlextMeltanoTypes.Singer.TapConfig].ok(config)
        except Exception as e:
            error_msg = f"Failed to create Singer tap config: {e}"
            logger.exception(error_msg)
            return FlextResult[FlextMeltanoTypes.Singer.TapConfig].fail(error_msg)

    @classmethod
    def create_singer_target_config(
        cls, name: str, namespace: str, pip_url: str, executable: str
    ) -> FlextResult[FlextMeltanoTypes.Singer.TargetConfig]:
        """Create Singer target configuration."""
        try:
            config_result = cls.create_plugin_config_dict(
                name, "loader", namespace, pip_url, executable
            )
            if not config_result.success:
                return FlextResult[FlextMeltanoTypes.Singer.TargetConfig].fail(
                    config_result.error or "Failed to create plugin config"
                )

            config = config_result.value
            config["settings"] = {}
            return FlextResult[FlextMeltanoTypes.Singer.TargetConfig].ok(config)
        except Exception as e:
            error_msg = f"Failed to create Singer target config: {e}"
            logger.exception(error_msg)
            return FlextResult[FlextMeltanoTypes.Singer.TargetConfig].fail(error_msg)

    @classmethod
    def create_dbt_config(
        cls, name: str, profile: str
    ) -> FlextResult[FlextMeltanoTypes.DBT.ProjectConfig]:
        """Create DBT project configuration."""
        try:
            config = {
                "name": FlextUtilities.TextProcessor.safe_string(name, "dbt_project"),
                "version": "1.0.0",
                "profile": FlextUtilities.TextProcessor.safe_string(profile, name),
                "model-paths": ["models"],
                "test-paths": ["tests"],
                "seed-paths": ["data"],
                "macro-paths": ["macros"],
                "snapshot-paths": ["snapshots"],
                "analysis-paths": ["analysis"],
                "target-path": "target",
                "clean-targets": ["target", "dbt_packages"],
            }
            return FlextResult[FlextMeltanoTypes.DBT.ProjectConfig].ok(
                cast("FlextMeltanoTypes.DBT.ProjectConfig", config)
            )
        except Exception as e:
            error_msg = f"Failed to create DBT config: {e}"
            logger.exception(error_msg)
            return FlextResult[FlextMeltanoTypes.DBT.ProjectConfig].fail(error_msg)

    @classmethod
    def validate_plugin_config(
        cls, config: FlextMeltanoTypes.Plugin.Config
    ) -> FlextResult[bool]:
        """Validate plugin configuration."""
        # Config is typed as Plugin.Config so isinstance check is unnecessary
        required_fields = ["name", "type"]
        for field in required_fields:
            if field not in config or not config.get(field):
                return FlextResult.fail(f"Missing required field: {field}")

        return FlextResult.ok(data=True)

    create_meltano_config = create_meltano_config_dict
    create_plugin_config = create_plugin_config_dict
    save_yaml_config = write_meltano_yml


# =============================================================================
# NOTE: For validation functions, import directly from flext_meltano.validators
# Removed circular import functions to comply with ruff PLC0415
# =============================================================================


# =============================================================================
# BACKWARD COMPATIBILITY ALIASES
# =============================================================================

# Validation functions already imported at top of file

# =============================================================================
# MODULE EXPORTS
# =============================================================================

__all__ = [
    # Main class only - no helper functions
    "FlextMeltanoUtilities",
]
