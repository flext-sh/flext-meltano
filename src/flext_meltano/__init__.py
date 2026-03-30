# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext meltano package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_meltano._constants import _LAZY_IMPORTS as _CHILD_LAZY_0
from flext_meltano._models import _LAZY_IMPORTS as _CHILD_LAZY_1
from flext_meltano._protocols import _LAZY_IMPORTS as _CHILD_LAZY_2
from flext_meltano._typings import _LAZY_IMPORTS as _CHILD_LAZY_3
from flext_meltano._utilities import _LAZY_IMPORTS as _CHILD_LAZY_4
from flext_meltano.dbt import _LAZY_IMPORTS as _CHILD_LAZY_5
from flext_meltano.meltano import _LAZY_IMPORTS as _CHILD_LAZY_6
from flext_meltano.services import _LAZY_IMPORTS as _CHILD_LAZY_7
from flext_meltano.singer import _LAZY_IMPORTS as _CHILD_LAZY_8

if TYPE_CHECKING:
    from flext_meltano.__version__ import *
    from flext_meltano._constants import *
    from flext_meltano._models import *
    from flext_meltano._protocols import *
    from flext_meltano._typings import *
    from flext_meltano._utilities import *
    from flext_meltano.api import *
    from flext_meltano.base import *
    from flext_meltano.cli import *
    from flext_meltano.constants import *
    from flext_meltano.dbt import *
    from flext_meltano.meltano import *
    from flext_meltano.models import *
    from flext_meltano.protocols import *
    from flext_meltano.services import *
    from flext_meltano.settings import *
    from flext_meltano.singer import *
    from flext_meltano.typings import *
    from flext_meltano.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    **_CHILD_LAZY_0,
    **_CHILD_LAZY_1,
    **_CHILD_LAZY_2,
    **_CHILD_LAZY_3,
    **_CHILD_LAZY_4,
    **_CHILD_LAZY_5,
    **_CHILD_LAZY_6,
    **_CHILD_LAZY_7,
    **_CHILD_LAZY_8,
    "FlextMeltano": "flext_meltano.api",
    "FlextMeltanoCLI": "flext_meltano.cli",
    "FlextMeltanoConstants": "flext_meltano.constants",
    "FlextMeltanoModels": "flext_meltano.models",
    "FlextMeltanoProtocols": "flext_meltano.protocols",
    "FlextMeltanoServiceBase": "flext_meltano.base",
    "FlextMeltanoSettings": "flext_meltano.settings",
    "FlextMeltanoTypes": "flext_meltano.typings",
    "FlextMeltanoUtilities": "flext_meltano.utilities",
    "__author__": "flext_meltano.__version__",
    "__author_email__": "flext_meltano.__version__",
    "__description__": "flext_meltano.__version__",
    "__license__": "flext_meltano.__version__",
    "__title__": "flext_meltano.__version__",
    "__url__": "flext_meltano.__version__",
    "__version__": "flext_meltano.__version__",
    "__version_info__": "flext_meltano.__version__",
    "_constants": "flext_meltano._constants",
    "_models": "flext_meltano._models",
    "_protocols": "flext_meltano._protocols",
    "_typings": "flext_meltano._typings",
    "_utilities": "flext_meltano._utilities",
    "api": "flext_meltano.api",
    "base": "flext_meltano.base",
    "c": ["flext_meltano.constants", "FlextMeltanoConstants"],
    "cli": "flext_meltano.cli",
    "constants": "flext_meltano.constants",
    "d": "flext_cli",
    "dbt": "flext_meltano.dbt",
    "e": "flext_cli",
    "h": "flext_cli",
    "m": ["flext_meltano.models", "FlextMeltanoModels"],
    "main": "flext_meltano.cli",
    "meltano": "flext_meltano.api",
    "models": "flext_meltano.models",
    "p": ["flext_meltano.protocols", "FlextMeltanoProtocols"],
    "protocols": "flext_meltano.protocols",
    "r": "flext_cli",
    "s": "flext_cli",
    "settings": "flext_meltano.settings",
    "t": ["flext_meltano.typings", "FlextMeltanoTypes"],
    "typings": "flext_meltano.typings",
    "u": ["flext_meltano.utilities", "FlextMeltanoUtilities"],
    "utilities": "flext_meltano.utilities",
    "x": "flext_cli",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
