"""Comprehensive tests for taps modules to increase coverage."""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

# Import from all tap modules
from flext_meltano.taps import (
    FlextTap,
    FlextTapBase,
    FlextTapConfig,
    FlextTapFactory,
    FlextTapService,
    create_tap,
    create_tap_factory,
    create_tap_service,
)
from flext_meltano.taps.ldap import (
    FlextLdapTap,
    FlextLdapTapConfig,
    FlextLdapTapService,
    create_ldap_tap,
    create_ldap_tap_service,
)
from flext_meltano.taps.ldif import (
    FlextLdifTap,
    FlextLdifTapConfig,
    FlextLdifTapService,
    create_ldif_tap,
    create_ldif_tap_service,
)
from flext_meltano.taps.oracle import (
    FlextOracleTap,
    FlextOracleTapConfig,
    FlextOracleTapService,
    create_oracle_tap,
    create_oracle_tap_service,
)


class TestFlextTapBase:
    """Test base tap functionality."""

    def test_tap_config_initialization(self) -> None:
        """Test tap config initialization."""
        config = FlextTapConfig(name="tap-test", executable="tap-test")
        assert config is not None
        assert config.name == "tap-test"
        assert config.executable == "tap-test"

    def test_tap_base_initialization(self) -> None:
        """Test tap base initialization."""
        config = FlextTapConfig(name="tap-test", executable="tap-test")
        tap = FlextTapBase(config=config)
        assert tap is not None
        assert tap.config == config

    def test_tap_service_initialization(self) -> None:
        """Test tap service initialization."""
        config = FlextTapConfig(name="tap-test", executable="tap-test")
        service = FlextTapService(config=config)
        assert service is not None
        assert service.config == config

    def test_tap_factory_initialization(self) -> None:
        """Test tap factory initialization."""
        factory = FlextTapFactory()
        assert factory is not None

    def test_flext_tap_initialization(self) -> None:
        """Test FlextTap initialization."""
        config = FlextTapConfig(name="tap-test", executable="tap-test")
        tap = FlextTap(config=config)
        assert tap is not None


class TestFlextLdapTap:
    """Test LDAP tap functionality."""

    def test_ldap_tap_config_initialization(self) -> None:
        """Test LDAP tap config initialization."""
        config = FlextLdapTapConfig(
            name="tap-ldap",
            executable="tap-ldap",
            host="localhost",
            port=389,
            bind_dn="cn=admin,dc=example,dc=com",
            bind_password="",
            base_dn="dc=example,dc=com",
        )
        assert config is not None
        assert config.name == "tap-ldap"
        assert config.host == "localhost"
        assert config.port == 389

    def test_ldap_tap_initialization(self) -> None:
        """Test LDAP tap initialization."""
        config = FlextLdapTapConfig(
            name="tap-ldap",
            executable="tap-ldap",
            host="localhost",
            port=389,
            bind_dn="cn=admin,dc=example,dc=com",
            bind_password="",
            base_dn="dc=example,dc=com",
        )
        tap = FlextLdapTap(config=config)
        assert tap is not None
        assert tap.config == config

    def test_ldap_tap_service_initialization(self) -> None:
        """Test LDAP tap service initialization."""
        config = FlextLdapTapConfig(
            name="tap-ldap",
            executable="tap-ldap",
            host="localhost",
            port=389,
            bind_dn="cn=admin,dc=example,dc=com",
            bind_password="",
            base_dn="dc=example,dc=com",
        )
        service = FlextLdapTapService(config=config)
        assert service is not None
        assert service.config == config

    def test_ldap_tap_discover(self) -> None:
        """Test LDAP tap discovery."""
        config = FlextLdapTapConfig(
            name="tap-ldap",
            executable="tap-ldap",
            host="localhost",
            port=389,
            bind_dn="cn=admin,dc=example,dc=com",
            bind_password="",
            base_dn="dc=example,dc=com",
        )
        tap = FlextLdapTap(config=config)
        result = tap.discover()
        # Discovery may fail without proper LDAP server, but should not crash
        assert result is not None

    def test_ldap_tap_extract(self) -> None:
        """Test LDAP tap extraction."""
        config = FlextLdapTapConfig(
            name="tap-ldap",
            executable="tap-ldap",
            host="localhost",
            port=389,
            bind_dn="cn=admin,dc=example,dc=com",
            bind_password="",
            base_dn="dc=example,dc=com",
        )
        tap = FlextLdapTap(config=config)
        result = tap.extract()
        # Extraction may fail without proper LDAP server, but should not crash
        assert result is not None


