"""Base models for flext-meltano.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import MutableSequence

from flext_cli import m


class FlextMeltanoModelsBase:
    """Base models for flext-meltano."""

    class EventedEntity(m.Entity):
        """Project entity with a construction-visible ``domain_events`` default.

        Why: the inherited ``m.Entity`` contract declares ``domain_events``
        through ``Annotated[..., Field(default_factory=list)]``; neither
        checker's dataclass_transform synthesis extracts that default from the
        annotated FieldInfo, so every concrete construction reported a missing
        ``domain_events`` argument. Re-declaring the same field with the same
        empty default as an assigned specifier value keeps the inherited
        contract while making the default visible to pyright and mypy.
        """

        domain_events: MutableSequence[m.DomainEvent] = m.Field(
            default_factory=list[m.DomainEvent],
            description="List of uncommitted domain events for event sourcing",
        )
