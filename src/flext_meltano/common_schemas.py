"""FLEXT Meltano Common Schemas - Centralized Singer Schema Definitions.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_core import FlextModel
from pydantic import ConfigDict, Field
from singer_sdk import typing as th


class FlextMeltanoPluginInfo(FlextModel):
    """Centralized plugin information model - NO DUPLICATION."""

    # Installation tests expect immutability for info objects
    model_config = ConfigDict(frozen=True)
    name: str = Field(..., description="Plugin name")
    type: str = Field(..., description="Plugin type (extractor/loader/transformer)")
    namespace: str = Field(..., description="Plugin namespace")
    description: str = Field(default="", description="Plugin description")
    version: str | None = Field(default=None, description="Plugin version")
    pip_url: str | None = Field(default=None, description="Pip installation URL")
    executable: str | None = Field(default=None, description="Plugin executable")
    installed: bool = Field(default=False, description="Whether plugin is installed")
    capabilities: list[str] = Field(
      default_factory=list,
      description="Plugin capabilities",
    )


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
          required=True,
          description="Database name",
      ),
    )

    # Oracle-specific connection schema
    ORACLE_CONNECTION_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
      *DATABASE_CONNECTION_SCHEMA.wrapped.values(),
      th.Property(
          "service_name",
          th.StringType,
          description="Oracle service name",
      ),
      th.Property(
          "sid",
          th.StringType,
          description="Oracle SID",
      ),
    )

    # LDAP connection schema
    LDAP_CONNECTION_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
      th.Property(
          "ldap_host",
          th.StringType,
          required=True,
          description="LDAP server host",
      ),
      th.Property(
          "ldap_port",
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
          "bind_password",
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
          "use_tls",
          th.BooleanType,
          default=False,
          description="Use TLS connection",
      ),
    )

    # File source schema
    FILE_SOURCE_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
      th.Property(
          "file_path",
          th.StringType,
          required=True,
          description="File path or URL",
      ),
      th.Property(
          "file_format",
          th.StringType,
          default="csv",
          description="File format (csv, json, parquet)",
      ),
      th.Property(
          "encoding",
          th.StringType,
          default="utf-8",
          description="File encoding",
      ),
    )

    # OAuth2 API schema
    OAUTH2_API_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
      th.Property(
          "client_id",
          th.StringType,
          required=True,
          description="OAuth2 client ID",
      ),
      th.Property(
          "client_secret",
          th.StringType,
          required=True,
          secret=True,
          description="OAuth2 client secret",
      ),
      th.Property(
          "auth_url",
          th.StringType,
          required=True,
          description="OAuth2 authorization URL",
      ),
      th.Property(
          "token_url",
          th.StringType,
          required=True,
          description="OAuth2 token URL",
      ),
      th.Property(
          "api_base_url",
          th.StringType,
          required=True,
          description="API base URL",
      ),
    )

    # Oracle OIC schema
    ORACLE_OIC_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
      th.Property(
          "oic_host",
          th.StringType,
          required=True,
          description="Oracle Integration Cloud host",
      ),
      th.Property(
          "username",
          th.StringType,
          required=True,
          description="OIC username",
      ),
      th.Property(
          "password",
          th.StringType,
          required=True,
          secret=True,
          description="OIC password",
      ),
      th.Property(
          "api_version",
          th.StringType,
          default="v1",
          description="OIC API version",
      ),
    )

    # Common extraction configuration
    EXTRACTION_CONFIG_SCHEMA: ClassVar[th.PropertiesList] = th.PropertiesList(
      th.Property(
          "start_date",
          th.DateTimeType,
          description="Start date for extraction",
      ),
      th.Property(
          "end_date",
          th.DateTimeType,
          description="End date for extraction",
      ),
      th.Property(
          "batch_size",
          th.IntegerType,
          default=1000,
          description="Batch size for extraction",
      ),
      th.Property(
          "max_records",
          th.IntegerType,
          description="Maximum records to extract",
      ),
      th.Property(
          "stream_maps",
          th.ObjectType(),
          description="Stream mappings configuration",
      ),
      th.Property(
          "stream_map_config",
          th.ObjectType(),
          description="Stream map configuration",
      ),
    )

    @classmethod
    def create_tap_schema(
      cls,
      connection_type: str,
      *,
      include_extraction_config: bool = True,
      additional_properties: th.PropertiesList | None = None,
    ) -> th.PropertiesList:
      """Create tap schemas with REAL reusability.

      Args:
          connection_type: Type of connection (oracle, ldap, file)
          include_extraction_config: Include common extraction settings
          additional_properties: Additional tap-specific properties

      Returns:
          Complete schema for the tap

      """
      # Get base connection schema properties
      if connection_type == "oracle":
          base_properties = list(cls.ORACLE_CONNECTION_SCHEMA.wrapped.values())
      elif connection_type == "ldap":
          base_properties = list(cls.LDAP_CONNECTION_SCHEMA.wrapped.values())
      elif connection_type == "file":
          base_properties = list(cls.FILE_SOURCE_SCHEMA.wrapped.values())
      elif connection_type == "oauth2":
          base_properties = list(cls.OAUTH2_API_SCHEMA.wrapped.values())
      elif connection_type == "oracle_oic":
          base_properties = list(cls.ORACLE_OIC_SCHEMA.wrapped.values())
      else:
          base_properties = list(cls.DATABASE_CONNECTION_SCHEMA.wrapped.values())

      # Build complete properties list
      all_properties = base_properties.copy()

      # Add extraction configuration if requested
      if include_extraction_config:
          all_properties.extend(cls.EXTRACTION_CONFIG_SCHEMA.wrapped.values())

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
    """Create Oracle OIC tap schema with common patterns."""
    return CommonSingerSchemas.create_tap_schema(
      "oracle_oic",
      include_extraction_config=True,
      additional_properties=additional_properties,
    )


# Clean public API
__all__: list[str] = [
    "CommonSingerSchemas",
    "create_file_tap_schema",
    "create_ldap_tap_schema",
    "create_oauth2_api_tap_schema",
    "create_oracle_oic_tap_schema",
    "create_oracle_tap_schema",
]
