"""FLEXT Meltano Utilities - Domain-specific Meltano utilities.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path

import yaml

from flext_core import FlextLogger, FlextResult, FlextTypes, FlextUtilities
from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.file_managers import FlextMeltanoFileManagers


class FlextMeltanoUtilities:
    """DOMAIN-SPECIFIC Meltano utilities - ONLY what cannot be generalized to flext-core."""

    @classmethod
    def create_meltano_config_dict(
        cls, project_id: str, project_name: str = ""
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create MELTANO-SPECIFIC configuration dictionary - DOMAIN-SPECIFIC ONLY."""
        logger = FlextLogger(__name__)
        try:
            # Delegate to FlextUtilities for text processing
            safe_project_id = FlextUtilities.TextProcessor.safe_string(project_id)
            safe_project_name = FlextUtilities.TextProcessor.safe_string(project_name)

            # DOMAIN-SPECIFIC: Meltano configuration structure
            config_dict = {
                "version": 1,
                "project_id": safe_project_id,
                "project_name": safe_project_name,
                "environments": [
                    {"name": env}
                    for env in FlextMeltanoConstants.Metadata.DEFAULT_ENVIRONMENTS
                ],
                "plugins": {
                    "extractors": [],
                    "loaders": [],
                    "transformers": [],
                    "orchestrators": [],
                },
                "metadata": {
                    "created_by": FlextMeltanoConstants.Metadata.CREATED_BY,
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),  # NO DUPLICATION
                    "flext_version": FlextMeltanoConstants.FLEXT_MELTANO_VERSION,
                },
            }
            return FlextResult[FlextTypes.Core.Dict].ok(config_dict)
        except Exception as e:
            error_msg = f"Failed to create Meltano config dict: {e}"
            logger.exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    @classmethod
    def write_meltano_yml(
        cls, config: FlextTypes.Core.Dict, target_path: Path
    ) -> FlextResult[bool]:
        """Write MELTANO-SPECIFIC YAML configuration - DOMAIN-SPECIFIC ONLY."""
        try:
            # DOMAIN-SPECIFIC: YAML writing (cannot be generalized to flext-core)
            with target_path.open("w", encoding="utf-8") as f:
                yaml.dump(config, f, default_flow_style=False, indent=2)
            return FlextResult[bool].ok(data=True)
        except Exception as e:
            error_msg = f"Failed to write {FlextMeltanoConstants.MeltanoSpecific.PROJECT_FILE}: {e}"
            FlextLogger(__name__).exception(error_msg)
            return FlextResult[bool].fail(error_msg)

    # NOTE: create_temp_directory moved to FlextMeltanoFileManagers (proper domain responsibility)

    @classmethod
    def create_plugin_config_dict(
        cls,
        name: str,
        plugin_type: str = "extractor",
        namespace: str = "",
        pip_url: str = "",
        executable: str = "",
    ) -> FlextResult[FlextTypes.Core.Dict]:
        """Create MELTANO-SPECIFIC plugin config using FlextUtilities foundation."""
        try:
            # Delegate to FlextUtilities for ALL text processing
            safe_name = FlextUtilities.TextProcessor.safe_string(name)
            safe_namespace = FlextUtilities.TextProcessor.safe_string(namespace)

            # DOMAIN-SPECIFIC: Meltano plugin-specific defaults
            safe_pip_url = FlextUtilities.TextProcessor.safe_string(pip_url)
            safe_executable = FlextUtilities.TextProcessor.safe_string(executable)

            config_dict: FlextTypes.Core.Dict = {
                "name": safe_name,
                "namespace": safe_namespace,
                "pip_url": safe_pip_url,
                "executable": safe_executable,
                "type": plugin_type or "extractor",
                "settings": {},
                "config": {},
                "metadata": {
                    "created_by": FlextMeltanoConstants.Metadata.CREATED_BY,
                    "created_at": FlextUtilities.Generators.generate_iso_timestamp(),  # NO DUPLICATION
                },
            }
            return FlextResult[FlextTypes.Core.Dict].ok(config_dict)
        except Exception as e:
            error_msg = f"Failed to create plugin config: {e}"
            FlextLogger(__name__).exception(error_msg)
            return FlextResult[FlextTypes.Core.Dict].fail(error_msg)

    @classmethod
    def load_yaml_config(cls, path: Path) -> FlextResult[FlextTypes.Core.Dict]:
        """Load YAML config - DELEGATES to FlextMeltanoFileManagers as SOURCE OF TRUTH.

        ZERO DUPLICATION: Uses FlextMeltanoFileManagers.load_yaml_config.
        """
        # Delegate to FlextMeltanoFileManagers
        result = FlextMeltanoFileManagers.load_yaml_config(path)
        if result.is_failure:
            return FlextResult[FlextTypes.Core.Dict].fail(
                result.error or "Failed to load YAML config"
            )

        return FlextResult[FlextTypes.Core.Dict].ok(dict(result.unwrap()))


__all__ = ["FlextMeltanoUtilities"]
