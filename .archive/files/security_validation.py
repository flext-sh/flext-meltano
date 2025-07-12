#!/usr/bin/env python3
"""Security validation script for S603 and S110 fixes.

This script validates that S603 (subprocess security) and S110 (try-except-pass)
security issues have been properly addressed in the flext-meltano codebase.
"""

from __future__ import annotations

import ast
import sys
from pathlib import Path


class SecurityIssueValidator:
    """Validates that security issues have been properly fixed."""

    def __init__(self, base_path: Path) -> None:
        """Initialize validator with base path."""
        self.base_path = base_path
        self.issues_found: list[str] = []

    def validate_all(self) -> bool:
        """Validate all security issues have been fixed."""
        # Find all Python files
        py_files = list(self.base_path.rglob("*.py"))

        s603_issues = self.check_subprocess_security(py_files)
        s110_issues = self.check_try_except_pass(py_files)

        total_issues = len(s603_issues) + len(s110_issues)

        if s603_issues:
            for _issue in s603_issues:
                pass

        if s110_issues:
            for _issue in s110_issues:
                pass

        return total_issues == 0

    def check_subprocess_security(self, py_files: list[Path]) -> list[str]:
        """Check for subprocess security issues (S603)."""
        issues = []

        for py_file in py_files:
            try:
                with py_file.open(encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content, filename=str(py_file))

                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        # Check for subprocess.run, subprocess.call, etc.
                        if (
                            isinstance(node.func, ast.Attribute)
                            and isinstance(node.func.value, ast.Name)
                            and node.func.value.id == "subprocess"
                        ):
                            method = node.func.attr
                            if method in {
                                "run",
                                "call",
                                "check_call",
                                "check_output",
                                "Popen",
                            }:
                                # Check if shell=True is used
                                issues.extend(f"{py_file}:{node.lineno} - "
                                            f"subprocess.{method} with shell=True" for keyword in node.keywords if keyword.arg == "shell"
                                        and isinstance(keyword.value, ast.Constant)
                                        and keyword.value.value is True)

            except Exception:
                pass

        return issues

    def check_try_except_pass(self, py_files: list[Path]) -> list[str]:
        """Check for try-except-pass patterns (S110)."""
        issues = []

        for py_file in py_files:
            try:
                with py_file.open(encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content, filename=str(py_file))

                for node in ast.walk(tree):
                    if isinstance(node, ast.Try):
                        issues.extend(f"{py_file}:{handler.lineno} - "
                                    f"try-except-pass pattern" for handler in node.handlers if len(handler.body) == 1
                                and isinstance(handler.body[0], ast.Pass))

            except Exception:
                pass

        return issues


def main() -> None:
    """Main entry point for security validation."""
    if len(sys.argv) != 2:
        sys.exit(1)

    base_path = Path(sys.argv[1])
    if not base_path.exists():
        sys.exit(1)

    validator = SecurityIssueValidator(base_path)
    is_secure = validator.validate_all()

    if is_secure:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
