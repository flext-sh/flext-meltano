# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_MELTANO_LAZY_IMPORTS_PART_02 = build_lazy_import_map(
    {
        "._constants": ("_constants",),
        "._models": ("_models",),
        "._protocols": ("_protocols",),
        "._typings": ("_typings",),
        "._utilities": ("_utilities",),
        ".api": ("meltano",),
        ".base": ("s",),
        ".cli": (
            "main",
        ),
        ".constants": ("c",),
        ".models": ("m",),
        ".protocols": ("p",),
        ".services": ("services",),
        ".services.singer_sdk": (
            "Sink",
            "Stream",
            "Tap",
            "Target",
        ),
        ".services.validators": ("FlextMeltanoValidators",),
        ".typings": (
            "FlextMeltanoTypes",
            "t",
        ),
        ".utilities": (
            "FlextMeltanoUtilities",
            "u",
        ),
        "flext_core": (
            "d",
            "e",
            "h",
            "r",
            "x",
        ),
    },
)

__all__: list[str] = ["FLEXT_MELTANO_LAZY_IMPORTS_PART_02"]
