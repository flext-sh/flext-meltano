"""Temporary pyright diagnosis probe. Deleted after use.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Annotated

from flext_cli import u

from flext_meltano import m


class ProbeSerializer(m.FlexibleModel):
    """Probe u.field_serializer with explicit mode."""

    payload: Annotated[dict[str, str], m.Field(description="Payload")] = m.Field(
        default_factory=dict,
    )

    @u.field_serializer("payload", mode="plain", when_used="json")
    def serialize(self, value: dict[str, str]) -> dict[str, str]:
        """Serialize.

        Returns:
            The resulting ``dict[str, str]``.

        """
        return dict(value)
