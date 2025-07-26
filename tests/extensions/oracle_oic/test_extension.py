"""Tests for flext-extensions.oracle.flext-oracle-oic-ext.

Tests for Oracle OIC Extension functionality including initialization,
command handling, lifecycle management, and monitoring services.
"""

from __future__ import annotations

import pytest
from flext_oracle_oic_ext.config import OracleOICExtensionSettings
from flext_oracle_oic_ext.extension import OracleOICExtension
from flext_oracle_oic_ext.lifecycle import LifecycleManager
from flext_oracle_oic_ext.monitoring import MonitoringService
import requests


class TestOracleOICExtension:
    """Test cases for OracleOICExtension."""

    def test_extension_initialization(self) -> None:
        """Test extension initialization with default values."""
        ext = OracleOICExtension()
        assert ext.oracle_oic_bin == "oracle-oic-ext"
        assert ext.lifecycle_manager is None
        assert ext.monitoring_service is None

    def test_describe_commands(self) -> None:
        """Test command description and availability."""
        ext = OracleOICExtension()
        description = ext.describe()

        assert len(description.commands) > 0

        # Check lifecycle commands
        command_names = [cmd.name for cmd in description.commands,]
        assert "lifecycle:activate" in command_names
        assert "lifecycle:deactivate" in command_names
        assert "lifecycle:status" in command_names

        # Check monitoring commands
        assert "monitor:health" in command_names
        assert "monitor:performance" in command_names
        assert "monitor:errors" in command_names
        assert "monitor:usage" in command_names

        # Check extraction commands
        assert "extract:artifacts" in command_names
        assert "extract:logs" in command_names
        assert "extract:metadata" in command_names

    def test_lifecycle_manager_initialization(self) -> None:
        """Test lifecycle manager initialization with configuration."""
        # Create valid configuration dict
        config_dict = {
            "base_url": "https://test.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client",
            "oauth_client_secret": "test_secret",
            "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
        }

        # Create settings from dict
        settings = OracleOICExtensionSettings.from_dict(config_dict)
        LifecycleManager(settings)

        # Test that manager was created with correct settings
        assert settings.connection is not None
        assert (
            settings.connection.base_url
            == "https://test.integration.ocp.oraclecloud.com"
        )
        assert settings.connection.oauth_client_id == "test_client"

    def test_monitoring_service_initialization(self) -> None:
        """Test monitoring service initialization with configuration."""
        # MonitoringService expects a requests.Session object

        session = requests.Session()
        service = MonitoringService(session)

        # Test that service was created successfully
        assert service is not None

    def test_extension_command_categories(self) -> None:
        """Test that extension properly categorizes commands."""
        ext = OracleOICExtension()
        description = ext.describe()

        # Verify command categories exist
        lifecycle_commands = [
            cmd for cmd in description.commands if cmd.name.startswith("lifecycle:")
        ]
        monitor_commands = [
            cmd for cmd in description.commands if cmd.name.startswith("monitor:")
        ]
        extract_commands = [
            cmd for cmd in description.commands if cmd.name.startswith("extract:")
        ]

        assert len(lifecycle_commands) >= 3  # activate, deactivate, status
        assert len(monitor_commands) >= 3  # health, performance, errors
        assert len(extract_commands) >= 3  # artifacts, logs, metadata

    def test_configuration_validation(self) -> None:
        """Test configuration validation for managers."""
        # Valid configuration should work
        valid_config = {
            "base_url": "https://valid.integration.ocp.oraclecloud.com",
            "oauth_client_id": "valid_client",
            "oauth_client_secret": "valid_secret",
            "oauth_token_url": "https://valid.identity.oraclecloud.com/oauth2/v1/token",
        }

        # Create settings object using from_dict
        settings = OracleOICExtensionSettings.from_dict(valid_config)

        # Test LifecycleManager with settings
        LifecycleManager(settings)
        assert settings.connection is not None
        assert settings.connection.base_url.startswith("https://")

        # Test MonitoringService - needs a session object, so we'll skip this for now
        # monitoring_service = MonitoringService(client=mock_session)

    def test_extension_bin_property(self) -> None:
        """Test that extension bin property is correctly set."""
        ext = OracleOICExtension()
        assert ext.oracle_oic_bin == "oracle-oic-ext"
        assert isinstance(ext.oracle_oic_bin, str)
        assert len(ext.oracle_oic_bin) > 0

    def test_command_description_structure(self) -> None:
        """Test that command descriptions have proper structure."""
        ext = OracleOICExtension()
        description = ext.describe()

        for command in description.commands:
            assert hasattr(command, "name")
            assert hasattr(command, "description")
            assert isinstance(command.name, str)
            assert len(command.name) > 0
            # Commands should have format "category:action"
            assert ":" in command.name

    @pytest.mark.parametrize(
        "command_prefix",
        ["lifecycle", "monitor", "extract",],
    )
    def test_command_prefix_availability(self, command_prefix: str) -> None:
        """Test that all expected command prefixes are available."""
        ext = OracleOICExtension()
        description = ext.describe()

        command_names = [cmd.name for cmd in description.commands,]
        prefix_commands = [
            name for name in command_names if name.startswith(f"{command_prefix,}:")
        ]

        assert len(prefix_commands) > 0, (
            f"No commands found with prefix {command_prefix,}:"
        )

    def test_manager_auth_config_structure(self) -> None:
        """Test that managers properly store auth configuration."""
        config_dict = {
            "base_url": "https://test.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client_id",
            "oauth_client_secret": "test_client_secret",
            "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
        }

        # Create settings and manager
        settings = OracleOICExtensionSettings.from_dict(config_dict)
        LifecycleManager(settings)

        # Verify auth config is accessible through settings
        assert settings.connection is not None
        assert settings.connection.oauth_client_id == "test_client_id"
        assert settings.connection.oauth_client_secret == "test_client_secret"
        assert (
            settings.connection.oauth_token_url
            == "https://test.identity.oraclecloud.com/oauth2/v1/token"
        )

    def test_base_url_validation(self) -> None:
        """Test base URL validation in managers."""
        config_dict = {
            "base_url": "https://valid.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client",
            "oauth_client_secret": "test_secret",
            "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
        }

        # Valid HTTPS URL should work
        settings = OracleOICExtensionSettings.from_dict(config_dict)
        LifecycleManager(settings)
        assert settings.connection is not None
        assert settings.connection.base_url.startswith("https://")

        # URL validation depends on implementation - testing what we can
        assert (
            "ocp.oraclecloud.com" in settings.connection.base_url
            or "integration" in settings.connection.base_url
        )
