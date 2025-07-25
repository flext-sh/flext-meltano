"""GrupoNOS Meltano Configuration - Consolidated Implementation.

Configuration classes for GrupoNOS Meltano orchestration, consolidated from
gruponos-meltano-native for centralized management.
"""

from __future__ import annotations

import os
from typing import Any

from flext_core import FlextValueObject
from pydantic import Field


class GruponosMeltanoOracleConnectionConfig(FlextValueObject):
    """Oracle connection configuration for GrupoNOS Meltano integration."""

    host: str = Field(..., description="Oracle database host")
    port: int = Field(default=1521, description="Oracle database port")
    service_name: str = Field(..., description="Oracle service name")
    username: str = Field(..., description="Oracle username")
    password: str = Field(..., description="Oracle password", repr=False)
    protocol: str = Field(default="TCP", description="Oracle protocol")

    def validate_domain_rules(self) -> None:
        """Validate Oracle connection configuration domain rules."""
        if not self.host.strip():
            msg = "Oracle host cannot be empty"
            raise ValueError(msg)
        if not self.service_name.strip():
            msg = "Oracle service name cannot be empty"
            raise ValueError(msg)


class GruponosMeltanoJobConfig(FlextValueObject):
    """Job configuration for GrupoNOS Meltano orchestration."""

    name: str = Field(..., description="Job name")
    description: str = Field(default="", description="Job description")
    schedule: str | None = Field(default=None, description="Job schedule")
    timeout: int = Field(default=3600, description="Job timeout in seconds")
    retry_count: int = Field(default=3, description="Number of retries")
    environment: str = Field(default="dev", description="Target environment")

    def validate_domain_rules(self) -> None:
        """Validate job configuration domain rules."""
        if not self.name.strip():
            msg = "Job name cannot be empty"
            raise ValueError(msg)


class GruponosMeltanoAlertConfig(FlextValueObject):
    """Alert configuration for GrupoNOS Meltano monitoring."""

    webhook_enabled: bool = Field(default=False, description="Enable webhook alerts")
    webhook_url: str | None = Field(default=None, description="Webhook URL")
    max_error_rate_percent: float = Field(default=5.0, description="Max error rate threshold")
    email_enabled: bool = Field(default=False, description="Enable email alerts")
    email_recipients: list[str] = Field(default_factory=list, description="Email recipients")

    # Additional alert configuration for compatibility
    slack_enabled: bool = Field(default=False, description="Enable Slack alerts")
    slack_webhook_url: str | None = Field(default=None, description="Slack webhook URL")
    alert_threshold: int = Field(default=1, description="Minimum failures before alerting")

    def validate_domain_rules(self) -> None:
        """Validate alert configuration domain rules."""
        if self.webhook_enabled and not self.webhook_url:
            msg = "Webhook URL required when webhook alerts are enabled"
            raise ValueError(msg)


class GruponosMeltanoTargetOracleConfig(FlextValueObject):
    """Target Oracle configuration for GrupoNOS Meltano."""

    oracle: GruponosMeltanoOracleConnectionConfig
    target_schema: str = Field(..., description="Target schema")
    parallel_degree: int = Field(default=1, description="Parallel processing degree")
    batch_size: int = Field(default=1000, description="Batch size for operations")

    # CLI compatibility attributes
    table_prefix: str = Field(default="", description="Table prefix")
    parallel_workers: int = Field(default=1, description="Parallel workers")

    @property
    def schema(self) -> str:
        """Legacy compatibility property for schema."""
        return self.target_schema

    def __post_init__(self) -> None:
        """Set legacy compatibility attributes."""
        if not self.parallel_workers:
            object.__setattr__(self, "parallel_workers", self.parallel_degree)

    def validate_domain_rules(self) -> None:
        """Validate target Oracle configuration domain rules."""
        if not self.target_schema.strip():
            msg = "Target schema cannot be empty"
            raise ValueError(msg)


