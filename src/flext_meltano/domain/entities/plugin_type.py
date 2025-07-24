"""PluginType enum for Meltano domain."""

from __future__ import annotations

from enum import StrEnum


class FlextMeltanoPluginType(StrEnum):
    """Meltano plugin types."""

    EXTRACTOR = "extractors"
    LOADER = "loaders"
    TRANSFORMER = "transformers"
    ORCHESTRATOR = "orchestrators"
    UTILITY = "utilities"
    FILE = "files"
