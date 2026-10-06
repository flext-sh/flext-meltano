"""Pytest bootstrap for flext-meltano local package resolution.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

# Copyright (c) 2025 FLEXT Team. All rights reserved.
from __future__ import annotations

from pathlib import Path

from flext_tests.pytest_bootstrap import install_local_packages

"""Pytest bootstrap for flext-meltano local package resolution."""


install_local_packages(Path(__file__).resolve().parent)
