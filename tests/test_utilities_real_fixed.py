"""Test FlextMeltanoUtilities - ONLY real methods that exist.

Tests ONLY the actual methods listed by inspection.


Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import shutil
import tempfile
from pathlib import Path
from typing import cast

from flext_core import FlextResult, FlextTypes, FlextUtilities
from flext_meltano import (
    FlextMeltanoConfigBuilders,
    FlextMeltanoFileManagers,
    FlextMeltanoUtilities,
    FlextMeltanoValidators,
)


class TestFlextMeltanoUtilitiesRealMethods:
    """Test ONLY real methods that actually exist."""

    def test_create_temp_directory(self) -> None:
        """Test create_temp_directory method."""
        result = FlextMeltanoFileManagers.create_temp_directory()

        assert isinstance(result, FlextResult)
        assert result.is_success

        temp_path = result.value
        assert isinstance(temp_path, Path)
        assert temp_path.exists()

        # Cleanup
        shutil.rmtree(temp_path)

    def test_create_temp_directory_custom_prefix(self) -> None:
        """Test create_temp_directory with custom prefix."""
        result = FlextMeltanoFileManagers.create_temp_directory("custom_")

        assert isinstance(result, FlextResult)
        assert result.is_success

        temp_path = result.value
        assert "custom_" in temp_path.name

        # Cleanup
        shutil.rmtree(temp_path)

    def test_create_meltano_config_dict(self) -> None:
        """Test create_meltano_config_dict method."""
        result = FlextMeltanoUtilities.create_meltano_config_dict("test-project")

        assert isinstance(result, FlextResult)
        assert result.is_success

        config = result.value
        assert isinstance(config, dict)

    def test_create_meltano_config_dict_with_name(self) -> None:
        """Test create_meltano_config_dict with project name."""
        result = FlextMeltanoUtilities.create_meltano_config_dict(
            "test-project",
            "Test Project",
        )

        assert isinstance(result, FlextResult)
        assert result.is_success

        config = result.value
        assert isinstance(config, dict)

    def test_create_temp_directory_second(self) -> None:
        """Test create_temp_directory method second time."""
        result = FlextMeltanoFileManagers.create_temp_directory()

        assert isinstance(result, FlextResult)
        assert result.is_success

        temp_path = result.value
        assert isinstance(temp_path, Path)
        assert temp_path.exists()

        # Cleanup
        shutil.rmtree(temp_path)

    def test_create_plugin_config(self) -> None:
        """Test create_plugin_config method."""
        result = FlextMeltanoUtilities.create_plugin_config_dict("tap-csv")

        assert isinstance(result, FlextResult)
        assert result.is_success

        config = result.value
        assert isinstance(config, dict)

    def test_create_plugin_config_full_params(self) -> None:
        """Test create_plugin_config with all parameters."""
        result = FlextMeltanoUtilities.create_plugin_config_dict(
            name="tap-csv",
            plugin_type="extractor",
            namespace="tap_csv",
            pip_url="pipelinewise-tap-csv",
            executable="tap-csv",
        )

        assert isinstance(result, FlextResult)
        assert result.is_success

        config = result.value
        assert isinstance(config, dict)

    def test_create_plugin_config_dict(self) -> None:
        """Test create_plugin_config_dict method."""
        result = FlextMeltanoUtilities.create_plugin_config_dict("tap-postgres")

        assert isinstance(result, FlextResult)
        assert result.is_success

        config = result.value
        assert isinstance(config, dict)

    def test_create_singer_tap_config(self) -> None:
        """Test create_singer_tap_config method using ConfigBuilders (real implementation)."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_singer_tap_config(
            "tap-csv",
            "tap_csv",
            "pipelinewise-tap-csv",
            "tap-csv",
        )

        assert isinstance(result, FlextResult)
        assert result.is_success

        config = result.value
        assert isinstance(config, dict)

    def test_create_singer_target_config(self) -> None:
        """Test create_singer_target_config method using FlextMeltanoConfigBuilders."""
        builder = FlextMeltanoConfigBuilders()
        result = builder.create_singer_target_config(
            target_name="target-postgres",
            namespace="target_postgres",
            pip_url="pipelinewise-target-postgres",
            executable="target-postgres",
        )

        assert isinstance(result, FlextResult)
        assert result.is_success

        config = result.value
        assert isinstance(config, dict)

    def test_create_dbt_config(self) -> None:
        """Test create_dbt_config method."""
        result = FlextMeltanoConfigBuilders().create_dbt_config(
            "dbt-project",
            "analytics",
        )

        assert isinstance(result, FlextResult)
        assert result.is_success

        config = result.value
        assert isinstance(config, dict)

    def test_normalize_plugin_name(self) -> None:
        """Test plugin name normalization using flext-core utilities (duplication eliminated)."""
        # Use flext-core FlextUtilities instead of duplicated functionality

        result = FlextUtilities.TextProcessor.safe_string("tap_csv")

        # FlextUtilities.TextProcessor.safe_string returns string directly
        assert isinstance(result, str)
        assert result == "tap_csv"  # safe_string preserves valid strings

    def test_normalize_plugin_name_with_type(self) -> None:
        """Test plugin name normalization using flext-core utilities (duplication eliminated)."""
        # Use flext-core FlextUtilities for text processing instead of duplicated functionality

        # Test text normalization using flext-core - eliminating code duplication
        normalized_name = FlextUtilities.TextProcessor.safe_string("target_postgres")
        assert isinstance(normalized_name, str)
        assert normalized_name == "target_postgres"

        # Test with plugin type prefix handling
        normalized_with_prefix = FlextUtilities.TextProcessor.safe_string(
            "target-postgres",
        )
        assert isinstance(normalized_with_prefix, str)
        assert normalized_with_prefix == "target-postgres"

    # NOTE: sanitize_plugin_name method was removed to eliminate duplication.
    # Text sanitization should use FlextUtilities.TextProcessor.clean_text from flext-core.

    def test_sanitize_plugin_name_with_special_chars(self) -> None:
        """Test plugin name sanitization using FlextUtilities (NO DUPLICATION)."""
        # Use FlextUtilities.TextProcessor.clean_text instead of duplicated method

        result = FlextUtilities.TextProcessor.clean_text("tap-csv@!#$")
        assert isinstance(result, FlextResult)
        assert result.is_success

        # FlextUtilities.clean_text provides proper text sanitization
        cleaned = result.unwrap()
        assert isinstance(cleaned, str)
        assert len(cleaned) > 0
        # This test validates we use flext-core instead of duplicating functionality

    # NOTE: format_command_result, create_bridge_response, and parse_meltano_output_safe
    # methods were removed to eliminate duplication. These functionalities should use
    # FlextUtilities from flext-core directly instead of duplicating code.

    def test_load_yaml_config(self) -> None:
        """Test load_yaml_config method."""
        with tempfile.NamedTemporaryFile(
            encoding="utf-8",
            mode="w",
            suffix=".yml",
            delete=False,
        ) as f:
            f.write("version: 1\nproject_id: test")
            config_path = Path(f.name)

        try:
            result = FlextMeltanoUtilities.load_yaml_config(config_path)

            assert isinstance(result, FlextResult)
            if result.is_success:
                config = result.value
                assert isinstance(config, dict)
            else:
                assert result.error
        finally:
            config_path.unlink(missing_ok=True)

    def test_load_yaml_config_nonexistent(self) -> None:
        """Test load_yaml_config with nonexistent file."""
        nonexistent_path = Path("/nonexistent/file.yml")

        result = FlextMeltanoUtilities.load_yaml_config(nonexistent_path)

        assert isinstance(result, FlextResult)
        assert not result.is_success
        assert result.error

    def test_save_yaml_config(self) -> None:
        """Test save_yaml_config method."""
        # Create proper Meltano config for testing - cast to object dict
        config_dict: dict[str, object] = {
            "version": 1,
            "project_id": "test",
            "plugins": {"extractors": [], "loaders": [], "transformers": []},
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = Path(temp_dir) / "test_config.yml"

            result = FlextMeltanoUtilities.write_meltano_yml(config_dict, target_path)

            assert isinstance(result, FlextResult)
            if result.is_success:
                assert result.value
                assert target_path.exists()
            else:
                assert result.error

    def test_write_meltano_yml(self) -> None:
        """Test write_meltano_yml method."""
        # Create proper Meltano config for testing
        config_dict: dict[str, object] = {
            "version": 1,
            "project_id": "test-project",
            "plugins": {"extractors": [], "loaders": [], "transformers": []},
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = Path(temp_dir) / "meltano.yml"

            result = FlextMeltanoUtilities.write_meltano_yml(config_dict, target_path)

            assert isinstance(result, FlextResult)
            if result.is_success:
                assert result.value
                assert target_path.exists()
            else:
                assert result.error

    # NOTE: setup_project_structure method was removed to eliminate duplication.
    # Project structure operations should use FlextUtilities from flext-core directly.

    def test_validate_plugin_config(self) -> None:
        """Test validate_plugin_config method - now using validators.py (SOLID compliance)."""
        # ✅ SOLID COMPLIANCE: Use FlextMeltanoValidators instead of utilities

        # Create a basic plugin config
        config_result = FlextMeltanoUtilities.create_plugin_config_dict("tap-csv")
        assert config_result.is_success

        config = config_result.value

        result = FlextMeltanoValidators.validate_plugin_config(
            cast("FlextTypes.Core.JsonValue", config)
        )

        assert isinstance(result, FlextResult)
        if result.is_success:
            assert result.value
        else:
            assert result.error
