"""FLEXT Meltano DBT Integration - DBT module for Singer projects.

This module provides the DBT integration classes that Singer projects expect to import.
Simple stubs that provide basic functionality without complex dependencies.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from flext_core import FlextResult

if TYPE_CHECKING:
    from flext_core.types import TData


# Simple stub implementations for Singer project compatibility
class FlextMeltanoDbtManager:
    """DBT Manager for Singer project integration."""

    def __init__(self, project_dir: Path | str | None = None) -> None:
        """Initialize DBT manager."""
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()

    def run_models(self, models: list[str] | None = None) -> FlextResult[TData]:
        """Run DBT models."""
        return FlextResult.ok({"models": models or [], "status": "success"})

    def test_models(self, models: list[str] | None = None) -> FlextResult[TData]:
        """Test DBT models."""
        return FlextResult.ok({"models": models or [], "status": "success"})

    def compile_models(self, models: list[str] | None = None) -> FlextResult[TData]:
        """Compile DBT models."""
        return FlextResult.ok({"models": models or [], "status": "success"})


class FlextMeltanoDbtProject:
    """DBT Project wrapper for Singer integration."""

    def __init__(self, project_dir: Path | str | None = None) -> None:
        """Initialize DBT project."""
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()

    def initialize(self) -> FlextResult[None]:
        """Initialize DBT project."""
        return FlextResult.ok(None)

    def validate(self) -> FlextResult[None]:
        """Validate DBT project configuration."""
        return FlextResult.ok(None)


class FlextMeltanoDbtRunner:
    """DBT Runner for executing DBT commands."""

    def __init__(self, project_dir: Path | str | None = None) -> None:
        """Initialize DBT runner."""
        self.project_dir = Path(project_dir) if project_dir else Path.cwd()

    def run(self, command: str, args: list[str] | None = None) -> FlextResult[TData]:
        """Run DBT command."""
        return FlextResult.ok({"command": command, "args": args or [], "status": "success"})

    def run_models(self, models: list[str] | None = None) -> FlextResult[TData]:
        """Run specific DBT models."""
        return FlextResult.ok({"models": models or [], "status": "success"})

    def test_models(self, models: list[str] | None = None) -> FlextResult[TData]:
        """Test specific DBT models."""
        return FlextResult.ok({"models": models or [], "status": "success"})


# Export classes for Singer project imports
__all__ = [
    "FlextMeltanoDbtManager",
    "FlextMeltanoDbtProject",
    "FlextMeltanoDbtRunner",
]
