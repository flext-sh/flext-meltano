"""Architecture standardizer for FLEXT Meltano Singer/Meltano/DBT consolidation.

Automatically standardizes imports and removes code duplication to ensure
all Singer/Meltano/DBT functionality is properly consolidated in flext-meltano.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path


class FlextSingerArchitectureStandardizer:
    """Standardizes Singer/Meltano architecture by consolidating in flext-meltano."""

    def __init__(self, flext_root: Path) -> None:
        """Initialize standardizer with FLEXT workspace root."""
        self.flext_root = flext_root
        self.tap_projects = list(flext_root.glob("flext-tap-*"))
        self.target_projects = list(flext_root.glob("flext-target-*"))
        self.dbt_projects = list(flext_root.glob("flext-dbt-*"))
        self.changes_made = 0

    def standardize_architecture(self) -> dict[str, Any]:
        """Standardize all Singer/Meltano/DBT architecture."""
        results = {
            "files_processed": 0,
            "changes_made": 0,
            "projects_standardized": [],
        }

        # Standardize all projects
        all_projects = self.tap_projects + self.target_projects + self.dbt_projects

        for project in all_projects:
            project_changes = self._standardize_project(project)

            if project_changes > 0:
                results["modified_projects"].append(project.name)
                results["total_changes"] += project_changes
            else:
                pass

        results["python_files_count"] = self._count_python_files(all_projects)

        return results

    def _standardize_project(self, project: Path) -> int:
        """Standardize imports in a single project."""
        changes = 0

        for py_file in project.glob("**/*.py"):
            if py_file.is_file() and not self._should_skip_file(py_file):
                file_changes = self._standardize_file(py_file)
                changes += file_changes

        return changes

    def _standardize_file(self, py_file: Path) -> int:
        """Standardize imports in a single Python file."""
        try:
            content = py_file.read_text(encoding="utf-8")
            original_content = content

            # Apply standardization patterns
            content = self._apply_import_standardizations(content)
            content = self._add_migration_comments(content)

            # Write back if changed
            if content != original_content:
                py_file.write_text(content, encoding="utf-8")
                return 1
            return 0  # noqa: TRY300

        except OSError:
            # Handle file I/O errors specifically
            return 0

    def _apply_import_standardizations(self, content: str) -> str:
        """Apply import standardization patterns."""
        standardizations = {
            # Singer SDK imports
            r"from singer_sdk import Tap": "from flext_meltano.singer import FlextMeltanoTap as Tap",
            r"from singer_sdk import Target": "from flext_meltano.singer import FlextMeltanoTarget as Target",
            r"from singer_sdk import Stream": "from flext_meltano import Stream",
            r"from singer_sdk import typing as th": "from flext_meltano import th",
            r"from singer_sdk\.sinks import Sink": "from flext_meltano import Sink",
            r"from singer_sdk\.sinks import SQLSink": "from flext_meltano import SQLSink",
            # Direct singer_sdk imports
            r"import singer_sdk": "# Use flext_meltano instead of direct singer_sdk import",
            # Type imports
            r"from singer_sdk\.typing import": "from flext_meltano import",
        }

        for pattern, replacement in standardizations.items():
            content = re.sub(pattern, replacement, content)

        return content

    def _add_migration_comments(self, content: str) -> str:
        """Add migration comments where appropriate."""
        # Add comment at the top if we detect singer_sdk usage
        if "from flext_meltano" in content and "# MIGRATED:" not in content:
            lines = content.split("\n")

            # Find the first import line and add comment before it
            for i, line in enumerate(lines):
                if line.startswith("from flext_meltano"):
                    lines.insert(
                        i,
                        "# MIGRATED: Singer SDK imports centralized via flext-meltano",
                    )
                    break

            content = "\n".join(lines)

        return content

    def _should_skip_file(self, py_file: Path) -> bool:
        """Check if file should be skipped."""
        skip_patterns = [
            "__pycache__",
            ".venv",
            ".mypy_cache",
            "test_",  # Skip test files for now
            "conftest.py",
        ]

        return any(pattern in str(py_file) for pattern in skip_patterns)

    def _count_python_files(self, projects: list[Any]) -> int:
        """Count total Python files processed."""
        count = 0
        for project in projects:
            for py_file in project.glob("**/*.py"):
                if py_file.is_file() and not self._should_skip_file(py_file):
                    count += 1
        return count
