"""Consumer-base facade mixin — exposes ``Tap`` / ``Target`` / ``Dbt`` on ``meltano``.

Composed into ``FlextMeltano`` via MRO so ``flext-(tap|target|dbt)-*`` projects
subclass ``meltano.Tap`` / ``meltano.Target`` / ``meltano.Dbt`` and never import a
private ``consumer_bases`` module.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from abc import ABC

from flext_meltano.services.consumer_bases.dbt_service_base import (
    FlextMeltanoDbtServiceBase,
)
from flext_meltano.services.consumer_bases.tap_service_base import (
    FlextMeltanoTapServiceBase,
)
from flext_meltano.services.consumer_bases.target_service_base import (
    FlextMeltanoTargetServiceBase,
)


class FlextMeltanoConsumerBases:
    """Namespace exposing the Singer/dbt consumer composition bases."""

    class Tap(FlextMeltanoTapServiceBase, ABC):
        """Singer tap consumer base — subclass as ``meltano.Tap``."""

    class Target(FlextMeltanoTargetServiceBase, ABC):
        """Singer target consumer base — subclass as ``meltano.Target``."""

    class Dbt(FlextMeltanoDbtServiceBase, ABC):
        """dbt consumer base — subclass as ``meltano.Dbt``."""


__all__: list[str] = ["FlextMeltanoConsumerBases"]
