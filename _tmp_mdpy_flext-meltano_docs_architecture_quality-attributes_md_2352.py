# from flext-meltano_docs/architecture/quality-attributes.md:2352
from __future__ import annotations
import pathlib


class QualityGate:
    """Automated quality gates for code commits."""

    def __init__(self, settings: QualityConfig):
        self.settings = settings
        self.checks = {
            "linting": self._check_linting,
            "type_checking": self._check_type_safety,
            "testing": self._check_test_coverage,
            "security": self._check_security,
            "documentation": self._check_documentation,
        }

    def run_quality_gates(self, staged_files: List[Path]) -> QualityGateResult:
        """Run all quality gates on staged files."""
        result = QualityGateResult()
        result.timestamp = datetime.utcnow()

        # Filter files by type
        code_files = [f for f in staged_files if self._is_code_file(f)]
        test_files = [f for f in staged_files if self._is_test_file(f)]
        doc_files = [f for f in staged_files if self._is_doc_file(f)]

        # Run checks
        for check_name, check_func in self.checks.items():
            try:
                check_result = check_func(code_files, test_files, doc_files)
                result.check_results[check_name] = check_result

                if not check_result.passed:
                    result.overall_passed = False
                    result.blocking_issues.extend(check_result.issues)

            except Exception as e:
                result.check_results[check_name] = CheckResult(
                    passed=False, issues=[f"Check execution failed: {e}"]
                )
                result.overall_passed = False

        return result

    def _check_linting(self, code_files, test_files, doc_files) -> CheckResult:
        """Check code linting compliance."""
        result = CheckResult()

        # Run Ruff linting
        cmd = ["ruff", "check"] + [str(f) for f in code_files + test_files]
        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode != 0:
            result.passed = False
            result.issues = process.stdout.split("\n")
            result.issues = [issue for issue in result.issues if issue.strip()]
        else:
            result.passed = True

        return result

    def _check_type_safety(self, code_files, test_files, doc_files) -> CheckResult:
        """Check type safety with Pyrefly."""
        result = CheckResult()

        # Run Pyrefly type checking
        cmd = ["pyrefly", "check"] + [str(f) for f in code_files]
        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode != 0:
            result.passed = False
            result.issues = process.stdout.split("\n")
            result.issues = [issue for issue in result.issues if issue.strip()]
        else:
            result.passed = True

        return result

    def _check_test_coverage(self, code_files, test_files, doc_files) -> CheckResult:
        """Check test coverage requirements."""
        result = CheckResult()

        if not test_files and code_files:
            result.passed = False
            result.issues = ["New code files require corresponding tests"]
            return result

        # Run coverage check (thresholds configured in pyproject.toml)
        cmd = ["pytest", "--cov", "--cov-report=term-missing", "tests/"]
        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode != 0:
            result.passed = False
            result.issues = ["Test coverage below 95% threshold"]
        else:
            result.passed = True

        return result

    def _check_security(self, code_files, test_files, doc_files) -> CheckResult:
        """Check security vulnerabilities."""
        result = CheckResult()

        # Run Bandit security scanner
        cmd = ["bandit", "-r"] + [str(f) for f in code_files]
        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode != 0:
            result.passed = False
            result.issues = process.stdout.split("\n")
            result.issues = [issue for issue in result.issues if "SEVERITY:" in issue]
        else:
            result.passed = True

        return result

    def _check_documentation(self, code_files, test_files, doc_files) -> CheckResult:
        """Check documentation requirements."""
        result = CheckResult()

        # Check for undocumented public functions
        undocumented = []
        for file_path in code_files:
            if file_path.suffix == ".py":
                undocumented.extend(self._check_file_documentation(file_path))

        if undocumented:
            result.passed = False
            result.issues = [
                f"Undocumented public function: {func}" for func in undocumented
            ]
        else:
            result.passed = True

        return result

    def _check_file_documentation(self, file_path: Path) -> t.StringList:
        """Check documentation in a single file."""
        undocumented = []

        try:
            with pathlib.Path(file_path).open("r", encoding="utf-8") as f:
                tree = ast.parse(f.read())

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                    # Check for docstring
                    if not ast.get_docstring(node):
                        undocumented.append(f"{file_path}:{node.lineno}:{node.name}")

        except Exception:
            pass  # Skip files that can't be parsed

        return undocumented

    def _is_code_file(self, file_path: Path) -> bool:
        """Check if file is a code file."""
        return file_path.suffix in [".py"]

    def _is_test_file(self, file_path: Path) -> bool:
        """Check if file is a test file."""
        return "test" in file_path.name and file_path.suffix == ".py"

    def _is_doc_file(self, file_path: Path) -> bool:
        """Check if file is a documentation file."""
        return file_path.suffix in [".md", ".rst", ".txt"]```
#### 2. Automated Code Review

