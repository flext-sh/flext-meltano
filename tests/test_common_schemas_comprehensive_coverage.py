"""Comprehensive Coverage Tests for Common Schemas Module.

**Purpose**: Test all classes and methods in common_schemas.py to achieve 100% coverage
**Scope**: CommonSingerSchemas class, schema definitions, and factory functions
**Target**: Increase common_schemas.py coverage from 0% to 100%

This module provides complete functional tests for centralized Singer schema
definitions and factory functions for consistent schema patterns.
"""

from __future__ import annotations

from singer_sdk import typing as th

from flext_meltano.common_schemas import (
    CommonSingerSchemas,
    __all__ as _schemas_all,
    create_file_tap_schema,
    create_ldap_tap_schema,
    create_oauth2_api_tap_schema,
    create_oracle_oic_tap_schema,
    create_oracle_tap_schema,
)


class TestCommonSingerSchemas:
    """Test CommonSingerSchemas class and its schema definitions."""

    def test_database_connection_schema_exists(self):
        """Test DATABASE_CONNECTION_SCHEMA is properly defined."""
        schema = CommonSingerSchemas.DATABASE_CONNECTION_SCHEMA

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Check required properties exist
        property_names = [prop.name for prop in schema.wrapped.values()]
        required_properties = ["host", "port", "username", "password", "database"]

        for prop_name in required_properties:
            assert prop_name in property_names

    def test_database_connection_schema_properties(self):
        """Test DATABASE_CONNECTION_SCHEMA property details."""
        properties = {
            prop.name: prop
            for prop in CommonSingerSchemas.DATABASE_CONNECTION_SCHEMA.wrapped.values()
        }

        # Test host property
        host_prop = properties["host"]
        assert not host_prop.optional  # not optional means required
        assert isinstance(host_prop.type_dict, type(th.StringType.type_dict))
        assert host_prop.description == "Database host"

        # Test port property
        port_prop = properties["port"]
        assert isinstance(port_prop.type_dict, type(th.IntegerType.type_dict))
        assert port_prop.description == "Database port"

        # Test password property (should be secret)
        password_prop = properties["password"]
        assert not password_prop.optional  # not optional means required
        assert password_prop.secret is True
        assert password_prop.description == "Database password"

    def test_oracle_connection_schema_exists(self):
        """Test ORACLE_CONNECTION_SCHEMA is properly defined."""
        schema = CommonSingerSchemas.ORACLE_CONNECTION_SCHEMA

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Check it includes base database properties plus Oracle-specific
        property_names = [prop.name for prop in schema.wrapped.values()]
        base_properties = ["host", "port", "username", "password", "database"]
        oracle_properties = ["service_name", "sid"]

        for prop_name in base_properties + oracle_properties:
            assert prop_name in property_names

    def test_oracle_connection_schema_extends_database(self):
        """Test ORACLE_CONNECTION_SCHEMA properly extends DATABASE_CONNECTION_SCHEMA."""
        oracle_properties = {
            prop.name: prop
            for prop in CommonSingerSchemas.ORACLE_CONNECTION_SCHEMA.wrapped.values()
        }

        # Test Oracle-specific properties
        service_name_prop = oracle_properties["service_name"]
        assert isinstance(service_name_prop.type_dict, type(th.StringType.type_dict))
        assert service_name_prop.description == "Oracle service name"

        sid_prop = oracle_properties["sid"]
        assert isinstance(sid_prop.type_dict, type(th.StringType.type_dict))
        assert sid_prop.description == "Oracle SID"

    def test_ldap_connection_schema_exists(self):
        """Test LDAP_CONNECTION_SCHEMA is properly defined."""
        schema = CommonSingerSchemas.LDAP_CONNECTION_SCHEMA

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Check LDAP-specific properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        ldap_properties = [
            "ldap_host",
            "ldap_port",
            "bind_dn",
            "bind_password",
            "base_dn",
            "use_tls",
        ]

        for prop_name in ldap_properties:
            assert prop_name in property_names

    def test_ldap_connection_schema_properties(self):
        """Test LDAP_CONNECTION_SCHEMA property details."""
        properties = {
            prop.name: prop
            for prop in CommonSingerSchemas.LDAP_CONNECTION_SCHEMA.wrapped.values()
        }

        # Test ldap_host property
        host_prop = properties["ldap_host"]
        assert not host_prop.optional  # not optional means required
        assert host_prop.description == "LDAP server host"

        # Test ldap_port with default
        port_prop = properties["ldap_port"]
        assert port_prop.default == 389
        assert port_prop.description == "LDAP server port"

        # Test bind_password (should be secret)
        password_prop = properties["bind_password"]
        assert not password_prop.optional  # not optional means required
        assert password_prop.secret is True
        assert password_prop.description == "LDAP bind password"

        # Test use_tls with boolean default
        tls_prop = properties["use_tls"]
        assert tls_prop.default is False
        assert isinstance(tls_prop.type_dict, type(th.BooleanType.type_dict))

    def test_file_source_schema_exists(self):
        """Test FILE_SOURCE_SCHEMA is properly defined."""
        schema = CommonSingerSchemas.FILE_SOURCE_SCHEMA

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Check file-specific properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        file_properties = ["file_path", "file_format", "encoding"]

        for prop_name in file_properties:
            assert prop_name in property_names

    def test_file_source_schema_properties(self):
        """Test FILE_SOURCE_SCHEMA property details."""
        properties = {
            prop.name: prop
            for prop in CommonSingerSchemas.FILE_SOURCE_SCHEMA.wrapped.values()
        }

        # Test file_path property (required)
        path_prop = properties["file_path"]
        assert not path_prop.optional  # not optional means required
        assert path_prop.description == "File path or URL"

        # Test file_format with default
        format_prop = properties["file_format"]
        assert format_prop.default == "csv"
        assert format_prop.description == "File format (csv, json, parquet)"

        # Test encoding with default
        encoding_prop = properties["encoding"]
        assert encoding_prop.default == "utf-8"
        assert encoding_prop.description == "File encoding"

    def test_oauth2_api_schema_exists(self):
        """Test OAUTH2_API_SCHEMA is properly defined."""
        schema = CommonSingerSchemas.OAUTH2_API_SCHEMA

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Check OAuth2-specific properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        oauth2_properties = [
            "client_id",
            "client_secret",
            "auth_url",
            "token_url",
            "api_base_url",
        ]

        for prop_name in oauth2_properties:
            assert prop_name in property_names

    def test_oauth2_api_schema_properties(self):
        """Test OAUTH2_API_SCHEMA property details."""
        properties = {
            prop.name: prop
            for prop in CommonSingerSchemas.OAUTH2_API_SCHEMA.wrapped.values()
        }

        # Test client_secret (should be secret)
        secret_prop = properties["client_secret"]
        assert not secret_prop.optional  # not optional means required
        assert secret_prop.secret is True
        assert secret_prop.description == "OAuth2 client secret"

        # Test required URLs
        for url_field in ["auth_url", "token_url", "api_base_url"]:
            url_prop = properties[url_field]
            assert not url_prop.optional  # not optional means required
            assert isinstance(url_prop.type_dict, type(th.StringType.type_dict))

    def test_oracle_oic_schema_exists(self):
        """Test ORACLE_OIC_SCHEMA is properly defined."""
        schema = CommonSingerSchemas.ORACLE_OIC_SCHEMA

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Check OIC-specific properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        oic_properties = ["oic_host", "username", "password", "api_version"]

        for prop_name in oic_properties:
            assert prop_name in property_names

    def test_oracle_oic_schema_properties(self):
        """Test ORACLE_OIC_SCHEMA property details."""
        properties = {
            prop.name: prop
            for prop in CommonSingerSchemas.ORACLE_OIC_SCHEMA.wrapped.values()
        }

        # Test oic_host (required)
        host_prop = properties["oic_host"]
        assert not host_prop.optional  # not optional means required
        assert host_prop.description == "Oracle Integration Cloud host"

        # Test password (should be secret)
        password_prop = properties["password"]
        assert not password_prop.optional  # not optional means required
        assert password_prop.secret is True
        assert password_prop.description == "OIC password"

        # Test api_version with default
        version_prop = properties["api_version"]
        assert version_prop.default == "v1"
        assert version_prop.description == "OIC API version"

    def test_extraction_config_schema_exists(self):
        """Test EXTRACTION_CONFIG_SCHEMA is properly defined."""
        schema = CommonSingerSchemas.EXTRACTION_CONFIG_SCHEMA

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Check extraction-specific properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        extraction_properties = [
            "start_date",
            "end_date",
            "batch_size",
            "max_records",
            "stream_maps",
            "stream_map_config",
        ]

        for prop_name in extraction_properties:
            assert prop_name in property_names

    def test_extraction_config_schema_properties(self):
        """Test EXTRACTION_CONFIG_SCHEMA property details."""
        properties = {
            prop.name: prop
            for prop in CommonSingerSchemas.EXTRACTION_CONFIG_SCHEMA.wrapped.values()
        }

        # Test datetime properties
        start_date_prop = properties["start_date"]
        assert isinstance(start_date_prop.type_dict, type(th.DateTimeType.type_dict))
        assert start_date_prop.description == "Start date for extraction"

        # Test batch_size with default
        batch_prop = properties["batch_size"]
        assert batch_prop.default == 1000
        assert isinstance(batch_prop.type_dict, type(th.IntegerType.type_dict))

        # Test object properties
        stream_maps_prop = properties["stream_maps"]
        assert isinstance(stream_maps_prop.type_dict, type(th.ObjectType().type_dict))

    def test_create_tap_schema_oracle(self):
        """Test create_tap_schema method with Oracle connection type."""
        schema = CommonSingerSchemas.create_tap_schema("oracle")

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include Oracle connection properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        oracle_properties = [
            "host",
            "port",
            "username",
            "password",
            "database",
            "service_name",
            "sid",
        ]
        extraction_properties = ["start_date", "batch_size", "stream_maps"]

        for prop_name in oracle_properties + extraction_properties:
            assert prop_name in property_names

    def test_create_tap_schema_ldap(self):
        """Test create_tap_schema method with LDAP connection type."""
        schema = CommonSingerSchemas.create_tap_schema("ldap")

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include LDAP connection properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        ldap_properties = [
            "ldap_host",
            "ldap_port",
            "bind_dn",
            "bind_password",
            "base_dn",
            "use_tls",
        ]
        extraction_properties = ["start_date", "batch_size"]

        for prop_name in ldap_properties + extraction_properties:
            assert prop_name in property_names

    def test_create_tap_schema_file(self):
        """Test create_tap_schema method with file connection type."""
        schema = CommonSingerSchemas.create_tap_schema("file")

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include file source properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        file_properties = ["file_path", "file_format", "encoding"]
        extraction_properties = ["start_date", "batch_size"]

        for prop_name in file_properties + extraction_properties:
            assert prop_name in property_names

    def test_create_tap_schema_oauth2(self):
        """Test create_tap_schema method with OAuth2 connection type."""
        schema = CommonSingerSchemas.create_tap_schema("oauth2")

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include OAuth2 API properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        oauth2_properties = [
            "client_id",
            "client_secret",
            "auth_url",
            "token_url",
            "api_base_url",
        ]
        extraction_properties = ["start_date", "batch_size"]

        for prop_name in oauth2_properties + extraction_properties:
            assert prop_name in property_names

    def test_create_tap_schema_oracle_oic(self):
        """Test create_tap_schema method with Oracle OIC connection type."""
        schema = CommonSingerSchemas.create_tap_schema("oracle_oic")

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include Oracle OIC properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        oic_properties = ["oic_host", "username", "password", "api_version"]
        extraction_properties = ["start_date", "batch_size"]

        for prop_name in oic_properties + extraction_properties:
            assert prop_name in property_names

    def test_create_tap_schema_unknown_type_defaults_to_database(self):
        """Test create_tap_schema method with unknown connection type defaults to database."""
        schema = CommonSingerSchemas.create_tap_schema("unknown_type")

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include default database connection properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        database_properties = ["host", "port", "username", "password", "database"]
        extraction_properties = ["start_date", "batch_size"]

        for prop_name in database_properties + extraction_properties:
            assert prop_name in property_names

        # Should NOT include Oracle-specific properties
        assert "service_name" not in property_names
        assert "sid" not in property_names

    def test_create_tap_schema_without_extraction_config(self):
        """Test create_tap_schema method without extraction configuration."""
        schema = CommonSingerSchemas.create_tap_schema(
            "oracle",
            include_extraction_config=False,
        )

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include Oracle connection properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        oracle_properties = [
            "host",
            "port",
            "username",
            "password",
            "database",
            "service_name",
            "sid",
        ]

        for prop_name in oracle_properties:
            assert prop_name in property_names

        # Should NOT include extraction properties
        extraction_properties = ["start_date", "batch_size", "stream_maps"]
        for prop_name in extraction_properties:
            assert prop_name not in property_names

    def test_create_tap_schema_with_additional_properties(self):
        """Test create_tap_schema method with additional properties."""
        # Create additional properties
        additional_props = th.PropertiesList(
            th.Property(
                "custom_field",
                th.StringType,
                required=True,
                description="Custom tap-specific field",
            ),
            th.Property(
                "optional_field",
                th.IntegerType,
                default=42,
                description="Optional custom field",
            ),
        )

        schema = CommonSingerSchemas.create_tap_schema(
            "oracle",
            additional_properties=additional_props,
        )

        assert schema is not None
        property_names = [prop.name for prop in schema.wrapped.values()]

        # Should include Oracle properties, extraction properties, AND custom properties
        oracle_properties = ["host", "service_name"]
        extraction_properties = ["start_date", "batch_size"]
        custom_properties = ["custom_field", "optional_field"]

        for prop_name in oracle_properties + extraction_properties + custom_properties:
            assert prop_name in property_names

    def test_create_tap_schema_all_combinations(self):
        """Test create_tap_schema method with all parameter combinations."""
        connection_types = ["oracle", "ldap", "file", "oauth2", "oracle_oic", "unknown"]

        for conn_type in connection_types:
            # Test with extraction config
            schema_with_extraction = CommonSingerSchemas.create_tap_schema(
                conn_type,
                include_extraction_config=True,
            )
            assert schema_with_extraction is not None

            # Test without extraction config
            schema_without_extraction = CommonSingerSchemas.create_tap_schema(
                conn_type,
                include_extraction_config=False,
            )
            assert schema_without_extraction is not None

            # Schema without extraction should have fewer properties
            with_props = len(list(schema_with_extraction.wrapped.values()))
            without_props = len(list(schema_without_extraction.wrapped.values()))
            assert with_props > without_props


