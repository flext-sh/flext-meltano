"""Integration lifecycle management for Oracle OIC using flext-core patterns.s.

This module provides a manager for integrating with Oracle OIC,
using flext-core patterns for FlextMeltanoResult, dependency injection,
and error handling.  Zero tolerance for code duplication.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

import httpx
from flext_core import FlextValueObject
from tenacity import retry, stop_after_attempt, wait_exponential

from flext_meltano import FlextMeltanoResult

# HTTP status constants
HTTP_OK = 200


def get_logger(name: str) -> logging.Logger:
    """Get logger instance for the given name.

    Args:
        name: Logger name.

    Returns:
        Logger instance.

    """
    return logging.getLogger(name)


if TYPE_CHECKING:
    from flext_meltano.extensions.oracle_oic.config import OracleOICExtensionSettings

logger = get_logger(__name__)


class IntegrationIdentifier(FlextValueObject):
    """Integration identifier value object using flext-core patterns."""

    integration_id: str
    version: str = "01.00.0000"

    def __str__(self) -> str:
        """Return string representation of integration identifier."""
        return f"{self.integration_id}|{self.version}"


class IntegrationStatus(FlextValueObject):
    """Integration status value object using flext-core patterns."""

    integration_id: str
    version: str | None = None
    status: str | None = None
    message: str | None = None
    last_updated: str | None = None


class LifecycleOperationResult(FlextValueObject):
    """Lifecycle operation result value object using flext-core patterns."""

    integration_id: str
    version: str | None = None
    operation: str | None = None
    success: bool = False
    message: str | None = None
    details: dict[str, Any] | None = None


class BulkOperationResult(FlextValueObject):
    """Bulk operation result value object using flext-core patterns."""

    total_count: int
    success_count: int
    failure_count: int
    successful_integrations: list[str]
    failed_integrations: list[dict[str, Any]]


class LifecycleManager:
    """Manages integration lifecycle operations in Oracle OIC using flext-core patterns."""

    def __init__(self, settings: OracleOICExtensionSettings) -> None:
        """Initialize lifecycle manager with OIC settings.

        Args:
            settings: Oracle OIC extension settings

        """
        self.settings = settings
        self._client: httpx.Client | None = None
        self._access_token: str | None = None

    @property
    def client(self) -> httpx.Client:
        """Get or create HTTP client with authentication headers.

        Returns:
            Configured httpx.Client for OIC API requests.

        """
        if not self._client:
            connection = self.settings.connection
            if connection is None:
                msg = "Connection settings not configured"
                raise ValueError(msg)
            self._client = httpx.Client(
                base_url=connection.base_url,
                headers=self._get_auth_headers(),
                timeout=self.settings.performance.request_timeout,
            )
        return self._client

    def _get_auth_headers(self) -> dict[str, str]:
        if not self._access_token:
            self._refresh_token()
        return {
            "Authorization": f"Bearer {self._access_token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        reraise=True,
    )
    def _refresh_token(self) -> None:
        try:
            with httpx.Client() as client:
                auth_config = self.settings.get_auth_config()
                response = client.post(
                    auth_config["oauth_token_url"],
                    data={
                        "grant_type": "client_credentials",
                        "client_id": auth_config["oauth_client_id"],
                        "client_secret": auth_config["oauth_client_secret"],
                        "scope": auth_config["oauth_scope"],
                    },
                    timeout=self.settings.performance.request_timeout,
                )
                response.raise_for_status()
                token_data = response.json()
                self._access_token = token_data["access_token"]
                logger.info("OAuth2 token refreshed successfully")
        except Exception:
            logger.exception("Failed to refresh OAuth2 token")
            raise

    def activate_integration(
        self,
        integration_id: str,
        version: str = "01.00.0000",
    ) -> FlextMeltanoResult[Any]:
        """Activate an integration in Oracle Integration Cloud.

        Args:
            integration_id: Unique identifier of the integration.
            version: Version of the integration (default: '01.00.0000').

        Returns:
            FlextMeltanoResult containing operation result with status and details.

        """
        identifier = IntegrationIdentifier(
            integration_id=integration_id,
            version=version,
        )

        logger.info("Activating integration", integration=str(identifier))

        try:
            # Validate integration before activation if enabled:
            if self.settings.lifecycle.validate_before_activate:
                validation_result = self.validate_integration(integration_id, version)
                if validation_result.is_failure:
                    return FlextMeltanoResult.fail(
                        f"Integration validation failed: {validation_result.error}",
                    )

            # Perform activation
            response = self.client.post(
                f"/ic/api/integration/v1/integrations/{identifier}/activate",
                timeout=self.settings.lifecycle.activation_timeout,
            )

            if response.status_code == HTTP_OK:
                result = LifecycleOperationResult(
                    integration_id=integration_id,
                    version=version,
                    operation="activate",
                    success=True,
                    message="Integration activated successfully",
                    details=response.json(),
                )
                logger.info(
                    "Integration activated successfully",
                    integration=str(identifier),
                )
                return FlextMeltanoResult.ok(result)
            error_message = f"Failed to activate integration {identifier}"
            logger.error(
                "%s - status_code: %d, response: %s",
                error_message,
                response.status_code,
                response.text,
            )
            return FlextMeltanoResult.fail(error_message)

        except Exception as e:
            error_message = f"Exception during activation of {identifier}: {e}"
            logger.exception(error_message)
            return FlextMeltanoResult.fail(error_message)

    def deactivate_integration(
        self,
        integration_id: str,
        version: str = "01.00.0000",
    ) -> FlextMeltanoResult[Any]:
        """Deactivate an integration in Oracle Integration Cloud.

        Args:
            integration_id: Unique identifier of the integration.
            version: Version of the integration (default: '01.00.0000').

        Returns:
            FlextMeltanoResult containing operation result with status and details.

        """
        identifier = IntegrationIdentifier(
            integration_id=integration_id,
            version=version,
        )

        logger.info("Deactivating integration", integration=str(identifier))

        try:
            response = self.client.post(
                f"/ic/api/integration/v1/integrations/{identifier}/deactivate",
                timeout=self.settings.lifecycle.activation_timeout,
            )

            if response.status_code == HTTP_OK:
                result = LifecycleOperationResult(
                    integration_id=integration_id,
                    version=version,
                    operation="deactivate",
                    success=True,
                    message="Integration deactivated successfully",
                    details=response.json(),
                )
                logger.info(
                    "Integration deactivated successfully",
                    integration=str(identifier),
                )
                return FlextMeltanoResult.ok(result)
            error_message = f"Failed to deactivate integration {identifier}"
            logger.error(
                "%s - status_code: %d, response: %s",
                error_message,
                response.status_code,
                response.text,
            )
            return FlextMeltanoResult.fail(error_message)

        except Exception as e:
            error_message = f"Exception during deactivation of {identifier}: {e}"
            logger.exception(error_message)
            return FlextMeltanoResult.fail(error_message)

    def get_integration_status(
        self,
        integration_id: str,
        version: str = "01.00.0000",
    ) -> FlextMeltanoResult[Any]:
        """Get current status of an integration.

        Args:
            integration_id: Unique identifier of the integration.
            version: Version of the integration (default: '01.00.0000').

        Returns:
            FlextMeltanoResult containing current integration status information.

        """
        identifier = IntegrationIdentifier(
            integration_id=integration_id,
            version=version,
        )

        try:
            response = self.client.get(
                f"/ic/api/integration/v1/integrations/{identifier}",
                timeout=self.settings.performance.request_timeout,
            )

            if response.status_code == HTTP_OK:
                data = response.json()
                status = IntegrationStatus(
                    integration_id=integration_id,
                    version=version,
                    status=data.get("status", "UNKNOWN"),
                    message=data.get("message"),
                    last_updated=data.get("lastUpdated"),
                )
                return FlextMeltanoResult.ok(status)
            error_message = f"Failed to get integration status for {identifier}"
            logger.error(
                "%s - status_code: %d, response: %s",
                error_message,
                response.status_code,
                response.text,
            )
            return FlextMeltanoResult.fail(error_message)

        except Exception as e:
            error_message = f"Exception getting status for {identifier}: {e}"
            logger.exception(error_message)
            return FlextMeltanoResult.fail(error_message)

    def bulk_activate(
        self,
        integration_list: list[dict[str, str]],
    ) -> FlextMeltanoResult[Any]:
        """Activate multiple integrations in batch.

        Args:
            integration_list: List of integration dictionaries with 'id' and optional 'version'.

        Returns:
            FlextMeltanoResult containing bulk operation results with success/failure counts.

        """
        logger.info("Starting bulk activation", count=len(integration_list))

        successful_integrations: list[str] = []
        failed_integrations: list[dict[str, Any]] = []

        for integration in integration_list:
            integration_id = integration["id"]
            version = integration.get("version", "01.00.0000")
            identifier = f"{integration_id}|{version}"

            result = self.activate_integration(integration_id, version)
            if result.success:
                successful_integrations.append(identifier)
            else:
                failed_integrations.append(
                    {
                        "integration": identifier,
                        "error": str(result.error) if result.error else "Unknown error",
                        "error_type": "ActivationError",
                    },
                )

        bulk_result = BulkOperationResult(
            total_count=len(integration_list),
            success_count=len(successful_integrations),
            failure_count=len(failed_integrations),
            successful_integrations=successful_integrations,
            failed_integrations=failed_integrations,
        )

        logger.info(
            "Bulk activation completed - total: %d, success: %d, failed: %d",
            bulk_result.total_count,
            bulk_result.success_count,
            bulk_result.failure_count,
        )

        return FlextMeltanoResult.ok(bulk_result)

    def bulk_deactivate(
        self,
        integration_list: list[dict[str, str]],
    ) -> FlextMeltanoResult[Any]:
        """Deactivate multiple integrations in batch.

        Args:
            integration_list: List of integration dictionaries with 'id' and optional 'version'.

        Returns:
            FlextMeltanoResult containing bulk operation results with success/failure counts.

        """
        logger.info("Starting bulk deactivation", count=len(integration_list))

        successful_integrations: list[str] = []
        failed_integrations: list[dict[str, Any]] = []

        for integration in integration_list:
            integration_id = integration["id"]
            version = integration.get("version", "01.00.0000")
            identifier = f"{integration_id}|{version}"

            result = self.deactivate_integration(integration_id, version)
            if result.success:
                successful_integrations.append(identifier)
            else:
                failed_integrations.append(
                    {
                        "integration": identifier,
                        "error": str(result.error) if result.error else "Unknown error",
                        "error_type": "ActivationError",
                    },
                )

        bulk_result = BulkOperationResult(
            total_count=len(integration_list),
            success_count=len(successful_integrations),
            failure_count=len(failed_integrations),
            successful_integrations=successful_integrations,
            failed_integrations=failed_integrations,
        )

        logger.info(
            "Bulk deactivation completed - total: %d, success: %d, failed: %d",
            bulk_result.total_count,
            bulk_result.success_count,
            bulk_result.failure_count,
        )

        return FlextMeltanoResult.ok(bulk_result)

    def validate_integration(
        self,
        integration_id: str,
        version: str = "01.00.0000",
    ) -> FlextMeltanoResult[Any]:
        """Validate an integration configuration.

        Args:
            integration_id: Unique identifier of the integration.
            version: Version of the integration (default: '01.00.0000').

        Returns:
            FlextMeltanoResult containing validation results and any errors found.

        """
        identifier = IntegrationIdentifier(
            integration_id=integration_id,
            version=version,
        )

        logger.info("Validating integration %s", identifier)

        try:
            response = self.client.post(
                f"/ic/api/integration/v1/integrations/{identifier}/validate",
                timeout=self.settings.performance.request_timeout,
            )

            if response.status_code == HTTP_OK:
                validation_result = response.json()
                is_valid = validation_result.get("valid", False)

                if is_valid:
                    logger.info(
                        "Integration validation successful for %s",
                        str(identifier),
                    )
                else:
                    logger.warning(
                        "Integration validation failed for %s with issues: %s",
                        str(identifier),
                        validation_result.get("issues", []),
                    )

                return FlextMeltanoResult.ok(validation_result)
            error_message = f"Failed to validate integration {identifier}"
            logger.error(
                "%s - status_code: %d, response: %s",
                error_message,
                response.status_code,
                response.text,
            )
            return FlextMeltanoResult.fail(error_message)

        except Exception as e:
            error_message = f"Exception during validation of {identifier}: {e}"
            logger.exception(error_message)
            return FlextMeltanoResult.fail(error_message)

    def __del__(self) -> None:
        """Clean up HTTP client resources."""
        if self._client:
            self._client.close()
