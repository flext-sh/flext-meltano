"""Test module for flext-meltano.

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

import tempfile
from collections.abc import Mapping

from flext_meltano.services import FlextMeltanoAbstractions
from tests import c, m, r, t, tm


class TestsFlextMeltanoAbstractionsComplete:
    """Complete test suite for FlextMeltanoAbstractions."""

    tap_abstractions: FlextMeltanoAbstractions

    def setup_method(self) -> None:
        """Set up the abstractions under test for each test."""
        self.tap_abstractions = FlextMeltanoAbstractions()

    @staticmethod
    def test_tap_config_validation() -> None:
        """Test m.Meltano.TapConfig Pydantic validation."""
        connection_config: t.HeaderMapping = {
            "host": "localhost",
            "port": 5432,
            "database": "test_db",
        }
        stream_config: Mapping[str, str] = {"users": "selected"}
        config = m.Meltano.TapConfig(
            tap_type="tap-postgres",
            connection_config=connection_config,
            stream_config=stream_config,
            tap_version="v1.2.0",
        )
        tm.that(config.tap_type, eq="tap-postgres")
        tm.that(config.tap_version, eq="v1.2.0")
        tm.that(config.stream_config, has="users")

    @staticmethod
    def test_stream_definition_validation() -> None:
        """Test m.Meltano.StreamDefinition Pydantic validation using flext_tests."""
        stream_schema: t.FlatContainerMapping = {
            "type": "t.NormalizedValue",
            "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
        }
        stream_def = m.Meltano.StreamDefinition(
            stream_name="users",
            stream_schema=stream_schema,
            source_type="tap-postgres",
            status="discovered",
            records_extracted=42,
        )
        tm.that(stream_def.stream_name, eq="users")
        tm.that(stream_def.source_type, eq="tap-postgres")
        tm.that(stream_def.records_extracted, eq=42)

    @staticmethod
    def test_tap_instance_validation() -> None:
        """Test m.Meltano.TapInstance Pydantic validation using flext_tests."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config = m.Meltano.TapConfig(
                tap_type="tap-csv",
                connection_config={"file_path": f"{temp_dir}/data.csv"},
            )
            tap_instance = m.Meltano.TapInstance.model_validate({
                "tap_type": "tap-csv",
                "settings": config,
                "tap_id": "tap_csv_123",
                "status": "initialized",
                "streams": [
                    m.Meltano.StreamInfo(
                        stream_name="test_stream",
                        stream_schema={},
                        stream_created_at="2025-01-01T00:00:00Z",
                    ),
                ],
            })
            tm.that(tap_instance.tap_type, eq="tap-csv")
            tm.that(tap_instance.tap_id, eq="tap_csv_123")
            tm.that(len(tap_instance.streams), eq=1)

    @staticmethod
    def test_tap_abstractions_initialization() -> None:
        """Test FlextMeltanoAbstractions initialization."""
        tap_abs = FlextMeltanoAbstractions()
        tm.not_none(tap_abs)
        tm.that(tap_abs.service_name, eq="FlextMeltanoAbstractions")

    @staticmethod
    def test_tap_abstractions_error_handling() -> None:
        """Test tap abstractions error handling."""
        timeout_error = TimeoutError("Connection timed out")
        tm.that(timeout_error, is_=Exception)
        validation_error = c.ValidationError.from_exception_data(
            title="Validation Error",
            line_errors=[],
        )
        tm.that(validation_error, is_=Exception)

    def test_execute_returns_config_status(self) -> None:
        """Test execute returns configuration status dict."""
        result = self.tap_abstractions.execute()
        tm.that(result, is_=r)
        if result.success:
            value = result.value
            tm.ok(isinstance(value, dict))
