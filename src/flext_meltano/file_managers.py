"""FLEXT Meltano File Management - Enterprise ELT file operations.

This module provides file management utilities for Meltano ELT operations
following FLEXT architectural patterns with proper error handling.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import shutil
import tempfile
from pathlib import Path
from typing import cast

import yaml
from flext_core import (
    FlextConstants,
    FlextLogger,
    FlextResult,
    FlextTypes,
    FlextUtilities,
)

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.typings import FlextMeltanoTypes
from flext_meltano.validators import FlextMeltanoValidators

logger = FlextLogger(__name__)


class FlextMeltanoFileManagers:
    """DOMAIN-SPECIFIC Meltano file managers using flext-core as SOURCE OF TRUTH.

    Contains ONLY Meltano-specific file operations that cannot be generalized to flext-core.
    ALL general file operations MUST use FlextUtilities from flext-core directly.

    ZERO DUPLICATION PRINCIPLE:
    - FlextUtilities.Files is SOURCE OF TRUTH for general file operations
    - Contains ONLY Meltano-specific operations (YAML configs, project structure)
    - Uses tempfile standard library with FlextUtilities validation
    """

    @classmethod
    def create_temp_directory(cls, prefix: str = "flext_meltano_") -> FlextResult[Path]:
        """Create temporary directory using direct tempfile implementation.

        Returns:
            FlextResult containing the created temporary directory path.

        """
        logger = FlextLogger(__name__)
        try:
            # Use direct tempfile.mkdtemp for temporary directory creation
            temp_dir = Path(tempfile.mkdtemp(prefix=prefix))
            logger.info(f"Created temporary directory: {temp_dir}")
            return FlextResult[Path].ok(data=temp_dir)
        except Exception as e:
            error_msg = f"Failed to create temp directory: {e}"
            logger.exception(error_msg)
            return FlextResult[Path].fail(error_msg)

    @classmethod
    def save_yaml_config(
        cls, config: FlextMeltanoTypes.MeltanoCore.FileConfigDict, file_path: Path
    ) -> FlextResult[bool]:
        """Save YAML config using direct implementation.

        Returns:
            FlextResult indicating success or failure of the save operation.

        """
        try:
            # Ensure parent directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            # Write YAML with proper encoding
            with file_path.open(
                "w", encoding=FlextConstants.Mixins.DEFAULT_ENCODING
            ) as f:
                yaml.dump(
                    config,
                    f,
                    indent=2,
                    default_flow_style=False,
                    sort_keys=False,
                )
            return FlextResult[bool].ok(data=True)
        except Exception as e:
            return FlextResult[bool].fail(f"Failed to save YAML config: {e}")

    @classmethod
    def load_yaml_config(
        cls, file_path: Path
    ) -> FlextResult[FlextMeltanoTypes.MeltanoCore.FileConfigDict]:
        """Load YAML config using FlextUtilities.Files validation + direct YAML.

        ZERO DUPLICATION: Uses FlextUtilities.Files.is_valid_path for validation.

        Returns:
            FlextResult containing the loaded YAML configuration.

        """
        try:
            # Basic path validation using flext-core utilities
            if not FlextUtilities.TypeGuards.is_string_non_empty(str(file_path)):
                return FlextResult[FlextMeltanoTypes.MeltanoCore.FileConfigDict].fail(
                    f"Invalid YAML file path: {file_path}",
                )

            if not file_path.exists():
                return FlextResult[FlextMeltanoTypes.MeltanoCore.FileConfigDict].fail(
                    f"YAML file not found: {file_path}"
                )

            with file_path.open(
                "r", encoding=FlextConstants.Mixins.DEFAULT_ENCODING
            ) as f:
                config_data: FlextMeltanoTypes.MeltanoCore.MeltanoConfigDict = (
                    yaml.safe_load(f)
                )

            if config_data is None:
                return FlextResult[FlextMeltanoTypes.MeltanoCore.FileConfigDict].ok(
                    data={}
                )

            if not isinstance(config_data, dict):
                return FlextResult[FlextMeltanoTypes.MeltanoCore.FileConfigDict].fail(
                    "YAML content is not a dictionary"
                )

            return FlextResult[FlextMeltanoTypes.MeltanoCore.FileConfigDict].ok(
                data=cast("FlextMeltanoTypes.MeltanoCore.FileConfigDict", config_data)
            )
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.MeltanoCore.FileConfigDict].fail(
                f"Failed to load YAML config: {e}"
            )

    @classmethod
    def validate_yaml_file(cls, file_path: Path) -> FlextResult[bool]:
        """Validate YAML using FlextUtilities.Files + direct YAML parsing.

        ZERO DUPLICATION: Uses FlextUtilities.Files.is_valid_path for validation.

        Returns:
            FlextResult indicating whether the YAML file is valid.

        """
        try:
            # Basic path validation using flext-core utilities
            if not FlextUtilities.TypeGuards.is_string_non_empty(str(file_path)):
                return FlextResult[bool].fail(f"Invalid YAML file path: {file_path}")

            if not file_path.exists():
                return FlextResult[bool].fail(f"YAML file not found: {file_path}")

            with file_path.open(
                "r", encoding=FlextConstants.Mixins.DEFAULT_ENCODING
            ) as f:
                yaml.safe_load(f)  # This will raise an exception if invalid YAML

            return FlextResult[bool].ok(data=True)
        except yaml.YAMLError as e:
            return FlextResult[bool].fail(f"Invalid YAML syntax: {e}")
        except Exception as e:
            return FlextResult[bool].fail(f"Failed to validate YAML: {e}")

    @classmethod
    def create_directory_structure(
        cls,
        base_path: Path,
        directories: FlextTypes.StringList,
    ) -> FlextResult[FlextTypes.StringDict]:
        """Create directory structure using direct pathlib implementation.

        Returns:
            FlextResult containing the created directory structure information.

        """
        try:
            created_paths: FlextTypes.StringDict = {}

            for directory in directories:
                dir_path = base_path / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                created_paths[directory] = str(dir_path)

            return FlextResult[FlextTypes.StringDict].ok(data=created_paths)
        except Exception as e:
            return FlextResult[FlextTypes.StringDict].fail(
                f"Failed to create directories: {e}",
            )

    @classmethod
    def setup_project_structure(
        cls,
        project_root: Path,
        _project_name: str,
    ) -> FlextResult[FlextMeltanoTypes.MeltanoCore.PathDict]:
        """Setup Meltano project structure using direct implementation.

        Returns:
            FlextResult containing the project structure information.

        """
        try:
            # Define Meltano directory structure
            directories = [
                "extract",
                "load",
                "transform",
                "analyze",
                "transform/models",
                "transform/tests",
                "transform/data",
            ]

            # Create directory structure
            created_paths: dict[str, Path | str] = {}
            for directory in directories:
                dir_path = project_root / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                created_paths[directory] = dir_path

            # Create essential config files
            configs = {
                FlextMeltanoConstants.Meltano.MELTANO_PROJECT_FILE: {
                    "version": 1,
                    "project_id": "project_name",
                    "project_name": "project_name",
                    "plugins": {
                        "extractors": [],
                        "loaders": [],
                        "transformers": [],
                    },
                },
                "transform/dbt_project.yml": {
                    "name": "project_name",
                    "version": "1.0.0",
                    "profile": "project_name",
                    "model-paths": ["models"],
                    "test-paths": ["tests"],
                },
            }

            for filename, config_data in configs.items():
                config_path = project_root / filename
                save_result = cls.save_yaml_config(
                    cast("FlextMeltanoTypes.MeltanoCore.FileConfigDict", config_data),
                    config_path,
                )
                if save_result.is_success:
                    created_paths[filename.replace("/", "_")] = str(config_path)

            # Add project root
            created_paths["project_root"] = project_root
            return FlextResult[FlextMeltanoTypes.MeltanoCore.PathDict].ok(
                data=created_paths
            )
        except Exception as e:
            return FlextResult[FlextMeltanoTypes.MeltanoCore.PathDict].fail(
                f"Failed to setup project structure: {e}"
            )

    @classmethod
    def cleanup_temp_directory(cls, temp_path: Path) -> FlextResult[bool]:
        """Cleanup temporary directory using direct implementation.

        Returns:
            FlextResult indicating success or failure of the cleanup operation.

        """
        try:
            if temp_path.exists() and temp_path.is_dir():
                shutil.rmtree(temp_path)
            return FlextResult[bool].ok(data=True)
        except Exception as e:
            return FlextResult[bool].fail(f"Failed to cleanup temp directory: {e}")

    @classmethod
    def validate_project_structure(cls, project_root: Path) -> FlextResult[bool]:
        """Validate Meltano project structure using centralized validator.

        Returns:
            FlextResult indicating whether the project structure is valid.

        """
        # Use centralized validator to eliminate duplication

        return FlextMeltanoValidators.validate_meltano_project_structure(project_root)


__all__ = ["FlextMeltanoFileManagers"]
