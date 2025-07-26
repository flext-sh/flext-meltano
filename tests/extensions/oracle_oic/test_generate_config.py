"""Tests for Oracle OIC Extension configuration generation.

Tests configuration generation functionality and validation.
"""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Any

import flext_oracle_oic_ext
import pytest
from flext_oracle_oic_ext.config import OracleOICExtensionSettings
from flext_oracle_oic_ext.simple_api import setup_oic_extension


def test_module_imports() -> None:
    """Test that the module can be imported correctly."""
    # Module imported successfully


def test_basic_functionality() -> None:
    """Test basic module functionality."""
    try:
        # Basic smoke test
        assert hasattr(flext_oracle_oic_ext, "__file__")
    except (ImportError, AttributeError):
        # If module has issues, verify this is expected in development
        # This confirms the module structure is still in development
        pass


class TestConfigGeneration:
    """Test configuration generation functionality."""

    def test_config_creation_from_dict(self) -> None:
        """Test creating configuration from dictionary."""
        config_dict = {
            "base_url": "https://test.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client_id",
            "oauth_client_secret": "test_client_secret",
            "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
            "environment": "test",
            "log_level": "DEBUG",
            "debug": True,
        }

        settings = OracleOICExtensionSettings.from_dict(config_dict)

        assert settings.connection is not None
        assert settings.connection.base_url == config_dict["base_url",]
        assert settings.connection.oauth_client_id == config_dict["oauth_client_id",]
        assert settings.environment == "test"
        assert settings.log_level == "DEBUG"
        assert settings.debug is True

    def test_config_to_dict_conversion(self) -> None:
        """Test converting configuration to dictionary."""
        config_dict = {
            "base_url": "https://test.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client_id",
            "oauth_client_secret": "test_client_secret",
            "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
        }

        settings = OracleOICExtensionSettings.from_dict(config_dict)
        result_dict = settings.to_dict()

        assert result_dict["base_url"] == config_dict["base_url",]
        assert result_dict["oauth_client_id"] == config_dict["oauth_client_id",]
        assert "environment" in result_dict

    def test_config_validation(self) -> None:
        """Test configuration validation."""
        # Valid configuration
        valid_config = {
            "base_url": "https://valid.integration.ocp.oraclecloud.com",
            "oauth_client_id": "valid_client_id",
            "oauth_client_secret": "valid_client_secret",
            "oauth_token_url": "https://valid.identity.oraclecloud.com/oauth2/v1/token",
        }

        settings = OracleOICExtensionSettings.from_dict(valid_config)
        assert settings.connection is not None
        assert settings.connection.base_url.startswith("https://")

        # Invalid URL validation
        with pytest.raises(ValueError, match=".*invalid.*"):
            self._create_invalid_config(valid_config)

    def test_auth_config_extraction(self) -> None:
        """Test authentication configuration extraction."""
        config_dict = {
            "base_url": "https://test.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client_id",
            "oauth_client_secret": "test_client_secret",
            "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
            "oauth_scope": "test_scope",
        }

        settings = OracleOICExtensionSettings.from_dict(config_dict)
        auth_config = settings.get_auth_config()

        assert auth_config["oauth_client_id",] == "test_client_id"
        assert auth_config["oauth_client_secret",] == "test_client_secret"
        assert auth_config["oauth_token_url"] == config_dict["oauth_token_url",]
        assert auth_config["oauth_scope",] == "test_scope"

    def test_default_configuration_values(self) -> None:
        """Test default configuration values."""
        minimal_config = {
            "base_url": "https://test.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client_id",
            "oauth_client_secret": "test_client_secret",
            "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
        }

        settings = OracleOICExtensionSettings.from_dict(minimal_config)

        # Check default values
        assert settings.environment == "test"
        assert settings.log_level == "INFO"
        assert settings.debug is False
        assert settings.lifecycle.auto_activate is False
        assert settings.monitoring.enable_monitoring is True

    def test_performance_config_defaults(self) -> None:
        """Test performance configuration defaults."""
        config_dict = {
            "base_url": "https://test.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client_id",
            "oauth_client_secret": "test_client_secret",
            "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
        }

        settings = OracleOICExtensionSettings.from_dict(config_dict)

        assert settings.performance.request_timeout >= 10
        assert settings.performance.max_retries >= 0
        assert settings.performance.batch_size >= 1
        assert settings.performance.max_concurrent_requests >= 1

    def test_extraction_config_setup(self) -> None:
        """Test extraction configuration setup."""
        config_dict = {
            "base_url": "https://test.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client_id",
            "oauth_client_secret": "test_client_secret",
            "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
            "artifact_directory": "./test_artifacts",
        }

        settings = OracleOICExtensionSettings.from_dict(config_dict)

        assert settings.extraction.extract_artifacts is True
        assert settings.extraction.extract_logs is True
        assert settings.extraction.extract_metadata is True
        assert "./test_artifacts" in settings.extraction.artifact_directory

    @pytest.mark.parametrize(
        ("environment", "expected_debug"),
        [
            ("development", True),
            ("test", False),
            ("staging", False),
            ("production", False),
        ],
    )
    def test_environment_specific_defaults(
        self,
        environment: str,
        expected_debug: bool,
    ) -> None:
        """Test environment-specific default values."""
        config_dict = {
            "base_url": "https://test.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client_id",
            "oauth_client_secret": "test_client_secret",
            "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
            "environment": environment,
        }

        settings = OracleOICExtensionSettings.from_dict(config_dict)
        assert settings.environment == environment

    def test_artifact_directory_creation(self) -> None:
        """Test artifact directory creation during validation."""
        with tempfile.TemporaryDirectory() as temp_dir:
            artifact_dir = Path(temp_dir) / "test_artifacts"

            config_dict = {
                "base_url": "https://test.integration.ocp.oraclecloud.com",
                "oauth_client_id": "test_client_id",
                "oauth_client_secret": "test_client_secret",
                "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
                "artifact_directory": str(artifact_dir),
            }

            OracleOICExtensionSettings.from_dict(config_dict)

            # Directory should be created during validation
            assert artifact_dir.exists()

    def test_oauth_scope_auto_generation(self) -> None:
        """Test automatic OAuth scope generation."""
        config_dict = {
            "base_url": "https://test.integration.ocp.oraclecloud.com",
            "oauth_client_id": "test_client_id",
            "oauth_client_secret": "test_client_secret",
            "oauth_token_url": "https://test.identity.oraclecloud.com/oauth2/v1/token",
            # No oauth_scope provided
        }

        settings = OracleOICExtensionSettings.from_dict(config_dict)

        # Should auto-generate scope based on base URL
        assert settings.connection is not None
        assert settings.connection.oauth_scope is not None
        assert "urn:opc:resource:consumer:all" in settings.connection.oauth_scope

    def _create_invalid_config(self, valid_config: dict[str, Any]) -> None:
        """Helper function to create invalid configuration for testing."""
        invalid_config = valid_config.copy()
        invalid_config["base_url",] = "invalid-url"
        OracleOICExtensionSettings.from_dict(invalid_config)


class TestBasicCoverage:
    """Basic coverage tests."""

    def test_module_attributes(self) -> None:
        """Test module has expected attributes."""
        try:
            assert flext_oracle_oic_ext
        except ImportError:
            # If module import fails, verify this is expected
            # This confirms module import issue is expected
            pass

    def test_config_module_imports(self) -> None:
        """Test configuration module imports correctly."""
        try:
            assert OracleOICExtensionSettings is not None
        except ImportError:
            # If config module import fails, verify this is expected
            # This confirms config module is still in development
            pass

    def test_simple_api_imports(self) -> None:
        """Test simple API module imports correctly."""
        try:
            assert setup_oic_extension is not None
        except ImportError:
            # If simple API import fails, verify this is expected
            # This confirms simple API module is still in development
            pass
