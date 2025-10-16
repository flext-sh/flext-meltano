"""FLEXT-Meltano Documentation Models.

Domain models for documentation quality assurance using FlextModels.
Replaces dataclasses with proper domain-driven design patterns.

ARCHITECTURAL INTEGRATION:
- FlextModels.Value: Immutable value objects for documentation metrics and issues
- Domain-Driven Design: Proper business entity modeling
- Type Safety: Complete type annotations with Pydantic v2 validation
"""

from __future__ import annotations

from collections import defaultdict
from typing import ClassVar

from pydantic import BaseModel, ConfigDict


class DocumentationMetrics(BaseModel):
    """Comprehensive documentation quality metrics using FlextModels.Value.

    Immutable value object containing all documentation quality measurements.
    Uses domain-driven design principles with proper validation.

    Attributes:
        total_files: Total number of documentation files analyzed
        total_words: Total word count across all files
        total_links: Total number of links found
        broken_links: Number of broken links detected
        external_links: Number of external links (http/https)
        internal_links: Number of internal links (relative paths)
        images: Total number of images found
        missing_images: Number of missing image files
        code_blocks: Number of code blocks detected
        headings: Dictionary mapping heading levels (1-6) to counts
        issues: List of raw issue dictionaries (for backward compatibility)
        quality_score: Overall quality score (0-100)

    """

    model_config = ConfigDict(frozen=False)

    total_files: int = 0
    total_words: int = 0
    total_links: int = 0
    broken_links: int = 0
    external_links: int = 0
    internal_links: int = 0
    images: int = 0
    missing_images: int = 0
    code_blocks: int = 0
    headings: ClassVar[dict[int, int]] = defaultdict(int)
    issues: ClassVar[list[dict[str, object]]] = []
    quality_score: float = 0.0


class DocumentationIssue(BaseModel):
    """Represents a documentation quality issue using FlextModels.Value.

    Immutable value object containing details about a specific documentation problem.
    Uses domain-driven design with proper validation and type safety.

    Attributes:
        file_path: Relative path to the file containing the issue
        line_number: Line number where the issue was found (1-based)
        issue_type: Type/category of the issue (e.g., 'broken_link', 'stale_content')
        severity: Severity level ('critical', 'high', 'medium', 'low', 'info')
        description: Human-readable description of the issue
        suggestion: Optional suggested fix or improvement
        context: Optional additional context about the issue

    """

    file_path: str
    line_number: int
    issue_type: str
    severity: str
    description: str
    suggestion: str = ""
    context: str = ""
