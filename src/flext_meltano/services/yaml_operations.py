"""YAML file operations extracted from FlextMeltanoFileManagers.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path

import yaml
from flext_cli import u
from flext_core import r

from flext_meltano import c, m, t


class FlextMeltanoYamlOperationsMixin:
    """Mixin providing YAML load/save/validate operations."""

    @classmethod
    def load_yaml_config(cls, file_path: Path) -> r[t.Meltano.FileConfigDict]:
        """Load YAML config with validation."""
        try:
            if not u.is_string_non_empty(str(file_path)):
                return r[t.Meltano.FileConfigDict].fail(
                    f"Failed to load YAML config: Invalid YAML file path: {file_path}",
                )
            if not file_path.exists():
                return r[t.Meltano.FileConfigDict].fail(
                    f"Failed to load YAML config: YAML file not found: {file_path}",
                )
            with file_path.open("r", encoding=c.DEFAULT_ENCODING) as f:
                config_data = yaml.safe_load(f)
            if config_data is None:
                return r[t.Meltano.FileConfigDict].fail(
                    f"Failed to load YAML config: Empty YAML file: {file_path}",
                )
            raw_validated = m.Meltano.ConfigMappingPayload.model_validate({
                "values": config_data,
            }).values
            validated = _normalize_file_config(raw_validated)
            return r[t.Meltano.FileConfigDict].ok(validated)
        except (
            yaml.YAMLError,
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
        ) as e:
            return r[t.Meltano.FileConfigDict].fail(f"Failed to load YAML config: {e}")

    @classmethod
    def save_yaml_config(
        cls, config: t.Meltano.FileConfigDict, file_path: Path
    ) -> r[bool]:
        """Save YAML config to file."""
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with file_path.open("w", encoding=c.DEFAULT_ENCODING) as f:
                yaml.dump(
                    config, f, indent=2, default_flow_style=False, sort_keys=False
                )
            return r[bool].ok(True)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
            return r[bool].fail(f"Failed to save YAML config: {exc}")

    @classmethod
    def validate_yaml_file(cls, file_path: Path) -> r[bool]:
        """Validate YAML file syntax and existence."""

        def _validate() -> r[bool]:
            if not u.is_string_non_empty(str(file_path)):
                return r[bool].fail(f"Invalid YAML file path: {file_path}")
            if not file_path.exists():
                return r[bool].fail(f"YAML file not found: {file_path}")
            with file_path.open("r", encoding=c.DEFAULT_ENCODING) as f:
                yaml.safe_load(f)
            return r[bool].ok(value=True)

        try:
            return _validate()
        except yaml.YAMLError as e:
            return r[bool].fail(f"Invalid YAML syntax: {e}")
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[bool].fail(f"Failed to validate YAML: {e}")


def _normalize_file_config(
    raw: Mapping[
        str,
        t.Scalar | Sequence[t.Scalar | None] | Mapping[str, t.Scalar | None] | None,
    ],
) -> t.ContainerMapping:
    """Normalize raw config values into ContainerMapping."""
    normalized: t.MutableContainerMapping = {}
    for key, value in raw.items():
        if value is None or u.is_scalar(value):
            normalized[key] = value
            continue
        if isinstance(value, list):
            normalized[key] = [item for item in value if item is not None]
            continue
        if isinstance(value, Mapping):
            nested: t.MutableConfigurationMapping = {}
            for nested_key, nested_value in value.items():
                if u.is_scalar(nested_value):
                    nested[str(nested_key)] = nested_value
            normalized[key] = nested
    return normalized


__all__ = ["FlextMeltanoYamlOperationsMixin"]
