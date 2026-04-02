"""FLEXT Meltano File Management - Enterprise ELT file operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import shutil
import tempfile
from collections.abc import Mapping, MutableMapping
from pathlib import Path
from typing import override

from flext_core import FlextLogger, r
from flext_meltano import (
    FlextMeltanoServiceBase,
    c,
    t,
    u,
)

_module_logger = FlextLogger(__name__)


class FlextMeltanoFileManagers(FlextMeltanoServiceBase):
    """DOMAIN-SPECIFIC Meltano file managers using flext-core as SOURCE OF TRUTH.

    Contains ONLY Meltano-specific file operations that cannot be generalized
    to flext-core.
    ALL general file operations MUST use u (FlextUtilities) directly.
    """

    @classmethod
    def cleanup_temp_directory(cls, temp_path: Path) -> r[bool]:
        """Cleanup temporary directory."""

        def _cleanup() -> bool:
            if temp_path.exists() and temp_path.is_dir():
                shutil.rmtree(temp_path)
            return True

        return u.try_(
            _cleanup,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(lambda e: f"Failed to cleanup temp directory: {e}")

    @classmethod
    def create_directory_structure(
        cls,
        base_path: Path,
        directories: t.StrSequence,
    ) -> r[t.StrMapping]:
        """Create directory structure using direct pathlib implementation."""

        def _create_dirs() -> t.StrMapping:
            created_paths: t.MutableStrMapping = {}
            for directory in directories:
                dir_path = base_path / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                created_paths[directory] = str(dir_path)
            return created_paths

        return u.try_(
            _create_dirs,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(lambda e: f"Failed to create directories: {e}")

    @classmethod
    def create_temp_directory(cls, prefix: str = "flext_meltano_") -> r[Path]:
        """Create temporary directory."""

        def _create() -> Path:
            temp_dir = Path(tempfile.mkdtemp(prefix=prefix))
            _module_logger.info("Created temporary directory", path=str(temp_dir))
            return temp_dir

        return u.try_(
            _create,
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(lambda e: f"Failed to create temp directory: {e}")

    @classmethod
    def setup_project_structure(
        cls,
        project_root: Path,
        _project_name: str,
    ) -> r[t.Meltano.PathDict]:
        """Setup Meltano project structure."""
        try:
            directories = [
                "extract",
                "load",
                "transform",
                "analyze",
                "transform/models",
                "transform/tests",
                "transform/data",
            ]
            created_paths: MutableMapping[str, Path | str] = {}
            for directory in directories:
                dir_path = project_root / directory
                dir_path.mkdir(parents=True, exist_ok=True)
                created_paths[directory] = dir_path
            empty_list: t.ContainerList = []
            plugin_items: Mapping[str, t.ContainerList] = {
                "extractors": list(empty_list),
                "loaders": list(empty_list),
                "transformers": list(empty_list),
            }
            meltano_config: t.Meltano.FileConfigDict = {
                "version": 1,
                "project_id": "project_name",
                "project_name": "project_name",
                "plugins": plugin_items,
            }
            model_paths: t.StrSequence = ["models"]
            test_paths: t.StrSequence = ["tests"]
            dbt_project_config: t.Meltano.FileConfigDict = {
                "name": "project_name",
                "version": "1.0.0",
                "profile": "project_name",
                "model-paths": model_paths,
                "test-paths": test_paths,
            }
            configs: Mapping[str, t.Meltano.FileConfigDict] = {
                c.Meltano.Paths.MELTANO_PROJECT_FILE: meltano_config,
                "transform/dbt_project.yml": dbt_project_config,
            }
            for filename, config_data in configs.items():
                config_path = project_root / filename
                save_result = cls.save_yaml_config(config_data, config_path)
                if save_result.is_success:
                    created_paths[filename.replace("/", "_")] = str(config_path)
            created_paths["project_root"] = project_root
            return r[t.Meltano.PathDict].ok(created_paths)
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[t.Meltano.PathDict].fail(f"Failed to setup project structure: {e}")

    @classmethod
    def validate_project_structure(cls, project_root: Path) -> r[bool]:
        """Validate Meltano project structure."""
        return u.Meltano.validate_project_structure(project_root)

    # ------------------------------------------------------------------
    # YAML operations — delegate to u.Meltano.* utilities
    # ------------------------------------------------------------------

    @classmethod
    def load_yaml_config(cls, file_path: Path) -> r[t.Meltano.FileConfigDict]:
        """Load YAML config with validation. Delegates to u.Meltano."""
        return u.Meltano.load_raw_yaml(file_path)

    @classmethod
    def save_yaml_config(
        cls, config: t.Meltano.FileConfigDict, file_path: Path
    ) -> r[bool]:
        """Save YAML config to file. Delegates to u.Meltano."""
        return u.Meltano.save_raw_yaml(config, file_path)

    @classmethod
    def validate_yaml_file(cls, file_path: Path) -> r[bool]:
        """Validate YAML file syntax and existence. Delegates to u.Meltano."""
        return u.Meltano.validate_yaml_syntax(file_path)

    @override
    def execute(self) -> r[t.Meltano.MeltanoConfigDict]:
        """Execute file managers service — returns current settings."""
        return r[t.Meltano.MeltanoConfigDict].ok(
            u.Meltano.coerce_config_mapping(self.settings)
        )


__all__ = ["FlextMeltanoFileManagers"]
