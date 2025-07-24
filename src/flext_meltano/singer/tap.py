"""FlextMeltano Singer Tap Integration.

Singer tap implementation following Clean Architecture patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult
from pydantic import BaseModel, Field

from flext_meltano.constants import (
    FlextMeltanoConstants,
)
from flext_meltano.helpers.cli import flext_run_singer_command

if TYPE_CHECKING:
    from pathlib import Path


class FlextMeltanoTap(BaseModel):
    """Singer tap integration.

    Represents a Singer tap with configuration and execution capabilities
    following Clean Architecture patterns.
    """

    # Core identification
    name: str = Field(
        ...,
        description="Tap name",
        min_length=1,
        max_length=100,
    )
    executable: str = Field(
        ...,
        description="Tap executable command",
        min_length=1,
    )

    # Configuration
    config_file: Path | None = Field(
        default=None,
        description="Path to tap configuration file",
    )
    catalog_file: Path | None = Field(
        default=None,
        description="Path to Singer catalog file",
    )
    state_file: Path | None = Field(
        default=None,
        description="Path to state file for incremental extraction",
    )

    # Execution settings
    timeout: int = Field(
        default=FlextMeltanoConstants.SINGER_TIMEOUT_DEFAULT,
        description="Tap execution timeout in seconds",
        gt=0,
    )
    batch_size: int = Field(
        default=FlextMeltanoConstants.SINGER_BATCH_SIZE_DEFAULT,
        description="Batch size for record processing",
        gt=0,
    )

    # Runtime information
    version: str | None = Field(
        default=None,
        description="Tap version",
    )
    description: str | None = Field(
        default=None,
        description="Tap description",
        max_length=500,
    )

    class Config:
        """Pydantic model configuration."""

        frozen = False
        validate_assignment = True
        extra = "forbid"

    def validate_configuration(self) -> FlextResult[dict[str, Any]]:
        """Validate tap configuration and requirements.

        Returns:
            FlextResult with validation results

        """
        try:
            validation_results: dict[str, Any] = {
                "tap_valid": True,
                "config_exists": True,
                "catalog_exists": True,
                "executable_valid": True,
                "issues": [],
            }

            # Check configuration file
            if self.config_file and not self.config_file.exists():
                validation_results["config_exists"] = False
                validation_results["tap_valid"] = False
                validation_results["issues"].append(
                    f"Configuration file not found: {self.config_file}",
                )

            # Check catalog file
            if self.catalog_file and not self.catalog_file.exists():
                validation_results["catalog_exists"] = False
                validation_results["tap_valid"] = False
                validation_results["issues"].append(
                    f"Catalog file not found: {self.catalog_file}",
                )

            # Validate executable name
            if not FlextMeltanoConstants.is_valid_plugin_name(self.executable):
                validation_results["executable_valid"] = False
                validation_results["tap_valid"] = False
                validation_results["issues"].append(
                    f"Invalid executable name: {self.executable}",
                )

            return FlextResult.ok(validation_results)

        except Exception as e:
            return FlextResult.fail(f"Tap validation failed: {e}")

    def discover_schema(self) -> FlextResult[dict[str, Any]]:
        """Discover tap schema using Singer discovery mode.

        Returns:
            FlextResult with discovered schema catalog

        """
        try:
            # Build discovery command
            command = [self.executable, "--discover"]

            # Execute discovery
            result = flext_run_singer_command(
                tap_command=command,
                config_file=self.config_file,
            )

            if not result.is_success:
                return FlextResult.fail(f"Schema discovery failed: {result.error}")

            # Parse discovery output
            if result.data is None:
                return FlextResult.fail("No discovery data returned")
            discovery_output = result.data.get("tap_stdout", "")

            try:
                import json

                catalog_data = json.loads(discovery_output)
                return FlextResult.ok(catalog_data)
            except json.JSONDecodeError as e:
                return FlextResult.fail(f"Failed to parse discovery output: {e}")

        except Exception as e:
            return FlextResult.fail(f"Schema discovery failed: {e}")

    def extract_data(
        self,
        target_command: list[str] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Extract data using Singer tap.

        Args:
            target_command: Optional target command for direct piping

        Returns:
            FlextResult with extraction results

        """
        try:
            # Validate configuration before extraction
            validation_result = self.validate_configuration()
            if not validation_result.is_success:
                return FlextResult.fail("Tap configuration invalid")

            # Build extraction command
            command = [self.executable]

            # Execute extraction
            result = flext_run_singer_command(
                tap_command=command,
                target_command=target_command,
                config_file=self.config_file,
                catalog_file=self.catalog_file,
                state_file=self.state_file,
            )

            if not result.is_success:
                return FlextResult.fail(f"Data extraction failed: {result.error}")

            if result.data is None:
                return FlextResult.fail("No extraction data returned")
            return FlextResult.ok(result.data)

        except Exception as e:
            return FlextResult.fail(f"Data extraction failed: {e}")

    def test_connection(self) -> FlextResult[dict[str, Any]]:
        """Test tap connection and configuration.

        Returns:
            FlextResult with connection test results

        """
        try:
            # Build test command (tap with limited records)
            command = [self.executable, "--config", str(self.config_file)]

            if self.catalog_file:
                command.extend(["--catalog", str(self.catalog_file)])

            # Execute with timeout
            result = flext_run_singer_command(
                tap_command=command,
                config_file=self.config_file,
                catalog_file=self.catalog_file,
            )

            test_results = {
                "connection_successful": result.is_success,
                "tap_output": result.data if result.is_success else None,
                "error_message": result.error if not result.is_success else None,
            }

            return FlextResult.ok(test_results)

        except Exception as e:
            return FlextResult.fail(f"Connection test failed: {e}")

    def get_info(self) -> FlextResult[dict[str, Any]]:
        """Get tap information and capabilities.

        Returns:
            FlextResult with tap information

        """
        try:
            # Try to get tap version and info
            version_result = flext_run_singer_command(
                tap_command=[self.executable, "--version"],
            )

            info_data = {
                "name": self.name,
                "executable": self.executable,
                "version": (
                    version_result.data.get("tap_stdout", "").strip()
                    if version_result.is_success and version_result.data
                    else self.version
                ),
                "description": self.description,
                "timeout": self.timeout,
                "batch_size": self.batch_size,
                "configuration": {
                    "config_file": str(self.config_file) if self.config_file else None,
                    "catalog_file": (
                        str(self.catalog_file) if self.catalog_file else None
                    ),
                    "state_file": str(self.state_file) if self.state_file else None,
                },
            }

            return FlextResult.ok(info_data)

        except Exception as e:
            return FlextResult.fail(f"Failed to get tap info: {e}")

    def update_state(self, new_state: dict[str, Any]) -> FlextResult[None]:
        """Update tap state file.

        Args:
            new_state: New state data to save

        Returns:
            FlextResult indicating success or failure

        """
        try:
            if not self.state_file:
                return FlextResult.fail("No state file configured for tap")

            import json

            # Write state to file
            self.state_file.write_text(
                json.dumps(new_state, indent=2),
                encoding="utf-8",
            )

            return FlextResult.ok(None)

        except Exception as e:
            return FlextResult.fail(f"Failed to update state: {e}")

    def to_dict(self) -> dict[str, Any]:
        """Convert tap to dictionary representation.

        Returns:
            Dictionary representation of the tap

        """
        return {
            "name": self.name,
            "executable": self.executable,
            "config_file": str(self.config_file) if self.config_file else None,
            "catalog_file": str(self.catalog_file) if self.catalog_file else None,
            "state_file": str(self.state_file) if self.state_file else None,
            "timeout": self.timeout,
            "batch_size": self.batch_size,
            "version": self.version,
            "description": self.description,
        }