class TestFactoryFunctions:
    """Test factory functions for creating tap schemas."""

    def test_create_oracle_tap_schema(self):
        """Test create_oracle_tap_schema factory function."""
        schema = create_oracle_tap_schema()

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include Oracle and extraction properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        expected_properties = [
            "host",
            "service_name",
            "sid",
            "start_date",
            "batch_size",
        ]

        for prop_name in expected_properties:
            assert prop_name in property_names

    def test_create_oracle_tap_schema_with_additional_properties(self):
        """Test create_oracle_tap_schema with additional properties."""
        additional_props = th.PropertiesList(
            th.Property(
                "oracle_specific",
                th.StringType,
                description="Oracle specific field",
            ),
        )

        schema = create_oracle_tap_schema(additional_props)

        assert schema is not None
        property_names = [prop.name for prop in schema.wrapped.values()]

        # Should include Oracle, extraction, and custom properties
        assert "host" in property_names  # Oracle
        assert "start_date" in property_names  # Extraction
        assert "oracle_specific" in property_names  # Custom

    def test_create_ldap_tap_schema(self):
        """Test create_ldap_tap_schema factory function."""
        schema = create_ldap_tap_schema()

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include LDAP and extraction properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        expected_properties = [
            "ldap_host",
            "bind_dn",
            "base_dn",
            "start_date",
            "batch_size",
        ]

        for prop_name in expected_properties:
            assert prop_name in property_names

    def test_create_ldap_tap_schema_with_additional_properties(self):
        """Test create_ldap_tap_schema with additional properties."""
        additional_props = th.PropertiesList(
            th.Property("ldap_filter", th.StringType, description="LDAP search filter"),
        )

        schema = create_ldap_tap_schema(additional_props)

        assert schema is not None
        property_names = [prop.name for prop in schema.wrapped.values()]

        assert "ldap_host" in property_names  # LDAP
        assert "start_date" in property_names  # Extraction
        assert "ldap_filter" in property_names  # Custom

    def test_create_file_tap_schema(self):
        """Test create_file_tap_schema factory function."""
        schema = create_file_tap_schema()

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include file and extraction properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        expected_properties = [
            "file_path",
            "file_format",
            "encoding",
            "start_date",
            "batch_size",
        ]

        for prop_name in expected_properties:
            assert prop_name in property_names

    def test_create_oauth2_api_tap_schema(self):
        """Test create_oauth2_api_tap_schema factory function."""
        schema = create_oauth2_api_tap_schema()

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include OAuth2 and extraction properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        expected_properties = [
            "client_id",
            "client_secret",
            "auth_url",
            "start_date",
            "batch_size",
        ]

        for prop_name in expected_properties:
            assert prop_name in property_names

    def test_create_oracle_oic_tap_schema(self):
        """Test create_oracle_oic_tap_schema factory function."""
        schema = create_oracle_oic_tap_schema()

        assert schema is not None
        assert isinstance(schema, th.PropertiesList)

        # Should include OIC and extraction properties
        property_names = [prop.name for prop in schema.wrapped.values()]
        expected_properties = [
            "oic_host",
            "username",
            "password",
            "api_version",
            "start_date",
            "batch_size",
        ]

        for prop_name in expected_properties:
            assert prop_name in property_names

    def test_all_factory_functions_with_none_additional_properties(self):
        """Test all factory functions work with None additional properties."""
        factory_functions = [
            create_oracle_tap_schema,
            create_ldap_tap_schema,
            create_file_tap_schema,
            create_oauth2_api_tap_schema,
            create_oracle_oic_tap_schema,
        ]

        for factory_func in factory_functions:
            schema = factory_func(None)
            assert schema is not None
            assert isinstance(schema, th.PropertiesList)
            assert len(list(schema.wrapped.values())) > 0


