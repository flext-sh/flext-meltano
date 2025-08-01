"""Common Singer Schemas - REAL DRY Implementation.

This module provides unified schema definitions that eliminate code duplication
across all flext-tap-*, flext-target-*, and flext-dbt-* projects.

REAL PROBLEM SOLVED: All Singer projects were duplicating schema definitions.
This centralizes common patterns and configurations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Any, ClassVar

from singer_sdk import typing as th


class CommonSingerSchemas:
    """REAL centralization of common Singer schema patterns."""

    # Common database connection schemas
    DATABASE_CONNECTION_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "host",
            th.StringType,
            required=True,
            description="Database host",
        ),
        th.Property(
            "port",
            th.IntegerType,  
            description="Database port",
        ),
        th.Property(
            "username",
            th.StringType,
            required=True,
            description="Database username",
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            secret=True,
            description="Database password",
        ),
        th.Property(
            "database",
            th.StringType,
            description="Database name",
        ),
    )

    # Oracle-specific extensions
    ORACLE_CONNECTION_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "host",
            th.StringType,
            required=True,
            description="Oracle database host",
        ),
        th.Property(
            "port",
            th.IntegerType,
            default=1521,
            description="Oracle database port",
        ),
        th.Property(
            "username",
            th.StringType,
            required=True,
            description="Oracle database username",
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            secret=True,
            description="Oracle database password",
        ),
        th.Property(
            "database",
            th.StringType,
            description="Oracle database name",
        ),
        th.Property(
            "service_name", 
            th.StringType, 
            description="Oracle service name"
        ),
        th.Property(
            "schema_name",
            th.StringType,
            description="Oracle schema name",
        ),
    )

    # LDAP-specific schemas
    LDAP_CONNECTION_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "host",
            th.StringType,
            required=True,
            description="LDAP server host",
        ),
        th.Property(
            "port",
            th.IntegerType,
            default=389,
            description="LDAP server port",
        ),
        th.Property(
            "bind_dn",
            th.StringType,
            required=True,
            description="LDAP bind DN",
        ),
        th.Property(
            "password",
            th.StringType,
            required=True,
            secret=True,
            description="LDAP bind password",
        ),
        th.Property(
            "base_dn",
            th.StringType,
            required=True,
            description="LDAP base DN",
        ),
        th.Property(
            "use_ssl",
            th.BooleanType,
            default=False,
            description="Use SSL connection",
        ),
    )

    # Common extraction configuration
    EXTRACTION_CONFIG_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "batch_size",
            th.IntegerType,
            default=10000,
            description="Batch size for data extraction",
        ),
        th.Property(
            "timeout",
            th.IntegerType,
            default=30,
            description="Connection timeout in seconds",
        ),
        th.Property(
            "max_workers",
            th.IntegerType,
            default=4,
            description="Maximum concurrent workers",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="Start date for incremental extraction",
        ),
    )

    # File-based source configurations
    FILE_SOURCE_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "file_path",
            th.StringType,
            description="Path to source file",
        ),
        th.Property(
            "directory_path",
            th.StringType,
            description="Path to source directory",
        ),
        th.Property(
            "file_pattern",
            th.StringType,
            default="*.ldif",
            description="File pattern to match",
        ),
        th.Property(
            "encoding",
            th.StringType,
            default="utf-8",
            description="File encoding",
        ),
    )

    # OAuth2/API-based connection schemas
    OAUTH2_API_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "oauth_client_id",
            th.StringType,
            required=True,
            description="OAuth2 client ID",
        ),
        th.Property(
            "oauth_client_secret",
            th.StringType,
            required=True,
            secret=True,
            description="OAuth2 client secret",
        ),
        th.Property(
            "oauth_endpoint",
            th.StringType,
            required=True,
            description="OAuth2 token endpoint URL",
        ),
        th.Property(
            "base_url",
            th.StringType,
            required=True,
            description="API base URL",
        ),
        th.Property(
            "oauth_scope",
            th.StringType,
            description="OAuth2 scope",
        ),
        th.Property(
            "api_version",
            th.StringType,
            default="v1",
            description="API version",
        ),
        th.Property(
            "request_timeout",
            th.IntegerType,
            default=30,
            description="Request timeout in seconds",
        ),
        th.Property(
            "max_retries",
            th.IntegerType,
            default=3,
            description="Maximum number of retries",
        ),
    )

    # Oracle OIC specific schema extensions
    ORACLE_OIC_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
        th.Property(
            "oauth_client_id",
            th.StringType,
            required=True, 
            description="OAuth2 client ID for IDCS",
        ),
        th.Property(
            "oauth_client_secret",
            th.StringType,
            required=True,
            secret=True,
            description="OAuth2 client secret for IDCS",
        ),
        th.Property(
            "oauth_token_url",
            th.StringType,
            required=True,
            description="IDCS OAuth2 token endpoint",
        ),
        th.Property(
            "oic_url",
            th.StringType,
            required=True,
            description="Oracle Integration Cloud URL",
        ),
        th.Property(
            "oauth_client_aud",
            th.StringType,
            description="OAuth2 audience for OIC resource access",
        ),
        th.Property(
            "oauth_scope",
            th.StringType,
            default="urn:opc:resource:consumer:all",
            description="OAuth2 scope for OIC",
        ),
        th.Property(
            "include_infrastructure",
            th.BooleanType,
            default=False,
            description="Include infrastructure streams",
        ),
        th.Property(
            "include_monitoring",
            th.BooleanType,
            default=False,
            description="Include monitoring streams",
        ),
        th.Property(
            "include_extended",
            th.BooleanType,
            default=False,
            description="Include extended streams",
        ),
    )

    @classmethod
    def create_tap_schema(
        self,
        connection_type: str,
        include_extraction_config: bool = True,
        additional_properties: th.PropertiesList | None = None,
    ) -> th.PropertiesList:
        """Factory method to create tap schemas with REAL reusability.
        
        Args:
            connection_type: Type of connection (oracle, ldap, file)
            include_extraction_config: Include common extraction settings
            additional_properties: Additional tap-specific properties
            
        Returns:
            Complete schema for the tap
        """
        # Get base connection schema properties
        if connection_type == "oracle":
            base_properties = list(self.ORACLE_CONNECTION_SCHEMA.wrapped.values())
        elif connection_type == "ldap":
            base_properties = list(self.LDAP_CONNECTION_SCHEMA.wrapped.values())
        elif connection_type == "file":
            base_properties = list(self.FILE_SOURCE_SCHEMA.wrapped.values())
        else:
            base_properties = list(self.DATABASE_CONNECTION_SCHEMA.wrapped.values())

        # Build complete properties list
        all_properties = base_properties
        
        if include_extraction_config:
            all_properties.extend(self.EXTRACTION_CONFIG_SCHEMA.wrapped.values())
        
        if additional_properties:
            all_properties.extend(additional_properties.wrapped.values())
            
        return th.PropertiesList(*all_properties)


# Factory functions for easy usage
def create_oracle_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create Oracle tap schema with common patterns."""
    return CommonSingerSchemas.create_tap_schema(
        "oracle", 
        include_extraction_config=True,
        additional_properties=additional_properties,
    )