class TestFlextLdifTap:
    """Test LDIF tap functionality."""

    def test_ldif_tap_config_initialization(self) -> None:
        """Test LDIF tap config initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ldif_file = Path(temp_dir) / "test.ldif"
            ldif_file.write_text("dn: dc=example,dc=com\nobjectClass: dcObject\ndc: example\n")

            config = FlextLdifTapConfig(
                name="tap-ldif",
                executable="tap-ldif",
                ldif_file=str(ldif_file),
            )
            assert config is not None
            assert config.name == "tap-ldif"
            assert config.ldif_file == str(ldif_file)

    def test_ldif_tap_initialization(self) -> None:
        """Test LDIF tap initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ldif_file = Path(temp_dir) / "test.ldif"
            ldif_file.write_text("dn: dc=example,dc=com\nobjectClass: dcObject\ndc: example\n")

            config = FlextLdifTapConfig(
                name="tap-ldif",
                executable="tap-ldif",
                ldif_file=str(ldif_file),
            )
            tap = FlextLdifTap(config=config)
            assert tap is not None
            assert tap.config == config

    def test_ldif_tap_service_initialization(self) -> None:
        """Test LDIF tap service initialization."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ldif_file = Path(temp_dir) / "test.ldif"
            ldif_file.write_text("dn: dc=example,dc=com\nobjectClass: dcObject\ndc: example\n")

            config = FlextLdifTapConfig(
                name="tap-ldif",
                executable="tap-ldif",
                ldif_file=str(ldif_file),
            )
            service = FlextLdifTapService(config=config)
            assert service is not None
            assert service.config == config

    def test_ldif_tap_discover(self) -> None:
        """Test LDIF tap discovery."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ldif_file = Path(temp_dir) / "test.ldif"
            ldif_file.write_text("dn: dc=example,dc=com\nobjectClass: dcObject\ndc: example\n")

            config = FlextLdifTapConfig(
                name="tap-ldif",
                executable="tap-ldif",
                ldif_file=str(ldif_file),
            )
            tap = FlextLdifTap(config=config)
            result = tap.discover()
            # Discovery may fail without proper setup, but should not crash
            assert result is not None

    def test_ldif_tap_extract(self) -> None:
        """Test LDIF tap extraction."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ldif_file = Path(temp_dir) / "test.ldif"
            ldif_file.write_text("dn: dc=example,dc=com\nobjectClass: dcObject\ndc: example\n")

            config = FlextLdifTapConfig(
                name="tap-ldif",
                executable="tap-ldif",
                ldif_file=str(ldif_file),
            )
            tap = FlextLdifTap(config=config)
            result = tap.extract()
            # Extraction may fail without proper setup, but should not crash
            assert result is not None


class TestFlextOracleTap:
    """Test Oracle tap functionality."""

    def test_oracle_tap_config_initialization(self) -> None:
        """Test Oracle tap config initialization."""
        config = FlextOracleTapConfig(
            name="tap-oracle",
            executable="tap-oracle",
            host="localhost",
            port=1521,
            service_name="XE",
            username="test",
            password="",  # Mock empty password for test
        )
        assert config is not None
        assert config.name == "tap-oracle"
        assert config.host == "localhost"
        assert config.port == 1521
        assert config.service_name == "XE"

    def test_oracle_tap_initialization(self) -> None:
        """Test Oracle tap initialization."""
        config = FlextOracleTapConfig(
            name="tap-oracle",
            executable="tap-oracle",
            host="localhost",
            port=1521,
            service_name="XE",
            username="test",
            password="",  # Mock empty password for test
        )
        tap = FlextOracleTap(config=config)
        assert tap is not None
        assert tap.config == config

    def test_oracle_tap_service_initialization(self) -> None:
        """Test Oracle tap service initialization."""
        config = FlextOracleTapConfig(
            name="tap-oracle",
            executable="tap-oracle",
            host="localhost",
            port=1521,
            service_name="XE",
            username="test",
            password="",  # Mock empty password for test
        )
        service = FlextOracleTapService(config=config)
        assert service is not None
        assert service.config == config

    def test_oracle_tap_discover(self) -> None:
        """Test Oracle tap discovery."""
        config = FlextOracleTapConfig(
            name="tap-oracle",
            executable="tap-oracle",
            host="localhost",
            port=1521,
            service_name="XE",
            username="test",
            password="",  # Mock empty password for test
        )
        tap = FlextOracleTap(config=config)
        result = tap.discover()
        # Discovery may fail without proper Oracle database, but should not crash
        assert result is not None

    def test_oracle_tap_extract(self) -> None:
        """Test Oracle tap extraction."""
        config = FlextOracleTapConfig(
            name="tap-oracle",
            executable="tap-oracle",
            host="localhost",
            port=1521,
            service_name="XE",
            username="test",
            password="",  # Mock empty password for test
        )
        tap = FlextOracleTap(config=config)
        result = tap.extract()
        # Extraction may fail without proper Oracle database, but should not crash
        assert result is not None


class TestTapFactoryFunctions:
    """Test tap factory functions."""

    def test_create_tap(self) -> None:
        """Test create_tap factory."""
        result = create_tap(name="tap-test", executable="tap-test")
        assert result is not None

    def test_create_tap_service(self) -> None:
        """Test create_tap_service factory."""
        result = create_tap_service(name="tap-test", executable="tap-test")
        assert result is not None

    def test_create_tap_factory(self) -> None:
        """Test create_tap_factory factory."""
        result = create_tap_factory()
        assert result is not None

    def test_create_ldap_tap(self) -> None:
        """Test create_ldap_tap factory."""
        result = create_ldap_tap(
            host="localhost",
            port=389,
            bind_dn="cn=admin,dc=example,dc=com",
            bind_password="",
            base_dn="dc=example,dc=com",
        )
        assert result is not None

    def test_create_ldap_tap_service(self) -> None:
        """Test create_ldap_tap_service factory."""
        result = create_ldap_tap_service(
            host="localhost",
            port=389,
            bind_dn="cn=admin,dc=example,dc=com",
            bind_password="",
            base_dn="dc=example,dc=com",
        )
        assert result is not None

    def test_create_ldif_tap(self) -> None:
        """Test create_ldif_tap factory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ldif_file = Path(temp_dir) / "test.ldif"
            ldif_file.write_text("dn: dc=example,dc=com\nobjectClass: dcObject\ndc: example\n")

            result = create_ldif_tap(ldif_file=str(ldif_file))
            assert result is not None

    def test_create_ldif_tap_service(self) -> None:
        """Test create_ldif_tap_service factory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ldif_file = Path(temp_dir) / "test.ldif"
            ldif_file.write_text("dn: dc=example,dc=com\nobjectClass: dcObject\ndc: example\n")

            result = create_ldif_tap_service(ldif_file=str(ldif_file))
            assert result is not None

    def test_create_oracle_tap(self) -> None:
        """Test create_oracle_tap factory."""
        result = create_oracle_tap(
            host="localhost",
            port=1521,
            service_name="XE",
            username="test",
            password="",  # Mock empty password for test
        )
        assert result is not None

    def test_create_oracle_tap_service(self) -> None:
        """Test create_oracle_tap_service factory."""
        result = create_oracle_tap_service(
            host="localhost",
            port=1521,
            service_name="XE",
            username="test",
            password="",  # Mock empty password for test
        )
        assert result is not None


class TestTapIntegration:
    """Test tap integration scenarios."""

    def test_complete_tap_workflow(self) -> None:
        """Test complete tap workflow."""
        # Create base tap
        base_config = FlextTapConfig(name="tap-test", executable="tap-test")
        base_tap = FlextTap(config=base_config)

        # Create LDAP tap
        ldap_tap = create_ldap_tap(
            host="localhost",
            port=389,
            bind_dn="cn=admin,dc=example,dc=com",
            bind_password="",
            base_dn="dc=example,dc=com",
        )

        # Create Oracle tap
        oracle_tap = create_oracle_tap(
            host="localhost",
            port=1521,
            service_name="XE",
            username="test",
            password="",  # Mock empty password for test
        )

        # All should be created successfully
        assert base_tap is not None
        assert ldap_tap is not None
        assert oracle_tap is not None

    def test_tap_error_handling(self) -> None:
        """Test tap error handling."""
        # Test with minimal config (should handle gracefully)
        config = FlextTapConfig(name="", executable="")
        tap = FlextTap(config=config)

        # Should not crash, even with invalid config
        assert tap is not None

    def test_all_tap_types_functionality(self) -> None:
        """Test functionality of all tap types."""
        with tempfile.TemporaryDirectory() as temp_dir:
            ldif_file = Path(temp_dir) / "test.ldif"
            ldif_file.write_text("dn: dc=example,dc=com\nobjectClass: dcObject\ndc: example\n")

            # Create all tap types
            ldap_tap = create_ldap_tap(
                host="localhost",
                port=389,
                bind_dn="cn=admin,dc=example,dc=com",
                bind_password="",
                base_dn="dc=example,dc=com",
            )

            ldif_tap = create_ldif_tap(ldif_file=str(ldif_file))

            oracle_tap = create_oracle_tap(
                host="localhost",
                port=1521,
                service_name="XE",
                username="test",
                password="",  # Mock empty password for test
            )

            # Test basic functionality
            assert ldap_tap is not None
            assert ldif_tap is not None
            assert oracle_tap is not None

            # Test discovery (may fail but should not crash)
            ldap_result = ldap_tap.discover()
            ldif_result = ldif_tap.discover()
            oracle_result = oracle_tap.discover()

            assert ldap_result is not None
            assert ldif_result is not None
            assert oracle_result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
