"""Tests for FLEXT Meltano models module.

Comprehensive tests for all model classes and backward compatibility aliases.
Zero tolerance for untested code.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from flext_meltano.models import (
    FlextMeltanoEnvironment,
    FlextMeltanoJob,
    FlextMeltanoPlugin,
    FlextMeltanoPlugins,
    FlextMeltanoProjectConfig,
    FlextMeltanoSchedule,
    # Backward compatibility aliases
    MeltanoEnvironment,
    MeltanoJob,
    MeltanoPlugin,
    MeltanoPlugins,
    MeltanoProjectConfig,
    MeltanoSchedule,
)


class TestFlextMeltanoPlugin:
    """Test FlextMeltanoPlugin model."""

    def test_plugin_creation_minimal(self) -> None:
        """Test plugin creation with minimal fields."""
        plugin = FlextMeltanoPlugin.model_validate({"name": "test-plugin"})

        assert plugin.name == "test-plugin"
        assert plugin.namespace is None
        assert plugin.pip_url is None
        assert plugin.executable is None
        assert plugin.config == {}
        assert plugin.settings == []
        assert plugin.variant is None
        assert plugin.docs is None
        assert plugin.description is None

    def test_plugin_creation_full(self) -> None:
        """Test plugin creation with all fields."""
        plugin = FlextMeltanoPlugin.model_validate(
            {
                "name": "tap-csv",
                "namespace": "tap_csv",
                "pip_url": "pipelinewise-tap-csv",
                "executable": "tap-csv",
                "config": {"files": [{"entity": "test", "path": "test.csv"}]},
                "settings": [{"name": "files", "kind": "array"}],
                "variant": "original",
                "docs": "https://hub.meltano.com/extractors/tap-csv",
                "description": "CSV extractor",
            },
        )

        assert plugin.name == "tap-csv"
        assert plugin.namespace == "tap_csv"
        assert plugin.pip_url == "pipelinewise-tap-csv"
        assert plugin.executable == "tap-csv"
        assert plugin.config == {
            "files": [{"entity": "test", "path": "test.csv"}],
        }
        assert plugin.settings == [{"name": "files", "kind": "array"}]
        assert plugin.variant == "original"
        assert plugin.docs == "https://hub.meltano.com/extractors/tap-csv"
        assert plugin.description == "CSV extractor"

    def test_plugin_validation_error(self) -> None:
        """Test plugin validation with missing required fields."""
        with pytest.raises(ValidationError):
            FlextMeltanoPlugin.model_validate(
                {},
            )  # Missing required 'name' field


class TestFlextMeltanoPlugins:
    """Test FlextMeltanoPlugins collection model."""

    def test_plugins_creation_empty(self) -> None:
        """Test plugins creation with empty collections."""
        plugins = FlextMeltanoPlugins.model_validate({})

        assert plugins.extractors == []
        assert plugins.loaders == []
        assert plugins.transformers == []
        assert plugins.files == []
        assert plugins.utilities == []
        assert plugins.orchestrators == []

    def test_plugins_creation_with_data(self) -> None:
        """Test plugins creation with actual plugin data."""
        extractor = FlextMeltanoPlugin.model_validate({"name": "tap-csv"})
        loader = FlextMeltanoPlugin.model_validate({"name": "target-jsonl"})

        plugins = FlextMeltanoPlugins.model_validate(
            {
                "extractors": [extractor.model_dump()],
                "loaders": [loader.model_dump()],
            },
        )

        assert len(plugins.extractors) == 1
        assert plugins.extractors[0,].name == "tap-csv"
        assert len(plugins.loaders) == 1
        assert plugins.loaders[0,].name == "target-jsonl"


class TestFlextMeltanoJob:
    """Test FlextMeltanoJob model."""

    def test_job_creation_minimal(self) -> None:
        """Test job creation with minimal fields."""
        job = FlextMeltanoJob.model_validate(
            {"job_name": "test-job", "tasks": ["tap-csv target-jsonl"]},
        )

        assert job.job_name == "test-job"
        assert job.tasks == ["tap-csv target-jsonl"]
        assert job.description is None
        assert job.env == {}

    def test_job_creation_full(self) -> None:
        """Test job creation with all fields."""
        job = FlextMeltanoJob.model_validate(
            {
                "job_name": "etl-job",
                "tasks": ["tap-csv target-jsonl"],
                "description": "Extract and load CSV data",
                "env": {"BATCH_SIZE": "1000"},
            },
        )

        assert job.job_name == "etl-job"
        assert job.tasks == ["tap-csv target-jsonl"]
        assert job.description == "Extract and load CSV data"
        assert job.env == {"BATCH_SIZE": "1000"}

    def test_job_validation_error(self) -> None:
        """Test job validation with missing required fields."""
        with pytest.raises(ValidationError):
            FlextMeltanoJob.model_validate(
                {"job_name": "test"},
            )  # Missing required 'tasks' field


class TestFlextMeltanoSchedule:
    """Test FlextMeltanoSchedule model."""

    def test_schedule_creation_minimal(self) -> None:
        """Test schedule creation with minimal fields."""
        schedule = FlextMeltanoSchedule.model_validate(
            {"name": "daily", "job": "etl-job", "cron_interval": "0 6 * * *"},
        )

        assert schedule.name == "daily"
        assert schedule.job == "etl-job"
        assert schedule.cron_interval == "0 6 * * *"
        assert schedule.timezone == "UTC"


class TestFlextMeltanoEnvironment:
    """Test FlextMeltanoEnvironment model."""

    def test_environment_creation_minimal(self) -> None:
        """Test environment creation with minimal fields."""
        env = FlextMeltanoEnvironment.model_validate({"name": "dev"})

        assert env.name == "dev"
        assert env.config == {}
        assert env.env == {}


class TestFlextMeltanoProjectConfig:
    """Test FlextMeltanoProjectConfig model."""

    def test_project_config_creation_minimal(self) -> None:
        """Test project config creation with minimal fields."""
        config = FlextMeltanoProjectConfig.model_validate(
            {"version": 1, "project_id": "test-project"},
        )

        assert config.version == 1
        assert config.project_id == "test-project"
        assert config.plugins.extractors == []
        assert config.jobs == []
        assert config.schedules == []
        assert config.environments == []
        assert config.default_environment is None
        assert config.project_root is None


class TestBackwardCompatibilityAliases:
    """Test that backward compatibility aliases work correctly."""

    def test_plugin_aliases(self) -> None:
        """Test that MeltanoPlugin is an alias for FlextMeltanoPlugin."""
        assert MeltanoPlugin is FlextMeltanoPlugin

    def test_plugins_aliases(self) -> None:
        """Test that MeltanoPlugins is an alias for FlextMeltanoPlugins."""
        assert MeltanoPlugins is FlextMeltanoPlugins

    def test_job_aliases(self) -> None:
        """Test that MeltanoJob is an alias for FlextMeltanoJob."""
        assert MeltanoJob is FlextMeltanoJob

    def test_schedule_aliases(self) -> None:
        """Test that MeltanoSchedule is an alias for FlextMeltanoSchedule."""
        assert MeltanoSchedule is FlextMeltanoSchedule

    def test_environment_aliases(self) -> None:
        """Test that MeltanoEnvironment is an alias for FlextMeltanoEnvironment."""
        assert MeltanoEnvironment is FlextMeltanoEnvironment

    def test_project_config_aliases(self) -> None:
        """Test that MeltanoProjectConfig is an alias for FlextMeltanoProjectConfig."""
        assert MeltanoProjectConfig is FlextMeltanoProjectConfig


class TestModelIntegration:
    """Test models working together in realistic scenarios."""

    def test_model_serialization(self) -> None:
        """Test that models can be serialized and deserialized."""
        original = FlextMeltanoPlugin.model_validate(
            {
                "name": "test-plugin",
                "config": {"setting": "value"},
                "settings": [{"name": "setting", "type": "string"}],
            },
        )

        # Test dict conversion
        plugin_dict = original.model_dump()
        assert plugin_dict["name",] == "test-plugin"
        assert plugin_dict["config",] == {"setting": "value"}

        # Test reconstruction from dict
        reconstructed = FlextMeltanoPlugin.model_validate(plugin_dict)
        assert reconstructed.name == original.name
        assert reconstructed.config == original.config
        assert reconstructed.settings == original.settings
