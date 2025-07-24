"""FlextMeltano Singer Target Integration.

Singer target implementation following Clean Architecture patterns.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextResult
from pydantic import BaseModel, Field

from flext_meltano.constants import FlextMeltanoConstants
from flext_meltano.helpers.cli import flext_run_singer_command

if TYPE_CHECKING:
    from pathlib import Path


class FlextMeltanoTarget(BaseModel):
    """Singer target integration.

    Represents a Singer target with configuration and execution capabilities
    following Clean Architecture patterns.
    """

    # Core identification
    name: str = Field(
        ...,
        description="Target name",
        min_length=1,
        max_length=100,
    )
    executable: str = Field(
        ...,
        description="Target executable command",
        min_length=1,
    )

    # Configuration
    config_file: Path | None = Field(
        default=None,
        description="Path to target configuration file",
    )

    # Execution settings
    timeout: int = Field(
        default=FlextMeltanoConstants.SINGER_TIMEOUT_DEFAULT,
        description="Target execution timeout in seconds",
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
        description="Target version",
    )
    description: str | None = Field(
        default=None,
        description="Target description",
        max_length=500,
    )

    class Config:
        """Pydantic model configuration."""

        frozen = False
        validate_assignment = True
        extra = "forbid"

    def validate_configuration(self) -> FlextResult[dict[str, Any]]:
        """Validate target configuration and requirements.

        Returns:
            FlextResult with validation results

        """
        try:
            validation_results: dict[str, Any] = {
                "target_valid": True,
                "config_exists": True,
                "executable_valid": True,
                "issues": [],
            }

            # Check configuration file
            if self.config_file and not self.config_file.exists():
                validation_results["config_exists"] = False
                validation_results["target_valid"] = False
                validation_results["issues"].append(
                    f"Configuration file not found: {self.config_file}",
                )

            # Validate executable name
            if not FlextMeltanoConstants.is_valid_plugin_name(self.executable):
                validation_results["executable_valid"] = False
                validation_results["target_valid"] = False
                validation_results["issues"].append(
                    f"Invalid executable name: {self.executable}",
                )

            return FlextResult.ok(validation_results)

        except Exception as e:
            return FlextResult.fail(f"Target validation failed: {e}")

    def load_data(
        self,
        input_data: str | None = None,
        tap_command: list[str] | None = None,
    ) -> FlextResult[dict[str, Any]]:
        """Load data using Singer target.

        Args:
            input_data: Raw Singer messages to load
            tap_command: Optional tap command for direct piping

        Returns:
            FlextResult with loading results

        """
        try:
            # Validate configuration before loading
            validation_result = self.validate_configuration()
            if not validation_result.is_success:
                return FlextResult.fail("Target configuration invalid")

            # Build target command
            command = [self.executable]

            if tap_command:
                # Execute tap | target pipeline
                result = flext_run_singer_command(
                    tap_command=tap_command,
                    target_command=command,
                    config_file=self.config_file,
                )
            else:
                # Execute target only with input data
                if not input_data:
                    return FlextResult.fail(
                        "Either input_data or tap_command must be provided",
                    )

                # TODO: Implement direct input data loading
                return FlextResult.fail("Direct input data loading not yet implemented")

            if not result.is_success:
                return FlextResult.fail(f"Data loading failed: {result.error}")

            return FlextResult.ok(result.data or {})

        except Exception as e:
            return FlextResult.fail(f"Data loading failed: {e}")

    def test_connection(self) -> FlextResult[dict[str, Any]]:
        """Test target connection and configuration.

        Returns:
            FlextResult with connection test results

        """
        try:
            # Build test command
            command = [self.executable, "--config", str(self.config_file)]

            # Execute with test data (empty catalog)

            # Create temporary test input
            import json
            import tempfile

            with tempfile.NamedTemporaryFile(
                mode="w", suffix=".json", delete=False,
            ) as f:
                # Write minimal test schema message
                test_message = {
                    "type": "SCHEMA",
                    "stream": "test_stream",
                    "schema": {"type": "object", "properties": {}},
                    "key_properties": [],
                }
                f.write(json.dumps(test_message) + "\n")
                temp_file = f.name

            try:
                # Execute target with test input
                result = flext_run_singer_command(
                    tap_command=["cat", temp_file],
                    target_command=command,
                    config_file=self.config_file,
                )

                test_results = {
                    "connection_successful": result.is_success,
                    "target_output": result.data if result.is_success else None,
                    "error_message": result.error if not result.is_success else None,
                }

                return FlextResult.ok(test_results)

            finally:
                # Clean up temporary file
                from pathlib import Path

                Path(temp_file).unlink()

        except Exception as e:
            return FlextResult.fail(f"Connection test failed: {e}")

    def get_info(self) -> FlextResult[dict[str, Any]]:
        """Get target information and capabilities.

        Returns:
            FlextResult with target information

        """
        try:
            # Try to get target version and info
            version_result = flext_run_singer_command(
                tap_command=[self.executable, "--version"],
            )

            info_data = {
                "name": self.name,
                "executable": self.executable,
                "version": (
                    (version_result.data or {}).get("tap_stdout", "").strip()
                    if version_result.is_success and version_result.data
                    else self.version
                ),
                "description": self.description,
                "timeout": self.timeout,
                "batch_size": self.batch_size,
                "configuration": {
                    "config_file": str(self.config_file) if self.config_file else None,
                },
            }

            return FlextResult.ok(info_data)

        except Exception as e:
            return FlextResult.fail(f"Failed to get target info: {e}")

    def validate_schema(
        self, schema_data: dict[str, Any],
    ) -> FlextResult[dict[str, Any]]:
        """Validate schema against target capabilities.

        Args:
            schema_data: Schema data to validate

        Returns:
            FlextResult with validation results

        """
        try:
            validation_results: dict[str, Any] = {
                "schema_valid": True,
                "supported_types": [],
                "unsupported_types": [],
                "issues": [],
            }

            # Extract schema properties
            if "streams" in schema_data:
                for stream in schema_data["streams"]:
                    if "schema" in stream and "properties" in stream["schema"]:
                        for prop_name, prop_def in stream["schema"][
                            "properties"
                        ].items():
                            prop_type = prop_def.get("type", "unknown")

                            # Basic type support validation
                            supported_types = {
                                "string",
                                "integer",
                                "number",
                                "boolean",
                                "array",
                                "object",
                                "null",
                            }

                            supported_list: list[str] = validation_results[
                                "supported_types"
                            ]
                            unsupported_list: list[str] = validation_results[
                                "unsupported_types"
                            ]
                            issues_list: list[str] = validation_results["issues"]

                            if prop_type in supported_types:
                                if prop_type not in supported_list:
                                    supported_list.append(prop_type)
                            elif prop_type not in unsupported_list:
                                unsupported_list.append(prop_type)
                                issues_list.append(
                                    f"Unsupported type '{prop_type}' in property '{prop_name}'",
                                )

            if validation_results["unsupported_types"]:
                validation_results["schema_valid"] = False

            return FlextResult.ok(validation_results)

        except Exception as e:
            return FlextResult.fail(f"Schema validation failed: {e}")

    def to_dict(self) -> dict[str, Any]:
        """Convert target to dictionary representation.

        Returns:
            Dictionary representation of the target

        """
        return {
            "name": self.name,
            "executable": self.executable,
            "config_file": str(self.config_file) if self.config_file else None,
            "timeout": self.timeout,
            "batch_size": self.batch_size,
            "version": self.version,
            "description": self.description,
        }
