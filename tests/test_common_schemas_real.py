"""REAL functional tests for common_schemas.py to achieve 95%+ coverage.

These tests exercise the ACTUAL functionality of CommonSingerSchemas class
and factory functions, validating real schema creation and validation patterns.
Following zero tolerance methodology - test ALL functionality.
"""

from singer_sdk import typing as th

from flext_meltano.common_schemas import (
    CommonSingerSchemas,
    create_file_tap_schema,
    create_ldap_tap_schema,
    create_oauth2_api_tap_schema,
    create_oracle_tap_schema,
)


class TestCommonSingerSchemasClass:
    """Test the CommonSingerSchemas class functionality - REAL execution."""

    def test_database_connection_schema_structure(self):
        """Test DATABASE_CONNECTION_SCHEMA has correct properties."""
        schema = CommonSingerSchemas.DATABASE_CONNECTION_SCHEMA
        assert isinstance(schema, th.PropertiesList)

        # Verify schema has properties
        properties = schema.wrapped
        assert len(properties) > 0

        # Check for expected properties
        property_names = [prop.name for prop in properties.values()]
        expected_props = ["host", "port", "username", "password", "database"]
        for prop in expected_props:
            assert prop in property_names

    def test_oracle_connection_schema_structure(self):
        """Test ORACLE_CONNECTION_SCHEMA has Oracle-specific properties."""
        schema = CommonSingerSchemas.ORACLE_CONNECTION_SCHEMA
        assert isinstance(schema, th.PropertiesList)

        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Oracle-specific properties
        oracle_props = ["host", "port", "username", "password", "service_name", "sid"]
        for prop in oracle_props:
            assert prop in property_names

    def test_ldap_connection_schema_structure(self):
        """Test LDAP_CONNECTION_SCHEMA has LDAP-specific properties."""
        schema = CommonSingerSchemas.LDAP_CONNECTION_SCHEMA
        assert isinstance(schema, th.PropertiesList)

        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # LDAP-specific properties
        ldap_props = ["ldap_host", "ldap_port", "bind_dn", "bind_password", "base_dn"]
        for prop in ldap_props:
            assert prop in property_names

    def test_create_tap_schema_oracle(self):
        """Test create_tap_schema method for Oracle connection type."""
        schema = CommonSingerSchemas.create_tap_schema(
            "oracle",
            include_extraction_config=True,
        )

        assert isinstance(schema, th.PropertiesList)
        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should include Oracle properties
        assert "host" in property_names
        assert "service_name" in property_names

        # Should include extraction config
        assert "start_date" in property_names
        assert "batch_size" in property_names

    def test_create_tap_schema_ldap(self):
        """Test create_tap_schema method for LDAP connection type."""
        schema = CommonSingerSchemas.create_tap_schema(
            "ldap",
            include_extraction_config=True,
        )

        assert isinstance(schema, th.PropertiesList)
        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should include LDAP properties
        assert "ldap_host" in property_names
        assert "bind_dn" in property_names

        # Should include extraction config
        assert "start_date" in property_names

    def test_create_tap_schema_file(self):
        """Test create_tap_schema method for file connection type."""
        schema = CommonSingerSchemas.create_tap_schema(
            "file",
            include_extraction_config=False,
        )

        assert isinstance(schema, th.PropertiesList)
        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should include file properties
        file_props_present = any(
            prop in property_names for prop in ["file_path", "files", "filepath"]
        )
        assert file_props_present

        # Should NOT include extraction config
        assert "start_date" not in property_names

    def test_create_tap_schema_oauth2(self):
        """Test create_tap_schema method for OAuth2 connection type."""
        schema = CommonSingerSchemas.create_tap_schema(
            "oauth2",
            include_extraction_config=True,
        )

        assert isinstance(schema, th.PropertiesList)
        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should include OAuth2 properties
        assert "client_id" in property_names
        assert "client_secret" in property_names

    def test_create_tap_schema_oracle_oic(self):
        """Test create_tap_schema method for Oracle OIC connection type."""
        schema = CommonSingerSchemas.create_tap_schema(
            "oracle_oic",
            include_extraction_config=True,
        )

        assert isinstance(schema, th.PropertiesList)
        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should include OIC properties
        assert "oic_host" in property_names
        assert "username" in property_names

    def test_create_tap_schema_default_database(self):
        """Test create_tap_schema method defaults to database schema for unknown types."""
        schema = CommonSingerSchemas.create_tap_schema(
            "unknown_type",
            include_extraction_config=True,
        )

        assert isinstance(schema, th.PropertiesList)
        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should default to database properties
        assert "host" in property_names
        assert "database" in property_names

    def test_create_tap_schema_with_additional_properties(self):
        """Test create_tap_schema method with additional properties."""
        additional_props = th.PropertiesList(
            th.Property("custom_field", th.StringType, description="Custom field"),
            th.Property("warehouse_code", th.StringType, description="Warehouse code"),
        )

        schema = CommonSingerSchemas.create_tap_schema(
            "oracle",
            include_extraction_config=True,
            additional_properties=additional_props,
        )

        assert isinstance(schema, th.PropertiesList)
        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should include additional properties
        assert "custom_field" in property_names
        assert "warehouse_code" in property_names

        # Should still include base properties
        assert "host" in property_names
        assert "service_name" in property_names


