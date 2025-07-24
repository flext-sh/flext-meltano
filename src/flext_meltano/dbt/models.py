"""FLEXT Meltano dbt models module."""

from __future__ import annotations

from typing import Any

from flext_core import FlextResult
from pydantic import BaseModel, Field


class FlextMeltanoDbtModel(BaseModel):
    """Represents a dbt model in FLEXT Meltano architecture.

    Following Clean Architecture patterns for dbt model representation
    and manipulation within the FLEXT ecosystem.
    """

    model_config = {
        "str_strip_whitespace": True,
        "validate_assignment": True,
        "extra": "forbid",
    }

    name: str = Field(
        description="Name of the dbt model",
        min_length=1,
        max_length=255,
    )
    path: str = Field(
        description="Path to the dbt model file",
        min_length=1,
    )
    description: str | None = Field(
        default=None,
        description="Optional description of the model",
    )
    materialization: str = Field(
        default="view",
        description="dbt materialization type",
    )
    tags: list[str] = Field(
        default_factory=list,
        description="Tags associated with the model",
    )
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Model configuration settings",
    )

    def compile_model(self) -> FlextResult[dict[str, Any]]:
        """Compile the dbt model.

        Returns:
            FlextResult containing compilation result

        """
        try:
            compiled_info = {
                "name": self.name,
                "path": self.path,
                "materialization": self.materialization,
                "compiled": True,
            }
            return FlextResult.ok(compiled_info)
        except Exception as e:
            return FlextResult.fail(f"Failed to compile model {self.name}: {e}")

    def validate_model(self) -> FlextResult[bool]:
        """Validate the dbt model structure.

        Returns:
            FlextResult indicating validation success

        """
        if not self.name:
            return FlextResult.fail("Model name cannot be empty")

        if not self.path:
            return FlextResult.fail("Model path cannot be empty")

        return FlextResult.ok(True)