def create_ldap_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create LDAP tap schema with common patterns.""" 
    return CommonSingerSchemas.create_tap_schema(
        "ldap",
        include_extraction_config=True,
        additional_properties=additional_properties,
    )



    @classmethod
    def create_tap_schema(
        self,
        connection_type: str,
        include_extraction_config: bool = True,
        additional_properties: th.PropertiesList | None = None,
    ) -> th.PropertiesList:
        """Factory method to create tap schemas with REAL reusability.
        
        Args:
            connection_type: Type of connection (oracle, ldap, file, oauth2, oracle_oic)
            include_extraction_config: Include common extraction settings
            additional_properties: Additional tap-specific properties
            
        Returns:
            Complete schema for the tap
        """
        # Get base connection schema properties
        if connection_type == "oracle":
            base_properties = list(self.ORACLE_CONNECTION_SCHEMA.wrapped.values())
        elif connection_type == "ldap":
            base_properties = list(self.LDAP_CONNECTION_SCHEMA.wrapped.values())
        elif connection_type == "file":
            base_properties = list(self.FILE_SOURCE_SCHEMA.wrapped.values())
        elif connection_type == "oauth2":
            base_properties = list(self.OAUTH2_API_SCHEMA.wrapped.values())
        elif connection_type == "oracle_oic":
            base_properties = list(self.ORACLE_OIC_SCHEMA.wrapped.values())
        else:
            base_properties = list(self.DATABASE_CONNECTION_SCHEMA.wrapped.values())

        # Build complete properties list
        all_properties = base_properties
        
        if include_extraction_config:
            all_properties.extend(self.EXTRACTION_CONFIG_SCHEMA.wrapped.values())
        
        if additional_properties:
            all_properties.extend(additional_properties.wrapped.values())
            
        return th.PropertiesList(*all_properties)


# Factory functions for easy usage
def create_oracle_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create Oracle tap schema with common patterns."""
    return CommonSingerSchemas.create_tap_schema(
        "oracle", 
        include_extraction_config=True,
        additional_properties=additional_properties,
    )


def create_ldap_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create LDAP tap schema with common patterns.""" 
    return CommonSingerSchemas.create_tap_schema(
        "ldap",
        include_extraction_config=True,
        additional_properties=additional_properties,
    )


def create_file_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create file-based tap schema with common patterns."""
    return CommonSingerSchemas.create_tap_schema(
        "file",
        include_extraction_config=True, 
        additional_properties=additional_properties,
    )


def create_oauth2_api_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create OAuth2 API tap schema with common patterns."""
    return CommonSingerSchemas.create_tap_schema(
        "oauth2",
        include_extraction_config=True,
        additional_properties=additional_properties,
    )


def create_oracle_oic_tap_schema(
    additional_properties: th.PropertiesList | None = None,
) -> th.PropertiesList:
    """Create Oracle OIC tap schema with IDCS OAuth2 patterns."""
    return CommonSingerSchemas.create_tap_schema(
        "oracle_oic",
        include_extraction_config=True,
        additional_properties=additional_properties,
    )