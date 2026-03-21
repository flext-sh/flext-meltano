"""Enhanced comprehensive tests for m module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import pytest
from flext_tests import m, u
from pydantic import ValidationError

from flext_meltano import m


class TestTapConfigEnhanced:
    """Enhanced tests for TapConfig model."""

    def test_tap_config_with_minimal_data(self) -> None:
        """Test TapConfig with minimal required data."""
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres", connection_config={"host": "localhost"}
        )
        u.Tests.Matchers.that(config.tap_type, eq="tap-postgres")
        u.Tests.Matchers.that(config.connection_config, eq={"host": "localhost"})
        u.Tests.Matchers.that(config.stream_config, eq={})
        u.Tests.Matchers.that(config.tap_version, eq="latest")

    def test_tap_config_with_full_data(self) -> None:
        """Test TapConfig with all fields populated."""
        config = m.Meltano.TapConfig(
            tap_type="tap-mysql",
            connection_config={
                "host": "db.example.com",
                "port": 3306,
                "user": "etl_user",
                "password": "secret",
            },
            stream_config={
                "users": "public",
                "orders": "commerce",
            },
            tap_version="1.0.0",
        )
        u.Tests.Matchers.that(config.tap_type, eq="tap-mysql")
        u.Tests.Matchers.that(config.connection_config["host"], eq="db.example.com")
        u.Tests.Matchers.that(config.connection_config["port"], eq=3306)
        u.Tests.Matchers.that("users" in config.stream_config, eq=True)
        u.Tests.Matchers.that(config.tap_version, eq="1.0.0")

    def test_tap_config_validation_empty_tap_type(self) -> None:
        """Test TapConfig validation with empty tap_type."""
        with pytest.raises(ValidationError, match="tap_type cannot be empty"):
            m.Meltano.TapConfig(tap_type="", connection_config={"host": "localhost"})

    def test_tap_config_validation_invalid_connection_config_type(self) -> None:
        """Test TapConfig validation with invalid connection_config type."""
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.Meltano.TapConfig(tap_type="tap-postgres", connection_config="invalid")  # type: ignore[arg-type]


class TestTargetConfigEnhanced:
    """Enhanced tests for TargetConfig model."""

    def test_target_config_with_minimal_data(self) -> None:
        """Test TargetConfig with minimal required data."""
        config = m.Meltano.TargetConfig(target_type="target-csv")
        u.Tests.Matchers.that(config.target_type, eq="target-csv")
        u.Tests.Matchers.that(config.connection_config, eq={})
        u.Tests.Matchers.that(config.batch_size is None, eq=True)
        u.Tests.Matchers.that(config.batch_wait_limit is None, eq=True)

    def test_target_config_with_full_data(self) -> None:
        """Test TargetConfig with all fields populated."""
        config = m.Meltano.TargetConfig(
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
        u.Tests.Matchers.that(config.target_type, eq="target-postgres")
        u.Tests.Matchers.that(config.connection_config["database"], eq="analytics")
        u.Tests.Matchers.that(config.batch_size, eq=1000)
        if config.batch_wait_limit is not None:
            u.Tests.Matchers.that(abs(config.batch_wait_limit - 30.0), lt=1e-9)

    def test_target_config_validation_empty_target_type(self) -> None:
        """Test TargetConfig validation with empty target_type."""
        with pytest.raises(ValidationError, match="target_type cannot be empty"):
            m.Meltano.TargetConfig(target_type="")

    def test_target_config_validation_invalid_batch_size_type(self) -> None:
        """Test TargetConfig validation with invalid batch_size type."""
        with pytest.raises(ValidationError, match="Input should be a valid integer"):
            m.Meltano.TargetConfig(target_type="target-csv", batch_size="invalid")  # type: ignore[arg-type]


class TestStreamInfoEnhanced:
    """Enhanced tests for StreamInfo model."""

    def test_stream_info_with_minimal_data(self) -> None:
        """Test StreamInfo with minimal required data."""
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object", "properties": "id"},
            stream_created_at="2025-01-01T00:00:00Z",
        )
        u.Tests.Matchers.that(stream.stream_name, eq="users")
        u.Tests.Matchers.that(stream.stream_schema["type"], eq="object")
        u.Tests.Matchers.that(stream.status, eq="initialized")
        u.Tests.Matchers.that(stream.records_loaded, eq=0)
        u.Tests.Matchers.that(stream.batches_processed, eq=0)
        u.Tests.Matchers.that(stream.stream_created_at, eq="2025-01-01T00:00:00Z")

    def test_stream_info_with_full_data(self) -> None:
        """Test StreamInfo with all fields populated."""
        stream = m.Meltano.StreamInfo(
            stream_name="orders",
            stream_schema={
                "type": "object",
                "properties": "id,order_date,amount",
            },
            key_properties=["id"],
            replication_method="FULL_TABLE",
            replication_key="order_date",
            stream_created_at="2025-01-01T00:00:00Z",
        )
        u.Tests.Matchers.that(stream.stream_name, eq="orders")
        u.Tests.Matchers.that(stream.key_properties, eq=["id"])
        u.Tests.Matchers.that(stream.replication_method, eq="FULL_TABLE")
        u.Tests.Matchers.that(stream.replication_key, eq="order_date")

    def test_stream_info_validation_empty_stream_name(self) -> None:
        """Test StreamInfo validation with empty stream_name."""
        with pytest.raises(
            ValidationError, match="String should have at least 1 character"
        ):
            m.Meltano.StreamInfo(
                stream_name="",
                stream_schema={"type": "object"},
                stream_created_at="2025-01-01T00:00:00Z",
            )

    def test_stream_info_validation_invalid_schema_type(self) -> None:
        """Test StreamInfo validation with invalid schema type."""
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.Meltano.StreamInfo(
                stream_name="users",
                stream_schema="invalid",  # type: ignore[arg-type]
                stream_created_at="2025-01-01T00:00:00Z",
            )


class TestMeltanoProjectModelEnhanced:
    """Enhanced tests for MeltanoProjectModel."""

    def test_meltano_project_with_minimal_data(self) -> None:
        """Test MeltanoProjectModel with minimal required data."""
        project = m.Meltano.MeltanoProjectModel(project_id="test-project")
        u.Tests.Matchers.that(project.project_id, eq="test-project")
        u.Tests.Matchers.that(project.project_version, eq="1")
        u.Tests.Matchers.that(project.default_environment, eq="dev")
        u.Tests.Matchers.that(project.plugins, eq={})
        u.Tests.Matchers.that(project.environments, eq={})

    def test_meltano_project_with_full_data(self) -> None:
        """Test MeltanoProjectModel with all fields populated."""
        project = m.Meltano.MeltanoProjectModel(
            project_id="analytics-project",
            project_version="2.0",
            default_environment="production",
            plugins={
                "extractors": "tap-postgres",
                "loaders": "target-csv",
            },
            environments={
                "dev": "development",
                "prod": "production",
            },
        )
        u.Tests.Matchers.that(project.project_id, eq="analytics-project")
        u.Tests.Matchers.that(project.project_version, eq="2.0")
        u.Tests.Matchers.that(project.default_environment, eq="production")
        u.Tests.Matchers.that("extractors" in project.plugins, eq=True)
        u.Tests.Matchers.that("dev" in project.environments, eq=True)
        u.Tests.Matchers.that("prod" in project.environments, eq=True)

    def test_meltano_project_validation_empty_project_id(self) -> None:
        """Test MeltanoProjectModel validation with empty project_id."""
        with pytest.raises(ValidationError, match="project_id cannot be empty"):
            m.Meltano.MeltanoProjectModel(project_id="")

    def test_meltano_project_validation_invalid_plugins_type(self) -> None:
        """Test MeltanoProjectModel validation with invalid plugins type."""
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.Meltano.MeltanoProjectModel(project_id="test-project", plugins="invalid")  # type: ignore[arg-type]


class TestPluginModelEnhanced:
    """Enhanced tests for PluginModel."""

    def test_plugin_model_with_minimal_data(self) -> None:
        """Test PluginModel with minimal required data."""
        plugin = m.Meltano.PluginModel(
            name="tap-postgres", namespace="tap_postgres", pip_url="tap-postgres"
        )
        u.Tests.Matchers.that(plugin.name, eq="tap-postgres")
        u.Tests.Matchers.that(plugin.namespace, eq="tap_postgres")
        u.Tests.Matchers.that(plugin.variant, eq="standard")
        u.Tests.Matchers.that(plugin.pip_url, eq="tap-postgres")
        u.Tests.Matchers.that(plugin.executable is None, eq=True)
        u.Tests.Matchers.that(plugin.capabilities, eq=[])
        u.Tests.Matchers.that(plugin.settings, eq={})
        u.Tests.Matchers.that(plugin.config_files, eq=[])

    def test_plugin_model_with_full_data(self) -> None:
        """Test PluginModel with all fields populated."""
        plugin = m.Meltano.PluginModel(
            name="tap-postgres",
            namespace="meltanolabs",
            variant="meltanolabs",
            pip_url="git+https://github.com/meltanolabs/tap-postgres.git",
            executable="tap-postgres",
            capabilities=["catalog", "discover", "sync"],
            settings={
                "host": "string",
                "port": "integer",
            },
            config_files=["config.json"],
        )
        u.Tests.Matchers.that(plugin.name, eq="tap-postgres")
        u.Tests.Matchers.that(plugin.namespace, eq="meltanolabs")
        u.Tests.Matchers.that(plugin.variant, eq="meltanolabs")
        u.Tests.Matchers.that(
            plugin.pip_url, eq="git+https://github.com/meltanolabs/tap-postgres.git"
        )
        u.Tests.Matchers.that(plugin.executable, eq="tap-postgres")
        u.Tests.Matchers.that("catalog" in plugin.capabilities, eq=True)
        u.Tests.Matchers.that(len(plugin.settings), eq=2)
        u.Tests.Matchers.that("host" in plugin.settings, eq=True)

    def test_plugin_model_validation_empty_name(self) -> None:
        """Test PluginModel validation with empty name."""
        with pytest.raises(
            ValidationError, match="String should have at least 1 character"
        ):
            m.Meltano.PluginModel(name="", namespace="")

    def test_plugin_model_validation_invalid_capabilities_type(self) -> None:
        """Test PluginModel validation with invalid capabilities type."""
        with pytest.raises(ValidationError, match="Input should be a valid list"):
            m.Meltano.PluginModel(
                name="tap-postgres",
                namespace="tap-postgres",
                capabilities="invalid",  # type: ignore[arg-type]
            )


class TestDbtProjectModelEnhanced:
    """Enhanced tests for DbtProjectModel."""

    def test_dbt_project_with_minimal_data(self) -> None:
        """Test DbtProjectModel with minimal required data."""
        dbt_project = m.Meltano.DbtProjectModel(
            name="analytics", dbt_version="1.0.0", profile="default"
        )
        u.Tests.Matchers.that(dbt_project.name, eq="analytics")
        u.Tests.Matchers.that(dbt_project.profile, eq="default")
        u.Tests.Matchers.that(dbt_project.dbt_version, eq="1.0.0")
        u.Tests.Matchers.that(dbt_project.config, eq={})
        u.Tests.Matchers.that(dbt_project.models, eq={})
        u.Tests.Matchers.that(dbt_project.sources, eq={})
        u.Tests.Matchers.that(dbt_project.tests, eq={})

    def test_dbt_project_with_full_data(self) -> None:
        """Test DbtProjectModel with all fields populated."""
        dbt_project = m.Meltano.DbtProjectModel(
            name="data-warehouse",
            profile="postgres",
            dbt_version="2.1.0",
            config={"materialized": "table", "on_schema_change": "fail_safe"},
            models={
                "staging": "view",
            },
            sources={"raw_data": "users"},
            tests={"unit": "test_user_validity"},
        )
        u.Tests.Matchers.that(dbt_project.name, eq="data-warehouse")
        u.Tests.Matchers.that(dbt_project.profile, eq="postgres")
        u.Tests.Matchers.that(dbt_project.dbt_version, eq="2.1.0")
        u.Tests.Matchers.that(dbt_project.config["materialized"], eq="table")
        u.Tests.Matchers.that("staging" in dbt_project.models, eq=True)
        u.Tests.Matchers.that("raw_data" in dbt_project.sources, eq=True)
        u.Tests.Matchers.that("unit" in dbt_project.tests, eq=True)

    def test_dbt_project_validation_empty_name(self) -> None:
        """Test DbtProjectModel validation with empty name."""
        with pytest.raises(ValidationError, match="name cannot be empty"):
            m.Meltano.DbtProjectModel(name="", profile="default")

    def test_dbt_project_validation_empty_profile(self) -> None:
        """Test DbtProjectModel validation with empty profile."""
        with pytest.raises(ValidationError, match="profile cannot be empty"):
            m.Meltano.DbtProjectModel(name="test-project", profile="")

    def test_dbt_project_validation_invalid_config_type(self) -> None:
        """Test DbtProjectModel validation with invalid config type."""
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.Meltano.DbtProjectModel(
                name="test-project",
                profile="default",
                config="invalid",  # type: ignore[arg-type]
            )


class TestModelIntegration:
    """Integration tests for model interactions."""

    def test_tap_and_target_config_integration(self) -> None:
        """Test integration between TapConfig and TargetConfig."""
        tap_config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "source.db.com", "port": 5432},
        )
        target_config = m.Meltano.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "target.db.com", "port": 5432},
        )
        u.Tests.Matchers.that(tap_config.tap_type, eq="tap-postgres")
        u.Tests.Matchers.that(target_config.target_type, eq="target-postgres")
        u.Tests.Matchers.that(tap_config.connection_config["host"], eq="source.db.com")
        u.Tests.Matchers.that(
            target_config.connection_config["host"], eq="target.db.com"
        )

    def test_plugin_model_with_project_integration(self) -> None:
        """Test PluginModel integration with MeltanoProjectModel."""
        plugin = m.Meltano.PluginModel(
            name="tap-mysql", namespace="meltanolabs", pip_url="tap-mysql"
        )
        project = m.Meltano.MeltanoProjectModel(
            project_id="mysql-etl", plugins={"extractors": "tap-mysql"}
        )
        u.Tests.Matchers.that(plugin.name in str(project.plugins), eq=True)
        u.Tests.Matchers.that(project.project_id, eq="mysql-etl")

    def test_stream_info_with_tap_config_integration(self) -> None:
        """Test StreamInfo integration with TapConfig."""
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "object", "properties": "id"},
            key_properties=["id"],
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tap_config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
            stream_config={"users": "public"},
        )
        u.Tests.Matchers.that(stream.stream_name in tap_config.stream_config, eq=True)
        u.Tests.Matchers.that(stream.key_properties, eq=["id"])
