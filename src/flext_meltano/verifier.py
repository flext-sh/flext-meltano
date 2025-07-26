"""Consolidation verifier for FLEXT Meltano Singer/Meltano/DBT integration.

Verifies that all Singer SDK, Meltano, and DBT functionality is properly
consolidated in flext-meltano without duplication.
"""

from __future__ import annotations

import logging
import re
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pathlib import Path

logger = logging.getLogger(__name__)


class FlextMeltanoConsolidationVerifier:
    """Verifies Singer/Meltano/DBT consolidation in flext-meltano."""

    def __init__(self, flext_root: Path) -> None:
        """Initialize verifier with FLEXT workspace root."""
        self.flext_root = flext_root
        self.tap_projects = list(flext_root.glob("flext-tap-*"))
        self.target_projects = list(flext_root.glob("flext-target-*"))
        self.dbt_projects = list(flext_root.glob("flext-dbt-*"))
        self.meltano_project = flext_root / "flext-meltano"

    def verify_consolidation(self) -> dict[str, Any]:
        """Verify consolidation status."""
        results = {
            "consolidation_successful": True,
            "issues": [],
            "stats": {},
        }

        # Check imports consistency
        inconsistent_imports = self._check_import_consistency()
        if inconsistent_imports:
            results["consistent"] = False
            results["issues"].extend(inconsistent_imports)

        # Check for code duplication
        duplications = self._check_code_duplication()
        if duplications:
            results["consistent"] = False
            results["issues"].extend(duplications)

        # Generate stats
        results["stats"] = {
            "tap_projects": len(self.tap_projects),
            "target_projects": len(self.target_projects),
            "dbt_projects": len(self.dbt_projects),
            "total_singer_projects": len(self.tap_projects) + len(self.target_projects),
            "issues_found": len(results["issues"]),
        }

        return results

    def _check_import_consistency(self) -> list[str]:
        """Check for inconsistent Singer SDK imports."""
        issues = []

        # Pattern for direct singer_sdk imports that should be from flext_meltano
        bad_patterns = [
            r"from singer_sdk import",
            r"import singer_sdk",
        ]

        all_projects = self.tap_projects + self.target_projects + self.dbt_projects

        for project in all_projects:
            for py_file in project.glob("**/*.py"):
                if py_file.is_file():
                    try:
                        content = py_file.read_text(encoding="utf-8")
                        # Use extend for better performance
                        found_issues = [
                            f"Direct singer_sdk import in {(py_file.relative_to(self.flext_root),)}"
                            for pattern in bad_patterns
                            if re.search(pattern, content)
                        ]
                        issues.extend(found_issues)
                    except (OSError, UnicodeDecodeError) as e:
                        # Log specific file read errors
                        logger.warning("Could not read file %s: %s", py_file, e)
                        continue

        return issues

    def _check_code_duplication(self) -> list[str]:
        """Check for code duplication that should be in flext-meltano."""
        issues = []

        # Check for duplicated Singer/Meltano functionality
        common_singer_functions = [
            "Stream",
            "Tap",
            "Target",
            "Sink",
            "SQLSink",
        ]

        all_projects = self.tap_projects + self.target_projects

        for project in all_projects:
            for py_file in project.glob("**/*.py"):
                if py_file.is_file():
                    try:
                        content = py_file.read_text(encoding="utf-8")
                        for func in common_singer_functions:
                            # Look for class definitions that might duplicate Singer SDK
                            pattern = f"class.*{(func,)}"
                            if re.search(pattern, content):
                                issues.append(
                                    f"Potential Singer functionality duplication in {py_file.relative_to(self.flext_root)}: {(func,)}",
                                )
                    except (UnicodeDecodeError, re.error) as e:
                        logger.warning("Error processing file %s: %s", py_file, e)
                        continue

        return issues

    def report_verification(self, results: dict[str, Any]) -> None:
        """Report verification results."""
        for category, issues in results.items():
            if issues:
                logger.warning("Found %s issues in category %s", len(issues), category)
                for issue in issues:
                    logger.warning("  - %s", issue)