class TestModuleExports:
    """Test module exports and public API."""

    def test_module_exports_defined(self):
        """Test that __all__ is properly defined."""
        expected_exports = [
            "CommonSingerSchemas",
            "create_file_tap_schema",
            "create_ldap_tap_schema",
            "create_oauth2_api_tap_schema",
            "create_oracle_oic_tap_schema",
            "create_oracle_tap_schema",
        ]

        assert isinstance(_schemas_all, list)
        assert len(_schemas_all) == 6
        for export in expected_exports:
            assert export in _schemas_all

    def test_all_exports_importable(self):
        """Test that all exported items can be imported."""
        # Verify all items are accessible
        assert CommonSingerSchemas is not None
        assert callable(create_file_tap_schema)
        assert callable(create_ldap_tap_schema)
        assert callable(create_oauth2_api_tap_schema)
        assert callable(create_oracle_oic_tap_schema)
        assert callable(create_oracle_tap_schema)


class TestIntegrationScenarios:
    """Integration tests for realistic schema usage scenarios."""

    def test_complete_tap_development_workflow(self):
        """Test complete workflow for developing a new tap."""
        # Scenario: Creating a new Oracle tap with custom properties
        custom_props = th.PropertiesList(
            th.Property(
                "query_timeout",
                th.IntegerType,
                default=30,
                description="Query timeout in seconds",
            ),
            th.Property(
                "enable_ssl",
                th.BooleanType,
                default=True,
                description="Enable SSL connection",
            ),
        )

        # Create schema using factory function
        schema = create_oracle_tap_schema(custom_props)

        # Verify complete schema has all expected components
        property_names = [prop.name for prop in schema.wrapped.values()]

        # Oracle base properties
        assert "host" in property_names
        assert "service_name" in property_names

        # Extraction config properties
        assert "start_date" in property_names
        assert "batch_size" in property_names

        # Custom properties
        assert "query_timeout" in property_names
        assert "enable_ssl" in property_names

    def test_schema_reusability_across_connection_types(self):
        """Test that schemas can be reused and extended across different connection types."""
        # Create schemas for different connection types
        connection_types = ["oracle", "ldap", "file", "oauth2", "oracle_oic"]
        schemas = {}

        for conn_type in connection_types:
            schemas[conn_type] = CommonSingerSchemas.create_tap_schema(conn_type)

        # Verify each schema is unique but includes extraction config
        for conn_type, schema in schemas.items():
            property_names = [prop.name for prop in schema.wrapped.values()]

            # All should have extraction config
            assert "start_date" in property_names
            assert "batch_size" in property_names

            # Each should have connection-specific properties
            if conn_type == "oracle":
                assert "service_name" in property_names
            elif conn_type == "ldap":
                assert "ldap_host" in property_names
            elif conn_type == "file":
                assert "file_path" in property_names
            elif conn_type == "oauth2":
                assert "client_id" in property_names
            elif conn_type == "oracle_oic":
                assert "oic_host" in property_names

    def test_schema_consistency_across_factory_functions(self):
        """Test that factory functions produce consistent schemas."""
        # Create schema using class method
        class_method_schema = CommonSingerSchemas.create_tap_schema("oracle")

        # Create schema using factory function
        factory_function_schema = create_oracle_tap_schema()

        # Should have same properties
        class_props = {prop.name for prop in class_method_schema.wrapped.values()}
        factory_props = {prop.name for prop in factory_function_schema.wrapped.values()}

        assert class_props == factory_props

    def test_error_resilience_with_edge_cases(self):
        """Test error resilience with edge case inputs."""
        # Test with empty additional properties
        empty_props = th.PropertiesList()
        schema = create_oracle_tap_schema(empty_props)
        assert schema is not None

        # Test with multiple factory functions
        all_schemas = [
            create_oracle_tap_schema(),
            create_ldap_tap_schema(),
            create_file_tap_schema(),
            create_oauth2_api_tap_schema(),
            create_oracle_oic_tap_schema(),
        ]

        # All should be valid PropertiesList instances
        for schema in all_schemas:
            assert isinstance(schema, th.PropertiesList)
            assert len(list(schema.wrapped.values())) > 0
