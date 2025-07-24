"""FLEXT Meltano Plugin Models.

Plugin models following Clean Architecture patterns.
"""

from __future__ import annotations

from typing import Any

from pydantic import Field

from flext_meltano.infrastructure.di_container import FlextMeltanoDomainEntity


class FlextMeltanoPlugin(FlextMeltanoDomainEntity):
    """Meltano plugin model with enterprise patterns."""

    name: str = Field(description="Plugin name")
    plugin_type: str = Field(description="Plugin type (extractor, loader, etc.)")
    namespace: str | None = Field(None, description="Plugin namespace")
    pip_url: str | None = Field(None, description="Python package URL")
    executable: str | None = Field(None, description="Executable command")
    config: dict[str, Any] = Field(
        default_factory=dict,
        description="Plugin configuration",
    )
    settings: list[dict[str, Any]] = Field(
        default_factory=list,
        description="Plugin settings",
    )
    variant: str | None = Field(None, description="Plugin variant")
    docs: str | None = Field(None, description="Documentation URL")
    description: str | None = Field(None, description="Plugin description")
    version: str | None = Field(None, description="Plugin version")
    installed: bool = Field(False, description="Whether plugin is installed")

    def is_extractor(self) -> bool:
        """Check if this is an extractor plugin."""
        return self.plugin_type == "extractors"

    def is_loader(self) -> bool:
        """Check if this is a loader plugin."""
        return self.plugin_type == "loaders"

    def is_transformer(self) -> bool:
        """Check if this is a transformer plugin."""
        return self.plugin_type == "transformers"

    def get_install_command(self) -> list[str]:
        """Get the command to install this plugin."""
        cmd = ["meltano", "add", self.plugin_type, self.name]
        if self.variant:
            cmd.extend(["--variant", self.variant])
        return cmd
