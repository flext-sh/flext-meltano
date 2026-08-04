"""FLEXT Meltano models - DBT result models."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping
from pathlib import Path
from typing import Annotated

from flext_cli import m, u

from flext_meltano import t


class FlextMeltanoModelsResultsDbt:
    """DBT-specific result models."""

    class DbtProjectInfo(m.ArbitraryTypesModel):
        """Information about a DBT project."""

        root: Annotated[Path, m.Field(description="Project root directory")]
        name: Annotated[str, m.Field(description="Project name")]
        dbt_version: Annotated[
            str | None, m.Field(default=None, description="DBT version")
        ] = None
        models_count: Annotated[
            t.NonNegativeInt, m.Field(default=0, description="Number of models")
        ] = 0
        tests_count: Annotated[
            t.NonNegativeInt, m.Field(default=0, description="Number of tests")
        ] = 0

    class DbtRunResult(m.ArbitraryTypesModel):
        """Result of a DBT model run operation."""

        success: Annotated[
            bool, m.Field(default=True, description="Whether the run was successful")
        ] = True
        models_run: Annotated[
            t.NonNegativeInt,
            m.Field(default=0, description="Number of models executed"),
        ] = 0
        status: Annotated[
            str,
            m.Field(
                default="completed", description="Run status (completed, failed, etc.)"
            ),
        ] = "completed"
        error_message: Annotated[
            str | None, m.Field(default=None, description="Error message if run failed")
        ] = None
        execution_time_seconds: Annotated[
            float | None,
            m.Field(default=None, description="Total execution time in seconds"),
        ] = None

    class DbtTestResult(m.ArbitraryTypesModel):
        """Result of a DBT test operation."""

        success: Annotated[
            bool, m.Field(default=True, description="Whether tests passed")
        ] = True
        tests_run: Annotated[
            t.NonNegativeInt, m.Field(default=0, description="Number of tests executed")
        ] = 0
        tests_passed: Annotated[
            t.NonNegativeInt, m.Field(default=0, description="Number of tests passed")
        ] = 0
        tests_failed: Annotated[
            t.NonNegativeInt, m.Field(default=0, description="Number of tests failed")
        ] = 0
        status: Annotated[
            str,
            m.Field(
                default="completed", description="Test status (completed, failed, etc.)"
            ),
        ] = "completed"
        error_message: Annotated[
            str | None,
            m.Field(default=None, description="Error message if tests failed"),
        ] = None
        execution_time_seconds: Annotated[
            float | None,
            m.Field(default=None, description="Total execution time in seconds"),
        ] = None

    class CommandExecutionResult(m.ArbitraryTypesModel):
        """Execution result model for Meltano command operations following flext-core patterns."""

        command: Annotated[
            t.StrSequence, m.Field(description="Command that was executed")
        ]
        success: Annotated[bool, m.Field(description="Whether the command succeeded")]
        exit_code: Annotated[int, m.Field(description="Process exit code")]
        output: Annotated[str, m.Field(description="Standard output")]
        error: Annotated[str, m.Field(description="Standard error")]
        execution_time: Annotated[
            t.NonNegativeFloat, m.Field(description="Execution time in seconds")
        ]

        @m.computed_field
        def timestamp(self) -> str:
            """ISO timestamp of when the result was generated."""
            return u.generate_iso_timestamp()

        def to_dict(self) -> Mapping[str, t.Scalar | t.StrSequence]:
            """Convert to dictionary representation.

            Returns:
            Mapping[str, t.Primitives | t.StrSequence]: Dictionary representation of execution result.

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