class GruponosMeltanoWMSSourceConfig(FlextValueObject):
    """WMS Source configuration for GrupoNOS Meltano."""

    oracle: GruponosMeltanoOracleConnectionConfig
    entities: list[str] = Field(default_factory=list, description="WMS entities to extract")
    enable_incremental: bool = Field(default=True, description="Enable incremental extraction")
    page_size: int = Field(default=500, description="Page size for extraction")

    # CLI compatibility attributes
    organization_id: str = Field(default="101", description="Organization ID")
    facility_code: str = Field(default="DC001", description="Facility code")
    source_schema: str = Field(default="WMS", description="Source schema")
    batch_size: int = Field(default=1000, description="Batch size")
    parallel_jobs: int = Field(default=1, description="Parallel jobs")
    extract_mode: str = Field(default="full", description="Extract mode")

    def validate_domain_rules(self) -> None:
        """Validate WMS source configuration domain rules."""
        if self.page_size <= 0:
            msg = "Page size must be positive"
            raise ValueError(msg)


class GruponosMeltanoSettings(FlextValueObject):
    """Complete settings for GrupoNOS Meltano orchestration."""

    project_name: str = Field(default="gruponos-meltano-native", description="Project name")
    environment: str = Field(default="dev", description="Current environment")
    debug_mode: bool = Field(default=False, description="Enable debug mode")
    dry_run: bool = Field(default=False, description="Enable dry run mode")

    # Optional configurations
    wms_source: GruponosMeltanoWMSSourceConfig | None = Field(default=None)
    target_oracle: GruponosMeltanoTargetOracleConfig | None = Field(default=None)
    alerts: GruponosMeltanoAlertConfig = Field(default_factory=GruponosMeltanoAlertConfig)

    # Legacy compatibility attributes
    app_name: str = Field(default="gruponos-meltano-native", description="Application name")
    version: str = Field(default="1.0.0", description="Application version")
    debug: bool = Field(default=False, description="Debug flag (legacy)")
    log_level: str = Field(default="INFO", description="Log level")
    meltano_project_root: str | None = Field(default=None, description="Meltano project root")
    meltano_environment: str = Field(default="dev", description="Meltano environment")
    meltano_state_backend: str = Field(default="filesystem", description="Meltano state backend")

    @property
    def oracle(self) -> GruponosMeltanoOracleConnectionConfig | None:
        """Get Oracle connection config (legacy compatibility)."""
        return self.target_oracle.oracle if self.target_oracle else None

    @property
    def meltano(self) -> dict[str, str] | None:
        """Get Meltano configuration (legacy compatibility)."""
        if self.meltano_project_root:
            return {
                "project_root": self.meltano_project_root,
                "environment": self.meltano_environment,
                "state_backend": self.meltano_state_backend,
            }
        return None

    @property
    def job(self) -> object:
        """Get job configuration (legacy compatibility)."""
        # Return an object with job attributes for CLI compatibility
        class JobConfig:
            job_name = "gruponos-etl-pipeline"
            schedule = "0 0 * * *"
            timeout_minutes = 60
            retry_attempts = 3
            retry_delay_seconds = 30

        return JobConfig()

    def is_debug_enabled(self) -> bool:
        """Check if debug mode is enabled (legacy compatibility)."""
        return self.debug_mode

    def validate_domain_rules(self) -> None:
        """Validate settings domain rules."""
        if not self.project_name.strip():
            msg = "Project name cannot be empty"
            raise ValueError(msg)

    def to_legacy_env(self) -> dict[str, str]:
        """Convert configuration to legacy environment variables format."""
        env_vars: dict[str, str] = {}

        env_vars["PROJECT_NAME"] = self.project_name
        env_vars["ENVIRONMENT"] = self.environment
        env_vars["DEBUG_MODE"] = str(self.debug_mode).lower()
        env_vars["DRY_RUN"] = str(self.dry_run).lower()

        if self.wms_source is not None:
            env_vars["WMS_HOST"] = self.wms_source.oracle.host
            env_vars["WMS_PORT"] = str(self.wms_source.oracle.port)
            env_vars["WMS_SERVICE_NAME"] = self.wms_source.oracle.service_name
            env_vars["WMS_USERNAME"] = self.wms_source.oracle.username
            # Note: Don't export passwords in legacy env

        if self.target_oracle is not None:
            env_vars["TARGET_ORACLE_HOST"] = self.target_oracle.oracle.host
            env_vars["TARGET_ORACLE_PORT"] = str(self.target_oracle.oracle.port)
            env_vars["TARGET_ORACLE_SERVICE_NAME"] = self.target_oracle.oracle.service_name
            env_vars["TARGET_ORACLE_USERNAME"] = self.target_oracle.oracle.username
            env_vars["TARGET_ORACLE_SCHEMA"] = self.target_oracle.target_schema

        return env_vars

    @classmethod
    def from_env(cls) -> GruponosMeltanoSettings:
        """Create settings from environment variables."""
        # Basic settings
        settings_data: dict[str, Any] = {
            "project_name": os.getenv("PROJECT_NAME", "gruponos-meltano-native"),
            "environment": os.getenv("ENVIRONMENT", "dev"),
            "debug_mode": os.getenv("DEBUG_MODE", "false").lower() == "true",
            "dry_run": os.getenv("DRY_RUN", "false").lower() == "true",
        }

        # WMS Source configuration (optional)
        wms_host = os.getenv("WMS_HOST")
        if wms_host:
            wms_oracle_config = GruponosMeltanoOracleConnectionConfig(
                host=wms_host,
                port=int(os.getenv("WMS_PORT", "1521")),
                service_name=os.getenv("WMS_SERVICE_NAME", "ORCL"),
                username=os.getenv("WMS_USERNAME", ""),
                password=os.getenv("WMS_PASSWORD", ""),
            )
            settings_data["wms_source"] = GruponosMeltanoWMSSourceConfig(
                oracle=wms_oracle_config,
                entities=os.getenv("WMS_ENTITIES", "").split(",") if os.getenv("WMS_ENTITIES") else [],
                enable_incremental=os.getenv("WMS_ENABLE_INCREMENTAL", "true").lower() == "true",
                page_size=int(os.getenv("WMS_PAGE_SIZE", "500")),
            )

        # Target Oracle configuration (optional)
        target_host = os.getenv("TARGET_ORACLE_HOST")
        if target_host:
            target_oracle_config = GruponosMeltanoOracleConnectionConfig(
                host=target_host,
                port=int(os.getenv("TARGET_ORACLE_PORT", "1521")),
                service_name=os.getenv("TARGET_ORACLE_SERVICE_NAME", "ORCL"),
                username=os.getenv("TARGET_ORACLE_USERNAME", ""),
                password=os.getenv("TARGET_ORACLE_PASSWORD", ""),
            )
            settings_data["target_oracle"] = GruponosMeltanoTargetOracleConfig(
                oracle=target_oracle_config,
                target_schema=os.getenv("TARGET_ORACLE_SCHEMA", "OIC"),
                parallel_degree=int(os.getenv("TARGET_ORACLE_PARALLEL_DEGREE", "1")),
                batch_size=int(os.getenv("TARGET_ORACLE_BATCH_SIZE", "1000")),
            )

        # Alert configuration
        settings_data["alerts"] = GruponosMeltanoAlertConfig(
            webhook_enabled=os.getenv("ALERT_WEBHOOK_ENABLED", "false").lower() == "true",
            webhook_url=os.getenv("ALERT_WEBHOOK_URL"),
            max_error_rate_percent=float(os.getenv("ALERT_MAX_ERROR_RATE", "5.0")),
            email_enabled=os.getenv("ALERT_EMAIL_ENABLED", "false").lower() == "true",
            email_recipients=os.getenv("ALERT_EMAIL_RECIPIENTS", "").split(",") if os.getenv("ALERT_EMAIL_RECIPIENTS") else [],
        )

        return cls(**settings_data)


def create_gruponos_meltano_settings(
    *,
    project_name: str = "gruponos-meltano-native",
    environment: str = "dev",
    debug_mode: bool = False,
    dry_run: bool = False,
    **kwargs: str | int | bool | dict[str, Any] | None,
) -> GruponosMeltanoSettings:
    """Create GrupoNOS Meltano settings factory."""
    return GruponosMeltanoSettings(
        project_name=project_name,
        environment=environment,
        debug_mode=debug_mode,
        dry_run=dry_run,
        **kwargs,
    )
