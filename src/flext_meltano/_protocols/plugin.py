"""FLEXT Meltano Protocols - Plugin and Stream protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Protocol, runtime_checkable

from flext_meltano import t


class FlextMeltanoProtocolsPlugin:
    """Plugin and Stream protocol definitions."""

    @runtime_checkable
    class Plugin(Protocol):
        """Meltano plugin interface with covariant return type."""

        name: str
        default_variant: str | None
        variants: t.ConfigurationMapping | None

        def execute(self, *args: t.Scalar, **kwargs: t.Scalar) -> t.Container:
            """Execute plugin with given arguments. # INTERFACE."""
            ...

        def get_config(self) -> t.ConfigurationMapping:
            """Get plugin configuration."""
            ...

        def validate_config(self, config: t.ConfigurationMapping) -> bool:
            """Validate plugin configuration. # INTERFACE."""
            ...

    @runtime_checkable
    class Stream(Protocol):
        """Singer stream interface with type safety."""

        name: str
        tap_stream_id: str
        schema: t.FlatContainerMapping

        def get_records(self) -> Sequence[t.FlatContainerMapping]:
            """Get records from the stream. # INTERFACE."""
            ...

        def sync_records(self) -> Sequence[t.FlatContainerMapping]:
            """Sync records from the stream. # INTERFACE."""
            ...
