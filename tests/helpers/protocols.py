"""Test protocols extending flext_meltano.protocols for test-specific protocols.

This module provides test-specific protocol definitions that extend the
production protocols from src/flext_meltano/protocols.py. All test protocols
use real inheritance to expose the full hierarchy and avoid duplication.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_meltano import FlextMeltanoProtocols


class TestsProtocols(FlextMeltanoProtocols):
    """Test-specific protocols extending FlextMeltanoProtocols.

    Provides test-specific protocol definitions that extend production
    protocols with test-specific interfaces. Uses real inheritance to
    expose the full hierarchy without duplication.
    """

    # Test-specific protocols can be added here as nested classes
    # All parent protocols are accessible via inheritance


# Standardized short name for use in tests (same pattern as flext-core)
p = TestsProtocols

__all__ = ["TestsProtocols", "p"]
