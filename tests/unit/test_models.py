"""Enhanced comprehensive tests for m module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import cast

import pytest
from flext_tests import tm
from pydantic import ValidationError

from tests import m, t


class TestFlextMeltanoModels:
    """Canonical tests for Meltano model validation and composition."""

    def test_tap_config_with_minimal_data(self) -> None:
        settings = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
        )
        tm.that(settings.tap_type, eq="tap-postgres")
        tm.that(settings.connection_config, eq={"host": "localhost"})
        tm.that(settings.stream_config, eq={})
        tm.that(settings.tap_version, eq="latest")

    def test_tap_config_with_full_data(self) -> None:
        settings = m.Meltano.TapConfig(
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
        tm.that(settings.tap_type, eq="tap-mysql")
        tm.that(settings.connection_config["host"], eq="db.example.com")
        tm.that(settings.connection_config["port"], eq=3306)
        tm.that(settings.stream_config, has="users")
        tm.that(settings.tap_version, eq="1.0.0")

    def test_tap_config_validation_empty_tap_type(self) -> None:
        with pytest.raises(ValidationError, match="tap_type cannot be empty"):
            m.Meltano.TapConfig(tap_type="", connection_config={"host": "localhost"})

    def test_tap_config_validation_invalid_connection_config_type(self) -> None:
        invalid_config = cast("t.ScalarMapping", "invalid")
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.Meltano.TapConfig(
                tap_type="tap-postgres",
                connection_config=invalid_config,
            )

    def test_target_config_with_minimal_data(self) -> None:
        settings = m.Meltano.TargetConfig(target_type="target-csv")
        tm.that(settings.target_type, eq="target-csv")
        tm.that(settings.connection_config, eq={})
        tm.that(settings.batch_size, none=True)
        tm.that(settings.batch_wait_limit, none=True)

    def test_target_config_with_full_data(self) -> None:
        settings = m.Meltano.TargetConfig(
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
        tm.that(settings.target_type, eq="target-postgres")
        tm.that(settings.connection_config["database"], eq="analytics")
        tm.that(settings.batch_size, eq=1000)
        if settings.batch_wait_limit is not None:
            tm.that(abs(settings.batch_wait_limit - 30.0), lt=1e-9)

    def test_target_config_validation_empty_target_type(self) -> None:
        with pytest.raises(ValidationError, match="target_type cannot be empty"):
            m.Meltano.TargetConfig(target_type="")

    def test_target_config_validation_invalid_batch_size_type(self) -> None:
        with pytest.raises(ValidationError, match="Input should be a valid integer"):
            m.Meltano.TargetConfig(
                target_type="target-csv", batch_size=cast("int", "invalid")
            )

    def test_stream_info_with_minimal_data(self) -> None:
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "t.NormalizedValue", "properties": "id"},
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tm.that(stream.stream_name, eq="users")
        tm.that(stream.stream_schema["type"], eq="t.NormalizedValue")
        tm.that(stream.status, eq="initialized")
        tm.that(stream.records_loaded, eq=0)
        tm.that(stream.batches_processed, eq=0)
        tm.that(stream.stream_created_at, eq="2025-01-01T00:00:00Z")

    def test_stream_info_with_full_data(self) -> None:
        stream = m.Meltano.StreamInfo(
            stream_name="orders",
            stream_schema={
                "type": "t.NormalizedValue",
                "properties": "id,order_date,amount",
            },
            key_properties=["id"],
            replication_method="FULL_TABLE",
            replication_key="order_date",
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tm.that(stream.stream_name, eq="orders")
        tm.that(stream.key_properties, eq=["id"])
        tm.that(stream.replication_method, eq="FULL_TABLE")
        tm.that(stream.replication_key, eq="order_date")

    def test_stream_info_validation_empty_stream_name(self) -> None:
        with pytest.raises(
            ValidationError,
            match="String should have at least 1 character",
        ):
            m.Meltano.StreamInfo(
                stream_name="",
                stream_schema={"type": "t.NormalizedValue"},
                stream_created_at="2025-01-01T00:00:00Z",
            )

    def test_stream_info_validation_invalid_schema_type(self) -> None:
        invalid_schema = cast("t.ScalarMapping", "invalid")
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.Meltano.StreamInfo(
                stream_name="users",
                stream_schema=invalid_schema,
                stream_created_at="2025-01-01T00:00:00Z",
            )

    def test_meltano_project_with_minimal_data(self) -> None:
        project = m.Meltano.MeltanoProjectModel(project_id="test-project")
        tm.that(project.project_id, eq="test-project")
        tm.that(project.project_version, eq="1")
        tm.that(project.default_environment, eq="dev")
        tm.that(project.plugins, eq={})
        tm.that(project.environments, eq={})

    def test_meltano_project_with_full_data(self) -> None:
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
        tm.that(project.project_id, eq="analytics-project")
        tm.that(project.project_version, eq="2.0")
        tm.that(project.default_environment, eq="production")
        tm.that(project.plugins, has="extractors")
        tm.that(project.environments, has="dev")
        tm.that(project.environments, has="prod")

    def test_meltano_project_validation_empty_project_id(self) -> None:
        with pytest.raises(ValidationError, match="project_id cannot be empty"):
            m.Meltano.MeltanoProjectModel(project_id="")

    def test_meltano_project_validation_invalid_plugins_type(self) -> None:
        invalid_plugins = cast("t.ScalarMapping", "invalid")
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.Meltano.MeltanoProjectModel(
                project_id="test-project",
                plugins=invalid_plugins,
            )

    def test_plugin_model_with_minimal_data(self) -> None:
        plugin = m.Meltano.PluginModel(
            name="tap-postgres",
            namespace="tap_postgres",
            pip_url="tap-postgres",
        )
        tm.that(plugin.name, eq="tap-postgres")
        tm.that(plugin.namespace, eq="tap_postgres")
        tm.that(plugin.variant, eq="standard")
        tm.that(plugin.pip_url, eq="tap-postgres")
        tm.that(plugin.executable, none=True)
        tm.that(plugin.capabilities, eq=[])
        tm.that(plugin.settings, eq={})
        tm.that(plugin.config_files, eq=[])

    def test_plugin_model_with_full_data(self) -> None:
        plugin = m.Meltano.PluginModel(
            name="tap-postgres",
            namespace="meltanolabs",
            variant="meltanolabs",
            pip_url="git+https://github.com/meltanolabs/tap-postgres.git",
            executable="tap-postgres",
            capabilities=["catalog", "discover", "sync"],
            settings={"host": "string", "port": "integer"},
            config_files=["settings.json"],
        )
        tm.that(plugin.name, eq="tap-postgres")
        tm.that(plugin.namespace, eq="meltanolabs")
        tm.that(plugin.variant, eq="meltanolabs")
        tm.that(
            plugin.pip_url, eq="git+https://github.com/meltanolabs/tap-postgres.git"
        )
        tm.that(plugin.executable, eq="tap-postgres")
        tm.that(plugin.capabilities, has="catalog")
        tm.that(len(plugin.settings), eq=2)
        tm.that(plugin.settings, has="host")

    def test_plugin_model_validation_empty_name(self) -> None:
        with pytest.raises(
            ValidationError,
            match="String should have at least 1 character",
        ):
            m.Meltano.PluginModel(name="", namespace="")

    def test_plugin_model_validation_invalid_capabilities_type(self) -> None:
        with pytest.raises(ValidationError, match="not allowed as a Sequence value"):
            m.Meltano.PluginModel(
                name="tap-postgres",
                namespace="tap-postgres",
                capabilities="invalid",
            )

    def test_dbt_project_with_minimal_data(self) -> None:
        dbt_project = m.Meltano.DbtProjectModel(
            name="analytics",
            dbt_version="1.0.0",
            profile="default",
        )
        tm.that(dbt_project.name, eq="analytics")
        tm.that(dbt_project.profile, eq="default")
        tm.that(dbt_project.dbt_version, eq="1.0.0")
        tm.that(dbt_project.settings, eq={})
        tm.that(dbt_project.models, eq={})
        tm.that(dbt_project.sources, eq={})
        tm.that(dbt_project.tests, eq={})

    def test_dbt_project_with_full_data(self) -> None:
        dbt_project = m.Meltano.DbtProjectModel(
            name="data-warehouse",
            profile="postgres",
            dbt_version="2.1.0",
            settings={"materialized": "table", "on_schema_change": "fail_safe"},
            models={"staging": "view"},
            sources={"raw_data": "users"},
            tests={"unit": "test_user_validity"},
        )
        tm.that(dbt_project.name, eq="data-warehouse")
        tm.that(dbt_project.profile, eq="postgres")
        tm.that(dbt_project.dbt_version, eq="2.1.0")
        tm.that(dbt_project.settings["materialized"], eq="table")
        tm.that(dbt_project.models, has="staging")
        tm.that(dbt_project.sources, has="raw_data")
        tm.that(dbt_project.tests, has="unit")

    def test_dbt_project_validation_empty_name(self) -> None:
        with pytest.raises(ValidationError, match="name cannot be empty"):
            m.Meltano.DbtProjectModel(name="", profile="default")

    def test_dbt_project_validation_empty_profile(self) -> None:
        with pytest.raises(ValidationError, match="profile cannot be empty"):
            m.Meltano.DbtProjectModel(name="test-project", profile="")

    def test_dbt_project_validation_invalid_config_type(self) -> None:
        invalid_config = cast("t.ScalarMapping", "invalid")
        with pytest.raises(ValidationError, match="Input should be a valid dictionary"):
            m.Meltano.DbtProjectModel(
                name="test-project",
                profile="default",
                settings=invalid_config,
            )

    def test_tap_and_target_config_integration(self) -> None:
        tap_config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "source.db.com", "port": 5432},
        )
        target_config = m.Meltano.TargetConfig(
            target_type="target-postgres",
            connection_config={"host": "target.db.com", "port": 5432},
        )
        tm.that(tap_config.tap_type, eq="tap-postgres")
        tm.that(target_config.target_type, eq="target-postgres")
        tm.that(tap_config.connection_config["host"], eq="source.db.com")
        tm.that(target_config.connection_config["host"], eq="target.db.com")

    def test_plugin_model_with_project_integration(self) -> None:
        plugin = m.Meltano.PluginModel(
            name="tap-mysql",
            namespace="meltanolabs",
            pip_url="tap-mysql",
        )
        project = m.Meltano.MeltanoProjectModel(
            project_id="mysql-etl",
            plugins={"extractors": "tap-mysql"},
        )
        tm.that(str(project.plugins), has=plugin.name)
        tm.that(project.project_id, eq="mysql-etl")

    def test_stream_info_with_tap_config_integration(self) -> None:
        stream = m.Meltano.StreamInfo(
            stream_name="users",
            stream_schema={"type": "t.NormalizedValue", "properties": "id"},
            key_properties=["id"],
            stream_created_at="2025-01-01T00:00:00Z",
        )
        tap_config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config={"host": "localhost"},
            stream_config={"users": "public"},
        )
        tm.that(tap_config.stream_config, has=stream.stream_name)
        tm.that(stream.key_properties, eq=["id"])
