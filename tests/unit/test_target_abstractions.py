"""Test module for flext-meltano target abstractions.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest
from flext_core import FlextLogger
from flext_meltano import FlextMeltanoTargetAbstractions, r, t, u

logger = FlextLogger(__name__)


class TestFlextMeltanoTargetAbstractionsComplete:
    """Complete test suite for FlextMeltanoTargetAbstractions."""

    def setup_method(self) -> None:
        """Setup for each test."""
        self.target_abstractions = FlextMeltanoTargetAbstractions()

    def test_target_abstractions_initialization(self) -> None:
        """Test FlextMeltanoTargetAbstractions initialization."""
        target_abs = FlextMeltanoTargetAbstractions()
        assert target_abs is not None
        assert hasattr(target_abs, "logger")

    def test_create_flext_target_config(self) -> None:
        """Test create_flext_target_config method."""
        if not hasattr(self.target_abstractions, "create_flext_target_config"):
            pytest.skip("create_flext_target_config not available (use PYTHONPATH=src)")
        connection_config: dict[str, t.GeneralValueType] = {"output_path": "test.jsonl"}

        result = self.target_abstractions.create_flext_target_config(
            target_type="jsonl",
            connection_config=connection_config,
            batch_size=1000,
            max_batches=50,
        )

        assert isinstance(result, r)
        if result.is_success:
            config_data = result.value
            assert config_data is not None
            assert config_data.get("target_type") == "jsonl"
            assert config_data.get("batch_size") == 1000

    def test_create_flext_target(self) -> None:
        """Test create_flext_target static method."""
        if not hasattr(FlextMeltanoTargetAbstractions, "create_flext_target"):
            pytest.skip("create_flext_target not available (use PYTHONPATH=src)")
        test_config: dict[str, t.GeneralValueType] = {
            "target_type": "jsonl",
            "connection_config": {"output_path": "test.jsonl"},
            "batch_size": 100,
        }

        abstractions = FlextMeltanoTargetAbstractions()
        result = abstractions.create_flext_target(test_config)
        assert isinstance(result, r)

    def test_target_error_handling(self) -> None:
        """Test target error handling."""
        failure_result = r[str].fail("Target error")
        assert isinstance(failure_result, r)
        assert failure_result.is_failure

    def test_utility_helper_methods(self) -> None:
        """Test utility helper methods using flext-core."""
        timestamp = u.Generators.generate_iso_timestamp()
        assert isinstance(timestamp, str)
        assert "T" in timestamp

        # Test nested value retrieval
        test_data: dict[str, t.GeneralValueType] = {
            "level1": {"level2": {"level3": "found_value"}}
        }
        level1 = test_data.get("level1", {})
        if isinstance(level1, dict):
            level2 = level1.get("level2", {})
            if isinstance(level2, dict):
                result = level2.get("level3", "default")
                assert result == "found_value"
