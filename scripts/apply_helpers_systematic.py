#!/usr/bin/env python3
"""FLEXT Meltano - Systematic Helpers Application Tool.

Script that applies boilerplate_reducers helpers to resolve lint errors
automatically and efficiently following SOLID+DRY+KISS principles.

Usage:
    python scripts/apply_helpers_systematic.py

Resolve:
- PT017: pytest fixture problems
- PLR2004: magic numbers
- ANN401: Any type annotations
- UP007: Union typing syntax
- TRY301/TRY300/TRY002: exception handling
- SIM115: simplification issues
"""

from __future__ import annotations

import re
import shutil
import tempfile
from pathlib import Path


class SystematicLintFixer:
    """Systematic lint corrections applier using helpers."""

    def __init__(self, project_root: Path | None = None) -> None:
        """Initialize systematic fixer."""
        self.project_root = project_root or Path.cwd()
        self.fixes_applied = 0
        self.errors_fixed = 0

    def fix_pt017_pytest_fixtures(self, file_path: Path) -> bool:
        """Fix PT017 - pytest fixture problems."""
        content = file_path.read_text(encoding="utf-8")

        # PT017: pytest.fixture() without request parameter
        pattern = r"@pytest\.fixture\(\s*\)"
        replacement = "@pytest.fixture"

        if re.search(pattern, content):
            content = re.sub(pattern, replacement, content)
            file_path.write_text(content, encoding="utf-8")
            self.fixes_applied += 1
            return True
        return False

    def fix_plr2004_magic_numbers(self, file_path: Path) -> bool:
        """Fix PLR2004 - magic numbers."""
        content = file_path.read_text(encoding="utf-8")
        original_content = content

        # Common magic numbers in our codebase
        magic_replacements = {
            r"\btimeout=300\b": "timeout=DEFAULT_TIMEOUT",
            r"\btimeout=60\b": "timeout=DISCOVERY_TIMEOUT",
            r"\bport=5432\b": "port=DEFAULT_POSTGRES_PORT",
            r"\bport=1521\b": "port=DEFAULT_ORACLE_PORT",
            r"\bport=3306\b": "port=DEFAULT_MYSQL_PORT",
            r"\b2 \*\* attempt\b": "BACKOFF_BASE ** attempt",
        }

        # Apply replacements
        for pattern, replacement in magic_replacements.items():
            content = re.sub(pattern, replacement, content)

        # Add constants at top if we made replacements
        if content != original_content:
            # Add constants after imports
            constants = """
# Timeout constants to avoid magic numbers
DEFAULT_TIMEOUT = 300
DISCOVERY_TIMEOUT = 60
DEFAULT_POSTGRES_PORT = 5432
DEFAULT_ORACLE_PORT = 1521
DEFAULT_MYSQL_PORT = 3306
BACKOFF_BASE = 2

"""
            # Find last import line
            lines = content.split("\n")
            last_import_idx = 0
            for i, line in enumerate(lines):
                if line.startswith(("import ", "from ")) and (
                    not line.startswith("from __future__")
                ):
                    last_import_idx = i

            # Insert constants after last import
            lines.insert(last_import_idx + 1, constants)
            content = "\n".join(lines)

            file_path.write_text(content, encoding="utf-8")
            self.fixes_applied += 1
            return True
        return False

    def fix_ann401_any_annotations(self, file_path: Path) -> bool:
        """Fix ANN401 - Any type annotations."""
        content = file_path.read_text(encoding="utf-8")

        # Replace common Any usages with more specific types
        replacements = {
            r"\bAny\b(?=\s*=\s*None)": "Any | None",
            r"dict\[str,\s*Any\]": "dict[str, object,]",  # Already correct format
            r"Dict\[str,\s*Any\]": "dict[str, object,]",  # Convert old style
            r"List\[Any\]": "list[Any,]",  # Convert old style
            r": Any\s*=\s*None": ": Any | None = None",
        }

        original_content = content
        for pattern, replacement in replacements.items():
            content = re.sub(pattern, replacement, content)

        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            self.fixes_applied += 1
            return True
        return False

    def fix_up007_union_syntax(self, file_path: Path) -> bool:
        """Fix UP007 - Union typing syntax."""
        content = file_path.read_text(encoding="utf-8")

        # Convert X | Y to X | Y
        # This is a simplified regex - for production use ast parsing
        pattern = r"Union\[([^]]+)\,]"

        def replace_union(match):
            types = match.group(1)
            # Simple split on comma (more complex parsing needed for nested types)
            type_list = [t.strip() for t in types.split(",")]
            return " | ".join(type_list)

        original_content = content
        content = re.sub(pattern, replace_union, content)

        # Remove Union import if no longer needed
        if "" not in content:
            content = re.sub(r" | Union" | "" | content)
            content = re.sub(r"Union | " | "" | content)

        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            self.fixes_applied += 1
            return True
        return False

    def fix_try_exception_handling(self, file_path: Path) -> bool:
        """Fix TRY301 | TRY300 | TRY002 - exception handling."""
        content = file_path.read_text(encoding="utf-8")
        original_content = content

        # TRY300: try block should not be too long
        # TRY301: raise within try block
        # TRY002: raise in except block

        # Use our helper for better exception handling
        helper_import = "from flext_meltano.helpers.boilerplate_reducers import with_error_handling\n"

        # Add import if not present
        if "with_error_handling" not in content and "try:" in content:
            lines = content.split("\n")
            # Find first import line
            first_import_idx = 0
            for i, line in enumerate(lines):
                if line.startswith(("import ", "from ")):
                    first_import_idx = i
                    break

            lines.insert(first_import_idx + 1, helper_import)
            content = "\n".join(lines)

        # Pattern to fix raise without from in except blocks (TRY002)
        content = re.sub(
            r"except (RuntimeError, ValueError, TypeError):\s*\n\s*raise\s*\n"
            | 'except (RuntimeError, ValueError, TypeError) as e:\n    raise RuntimeError("Operation failed") from e\n'
            | content,
        )

        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            self.fixes_applied += 1
            return True
        return False

    def fix_sim115_simplification(self, file_path: Path) -> bool:
        """Fix SIM115 - simplification issues."""
        content = file_path.read_text(encoding="utf-8")

        # SIM115: Use context manager for opening files

        # More specific: fix subprocess.PIPE usage
        content = re.sub(
            r'stdout=open\(([^)+),\s*["\']w["\',]\)',
            r'stdout=open(\1, "w")',
            content,
        )

        if "stdout=open(" in content:
            file_path.write_text(content, encoding="utf-8")
            self.fixes_applied += 1
            return True
        return False

    def apply_systematic_fixes(self) -> dict[str, int]:
        """Apply all systematic fixes to project."""
        results = {}

        # Find all Python files
        python_files = list(self.project_root.rglob("*.py"))
        python_files = [
            f for f in python_files if not any(part.startswith(".") for part in f.parts)
        ]

        for file_path in python_files:
            if not file_path.exists():
                continue

            print(f"Processing {file_path.relative_to(self.project_root)}")

            # Apply each fix type
            fixes = {
                "PT017": self.fix_pt017_pytest_fixtures(file_path),
                "PLR2004": self.fix_plr2004_magic_numbers(file_path),
                "ANN401": self.fix_ann401_any_annotations(file_path),
                "UP007": self.fix_up007_union_syntax(file_path),
                "TRY": self.fix_try_exception_handling(file_path),
                "SIM115": self.fix_sim115_simplification(file_path),
            }

            # Count fixes per type
            for fix_type, applied in fixes.items():
                if applied:
                    results.setdefault(fix_type, 0)
                    results[fix_type] += 1

        return results

    def backup_project(self) -> Path:
        """Create backup before applying fixes."""
        backup_dir = Path(tempfile.mkdtemp(prefix="flext_meltano_backup_"))
        shutil.copytree(self.project_root, backup_dir / "original")
        return backup_dir

    def run_systematic_application(self) -> dict[str, object]:
        """Run complete systematic application of helpers."""
        print("🚀 Starting systematic helper application...")

        # Create backup
        backup_path = self.backup_project()
        print(f"📦 Backup created at: {backup_path}")

        # Apply fixes
        results = self.apply_systematic_fixes()

        return {
            "fixes_applied": self.fixes_applied,
            "results_by_type": results,
            "backup_location": str(backup_path),
            "success": True,
        }


def main() -> None:
    """Execute the main application entry point."""
    fixer = SystematicLintFixer()

    print("🔧 FLEXT Meltano - Aplicador Sistemático de Helpers")
    print("=" * 60)

    results = fixer.run_systematic_application()

    print("\n✅ Systematic Application Complete!")
    print(f"📊 Total fixes applied: {results['fixes_applied']}")
    print(f"📦 Backup location: {results['backup_location']}")

    print("\n🎯 Fixes by type:")
    for fix_type, count in results["results_by_type"].items():
        print(f"  {fix_type}: {count} files")

    print("\n🧪 Next steps:")
    print("1. Run: make lint")
    print("2. Run: make type-check")
    print("3. Run: make test")
    print("4. Run: make validate")


if __name__ == "__main__":
    main()
