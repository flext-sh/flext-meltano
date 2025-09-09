"""FLEXT Meltano Constants - Meltano-specific constants extending FlextConstants hierarchical system.

Provides comprehensive Meltano-specific constants following the FlextConstants pattern with
domain organization, type-safe Final annotations, and hierarchical structure. All constants
related to Meltano, Singer SDK, DBT, and ELT pipelines are organized under single class.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_core import FlextConstants


class FlextMeltanoConstants(FlextConstants):
    """Meltano-specific hierarchical constants system extending FlextConstants.

    This class inherits all core FLEXT constants and adds Meltano-specific
    constant definitions organized by domain functionality following the
    same hierarchical pattern as FlextConstants.
    """

    # =========================================================================
    # CORE DOMAIN - Meltano system identification and metadata
    # =========================================================================

    class Core(FlextConstants.Core):
        """Meltano core system constants extending FlextConstants.Core."""

        # Use new names to avoid overriding final attributes from parent
        MELTANO_NAME: Final[str] = "FLEXT-MELTANO"
        MELTANO_VERSION: Final[str] = "2.0.0-enterprise"
        DESCRIPTION: Final[str] = (
            "Enterprise Meltano/Singer/DBT integration for FLEXT ecosystem"
        )
        AUTHOR: Final[str] = "FLEXT Team"

        # Meltano ecosystem integration
        MELTANO_VERSION_REQUIRED: Final[str] = "3.9.1"
        SINGER_SDK_VERSION_REQUIRED: Final[str] = "0.48.0"
        DBT_VERSION_REQUIRED: Final[str] = "1.10.5"

    # =========================================================================
    # PLUGIN DOMAIN - Meltano plugin management constants
    # =========================================================================

    class Plugin:
        """Meltano plugin management constants."""

        # Plugin types
        TYPE_TAP: Final[str] = "extractors"
        TYPE_TARGET: Final[str] = "loaders"
        TYPE_TRANSFORM: Final[str] = "transformers"

        # Plugin variants and sources
        DEFAULT_VARIANT: Final[str] = "meltanolabs"
        HUB_URL: Final[str] = "https://hub.meltano.com"

        # Plugin discovery and installation
        DISCOVERY_TIMEOUT: Final[int] = 30
        INSTALLATION_TIMEOUT: Final[int] = 300

    # =========================================================================
    # SINGER DOMAIN - Singer SDK integration constants
    # =========================================================================

    class SingerSDK:
        """Singer SDK integration constants."""

        # Message types
        MESSAGE_TYPE_RECORD: Final[str] = "RECORD"
        MESSAGE_TYPE_SCHEMA: Final[str] = "SCHEMA"
        MESSAGE_TYPE_STATE: Final[str] = "STATE"
        MESSAGE_TYPE_METRIC: Final[str] = "METRIC"

        # Stream processing
        DEFAULT_BATCH_SIZE: Final[int] = 1000
        MAX_BATCH_SIZE: Final[int] = 10000

        # Performance and limits
        DEFAULT_REQUEST_TIMEOUT: Final[int] = 300
        MAX_CONCURRENT_STREAMS: Final[int] = 10

    # =========================================================================
    # DBT DOMAIN - DBT Core integration constants
    # =========================================================================

    class DBTCore:
        """DBT Core integration constants."""

        # Project structure
        DEFAULT_PROFILES_DIR: Final[str] = "~/.dbt"
        DEFAULT_PROJECT_DIR: Final[str] = "./dbt_project"
        PROJECT_FILE: Final[str] = "dbt_project.yml"
        PROFILES_FILE: Final[str] = "profiles.yml"
        MANIFEST_FILE: Final[str] = "manifest.json"

        # Commands
        COMMAND_RUN: Final[str] = "run"
        COMMAND_TEST: Final[str] = "test"
        COMMAND_BUILD: Final[str] = "build"
        COMMAND_COMPILE: Final[str] = "compile"

        # Model materialization
        MATERIALIZATION_TABLE: Final[str] = "table"
        MATERIALIZATION_VIEW: Final[str] = "view"
        MATERIALIZATION_INCREMENTAL: Final[str] = "incremental"

    # =========================================================================
    # ELT DOMAIN - Extract-Load-Transform pipeline constants
    # =========================================================================

    class ELT:
        """Extract-Load-Transform pipeline constants."""

        # Pipeline stages
        EXTRACT_STAGE: Final[str] = "extract"
        LOAD_STAGE: Final[str] = "load"
        TRANSFORM_STAGE: Final[str] = "transform"

        # Pipeline status
        STATUS_PENDING: Final[str] = "pending"
        STATUS_RUNNING: Final[str] = "running"
        STATUS_SUCCESS: Final[str] = "success"
        STATUS_FAILED: Final[str] = "failed"

        # Performance
        DEFAULT_PIPELINE_TIMEOUT: Final[int] = 3600  # 1 hour
        DEFAULT_RETRY_ATTEMPTS: Final[int] = 3

    # =========================================================================
    # BRIDGE DOMAIN - Go service integration constants
    # =========================================================================

    class Bridge:
        """Go service integration constants."""

        # Service configuration
        DEFAULT_HOST: Final[str] = "localhost"
        DEFAULT_PORT: Final[int] = 8081
        API_VERSION: Final[str] = "v1"

        # Endpoints
        HEALTH_ENDPOINT: Final[str] = "/health"
        VERSION_ENDPOINT: Final[str] = "/version"

        # Communication
        DEFAULT_TIMEOUT: Final[int] = 30
        JSON_CONTENT_TYPE: Final[str] = "application/json"


__all__ = [
    "FlextMeltanoConstants",
]
