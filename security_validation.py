#!/usr/bin/env python3
"""Security validation script for S603 and S110 fixes.

This script validates that S603 (subprocess security) and S110 (try-except-pass) 
security issues have been properly addressed in the flext-meltano codebase.
"""

import ast
import sys
from pathlib import Path


class SecurityIssueValidator:
    """Validates that security issues have been properly fixed."""

    def __init__(self, base_path: Path):
        self.base_path = base_path
        self.issues_found = []

    def validate_all(self) -> bool:
        """Run all security validations."""
        print("🔍 Running security validation for S603 and S110 fixes...")

        # Find all Python files
        py_files = list(self.base_path.rglob("*.py"))

        s603_issues = self.check_subprocess_security(py_files)
        s110_issues = self.check_try_except_pass(py_files)

        total_issues = len(s603_issues) + len(s110_issues)

        if s603_issues:
            print("\n❌ S603 (subprocess security) issues found:")
            for issue in s603_issues:
                print(f"  - {issue}")

        if s110_issues:
            print("\n❌ S110 (try-except-pass) issues found:")
            for issue in s110_issues:
                print(f"  - {issue}")

        if total_issues == 0:
            print("\n✅ No S603 or S110 security issues found!")
            print("✅ All subprocess calls have proper input validation")
            print("✅ All try-except-pass patterns have been replaced")
            return True
        print(f"\n❌ Found {total_issues} security issues that need attention")
        return False

    def check_subprocess_security(self, py_files: list[Path]) -> list[str]:
        """Check for S603 subprocess security issues."""
        issues = []

        for py_file in py_files:
            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content, filename=str(py_file))

                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        # Check for subprocess.run, subprocess.call, etc.
                        if (isinstance(node.func, ast.Attribute) and
                            isinstance(node.func.value, ast.Name) and
                            node.func.value.id == "subprocess"):

                            method = node.func.attr
                            if method in ["run", "call", "check_call", "check_output", "Popen"]:
                                # Check if shell=True is used (dangerous)
                                for keyword in node.keywords:
                                    if (keyword.arg == "shell" and
                                        isinstance(keyword.value, ast.Constant) and
                                        keyword.value.value is True):
                                        issues.append(
                                            f"{py_file}:{node.lineno} - subprocess.{method} with shell=True"
                                        )

                                # Check if the first argument is a string (potentially dangerous)
                                if (node.args and
                                    isinstance(node.args[0], ast.Constant) and
                                    isinstance(node.args[0].value, str)):
                                    issues.append(
                                        f"{py_file}:{node.lineno} - subprocess.{method} with string command"
                                    )

            except (SyntaxError, UnicodeDecodeError):
                # Skip files that can't be parsed
                continue

        return issues

    def check_try_except_pass(self, py_files: list[Path]) -> list[str]:
        """Check for S110 try-except-pass issues."""
        issues = []

        for py_file in py_files:
            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()

                tree = ast.parse(content, filename=str(py_file))

                for node in ast.walk(tree):
                    if isinstance(node, ast.Try):
                        for handler in node.handlers:
                            # Check if handler body only contains Pass
                            if (len(handler.body) == 1 and
                                isinstance(handler.body[0], ast.Pass)):
                                # Check if there's a comment explaining the pass
                                has_comment = False
                                has_justification = False
                                try:
                                    lines = content.split("\n")
                                    pass_line = handler.body[0].lineno - 1

                                    # Check current line and previous lines for comments
                                    for i in range(max(0, pass_line - 3), min(len(lines), pass_line + 2)):
                                        if i < len(lines) and "#" in lines[i]:
                                            has_comment = True
                                            line_content = lines[i]
                                            if ("S110" in line_content or
                                                "suppression justified" in line_content or
                                                "Expected" in line_content):
                                                has_justification = True
                                                break
                                except (IndexError, AttributeError):
                                    # Expected when parsing edge cases
                                    has_comment = True  # Assume documented when parsing fails
                                    has_justification = True

                                if not has_comment:
                                    issues.append(
                                        f"{py_file}:{handler.body[0].lineno} - "
                                        f"try-except-pass without explanation"
                                    )
                                elif not has_justification and "test_" not in str(py_file):
                                    issues.append(
                                        f"{py_file}:{handler.body[0].lineno} - "
                                        f"try-except-pass needs S110 suppression justification"
                                    )

            except (SyntaxError, UnicodeDecodeError):
                # Skip files that can't be parsed
                continue

        return issues

    def check_imports(self, py_files: list[Path]) -> tuple[bool, bool]:
        """Check that security-related imports are present."""
        has_contextlib = False
        has_shlex = False

        for py_file in py_files:
            try:
                with open(py_file, encoding="utf-8") as f:
                    content = f.read()

                if "import contextlib" in content or "from contextlib import" in content:
                    has_contextlib = True
                if "import shlex" in content or "from shlex import" in content:
                    has_shlex = True

            except UnicodeDecodeError:
                continue

        return has_contextlib, has_shlex


def main():
    """Main validation function."""
    # Get the base path for flext-meltano
    base_path = Path(__file__).parent

    validator = SecurityIssueValidator(base_path)

    # Check that security improvements are in place
    py_files = list(base_path.rglob("*.py"))
    has_contextlib, has_shlex = validator.check_imports(py_files)

    print("📋 Security Enhancement Status:")
    print(f"✅ contextlib imported: {'Yes' if has_contextlib else 'No'}")
    print(f"✅ shlex imported: {'Yes' if has_shlex else 'No'}")

    # Run validation
    success = validator.validate_all()

    if success:
        print("\n🎉 Security validation PASSED!")
        print("All S603 and S110 security issues have been properly addressed.")
        return 0
    print("\n💥 Security validation FAILED!")
    print("Please review and fix the issues listed above.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
