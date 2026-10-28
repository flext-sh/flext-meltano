"""FLEXT Meltano models - Command result models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from collections.abc import Sequence
from typing import Annotated

from flext_cli import m, u

from flext_meltano import t


class FlextMeltanoModelsResultsDbt:
    """Command result models."""

    class CommandExecutionResult(m.ArbitraryTypesModel):
        """Execution result model for Meltano command operations.

        Following flext-core patterns.
        """

        command: Annotated[
            Sequence[str],
            m.Field(description="Command that was executed"),
        ]
        success: Annotated[bool, m.Field(description="Whether the command succeeded")]
        exit_code: Annotated[int, m.Field(description="Process exit code")]
        output: Annotated[str, m.Field(description="Standard output")]
        error: Annotated[str, m.Field(description="Standard error")]
        execution_time: Annotated[
            t.NonNegativeFloat,
            m.Field(description="Execution time in seconds"),
        ]

        @m.computed_field
        @property
        def timestamp(self) -> str:
            """ISO timestamp of when the result was generated.

            Returns:
                The resulting ``str``.

            """
            return u.generate_iso_timestamp()


__all__: list[str] = ["FlextMeltanoModelsResultsDbt"]
