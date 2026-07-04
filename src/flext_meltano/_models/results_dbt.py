"""FLEXT Meltano models - DBT result models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from flext_cli import m, u
from flext_meltano.typings import FlextMeltanoTypes as t

if TYPE_CHECKING:
    from collections.abc import (
        MutableMapping,
    )
    from pathlib import Path


class FlextMeltanoModelsResultsDbt:
    """DBT-specific result models."""

    class DbtProjectInfo(m.ArbitraryTypesModel):
        """Information about a DBT project."""

        root: Annotated[Path, u.Field(description="Project root directory")]
        name: Annotated[str, u.Field(description="Project name")]
        dbt_version: Annotated[
            str | None,
            u.Field(default=None, description="DBT version"),
        ] = None
        models_count: Annotated[
            t.NonNegativeInt,
            u.Field(default=0, description="Number of models"),
        ] = 0
        tests_count: Annotated[
            t.NonNegativeInt,
            u.Field(default=0, description="Number of tests"),
        ] = 0

    class CommandExecutionResult(m.ArbitraryTypesModel):
        """Execution result model for Meltano command operations following flext-core patterns."""

        command: Annotated[
            t.StrSequence,
            u.Field(description="Command that was executed"),
        ]
        success: Annotated[bool, u.Field(description="Whether the command succeeded")]
        exit_code: Annotated[int, u.Field(description="Process exit code")]
        output: Annotated[str, u.Field(description="Standard output")]
        error: Annotated[str, u.Field(description="Standard error")]
        execution_time: Annotated[
            t.NonNegativeFloat,
            u.Field(description="Execution time in seconds"),
        ]

        @u.computed_field()
        @property
        def timestamp(self) -> str:
            """ISO timestamp of when the result was generated."""
            return u.generate_iso_timestamp()

        def to_dict(self) -> t.MappingKV[str, t.Scalar | t.StrSequence]:
            """Convert to dictionary representation.

            Returns:
            t.MappingKV[str, t.Primitives | t.StrSequence]: Dictionary representation of execution result.

            """
            dumped: MutableMapping[str, t.Scalar | t.StrSequence] = {}
            dumped["command"] = self.command
            dumped["success"] = self.success
            dumped["exit_code"] = self.exit_code
            dumped["output"] = self.output
            dumped["error"] = self.error
            dumped["execution_time"] = self.execution_time
            dumped["timestamp"] = u.generate_iso_timestamp()
            return dumped
