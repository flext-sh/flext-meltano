"""Enhanced comprehensive tests for m module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from flext_meltano import m


class TestTapConfigEnhanced:
    """Enhanced tests for TapConfig model."""

    def test_tap_config_with_minimal_data(self) -> None:
        """Test TapConfig with minimal required data."""
        config = m.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
        )

        assert config.tap_type == "tap-postgres"
        assert config.connection_config == {"host": "localhost"}
        assert config.stream_config == {}
        assert config.version == "latest"

    def test_tap_config_with_full_data(self) -> None:
        """Test TapConfig with all fields populated."""
        config = m.TapConfig(
            tap_type="tap-mysql",
            connection_config={
                "host": "db.example.com",
                "port": 3306,
                "user": "admin",
                "password": "secret",
            },
            stream_config={
                "users": {"schema": "public"},
                "orders": {"schema": "commerce"},
            },
            version="1.0.0",
        )

        assert config.tap_type == "tap-mysql"
        assert config.connection_config["host"] == "db.example.com"
        assert config.connection_config["port"] == 3306
        assert "users" in config.stream_config
        assert config.version == "1.0.0"

    def test_tap_config_validation_empty_tap_type(self) -> None:
        """Test TapConfig validation with empty tap_type."""
        with pytest.raises(ValidationError, match="tap_type cannot be empty"):
            m.TapConfig(tap_type="", connection_config={"host": "localhost"})

    def test_tap_config_validation_invalid_connection_config_type(self) -> None:
        """Test TapConfig validation with invalid connection_config type."""
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.TapConfig(
                tap_type="tap-postgres",
                connection_config="invalid",  # Should be dict
            )


class TestTargetConfigEnhanced:
    """Enhanced tests for TargetConfig model."""

    def test_target_config_with_minimal_data(self) -> None:
        """Test TargetConfig with minimal required data."""
        config = m.TargetConfig(target_type="target-csv")

        assert config.target_type == "target-csv"
        assert config.connection_config == {}
        assert config.batch_size is None
        assert config.batch_wait_limit is None

    def test_target_config_with_full_data(self) -> None:
        """Test TargetConfig with all fields populated."""
        config = m.TargetConfig(
            target_type="target-postgres",
            connection_config={
                "host": "localhost",
                "port": 5432,
                "database": "analytics",
                "user": "etl_user",
                "password": "etl_pass",
            },
            batch_size=1000,
            batch_wait_limit=30.0,
        )

        assert config.target_type == "target-postgres"
        assert config.connection_config["database"] == "analytics"
        assert config.batch_size == 1000
        assert config.batch_wait_limit == 30.0

    def test_target_config_validation_empty_target_type(self) -> None:
        """Test TargetConfig validation with empty target_type."""
        with pytest.raises(ValidationError, match="target_type cannot be empty"):
            m.TargetConfig(target_type="", connection_config={"host": "localhost"})

    def test_target_config_validation_invalid_batch_size_type(self) -> None:
        """Test TargetConfig validation with invalid batch_size type."""
        with pytest.raises(ValidationError, match="Input should be a valid integer"):
            m.TargetConfig(
                target_type="target-csv",
                batch_size="invalid",  # Should be int
            )


class TestStreamInfoEnhanced:
    """Enhanced tests for StreamInfo model."""

    def test_stream_info_with_minimal_data(self) -> None:
        """Test StreamInfo with minimal required data."""
        stream = m.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            created_at="2025-01-01T00:00:00Z",
        )

        assert stream.stream_name == "users"
        assert stream.stream_schema["type"] == "object"
        assert stream.status == "initialized"
        assert stream.records_loaded == 0
        assert stream.batches_processed == 0
        assert stream.created_at == "2025-01-01T00:00:00Z"

    def test_stream_info_with_full_data(self) -> None:
        """Test StreamInfo with all fields populated."""
        stream = m.StreamInfo(
            stream_name="orders",
            stream_schema={
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "order_date": {"type": "string", "format": "date-time"},
                    "amount": {"type": "number"},
                },
            },
            key_properties=["id"],
            replication_method="FULL_TABLE",
            replication_key="order_date",
            created_at="2025-01-01T00:00:00Z",
        )

        assert stream.stream_name == "orders"
        assert stream.key_properties == ["id"]
        assert stream.replication_method == "FULL_TABLE"
        assert stream.replication_key == "order_date"

    def test_stream_info_validation_empty_stream_name(self) -> None:
        """Test StreamInfo validation with empty stream_name."""
        with pytest.raises(
            ValidationError,
            match="String should have at least 1 character",
        ):
            m.StreamInfo(
                stream_name="",
                stream_schema={"type": "object"},
                created_at="2025-01-01T00:00:00Z",
            )

    def test_stream_info_validation_invalid_schema_type(self) -> None:
        """Test StreamInfo validation with invalid schema type."""
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.StreamInfo(
                stream_name="users",
                stream_schema="invalid",  # Should be dict
                created_at="2025-01-01T00:00:00Z",
            )


class TestMeltanoProjectModelEnhanced:
    """Enhanced tests for MeltanoProjectModel."""

    def test_meltano_project_with_minimal_data(self) -> None:
        """Test MeltanoProjectModel with minimal required data."""
        project = m.MeltanoProjectModel(project_id="test-project")

        assert project.project_id == "test-project"
        assert project.version == "1"
        assert project.default_environment == "dev"
        assert project.plugins == {}
        assert project.environments == {}

    def test_meltano_project_with_full_data(self) -> None:
        """Test MeltanoProjectModel with all fields populated."""
        project = m.MeltanoProjectModel(
            project_id="analytics-project",
            version="2.0",
            default_environment="production",
            plugins={
                "extractors": [{"name": "tap-postgres"}],
                "loaders": [{"name": "target-csv"}],
            },
            environments={
                "dev": {"plugins": {"extractors": []}},
                "prod": {"plugins": {"extractors": [{"name": "tap-postgres"}]}},
            },
        )

        assert project.project_id == "analytics-project"
        assert project.version == "2.0"
        assert project.default_environment == "production"
        assert "extractors" in project.plugins
        assert "dev" in project.environments
        assert "prod" in project.environments

    def test_meltano_project_validation_empty_project_id(self) -> None:
        """Test MeltanoProjectModel validation with empty project_id."""
        with pytest.raises(ValidationError, match="project_id cannot be empty"):
            m.MeltanoProjectModel(project_id="")

    def test_meltano_project_validation_invalid_plugins_type(self) -> None:
        """Test MeltanoProjectModel validation with invalid plugins type."""
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.MeltanoProjectModel(
                project_id="test-project",
                plugins="invalid",  # Should be dict
            )


class TestPluginModelEnhanced:
    """Enhanced tests for PluginModel."""

    def test_plugin_model_with_minimal_data(self) -> None:
        """Test PluginModel with minimal required data."""
        plugin = m.PluginModel(
            name="tap-postgres",
            namespace="tap_postgres",
            pip_url="tap-postgres",
        )

        assert plugin.name == "tap-postgres"
        assert plugin.namespace == "tap_postgres"
        assert plugin.variant == "standard"
        assert plugin.pip_url == "tap-postgres"
        assert plugin.executable is None
        assert plugin.capabilities == []
        assert plugin.settings == {}
        assert plugin.config_files == []

    def test_plugin_model_with_full_data(self) -> None:
        """Test PluginModel with all fields populated."""
        plugin = m.PluginModel(
            name="tap-postgres",
            namespace="meltanolabs",
            variant="meltanolabs",
            pip_url="git+https://github.com/meltanolabs/tap-postgres.git",
            executable="tap-postgres",
            capabilities=["catalog", "discover", "sync"],
            settings={
                "host": {
                    "kind": "string",
                    "label": "Host",
                    "description": "PostgreSQL host",
                },
            },
            config_files=["config.json"],
        )

        assert plugin.name == "tap-postgres"
        assert plugin.namespace == "meltanolabs"
        assert plugin.variant == "meltanolabs"
        assert plugin.pip_url == "git+https://github.com/meltanolabs/tap-postgres.git"
        assert plugin.executable == "tap-postgres"
        assert "catalog" in plugin.capabilities
        assert len(plugin.settings) == 1
        assert "host" in plugin.settings

    def test_plugin_model_validation_empty_name(self) -> None:
        """Test PluginModel validation with empty name."""
        with pytest.raises(
            ValidationError,
            match="String should have at least 1 character",
        ):
            m.PluginModel(name="", namespace="")

    def test_plugin_model_validation_invalid_capabilities_type(self) -> None:
        """Test PluginModel validation with invalid capabilities type."""
        with pytest.raises(ValidationError, match="Input should be a valid list"):
            m.PluginModel(
                name="tap-postgres",
                namespace="tap-postgres",
                capabilities="invalid",  # Should be list
            )


class TestDbtProjectModelEnhanced:
    """Enhanced tests for DbtProjectModel."""

    def test_dbt_project_with_minimal_data(self) -> None:
        """Test DbtProjectModel with minimal required data."""
        dbt_project = m.DbtProjectModel(
            name="analytics",
            version="1.0.0",
            profile="default",
        )

        assert dbt_project.name == "analytics"
        assert dbt_project.profile == "default"
        assert dbt_project.version == "1.0.0"
        assert dbt_project.config == {}
        assert dbt_project.models == {}
        assert dbt_project.sources == {}
        assert dbt_project.tests == {}

    def test_dbt_project_with_full_data(self) -> None:
        """Test DbtProjectModel with all fields populated."""
        dbt_project = m.DbtProjectModel(
            name="data-warehouse",
            profile="postgres",
            version="2.1.0",
            config={"materialized": "table", "on_schema_change": "fail_safe"},
            models={
                "staging": {
                    "materialized": "view",
                    "models": ["stg_users", "stg_orders"],
                },
            },
            sources={"raw_data": {"tables": ["users", "orders"]}},
            tests={"unit": {"models": ["test_user_validity"]}},
        )

        assert dbt_project.name == "data-warehouse"
        assert dbt_project.profile == "postgres"
        assert dbt_project.version == "2.1.0"
        assert dbt_project.config["materialized"] == "table"
        assert "staging" in dbt_project.models
        assert "raw_data" in dbt_project.sources
        assert "unit" in dbt_project.tests

    def test_dbt_project_validation_empty_name(self) -> None:
        """Test DbtProjectModel validation with empty name."""
        with pytest.raises(ValidationError, match="name cannot be empty"):
            m.DbtProjectModel(name="", profile="default")

    def test_dbt_project_validation_empty_profile(self) -> None:
        """Test DbtProjectModel validation with empty profile."""
        with pytest.raises(ValidationError, match="profile cannot be empty"):
            m.DbtProjectModel(name="test-project", profile="")

    def test_dbt_project_validation_invalid_config_type(self) -> None:
        """Test DbtProjectModel validation with invalid config type."""
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.DbtProjectModel(
                name="test-project",
                profile="default",
                config="invalid",  # Should be dict
            )


class TestModelIntegration:
    """Integration tests for model interactions."""

    def test_tap_and_target_config_integration(self) -> None:
        """Test integration between TapConfig and TargetConfig."""
        tap_config = m.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "source.db.com", "port": 5432},
        )

        target_config = m.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "target.db.com", "port": 5432},
        )

        # Both configs should be valid
        assert tap_config.tap_type == "tap-postgres"
        assert target_config.target_type == "target-postgres"
        assert tap_config.connection_config["host"] == "source.db.com"
        assert target_config.connection_config["host"] == "target.db.com"

    def test_plugin_model_with_project_integration(self) -> None:
        """Test PluginModel integration with MeltanoProjectModel."""
        plugin = m.PluginModel(
            name="tap-mysql",
            namespace="meltanolabs",
            pip_url="tap-mysql",
        )

        project = m.MeltanoProjectModel(
            project_id="mysql-etl",
            plugins={"extractors": [{"name": "tap-mysql"}]},
        )

        assert plugin.name in str(project.plugins)
        assert project.project_id == "mysql-etl"

    def test_stream_info_with_tap_config_integration(self) -> None:
        """Test StreamInfo integration with TapConfig."""
        stream = m.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object", "properties": {"id": {"type": "integer"}}},
            key_properties=["id"],
            created_at="2025-01-01T00:00:00Z",
        )

        tap_config = m.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
            stream_config={"users": {"schema": "public"}},
        )

        assert stream.stream_name in tap_config.stream_config
        assert stream.key_properties == ["id"]