class TestSchemaFactoryFunctions:
    """Test the factory functions for schema creation - REAL execution."""

    def test_create_oracle_tap_schema_function(self):
        """Test create_oracle_tap_schema factory function."""
        schema = create_oracle_tap_schema()

        assert isinstance(schema, th.PropertiesList)
        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should include Oracle properties
        assert "host" in property_names
        assert "service_name" in property_names

        # Should include extraction config by default
        assert "start_date" in property_names
        assert "batch_size" in property_names

    def test_create_oracle_tap_schema_with_additional_props(self):
        """Test create_oracle_tap_schema with additional properties."""
        additional = th.PropertiesList(
            th.Property(
                "warehouse_code", th.StringType, description="WMS warehouse code",
            ),
        )

        schema = create_oracle_tap_schema(additional_properties=additional)

        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        assert "warehouse_code" in property_names
        assert "host" in property_names

    def test_create_ldap_tap_schema_function(self):
        """Test create_ldap_tap_schema factory function."""
        schema = create_ldap_tap_schema()

        assert isinstance(schema, th.PropertiesList)
        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should include LDAP properties
        assert "ldap_host" in property_names
        assert "bind_dn" in property_names

    def test_create_file_tap_schema_function(self):
        """Test create_file_tap_schema factory function."""
        schema = create_file_tap_schema()

        assert isinstance(schema, th.PropertiesList)
        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should include file properties
        file_props_present = any(
            prop in property_names for prop in ["file_path", "files", "filepath"]
        )
        assert file_props_present

    def test_create_oauth2_api_tap_schema_function(self):
        """Test create_oauth2_api_tap_schema factory function."""
        schema = create_oauth2_api_tap_schema()

        assert isinstance(schema, th.PropertiesList)
        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should include OAuth2 properties
        assert "client_id" in property_names
        assert "client_secret" in property_names


class TestSchemaValidation:
    """Test schema validation and structure - REAL validation."""

    def test_schema_properties_have_correct_types(self):
        """Test that schema properties have correct Singer SDK types."""
        schema = CommonSingerSchemas.DATABASE_CONNECTION_SCHEMA
        properties = schema.wrapped

        for prop in properties.values():
            assert hasattr(prop, "name")
            assert hasattr(prop, "type_dict")
            assert isinstance(prop.name, str)
            assert len(prop.name) > 0

    def test_extraction_config_schema_structure(self):
        """Test EXTRACTION_CONFIG_SCHEMA has expected properties."""
        schema = CommonSingerSchemas.EXTRACTION_CONFIG_SCHEMA
        assert isinstance(schema, th.PropertiesList)

        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        expected_props = ["start_date", "batch_size", "max_records", "stream_maps"]
        for prop in expected_props:
            assert prop in property_names

    def test_file_source_schema_structure(self):
        """Test FILE_SOURCE_SCHEMA has file-specific properties."""
        schema = CommonSingerSchemas.FILE_SOURCE_SCHEMA
        assert isinstance(schema, th.PropertiesList)

        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        # Should have file-related properties
        file_props_present = any(
            prop in property_names for prop in ["file_path", "files", "filepath"]
        )
        assert file_props_present

    def test_oauth2_api_schema_structure(self):
        """Test OAUTH2_API_SCHEMA has OAuth2-specific properties."""
        schema = CommonSingerSchemas.OAUTH2_API_SCHEMA
        assert isinstance(schema, th.PropertiesList)

        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        oauth2_props = ["client_id", "client_secret", "auth_url", "token_url"]
        for prop in oauth2_props:
            assert prop in property_names

    def test_oracle_oic_schema_structure(self):
        """Test ORACLE_OIC_SCHEMA has OIC-specific properties."""
        schema = CommonSingerSchemas.ORACLE_OIC_SCHEMA
        assert isinstance(schema, th.PropertiesList)

        properties = schema.wrapped
        property_names = [prop.name for prop in properties.values()]

        oic_props = ["oic_host", "username", "password"]
        for prop in oic_props:
            assert prop in property_names
