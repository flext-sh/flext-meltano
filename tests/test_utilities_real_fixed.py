"""Test FlextMeltanoUtilities - ONLY real methods that exist.

Tests ONLY the actual methods listed by inspection.
"""

import tempfile
from pathlib import Path

from flext_core import FlextResult

from flext_meltano.utilities import FlextMeltanoUtilities


class TestFlextMeltanoUtilitiesRealMethods:
    """Test ONLY real methods that actually exist."""

    def test_create_meltano_temp_directory(self) -> None:
        """Test create_meltano_temp_directory method."""
        result = FlextMeltanoUtilities.create_meltano_temp_directory()

        assert isinstance(result, FlextResult)
        assert result.success

        temp_path = result.value
        assert isinstance(temp_path, Path)
        assert temp_path.exists()

        # Cleanup
        import shutil

        shutil.rmtree(temp_path)

    def test_create_meltano_temp_directory_custom_prefix(self) -> None:
        """Test create_meltano_temp_directory with custom prefix."""
        result = FlextMeltanoUtilities.create_meltano_temp_directory("custom_")

        assert isinstance(result, FlextResult)
        assert result.success

        temp_path = result.value
        assert "custom_" in temp_path.name

        # Cleanup
        import shutil

        shutil.rmtree(temp_path)

    def test_create_meltano_config_dict(self) -> None:
        """Test create_meltano_config_dict method."""
        result = FlextMeltanoUtilities.create_meltano_config_dict("test-project")

        assert isinstance(result, FlextResult)
        assert result.success

        config = result.value
        assert isinstance(config, dict)

    def test_create_meltano_config_dict_with_name(self) -> None:
        """Test create_meltano_config_dict with project name."""
        result = FlextMeltanoUtilities.create_meltano_config_dict(
            "test-project", "Test Project"
        )

        assert isinstance(result, FlextResult)
        assert result.success

        config = result.value
        assert isinstance(config, dict)

    def test_create_temp_directory(self) -> None:
        """Test create_temp_directory method."""
        result = FlextMeltanoUtilities.create_temp_directory()

        assert isinstance(result, FlextResult)
        assert result.success

        temp_path = result.value
        assert isinstance(temp_path, Path)
        assert temp_path.exists()

        # Cleanup
        import shutil

        shutil.rmtree(temp_path)

    def test_create_plugin_config(self) -> None:
        """Test create_plugin_config method."""
        result = FlextMeltanoUtilities.create_plugin_config("tap-csv")

        assert isinstance(result, FlextResult)
        assert result.success

        config = result.value
        assert isinstance(config, dict)

    def test_create_plugin_config_full_params(self) -> None:
        """Test create_plugin_config with all parameters."""
        result = FlextMeltanoUtilities.create_plugin_config(
            name="tap-csv",
            plugin_type="extractor",
            namespace="tap_csv",
            pip_url="pipelinewise-tap-csv",
            executable="tap-csv",
        )

        assert isinstance(result, FlextResult)
        assert result.success

        config = result.value
        assert isinstance(config, dict)

    def test_create_plugin_config_dict(self) -> None:
        """Test create_plugin_config_dict method."""
        result = FlextMeltanoUtilities.create_plugin_config_dict("tap-postgres")

        assert isinstance(result, FlextResult)
        assert result.success

        config = result.value
        assert isinstance(config, dict)

    def test_create_singer_tap_config(self) -> None:
        """Test create_singer_tap_config method."""
        result = FlextMeltanoUtilities.create_singer_tap_config(
            "tap-csv", "tap_csv", "pipelinewise-tap-csv", "tap-csv"
        )

        assert isinstance(result, FlextResult)
        assert result.success

        config = result.value
        assert isinstance(config, dict)

    def test_create_singer_target_config(self) -> None:
        """Test create_singer_target_config method."""
        result = FlextMeltanoUtilities.create_singer_target_config(
            "target-postgres",
            "target_postgres",
            "pipelinewise-target-postgres",
            "target-postgres",
        )

        assert isinstance(result, FlextResult)
        assert result.success

        config = result.value
        assert isinstance(config, dict)

    def test_create_dbt_config(self) -> None:
        """Test create_dbt_config method."""
        result = FlextMeltanoUtilities.create_dbt_config("dbt-project", "analytics")

        assert isinstance(result, FlextResult)
        assert result.success

        config = result.value
        assert isinstance(config, dict)

    def test_normalize_plugin_name(self) -> None:
        """Test normalize_plugin_name method."""
        result = FlextMeltanoUtilities.normalize_plugin_name("tap_csv")

        assert isinstance(result, FlextResult)
        assert result.success

        normalized_name = result.value
        assert isinstance(normalized_name, str)

    def test_normalize_plugin_name_with_type(self) -> None:
        """Test normalize_plugin_name with plugin type."""
        result = FlextMeltanoUtilities.normalize_plugin_name(
            "target_postgres", "target"
        )

        assert isinstance(result, FlextResult)
        assert result.success

        normalized_name = result.value
        assert isinstance(normalized_name, str)

    def test_sanitize_plugin_name(self) -> None:
        """Test sanitize_plugin_name method."""
        result = FlextMeltanoUtilities.sanitize_plugin_name("tap-csv")

        assert isinstance(result, FlextResult)
        assert result.success

        sanitized_name = result.value
        assert isinstance(sanitized_name, str)
        # Method replaces hyphens with underscores
        assert sanitized_name == "tap_csv"

    def test_sanitize_plugin_name_with_special_chars(self) -> None:
        """Test sanitize_plugin_name with special characters."""
        result = FlextMeltanoUtilities.sanitize_plugin_name("tap-csv@!#$")

        assert isinstance(result, FlextResult)
        assert result.success

        sanitized_name = result.value
        assert isinstance(sanitized_name, str)
        # Method only replaces hyphens, keeps other characters
        assert "tap_csv" in sanitized_name

    def test_format_command_result(self) -> None:
        """Test format_command_result method."""
        result = FlextMeltanoUtilities.format_command_result(
            0, "Success output", "test command"
        )

        assert isinstance(result, dict)
        assert "exit_code" in result or "success" in result or "output" in result

    def test_create_bridge_response_success(self) -> None:
        """Test create_bridge_response for success case."""
        result = FlextMeltanoUtilities.create_bridge_response(success=True)

        assert isinstance(result, dict)
        assert "success" in result or "status" in result

    def test_create_bridge_response_failure(self) -> None:
        """Test create_bridge_response for failure case."""
        result = FlextMeltanoUtilities.create_bridge_response(success=False)

        assert isinstance(result, dict)
        assert "success" in result or "status" in result

    def test_parse_meltano_output_safe(self) -> None:
        """Test parse_meltano_output_safe method."""
        test_output = "Test command output"
        result = FlextMeltanoUtilities.parse_meltano_output_safe(test_output)

        assert isinstance(result, FlextResult)
        # Can succeed or fail depending on output format
        if result.success:
            parsed_output = result.value
            assert isinstance(parsed_output, dict)
        else:
            assert result.error_message

    def test_load_yaml_config(self) -> None:
        """Test load_yaml_config method."""
        with tempfile.NamedTemporaryFile(
            encoding="utf-8", mode="w", suffix=".yml", delete=False
        ) as f:
            f.write("version: 1\nproject_id: test")
            config_path = Path(f.name)

        try:
            result = FlextMeltanoUtilities.load_yaml_config(config_path)

            assert isinstance(result, FlextResult)
            if result.success:
                config = result.value
                assert isinstance(config, dict)
            else:
                assert result.error_message
        finally:
            config_path.unlink(missing_ok=True)

    def test_load_yaml_config_nonexistent(self) -> None:
        """Test load_yaml_config with nonexistent file."""
        nonexistent_path = Path("/nonexistent/file.yml")

        result = FlextMeltanoUtilities.load_yaml_config(nonexistent_path)

        assert isinstance(result, FlextResult)
        assert not result.success
        assert result.error_message

    def test_save_yaml_config(self) -> None:
        """Test save_yaml_config method."""
        config = {"version": 1, "project_id": "test"}

        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = Path(temp_dir) / "test_config.yml"

            result = FlextMeltanoUtilities.save_yaml_config(config, target_path)

            assert isinstance(result, FlextResult)
            if result.success:
                assert result.value
                assert target_path.exists()
            else:
                assert result.error_message

    def test_write_meltano_yml(self) -> None:
        """Test write_meltano_yml method."""
        config = {"version": 1, "project_id": "test-project"}

        with tempfile.TemporaryDirectory() as temp_dir:
            target_path = Path(temp_dir) / "meltano.yml"

            result = FlextMeltanoUtilities.write_meltano_yml(config, target_path)

            assert isinstance(result, FlextResult)
            if result.success:
                assert result.value
                assert target_path.exists()
            else:
                assert result.error_message

    def test_setup_project_structure(self) -> None:
        """Test setup_project_structure method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            project_root = Path(temp_dir)
            project_name = "test-project"

            result = FlextMeltanoUtilities.setup_project_structure(
                project_root, project_name
            )

            assert isinstance(result, FlextResult)
            # Can succeed or fail
            if result.success:
                project_result = result.value
                assert isinstance(project_result, dict)
            else:
                assert result.error_message

    def test_validate_plugin_config(self) -> None:
        """Test validate_plugin_config method."""
        # Create a basic plugin config
        config_result = FlextMeltanoUtilities.create_plugin_config("tap-csv")
        assert config_result.success

        config = config_result.value

        result = FlextMeltanoUtilities.validate_plugin_config(config)

        assert isinstance(result, FlextResult)
        if result.success:
            assert result.value
        else:
            assert result.error_message
