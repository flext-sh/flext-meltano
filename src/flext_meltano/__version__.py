"""Package version and metadata information.

Provides version information and package metadata using standard library
metadata extraction.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import PackageMetadata, metadata

from flext_core import t

_metadata: PackageMetadata | t.StrMapping = metadata("flext_meltano")
__version__ = _metadata["Version"]
__version_info__ = tuple(
    int(part) if part.isdigit() else part for part in __version__.split(".")
)
__title__ = _metadata["Name"]
__description__ = _metadata["Summary"]
__author__ = _metadata["Author"]
__author_email__ = _metadata["Author-Email"]
__license__ = _metadata.get("License", "")
__url__ = _metadata.get("Home-Page", "")
__all__ = [
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
]
