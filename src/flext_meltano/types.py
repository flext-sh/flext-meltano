"""FLEXT Meltano Types - Data pipeline type definitions.

This module centralizes all TypedDict definitions and type aliases used across
the FLEXT Meltano data pipeline infrastructure.

Patterns used:
- TypedDict for structured data with known keys
- Union types for flexible configurations
- Generic type parameters for reusable patterns
"""

from __future__ import annotations

from typing import Any, TypedDict

__all__ = [
    "DbtTransformationResult",
    "EltPipelineResult",
    "SingerExecutionResult",
    "SingerProcessingResult",
]


class DbtTransformationResult(TypedDict):
    """Type definition for DBT transformation results."""

    success: bool
    exit_code: int
    models_run: str | list[str]
    execution_method: str
    project_dir: str
    execution_time: float | None


class SingerProcessingResult(TypedDict):
    """Type definition for Singer message processing results."""

    streams_processed: int
    messages_processed: int
    state_updates: int
    execution_method: str


class SingerExecutionResult(TypedDict):
    """Type definition for Singer pipeline execution results."""

    success: str
    execution_method: str
    tap_name: str
    target_name: str
    streams_processed: int
    messages_processed: int
    state_updates: int


class EltPipelineResult(TypedDict):
    """Type definition for complete E-L-T pipeline results."""

    extraction: dict[str, Any]
    loading: dict[str, Any]
    transformation: dict[str, Any]
    overall_success: str
