# AUTO-GENERATED FILE — Regenerate with: make gen
"""Package version and metadata for flext-meltano.

Subclass of ``FlextVersion`` — overrides only ``_metadata``.
All derived attributes (``__version__``, ``__title__``, etc.) are
computed automatically via ``FlextVersion.__init_subclass__``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import PackageMetadata, metadata

from flext_core import FlextVersion


class FlextMeltanoVersion(FlextVersion):
    """flext-meltano version — MRO-derived from FlextVersion."""

    _metadata: PackageMetadata = metadata("flext-meltano")


__version__ = FlextMeltanoVersion.__version__
__version_info__ = FlextMeltanoVersion.__version_info__
__title__ = FlextMeltanoVersion.__title__
__description__ = FlextMeltanoVersion.__description__
__author__ = FlextMeltanoVersion.__author__
__author_email__ = FlextMeltanoVersion.__author_email__
__license__ = FlextMeltanoVersion.__license__
__url__ = FlextMeltanoVersion.__url__
__all__: list[str] = [
    "FlextMeltanoVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
]
