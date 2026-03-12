"""FLEXT Meltano Utilities - Domain-specific Meltano utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pathlib import Path
from typing import TextIO

import yaml
from flext_cli import FlextCliUtilities
from flext_core import FlextLogger, FlextUtilities, r

from flext_meltano import FlextMeltanoFileManagers, c, m, t


class FlextMeltanoUtilities(FlextCliUtilities):
    """DOMAIN-SPECIFIC Meltano utilities.

    ONLY what cannot be generalized to flext-core.
    Inherits from FlextUtilities to avoid duplication and ensure consistency.
    """

    class Meltano:
        """Plugin-related utility methods.

        NOTE: These methods were moved from constants.py to follow
        FLEXT pattern: constants contain ONLY pure constants, no methods.
        """

        @classmethod
        def _close_file_handle(cls, file_handle: TextIO) -> r[None]:
            """Close file handle safely.

            Args:
            file_handle: File handle to close.

            Returns:
            r indicating close operation result.

            """
            try:
                file_handle.close()
                return r[None].ok(None)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as err:
                _ = FlextLogger(__name__).warning(f"Error closing file handle: {err}")
                return r[None].ok(None)

        @classmethod
        def _open_yaml_file_for_writing(cls, target_path: Path) -> r[TextIO]:
            """Open YAML file for writing with validation.

            Args:
            target_path: Path to open for writing.

            Returns:
            r containing file handle or error.

            """

            def open_file() -> TextIO:
                target_path.parent.mkdir(parents=True, exist_ok=True)
                return target_path.open("w", encoding=c.Utilities.DEFAULT_ENCODING)

            return FlextUtilities.try_(
                open_file,
                catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
            ).map_error(lambda e: f"Failed to open file for writing: {e}")

        @classmethod
        def _validate_yaml_path(cls, path: Path) -> r[Path]:
            """Validate YAML file path before loading."""
            if not path.exists():
                return r[Path].fail(f"File does not exist: {path}")
            if not path.is_file():
                return r[Path].fail(f"Path is not a file: {path}")
            suffix = u.Conversion.normalize(path.suffix, case="lower")
            if suffix not in {".yml", ".yaml"}:
                return r[Path].fail(f"File is not a YAML file: {path}")
            return r[Path].ok(path)

        @classmethod
        def _write_yaml_content(
            cls, file_handle: TextIO, config: t.Meltano.MeltanoConfigDict
        ) -> r[bool]:
            """Write YAML content to file handle."""
            if getattr(file_handle, "write", None) is None:
                return r[bool].fail("Invalid file handle: missing write method")
            try:
                yaml.dump(
                    config,
                    file_handle,
                    Dumper=yaml.Dumper,
                    default_flow_style=False,
                    indent=2,
                    allow_unicode=True,
                )
                return r[bool].ok(value=True)
            except (yaml.YAMLError, ValueError, TypeError, AttributeError):
                return r[bool].fail(
                    "Failed to write YAML content: non-serializable object"
                )

        @classmethod
        def create_meltano_config_dict(
            cls,
            project_id: str,
            project_name: str = "",
            version: str | None = None,
            default_environment: str | None = None,
            plugins: t.Meltano.MeltanoConfigDict | None = None,
            environments: t.Meltano.MeltanoConfigDict | None = None,
        ) -> r[t.Meltano.MeltanoConfigDict]:
            """Create MELTANO-SPECIFIC configuration dictionary - DOMAIN-SPECIFIC ONLY."""
            try:
                raw_config: t.Meltano.MeltanoConfigDict = {
                    "project_id": project_id,
                    "project_name": project_name or project_id,
                    "version": version or 1,
                    "default_environment": default_environment,
                    "environments": environments,
                    "plugins": plugins,
                }
                default_envs: list[dict[str, str]] = [
                    {"name": env} for env in c.Meltano.Metadata.DEFAULT_ENVIRONMENTS
                ]
                project_id_val = str(raw_config.get("project_id", ""))
                project_name_val = str(
                    raw_config.get("project_name") or raw_config.get("project_id") or ""
                )
                cfg = u.build(
                    raw_config,
                    ops={"transform": {"normalize": False, "strip_none": False}},
                )
                cfg_dict = m.Meltano.ConfigMappingPayload.model_validate({
                    "values": cfg
                }).values
                plugins_val = cfg_dict.get("plugins")
                plugins_dict: dict[str, object] = {}
                if isinstance(plugins_val, dict):
                    plugins_dict = plugins_val
                result_cfg: t.Meltano.MeltanoConfigDict = {
                    "version": cfg_dict.get("version", 1),
                    "project_id": u.Text.safe_string(project_id_val),
                    "project_name": u.Text.safe_string(project_name_val),
                    "environments": cfg_dict.get("environments") or default_envs,
                    "plugins": plugins_dict,
                    "metadata": {
                        "created_by": c.Meltano.Metadata.CREATED_BY,
                        "created_at": u.Generators.generate_iso_timestamp(),
                        "flext_version": c.Meltano.FLEXT_MELTANO_VERSION,
                    },
                }
                default_env_val = cfg_dict.get("default_environment")
                if default_env_val is not None:
                    result_cfg["default_environment"] = default_env_val
                elif not project_name:
                    result_cfg["default_environment"] = (
                        c.Meltano.Metadata.DEFAULT_ENVIRONMENTS[0]
                    )
                return r[t.Meltano.MeltanoConfigDict].ok(result_cfg)
            except (ValueError, TypeError, KeyError, AttributeError, OSError) as err:
                return r[t.Meltano.MeltanoConfigDict].fail(
                    f"Failed to create Meltano config dict: {err}"
                )

        @classmethod
        def create_plugin_config_dict(
            cls,
            name: str,
            plugin_type: str = "extractor",
            namespace: str = "",
            pip_url: str = "",
            executable: str = "",
        ) -> r[t.Meltano.PluginConfigDict]:
            """Create MELTANO-SPECIFIC plugin config using DSL builder pattern."""
            raw: dict[str, t.JsonValue] = {
                "name": name,
                "namespace": namespace,
                "pip_url": pip_url,
                "executable": executable,
                "type": plugin_type or "extractor",
            }

            def safe_str(val: object) -> str:
                return u.Text.safe_string(str(val)) if val else ""

            def build_plugin(
                d: t.Meltano.PluginConfigDict,
            ) -> t.Meltano.PluginConfigDict:
                type_val = d.get("type", "extractor")
                return {
                    "name": safe_str(d.get("name", "")),
                    "namespace": safe_str(d.get("namespace", "")),
                    "pip_url": safe_str(d.get("pip_url", "")),
                    "executable": safe_str(d.get("executable", "")),
                    "type": str(type_val) if type_val else "extractor",
                    "settings": {},
                    "config": {},
                    "metadata": {
                        "created_by": c.Meltano.Metadata.CREATED_BY,
                        "created_at": u.Generators.generate_iso_timestamp(),
                    },
                }

            cfg = u.build(
                raw, ops={"transform": {"normalize": False, "strip_none": False}}
            )
            cfg_dict = m.Meltano.ConfigMappingPayload.model_validate({
                "values": cfg
            }).values
            result = build_plugin(cfg_dict)
            return r[t.Meltano.PluginConfigDict].ok(result)

        @classmethod
        def default_catalog(cls) -> list[t.Meltano.PluginDefinition]:
            """Provide default plugin catalog entries for discovery workflows."""
            return [
                {
                    "type": plugin_type.value,
                    "variant": c.Meltano.Plugin.DEFAULT_VARIANT,
                    "registry": c.Meltano.Plugin.HUB_URL,
                    "identifiers": [plugin_type.value],
                }
                for plugin_type in c.Meltano.Enums.PluginType.__members__.values()
            ]

        @classmethod
        def get_all_plugins(cls) -> list[t.Meltano.PluginDefinition]:
            """Compatibility shim for existing discovery logic."""
            return cls.default_catalog()

        @classmethod
        def load_yaml_config(cls, path: Path) -> r[t.Meltano.MeltanoConfigDict]:
            """Load YAML config using monadic composition with resource management.

            Uses r monadic patterns to chain file loading, validation,
            and type conversion with automatic error propagation and resource cleanup.
            ZERO DUPLICATION: Delegates to FlextMeltanoFileManagers as SOURCE OF TRUTH.

            Args:
            path: Path to YAML configuration file.

            Returns:
            r containing loaded configuration dictionary.

            """

            def convert_to_dict(
                config_dict: t.Meltano.FileConfigDict,
            ) -> t.Meltano.MeltanoConfigDict:
                """Type-safe conversion from FileConfigDict to MeltanoConfigDict."""
                return m.Meltano.ConfigMappingPayload.model_validate({
                    "values": config_dict
                }).values

            result = (
                r[Path]
                .ok(path)
                .flat_map(cls._validate_yaml_path)
                .flat_map(FlextMeltanoFileManagers.load_yaml_config)
                .map(convert_to_dict)
            )
            return (
                result
                if result.is_success
                else r[t.Meltano.MeltanoConfigDict].fail(
                    result.error or f"Loading YAML config from {path} failed"
                )
            )

        @classmethod
        def load_yaml_file(cls, file_path: Path) -> r[t.Meltano.MeltanoConfigDict]:
            """Load YAML file."""
            return cls.load_yaml_config(file_path)

        @classmethod
        def save_yaml_file(
            cls, file_path: Path, content: t.Meltano.MeltanoConfigDict
        ) -> r[Path]:
            """Save content to YAML file."""
            result = cls.write_meltano_yml(content, file_path)
            return (
                r[Path].ok(file_path)
                if result.is_success
                else r[Path].fail(result.error or "Failed to save YAML file")
            )

        @classmethod
        def write_meltano_yml(
            cls, config: t.Meltano.MeltanoConfigDict, target_path: Path
        ) -> r[bool]:
            """Write MELTANO-SPECIFIC YAML configuration using monadic resource management.

            Uses r.with_resource() for automatic file handle management
            and composable error handling with proper resource cleanup.
            DOMAIN-SPECIFIC: YAML writing (cannot be generalized to flext-core).

            Args:
            config: Configuration dictionary to write.
            target_path: Path where to write the YAML file.

            Returns:
            r indicating write operation success.

            """

            def write_operation(
                _unused_value: object, file_handle: TextIO, /
            ) -> r[bool]:
                return cls._write_yaml_content(file_handle, config)

            def cleanup_file_handle(file_handle: TextIO) -> None:
                try:
                    file_handle.close()
                except (
                    ValueError,
                    TypeError,
                    KeyError,
                    AttributeError,
                    OSError,
                ) as err:
                    _ = FlextLogger(__name__).warning(
                        f"Error closing file handle: {err}"
                    )

            try:
                open_result = cls._open_yaml_file_for_writing(target_path)
                if open_result.is_failure:
                    filename = c.Meltano.Paths.MELTANO_PROJECT_FILE
                    return r[bool].fail(f"Writing {filename}: {open_result.error}")
                resource = open_result.value
                try:
                    return write_operation(None, resource)
                finally:
                    cleanup_file_handle(resource)
            except (
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as err:
                filename = c.Meltano.Paths.MELTANO_PROJECT_FILE
                return r[bool].fail(f"Writing {filename}: {err}")

        @staticmethod
        def create_project_file(
            file_path: Path, content: str | t.Meltano.MeltanoConfigDict
        ) -> r[Path]:
            """Create a project file with content."""
            if not isinstance(content, str | dict):
                return r[Path].fail("Invalid content type: must be string or dict")
            content_guard: str | dict[str, object] = content

            def create_file() -> Path:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                content_str = m.Meltano.FileContentPayload.model_validate({
                    "content": content_guard
                }).content
                file_path.write_text(content_str, encoding="utf-8")
                return file_path

            return FlextUtilities.try_(
                create_file,
                catch=(OSError, ValueError, yaml.YAMLError),
            ).map_error(lambda e: f"Failed to create project file: {e}")

        @staticmethod
        def directory_exists(path: Path) -> r[bool]:
            """Check if directory exists."""
            return FlextUtilities.try_(
                lambda: path.exists() and path.is_dir(),
                catch=(OSError, ValueError),
            ).map_error(lambda e: f"Failed to check directory existence: {e}")

        @staticmethod
        def supported_types() -> list[str]:
            """Return the supported plugin type identifiers."""
            return [
                plugin_type.value
                for plugin_type in c.Meltano.Enums.PluginType.__members__.values()
            ]

        @staticmethod
        def validate_project_structure(project_path: Path) -> r[bool]:
            """Validate Meltano project structure."""
            try:
                if not project_path.exists():
                    return r[bool].fail(f"Project path does not exist: {project_path}")
                meltano_file = project_path / c.Meltano.Paths.MELTANO_PROJECT_FILE
                fallback_file = project_path / "meltano.yml"
                config_file = (
                    meltano_file
                    if meltano_file.exists()
                    else fallback_file
                    if fallback_file.exists()
                    else None
                )
                if config_file:
                    return r[bool].ok(True)
                return r[bool].fail(f"Meltano config file not found: {meltano_file}")
            except (OSError, ValueError) as err:
                return r[bool].fail(f"Failed to validate project structure: {err}")


u = FlextMeltanoUtilities
__all__ = ["FlextMeltanoUtilities", "u"]
