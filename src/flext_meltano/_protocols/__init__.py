# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Protocols package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextMeltanoProtocolsBase": ".cli",
    "FlextMeltanoProtocolsPlugin": ".plugin",
    "FlextMeltanoProtocolsProject": ".project",
    "FlextMeltanoProtocolsServices": ".services",
    "FlextMeltanoProtocolsSinger": ".singer",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
