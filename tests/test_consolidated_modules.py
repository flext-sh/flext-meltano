"""Test consolidated modules (taps, targets, orchestration).

# Constants
HTTP_OK = 200
EXPECTED_BULK_SIZE = 2
EXPECTED_TOTAL_PAGES = 8
EXPECTED_DATA_COUNT = 3

Comprehensive tests for the consolidated modules that provide
unified implementations for Singer taps, targets, and DBT orchestration.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from flext_meltano.orchestration.dbt import (
    FlextLDAPDbtOrchestrator,
    FlextLDIFDbtOrchestrator,
    FlextOracleDbtOrchestrator,
    FlextOracleWMSDbtOrchestrator,
)
from flext_meltano.taps.ldap import FlextTapLDAP, TapLDAPConfig
from flext_meltano.taps.ldif import FlextTapLDIF, TapLDIFConfig
from flext_meltano.taps.oracle import FlextTapOracle, TapOracle, TapOracleConfig
from flext_meltano.targets.ldap import (
    FlextLDAPTarget,
    FlextLDAPTargetConfig,
    TargetLDAP,
    TargetLDAPConfig,
)
from flext_meltano.targets.ldif import FlextLDIFTarget, FlextLDIFTargetConfig
from flext_meltano.targets.oracle import (
    FlextOracleTarget,
    FlextOracleTargetConfig,
    LoadMethod,
)


class TestConsolidatedTaps:
    """Test consolidated tap implementations."""

    def test_oracle_tap_configuration(self) -> None:
        """Test Oracle tap configuration."""
        config = TapOracleConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service_name="XE",
            oracle_username="test",
            oracle_password="",  # Mock empty password for test
        )

        if config.oracle_host != "localhost":

            msg = f"Expected {"localhost"}, got {config.oracle_host}"
            raise AssertionError(msg)
        assert config.oracle_port == 1521
        if config.oracle_service_name != "XE":
            msg = f"Expected {"XE"}, got {config.oracle_service_name}"
            raise AssertionError(msg)
        assert config.default_replication_method == "FULL_TABLE"

    def test_oracle_tap_initialization(self) -> None:
        """Test Oracle tap initialization."""
        config_dict = {
            "oracle_host": "localhost",
            "oracle_service_name": "XE",
            "oracle_username": "test",
            "oracle_password": "test",
        }

        tap = FlextTapOracle(config=config_dict)
        if tap.name != "tap-oracle":
            msg = f"Expected {"tap-oracle"}, got {tap.name}"
            raise AssertionError(msg)
        assert tap._typed_config.oracle_host == "localhost"

    def test_oracle_tap_stream_discovery(self) -> None:
        """Test Oracle tap stream discovery."""
        config_dict = {
            "oracle_host": "localhost",
            "oracle_service_name": "XE",
            "oracle_username": "test",
            "oracle_password": "test",
        }

        tap = FlextTapOracle(config=config_dict)
        streams = tap.discover_streams()
        assert isinstance(streams, list)

    def test_ldap_tap_configuration(self) -> None:
        """Test LDAP tap configuration."""
        config = TapLDAPConfig(
            ldap_host="localhost",
            ldap_port=389,
            ldap_bind_dn="cn=admin,dc=example,dc=com",
            ldap_bind_password="",  # Mock empty password for test
            base_dn="dc=example,dc=com",
        )

        if config.ldap_host != "localhost":

            msg = f"Expected {"localhost"}, got {config.ldap_host}"
            raise AssertionError(msg)
        assert config.ldap_port == 389
        if config.ldap_use_ssl:
            msg = f"Expected False, got {config.ldap_use_ssl}"
            raise AssertionError(msg)
        assert config.search_filter == "(objectClass=*)"

    def test_ldap_tap_initialization(self) -> None:
        """Test LDAP tap initialization."""
        config_dict = {
            "ldap_host": "localhost",
            "ldap_bind_dn": "cn=admin,dc=example,dc=com",
            "ldap_bind_password": "admin",
            "base_dn": "dc=example,dc=com",
        }

        tap = FlextTapLDAP(config=config_dict)
        if tap.name != "tap-ldap":
            msg = f"Expected {"tap-ldap"}, got {tap.name}"
            raise AssertionError(msg)
        assert tap._typed_config.ldap_host == "localhost"

    def test_ldif_tap_configuration(self) -> None:
        """Test LDIF tap configuration."""
        config = TapLDIFConfig(
            input_file="/path/to/file.ldif",
            encoding="utf-8",
            batch_size=500,
        )

        if config.input_file != "/path/to/file.ldif":

            msg = f"Expected {"/path/to/file.ldif"}, got {config.input_file}"
            raise AssertionError(msg)
        assert config.encoding == "utf-8"
        if config.batch_size != 500:
            msg = f"Expected {500}, got {config.batch_size}"
            raise AssertionError(msg)

    def test_ldif_tap_initialization(self) -> None:
        """Test LDIF tap initialization."""
        config_dict = {
            "input_file": "/path/to/file.ldif",
        }

        tap = FlextTapLDIF(config=config_dict)
        if tap.name != "tap-ldif":
            msg = f"Expected {"tap-ldif"}, got {tap.name}"
            raise AssertionError(msg)
        assert tap._typed_config.input_file == "/path/to/file.ldif"


class TestConsolidatedTargets:
    """Test consolidated target implementations."""

    def test_oracle_target_configuration(self) -> None:
        """Test Oracle target configuration."""
        config = FlextOracleTargetConfig(
            oracle_host="localhost",
            oracle_port=1521,
            oracle_service_name="XE",
            oracle_username="test",
            oracle_password="",  # Mock empty password for test
            load_method=LoadMethod.UPSERT,
            batch_size=2000,
        )

        if config.oracle_host != "localhost":

            msg = f"Expected {"localhost"}, got {config.oracle_host}"
            raise AssertionError(msg)
        assert config.load_method == LoadMethod.UPSERT
        if config.batch_size != 2000:
            msg = f"Expected {2000}, got {config.batch_size}"
            raise AssertionError(msg)
        assert config.default_target_schema == "PUBLIC"

    def test_oracle_target_initialization(self) -> None:
        """Test Oracle target initialization."""
        config_dict = {
            "oracle_host": "localhost",
            "oracle_service_name": "XE",
            "oracle_username": "test",
            "oracle_password": "test",
        }

        target = FlextOracleTarget(config=config_dict)
        if target.name != "target-oracle":
            msg = f"Expected {"target-oracle"}, got {target.name}"
            raise AssertionError(msg)
        assert target._typed_config.oracle_host == "localhost"

    def test_oracle_target_sink_creation(self) -> None:
        """Test Oracle target sink creation."""
        config_dict = {
            "oracle_host": "localhost",
            "oracle_service_name": "XE",
            "oracle_username": "test",
            "oracle_password": "test",
        }

        target = FlextOracleTarget(config=config_dict)
        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
            },
        }
        sink = target.get_sink("test_stream", schema=schema)
        assert sink is not None
        if sink.stream_name != "test_stream":
            msg = f"Expected {"test_stream"}, got {sink.stream_name}"
            raise AssertionError(msg)

    def test_load_method_enum(self) -> None:
        """Test LoadMethod enum values."""
        if LoadMethod.APPEND_ONLY.value != "append-only":
            msg = f"Expected {"append-only"}, got {LoadMethod.APPEND_ONLY.value}"
            raise AssertionError(msg)
        assert LoadMethod.UPSERT.value == "upsert"
        if LoadMethod.TRUNCATE_INSERT.value != "truncate-insert":
            msg = f"Expected {"truncate-insert"}, got {LoadMethod.TRUNCATE_INSERT.value}"
            raise AssertionError(msg)

    def test_ldap_target_configuration(self) -> None:
        """Test LDAP target configuration."""
        config = FlextLDAPTargetConfig(
            ldap_host="localhost",
            ldap_port=389,
            ldap_bind_dn="cn=admin,dc=example,dc=com",
            ldap_bind_password="",  # Mock empty password for test
            base_dn="dc=example,dc=com",
        )

        if config.ldap_host != "localhost":

            msg = f"Expected {"localhost"}, got {config.ldap_host}"
            raise AssertionError(msg)
        assert config.ldap_port == 389
        if config.ldap_use_ssl:
            msg = f"Expected False, got {config.ldap_use_ssl}"
            raise AssertionError(msg)

    def test_ldap_target_initialization(self) -> None:
        """Test LDAP target initialization."""
        config_dict = {
            "ldap_host": "localhost",
            "ldap_bind_dn": "cn=admin,dc=example,dc=com",
            "ldap_bind_password": "admin",
            "base_dn": "dc=example,dc=com",
        }

        target = FlextLDAPTarget(config=config_dict)
        if target.name != "target-ldap":
            msg = f"Expected {"target-ldap"}, got {target.name}"
            raise AssertionError(msg)
        assert target._typed_config.ldap_host == "localhost"

    def test_ldif_target_configuration(self) -> None:
        """Test LDIF target configuration."""
        config = FlextLDIFTargetConfig(
            output_file="/path/to/output.ldif",
            line_length=80,
            base64_encode=True,
            include_timestamps=False,
            base_dn="dc=example,dc=com",
        )

        if config.output_file != "/path/to/output.ldif":

            msg = f"Expected {"/path/to/output.ldif"}, got {config.output_file}"
            raise AssertionError(msg)
        assert config.line_length == 80
        if not (config.base64_encode):
            msg = f"Expected True, got {config.base64_encode}"
            raise AssertionError(msg)
        if config.include_timestamps:
            msg = f"Expected False, got {config.include_timestamps}"
            raise AssertionError(msg)
        assert config.base_dn == "dc=example,dc=com"

    def test_ldif_target_initialization(self) -> None:
        """Test LDIF target initialization."""
        config_dict = {
            "output_file": "/path/to/output.ldif",
        }

        target = FlextLDIFTarget(config=config_dict)
        if target.name != "target-ldif":
            msg = f"Expected {"target-ldif"}, got {target.name}"
            raise AssertionError(msg)
        assert target._typed_config.output_file == "/path/to/output.ldif"


class TestDBTOrchestrators:
    """Test DBT orchestrators."""

    def test_oracle_wms_orchestrator(self) -> None:
        """Test Oracle WMS DBT orchestrator."""
        orchestrator = FlextOracleWMSDbtOrchestrator()

        result = orchestrator.orchestrate_wms_pipeline()
        assert result.is_success
        assert result.data is not None
        if result.data["status"] != "success":
            msg = f"Expected {"success"}, got {result.data["status"]}"
            raise AssertionError(msg)
        if "staging_wms_inventory" not in result.data["models"]:  # type: ignore[operator]
            msg = f"Expected {"staging_wms_inventory"} in {result.data["models"]}"
            raise AssertionError(msg)  # type: ignore[operator]

    def test_oracle_wms_orchestrator_custom_models(self) -> None:
        """Test Oracle WMS orchestrator with custom models."""
        orchestrator = FlextOracleWMSDbtOrchestrator()

        custom_models = ["custom_model1", "custom_model2"]
        result = orchestrator.orchestrate_wms_pipeline(models=custom_models)
        assert result.is_success
        assert result.data is not None
        if result.data["models"] != custom_models:
            msg = f"Expected {custom_models}, got {result.data["models"]}"
            raise AssertionError(msg)

    def test_oracle_wms_validation(self) -> None:
        """Test Oracle WMS data validation."""
        orchestrator = FlextOracleWMSDbtOrchestrator()

        result = orchestrator.validate_wms_data()
        assert result.is_success
        assert result.data is not None
        if result.data["validation"] != "passed":
            msg = f"Expected {"passed"}, got {result.data["validation"]}"
            raise AssertionError(msg)

    def test_oracle_wms_refresh(self) -> None:
        """Test Oracle WMS data refresh."""
        orchestrator = FlextOracleWMSDbtOrchestrator()

        result = orchestrator.execute_wms_refresh()
        assert result.is_success
        assert result.data is not None
        if result.data["refresh"] != "completed":
            msg = f"Expected {"completed"}, got {result.data["refresh"]}"
            raise AssertionError(msg)

    def test_oracle_generic_orchestrator(self) -> None:
        """Test generic Oracle DBT orchestrator."""
        orchestrator = FlextOracleDbtOrchestrator()

        result = orchestrator.orchestrate_oracle_pipeline()
        assert result.is_success
        assert result.data is not None
        if result.data["status"] != "success":
            msg = f"Expected {"success"}, got {result.data["status"]}"
            raise AssertionError(msg)
        if "staging_oracle_tables" not in result.data["models"]:  # type: ignore[operator]
            msg = f"Expected {"staging_oracle_tables"} in {result.data["models"]}"
            raise AssertionError(msg)  # type: ignore[operator]

    def test_ldap_orchestrator(self) -> None:
        """Test LDAP DBT orchestrator."""
        orchestrator = FlextLDAPDbtOrchestrator()

        result = orchestrator.orchestrate_ldap_pipeline()
        assert result.is_success
        assert result.data is not None
        if result.data["status"] != "success":
            msg = f"Expected {"success"}, got {result.data["status"]}"
            raise AssertionError(msg)
        if "staging_ldap_users" not in result.data["models"]:  # type: ignore[operator]
            msg = f"Expected staging_ldap_users in {result.data['models']}"
            raise AssertionError(msg)

    def test_ldif_orchestrator(self) -> None:
        """Test LDIF DBT orchestrator."""
        orchestrator = FlextLDIFDbtOrchestrator()

        result = orchestrator.orchestrate_ldif_pipeline()
        assert result.is_success
        assert result.data is not None
        if result.data["status"] != "success":
            msg = f"Expected {"success"}, got {result.data["status"]}"
            raise AssertionError(msg)
        if "staging_ldif_entries" not in result.data["models"]:  # type: ignore[operator]
            msg = f"Expected staging_ldif_entries in {result.data['models']}"
            raise AssertionError(msg)

    def test_orchestrator_project_dir_setting(self) -> None:
        """Test orchestrator project directory setting."""

        project_dir = Path("/test/project")
        orchestrator = FlextOracleWMSDbtOrchestrator(project_dir=project_dir)
        if orchestrator.project_dir != project_dir:
            msg = f"Expected {project_dir}, got {orchestrator.project_dir}"
            raise AssertionError(msg)

    def test_orchestrator_project_dir_string(self) -> None:
        """Test orchestrator with string project directory."""
        project_dir_str = "/test/project"
        orchestrator = FlextLDAPDbtOrchestrator(project_dir=project_dir_str)
        if str(orchestrator.project_dir) != project_dir_str:
            msg = f"Expected {project_dir_str}, got {orchestrator.project_dir!s}"
            raise AssertionError(msg)


class TestLegacyAliases:
    """Test legacy compatibility aliases."""

    def test_tap_legacy_alias(self) -> None:
        """Test legacy tap aliases."""

        assert TapOracle is FlextTapOracle

    def test_target_legacy_aliases(self) -> None:
        """Test legacy target aliases."""

        assert TargetLDAP is FlextLDAPTarget
        assert TargetLDAPConfig is FlextLDAPTargetConfig


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
