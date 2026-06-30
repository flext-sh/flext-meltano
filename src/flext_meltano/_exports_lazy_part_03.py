# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_MELTANO_LAZY_IMPORTS_PART_03 = build_lazy_import_map(
    {
        "._utilities.singer": ("FlextMeltanoUtilitiesSinger",),
        ".api": ("meltano",),
        ".base": ("s",),
        ".cli": (
            "cli",
            "main",
        ),
        ".constants": ("c",),
        ".models": ("m",),
        ".protocols": ("p",),
        ".services": ("services",),
        ".services.singer_sdk": (
            "Record",
            "Sink",
            "Stream",
            "Tap",
            "Target",
        ),
        ".services.validators": ("FlextMeltanoValidators",),
        ".typings": ("t",),
        ".utilities": ("u",),
    },
)

__all__: list[str] = ["FLEXT_MELTANO_LAZY_IMPORTS_PART_03"]
