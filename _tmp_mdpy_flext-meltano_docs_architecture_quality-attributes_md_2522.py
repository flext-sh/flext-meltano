# from flext-meltano_docs/architecture/quality-attributes.md:2522
from __future__ import annotations
import pathlib


class AutomatedCodeReview:
    """Automated code review system."""

    def __init__(self, rules_config: Dict[str, t.JsonValue]):
        self.rules = rules_config
        self.review_results = []

    def review_pull_request(self, pr_details: PRDetails) -> CodeReviewResult:
        """Perform automated code review on pull request."""
        result = CodeReviewResult(pr_number=pr_details.number)

        # Analyze changed files
        for file_path in pr_details.changed_files:
            file_review = self._review_file(file_path, pr_details)
            result.file_reviews.append(file_review)

        # Overall assessment
        result.overall_score = self._calculate_overall_score(result.file_reviews)
        result.recommendations = self._generate_recommendations(result.file_reviews)
        result.blocking_issues = self._identify_blocking_issues(result.file_reviews)

        return result

    def _review_file(self, file_path: str, pr_details: PRDetails) -> FileReviewResult:
        """Review a single file."""
        result = FileReviewResult(file_path=file_path)

        try:
            # Read file content
            content = pathlib.Path(file_path).read_text(encoding="utf-8")

            # Apply review rules
            result.issues = self._apply_review_rules(content, file_path)

            # Calculate quality score
            result.quality_score = self._calculate_file_score(result.issues)

            # Generate suggestions
            result.suggestions = self._generate_file_suggestions(
                result.issues, file_path
            )

        except Exception as e:
            result.issues = [f"File review failed: {e}"]
            result.quality_score = 0

        return result

    def _apply_review_rules(self, content: str, file_path: str) -> t.StringList:
        """Apply code review rules to file content."""
        issues = []

        # Complexity checks
        complexity = self._calculate_cyclomatic_complexity(content)
        if complexity > self.rules.get("max_complexity", 10):
            issues.append(
                f"High cyclomatic complexity: {complexity} (max: {self.rules['max_complexity']})"
            )

        # Line length checks
        lines = content.split("\n")
        long_lines = [
            i
            for i, line in enumerate(lines, 1)
            if len(line) > self.rules.get("max_line_length", 120)
        ]
        if long_lines:
            issues.append(f"Long lines found at: {', '.join(map(str, long_lines[:5]))}")

        # TODO comment checks
        todo_count = content.upper().count("TODO") + content.upper().count("FIXME")
        if todo_count > self.rules.get("max_todos", 3):
            issues.append(f"Too many TODO comments: {todo_count}")

        # Import organization
        import_issues = self._check_import_organization(content)
        issues.extend(import_issues)

        # Security checks
        security_issues = self._check_security_issues(content)
        issues.extend(security_issues)

        return issues

    def _calculate_cyclomatic_complexity(self, content: str) -> int:
        """Calculate cyclomatic complexity of code."""
        complexity = 1  # Base complexity

        # Count decision points
        decision_keywords = ["if", "elif", "for", "while", "except", "with", "assert"]
        lines = content.split("\n")

        for line in lines:
            stripped = line.strip()
            if any(keyword in stripped for keyword in decision_keywords):
                complexity += 1

        return complexity

    def _check_import_organization(self, content: str) -> t.StringList:
        """Check import organization and style."""
        issues = []
        lines = content.split("\n")

        # Find import sections
        stdlib_imports = []
        third_party_imports = []
        local_imports = []

        in_imports = False
        for line in lines:
            stripped = line.strip()

            if stripped.startswith("import ") or stripped.startswith("from "):
                in_imports = True
                if "." not in stripped.split()[1] or stripped.split()[1].startswith(
                    "flext"
                ):
                    local_imports.append(stripped)
                elif any(lib in stripped for lib in ["os", "sys", "json", "datetime"]):
                    stdlib_imports.append(stripped)
                else:
                    third_party_imports.append(stripped)
            elif in_imports and stripped:
                # Check if imports are properly grouped
                if stdlib_imports and third_party_imports and not local_imports:
                    pass  # Proper grouping
                elif len(stdlib_imports) > 5 and not third_party_imports:
                    issues.append(
                        "Consider grouping imports: stdlib, third-party, local"
                    )
                break

        return issues

    def _check_security_issues(self, content: str) -> t.StringList:
        """Check for common security issues."""
        issues = []

        # Check for hardcoded secrets
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
        ]

        for pattern in secret_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                issues.append("Potential hardcoded secret detected")

        # Check for SQL injection vulnerabilities
        if "execute(" in content and ("%" in content or "+" in content):
            issues.append("Potential SQL injection vulnerability")

        # Check for unsafe eval usage
        if "eval(" in content or "exec(" in content:
            issues.append("Use of eval/exec detected - security risk")

        return issues

    def _calculate_file_score(self, issues: t.StringList) -> float:
        """Calculate quality score for a file."""
        base_score = 100.0

        # Deduct points for issues
        for issue in issues:
            if "complexity" in issue.lower():
                base_score -= 20
            elif "security" in issue.lower():
                base_score -= 30
            elif "line" in issue.lower():
                base_score -= 5
            elif "todo" in issue.lower():
                base_score -= 10
            else:
                base_score -= 5

        return max(0, base_score)

    def _generate_file_suggestions(
        self, issues: t.StringList, file_path: str
    ) -> t.StringList:
        """Generate improvement suggestions for a file."""
        suggestions = []

        for issue in issues:
            if "complexity" in issue:
                suggestions.append(
                    "Consider breaking down complex functions into smaller ones"
                )
            elif "security" in issue:
                suggestions.append("Review and remove hardcoded secrets")
            elif "line" in issue:
                suggestions.append("Break long lines for better readability")
            elif "todo" in issue:
                suggestions.append("Address outstanding TODO items")
            elif "import" in issue:
                suggestions.append("Organize imports: stdlib, third-party, local")

        return suggestions

    def _calculate_overall_score(self, file_reviews: List[FileReviewResult]) -> float:
        """Calculate overall PR quality score."""
        if not file_reviews:
            return 100.0

        total_score = sum(review.quality_score for review in file_reviews)
        return total_score / len(file_reviews)

    def _generate_recommendations(
        self, file_reviews: List[FileReviewResult]
    ) -> t.StringList:
        """Generate overall recommendations for the PR."""
        recommendations = []

        # Analyze issue patterns
        all_issues = [issue for review in file_reviews for issue in review.issues]

        if any("security" in issue.lower() for issue in all_issues):
            recommendations.append("Address security issues before merging")

        if any("complexity" in issue.lower() for issue in all_issues):
            recommendations.append("Consider refactoring complex functions")

        complexity_issues = sum(
            1 for issue in all_issues if "complexity" in issue.lower()
        )
        if complexity_issues > len(file_reviews) / 2:
            recommendations.append(
                "Overall code complexity is high - consider architectural improvements"
            )

        if not recommendations:
            recommendations.append(
                "Code quality is acceptable - proceed with manual review"
            )

        return recommendations

    def _identify_blocking_issues(
        self, file_reviews: List[FileReviewResult]
    ) -> t.StringList:
        """Identify issues that should block the PR."""
        blocking = []

        for review in file_reviews:
            for issue in review.issues:
                if any(
                    keyword in issue.lower()
                    for keyword in ["security", "hardcoded", "vulnerability"]
                ):
                    blocking.append(f"{review.file_path}: {issue}")

        return blocking```
______________________________________________________________________

## 🎨 Usability

### API Design Principles

