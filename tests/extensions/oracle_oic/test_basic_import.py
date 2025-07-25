"""Basic test to verify flext-extensions.oracle.flext-oracle-oic-ext imports work."""


def test_basic_import() -> None:
    """Test that we can import the module."""
    import flext_oracle_oic_ext

    assert flext_oracle_oic_ext is not None


def test_config_import() -> None:
    """Test that we can import config."""
    from flext_oracle_oic_ext.config import OracleOICExtensionSettings

    assert OracleOICExtensionSettings is not None
