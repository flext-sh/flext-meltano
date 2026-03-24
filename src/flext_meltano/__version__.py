"""Package version and metadata information.

Provides version information and package metadata using standard library
metadata extraction.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import PackageMetadata, PackageNotFoundError, metadata

try:
    _metadata: PackageMetadata | t.StrMapping = metadata("flext_meltano")
except PackageNotFoundError:
    _metadata = {
        "Version": "0.0.0.dev0",
        "Name": "flext_meltano",
        "Summary": "FLEXT Meltano - Enterprise Data Integration Platform",
        "Author": "FLEXT Team",
        "Author-Email": "team@flext.sh",
        "License": "MIT",
        "Home-Page": "https://github.com/flext-sh/flext",
    }
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
