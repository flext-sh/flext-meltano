# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

TESTS_FLEXT_MELTANO_LAZY_IMPORTS_PART_02 = build_lazy_import_map(
    {
        ".base": ("s",),
        ".models": ("m",),
        ".protocols": ("p",),
        ".typings": ("t",),
        ".unit": ("unit",),
        ".utilities": ("u",),
        "flext_tests": (
            "r",
            "td",
            "tf",
            "tk",
            "tm",
            "tv",
            "x",
        ),
    },
)

__all__: list[str] = ["TESTS_FLEXT_MELTANO_LAZY_IMPORTS_PART_02"]
