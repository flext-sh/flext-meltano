"""FLEXT Meltano Protocols - Project, Adapter, and IndexedPlugin protocols.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path
from typing import Protocol, runtime_checkable

from flext_cli import p

from flext_meltano import t


class FlextMeltanoProtocolsProject:
    """Project, Adapter, and IndexedPlugin protocol definitions."""

    @runtime_checkable
    class Project(Protocol):
        """Meltano Project protocol for type-safe project operations.

        Represents the interface for a Meltano project value that can be
        passed to plugin discovery, pipeline execution, and other operations.
        """

        @property
        def root_dir(self) -> Path:
            """Project root directory."""
            ...

        def find_plugins(
            self, plugin_type: str
        ) -> Sequence[t.Meltano.PluginDefinition]:
            """Find plugins of specified type."""
            ...

    @runtime_checkable
    class DbtConnectionProfile(Protocol):
        """Canonical dbt connection profile surface.

        Consumer DBT projects expose a typed model (``m.<Ns>.DbtConnectionProfile``)
        satisfying this protocol rather than passing raw dictionaries.
        """

        @property
        def type(self) -> str:
            """DBT adapter type."""
            ...

        @property
        def project(self) -> str:
            """DBT project name."""
            ...

        def model_dump(self, *, mode: str = ...) -> t.JsonMapping:
            """Serialize the profile to a JSON-safe mapping."""
            ...

    @runtime_checkable
    class Adapter(Protocol):
        """Protocol for data adapters (tap/target/sink adapters).

        Represents the interface for adapters used in data extraction,
        loading, and transformation operations.
        """

        @property
        def is_connected(self) -> bool:
            """Check if adapter is currently connected."""
            ...

        def connect(self) -> p.Result[bool]:
            """Establish connection to the data source/sink."""
            ...

        def disconnect(self) -> p.Result[bool]:
            """Close connection to the data source/sink."""
            ...

    @runtime_checkable
    class IndexedPlugin(Protocol):
        """Protocol for indexed plugin objects used in plugin discovery.

        Represents plugin metadata accessed via u.get() for attributes
        like variants, default_variant, logo_url.
        """

        @property
        def default_variant(self) -> str | None:
            """Default variant name."""
            ...

        @property
        def logo_url(self) -> str | None:
            """Plugin logo URL."""
            ...

        @property
        def name(self) -> str:
            """Plugin name."""
            ...

        @property
        def variants(self) -> t.ConfigurationMapping | None:
            """Available variants."""
            ...
