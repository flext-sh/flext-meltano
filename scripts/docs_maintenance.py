#!/usr/bin/env python3
"""FLEXT-Meltano Documentation Maintenance Framework.

Comprehensive documentation quality assurance, validation, and maintenance system.
Provides automated auditing, link validation, style checking, and quality reporting.

Usage:
    python scripts/docs_maintenance.py --audit
    python scripts/docs_maintenance.py --validate
    python scripts/docs_maintenance.py --report
    python scripts/docs_maintenance.py --comprehensive

Author: FLEXT Documentation Team
Version: 1.0.0
"""

from __future__ import annotations

import re
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import cast
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from flext_core import (
    FlextLogger,
    FlextResult,
    FlextService,
)

from flext_meltano import FlextMeltanoTypes

from .docs_config import DocsConfig
from .docs_models import DocumentationIssue, DocumentationMetrics


class DocumentationAuditor(FlextService):
    """Comprehensive documentation quality auditor using FLEXT ecosystem.

    Extends FlextService with structured logging, error handling, and FLEXT patterns.
    Provides comprehensive documentation quality analysis with railway-oriented error handling.
    """

    def __init__(
        self,
        root_path: str = ".",
        logger: FlextLogger | None = None,
    ) -> None:
        """Initialize DocumentationAuditor with FLEXT integration.

        Args:
            root_path: Root path for documentation analysis
            logger: FlextLogger instance (injected via container)

        """
        super().__init__(logger=logger)

        self.root_path = Path(root_path)
        self.metrics = DocumentationMetrics()
        self.issues: list[DocumentationIssue] = []

        # Access configuration via singleton
        self._config = DocsConfig.get_instance()

    def audit_all_files(self) -> FlextResult[DocumentationMetrics]:
        """Perform comprehensive audit of all documentation files using FLEXT patterns.

        Returns:
            FlextResult containing audit metrics or error information

        """
        self.logger.info("Starting comprehensive documentation audit")

        try:
            # Find all markdown files
            md_files = list(self.root_path.rglob("*.md"))
            md_files.extend(self.root_path.rglob("*.mdx"))

            self.metrics.total_files = len(md_files)
            self.logger.info("Documentation files discovered", count=len(md_files))

            for file_path in md_files:
                audit_result = self._audit_single_file(file_path)
                if not audit_result.is_success:
                    self.logger.warning(
                        "File audit failed",
                        file=str(file_path),
                        error=audit_result.error,
                    )

            # Calculate quality score
            self._calculate_quality_score()

            self.logger.info(
                "Documentation audit completed successfully",
                quality_score=self.metrics.quality_score,
                total_issues=len(self.issues),
            )
            return FlextResult.ok(self.metrics)

        except Exception as e:
            error_msg = f"Documentation audit failed: {e}"
            self.logger.exception("Documentation audit failed", error=error_msg)
            return FlextResult.fail(error_msg)

    def _audit_single_file(self, file_path: Path) -> FlextResult[None]:
        """Audit a single documentation file using FLEXT error handling.

        Args:
            file_path: Path to the file to audit

        Returns:
            FlextResult indicating success or failure

        """
        try:
            with Path(file_path).open(encoding="utf-8") as f:
                content = f.read()
                lines = content.split("\n")

            # Basic metrics
            word_count = len(content.split())
            self.metrics.total_words += word_count

            # Check file age
            file_age_days = (time.time() - file_path.stat().st_mtime) / (24 * 3600)
            if file_age_days > self._config.max_file_age_days:
                self._add_issue(
                    file_path,
                    1,
                    "stale_content",
                    "medium",
                    f"File is {file_age_days:.0f} days old (max: {self._config.max_file_age_days})",
                    "Update content or mark as stable",
                )

            # Check minimum word count
            if word_count < self._config.min_words_per_file:
                self._add_issue(
                    file_path,
                    1,
                    "insufficient_content",
                    "low",
                    f"File has only {word_count} words (min: {self._config.min_words_per_file})",
                    "Add more detailed content",
                )

            # Analyze content structure
            self._analyze_content_structure(file_path, content, lines)

            # Check links and references
            self._analyze_links_and_references(file_path, content, lines)

            # Check formatting and style
            self._analyze_formatting_and_style(file_path, content, lines)

            return FlextResult.ok(None)

        except Exception as e:
            error_msg = f"Error reading file: {e!s}"
            self.logger.warning(
                "File audit failed", file=str(file_path), error=error_msg
            )

            self._add_issue(
                file_path,
                1,
                "file_error",
                "critical",
                error_msg,
                "Check file permissions and encoding",
            )

            return FlextResult.fail(error_msg)

    def _analyze_content_structure(
        self, file_path: Path, content: str, lines: list[str]
    ) -> None:
        """Analyze content structure and organization."""
        # Check for required headings
        heading_levels = set()
        for line in lines:
            if line.startswith("#"):
                level = len(line.split()[0]) if line.split() else 0
                heading_levels.add(level)
                self.metrics.headings[level] += 1

        # Check for missing basic structure
        if not any("##" in line for line in lines[:10]):
            self._add_issue(
                file_path,
                1,
                "missing_structure",
                "medium",
                "File lacks basic heading structure",
                "Add proper heading hierarchy",
            )

        # Check for TODO/FIXME markers
        todo_count = content.upper().count("TODO") + content.upper().count("FIXME")
        if todo_count > 0:
            self._add_issue(
                file_path,
                1,
                "todo_markers",
                "info",
                f"Found {todo_count} TODO/FIXME markers",
                "Address outstanding items",
            )

    def _analyze_links_and_references(
        self, file_path: Path, content: str, _lines: list[str]
    ) -> None:
        """Analyze links and references in the document."""
        # Find all links
        link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
        links = re.findall(link_pattern, content)

        for _link_text, link_url in links:
            self.metrics.total_links += 1

            if link_url.startswith(("http://", "https://")):
                self.metrics.external_links += 1
            else:
                self.metrics.internal_links += 1
                # Check if internal link exists
                if not self._validate_internal_link(file_path, link_url):
                    self._add_issue(
                        file_path,
                        1,
                        "broken_internal_link",
                        "high",
                        f"Broken internal link: {link_url}",
                        "Fix or remove broken link",
                    )

        # Find images
        image_pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
        images = re.findall(image_pattern, content)
        self.metrics.images += len(images)

        for alt_text, image_url in images:
            if not alt_text.strip():
                self._add_issue(
                    file_path,
                    1,
                    "missing_alt_text",
                    "medium",
                    f"Image missing alt text: {image_url}",
                    "Add descriptive alt text",
                )

            if image_url.startswith(("http://", "https://")):
                # External images - could validate if needed
                pass
            else:
                # Internal images - check if file exists
                image_path = file_path.parent / image_url
                if not image_path.exists():
                    self.metrics.missing_images += 1
                    self._add_issue(
                        file_path,
                        1,
                        "missing_image",
                        "high",
                        f"Missing image file: {image_url}",
                        "Add image file or fix path",
                    )

    def _analyze_formatting_and_style(
        self, file_path: Path, content: str, lines: list[str]
    ) -> None:
        """Analyze formatting and style consistency."""
        # Check line lengths
        long_lines = [
            i
            for i, line in enumerate(lines, 1)
            if len(line) > self._config.max_line_length
        ]
        if long_lines:
            self._add_issue(
                file_path,
                long_lines[0],
                "long_lines",
                "low",
                f"Found {len(long_lines)} lines longer than {self._config.max_line_length} characters",
                "Break long lines for better readability",
            )

        # Check for code blocks
        code_block_count = content.count("```")
        self.metrics.code_blocks += (
            code_block_count // 2
        )  # Each block has opening and closing

        # Check for inconsistent list formatting
        list_lines = [
            line
            for line in lines
            if line.strip().startswith(("- ", "* ", "1. ", "2. "))
        ]
        if list_lines:
            # Check for mixed list types
            dash_count = sum(1 for line in list_lines if line.strip().startswith("- "))
            asterisk_count = sum(
                1 for line in list_lines if line.strip().startswith("* ")
            )
            sum(1 for line in list_lines if re.match(r"\s*\d+\.", line.strip()))

            if dash_count > 0 and asterisk_count > 0:
                self._add_issue(
                    file_path,
                    1,
                    "mixed_list_styles",
                    "low",
                    "Mixed dash (-) and asterisk (*) list markers",
                    "Use consistent list marker style",
                )

    def _validate_internal_link(self, file_path: Path, link_url: str) -> bool:
        """Validate internal link exists."""
        # Remove anchor from link
        clean_url = link_url.split("#", maxsplit=1)[0]

        if not clean_url:
            return True  # Empty link or just anchor

        # Handle relative paths
        if clean_url.startswith(("./", "../")):
            target_path = (file_path.parent / clean_url).resolve()
        elif clean_url.startswith("/"):
            target_path = self.root_path / clean_url[1:]
        else:
            target_path = self.root_path / clean_url

        return target_path.exists()

    def _add_issue(
        self,
        file_path: Path,
        line_number: int,
        issue_type: str,
        severity: str,
        description: str,
        suggestion: str = "",
    ) -> None:
        """Add a documentation issue."""
        issue = DocumentationIssue(
            file_path=str(file_path.relative_to(self.root_path)),
            line_number=line_number,
            issue_type=issue_type,
            severity=severity,
            description=description,
            suggestion=suggestion,
        )
        self.issues.append(issue)

    def _calculate_quality_score(self) -> None:
        """Calculate overall documentation quality score."""
        if not self.metrics.total_files:
            self.metrics.quality_score = 0.0
            return

        # Base score components
        scores = []

        # Content freshness (20%)
        fresh_files = sum(
            1 for issue in self.issues if issue.issue_type == "stale_content"
        )
        freshness_score = max(
            0.0, 100.0 - (fresh_files / self.metrics.total_files) * 50.0
        )
        scores.append(("freshness", freshness_score, 20))

        # Link health (25%)
        broken_link_ratio = self.metrics.broken_links / max(1, self.metrics.total_links)
        link_score = max(
            0.0, 100.0 - broken_link_ratio * 200.0
        )  # Penalty for broken links
        scores.append(("links", link_score, 25))

        # Structure completeness (25%)
        structured_files = sum(
            1 for issue in self.issues if issue.issue_type == "missing_structure"
        )
        structure_score = max(
            0.0, 100.0 - (structured_files / self.metrics.total_files) * 30.0
        )
        scores.append(("structure", structure_score, 25))

        # Formatting quality (15%)
        formatting_issues_count = sum(
            1
            for issue in self.issues
            if issue.issue_type in {"mixed_list_styles", "long_lines"}
        )
        formatting_score = max(
            0.0, 100.0 - (formatting_issues_count / self.metrics.total_files) * 20.0
        )
        scores.append(("formatting", formatting_score, 15))

        # Accessibility (15%)
        accessibility_issues = sum(
            1
            for issue in self.issues
            if issue.issue_type in {"missing_alt_text", "missing_image"}
        )
        accessibility_score = max(
            0.0, 100.0 - (accessibility_issues / self.metrics.total_files) * 25.0
        )
        scores.append(("accessibility", accessibility_score, 15))

        # Calculate weighted average
        total_weighted_score = sum(score * weight for _, score, weight in scores)
        total_weight = sum(weight for _, _, weight in scores)

        self.metrics.quality_score = round(total_weighted_score / total_weight, 1)


class LinkValidator:
    """Advanced link validation system."""

    def __init__(self, timeout: int | None = None, retries: int | None = None) -> None:
        """Initialize link validator with timeout and retry configuration."""
        config = DocsConfig.get_instance()
        self.timeout = timeout or config.link_validation_timeout
        self.retries = retries or config.link_validation_retries
        self.valid_cache: dict[str, bool] = {}
        self.checked_urls: set[str] = set()

    def validate_all_links(
        self, root_path: str | Path = "."
    ) -> FlextMeltanoTypes.MeltanoCore.ExecutionResultDict:
        """Validate all external links in documentation."""
        if isinstance(root_path, str):
            root_path = Path(root_path)
        results: FlextMeltanoTypes.MeltanoCore.ExecutionResultDict = {
            "total_links": 0,
            "valid_links": 0,
            "broken_links": [],
            "timeout_links": [],
            "checked_links": [],
        }

        # Find all markdown files
        md_files = list(root_path.rglob("*.md"))
        md_files.extend(root_path.rglob("*.mdx"))

        for file_path in md_files:
            file_results = self._validate_file_links(file_path)
            total_links = cast("int", results["total_links"])
            file_total = cast("int", file_results["total_links"])
            results["total_links"] = total_links + file_total

            valid_links = cast("int", results["valid_links"])
            file_valid = cast("int", file_results["valid_links"])
            results["valid_links"] = valid_links + file_valid

            broken_links = cast("list[object]", results["broken_links"])
            file_broken = cast("list[object]", file_results["broken_links"])
            broken_links.extend(file_broken)

            timeout_links = cast("list[object]", results["timeout_links"])
            file_timeout = cast("list[object]", file_results["timeout_links"])
            timeout_links.extend(file_timeout)

            checked_links = cast("list[object]", results["checked_links"])
            file_checked = cast("list[object]", file_results["checked_links"])
            checked_links.extend(file_checked)

        return results

    def _validate_file_links(
        self, file_path: Path
    ) -> FlextMeltanoTypes.MeltanoCore.ExecutionResultDict:
        """Validate links in a single file."""
        results: FlextMeltanoTypes.MeltanoCore.ExecutionResultDict = {
            "total_links": 0,
            "valid_links": 0,
            "broken_links": [],
            "timeout_links": [],
            "checked_links": [],
        }

        try:
            with Path(file_path).open(encoding="utf-8") as f:
                content = f.read()

            # Find all external links
            link_pattern = r"\[([^\]]+)\]\((https?://[^)]+)\)"
            links = re.findall(link_pattern, content)

            for link_text, link_url in links:
                total_links = cast("int", results["total_links"])
                results["total_links"] = total_links + 1

                if link_url in self.checked_urls:
                    # Already checked this URL
                    if self.valid_cache.get(link_url, False):
                        valid_links = cast("int", results["valid_links"])
                        results["valid_links"] = valid_links + 1
                    continue

                checked_links = cast("list[object]", results["checked_links"])
                checked_links.append({
                    "file": str(file_path.relative_to(Path())),
                    "text": link_text,
                    "url": link_url,
                })

                is_valid = self._validate_url(link_url)

                if is_valid:
                    valid_links = cast("int", results["valid_links"])
                    results["valid_links"] = valid_links + 1
                    self.valid_cache[link_url] = True
                else:
                    broken_links = cast("list[object]", results["broken_links"])
                    broken_links.append({
                        "file": str(file_path.relative_to(Path())),
                        "text": link_text,
                        "url": link_url,
                        "error": "Link validation failed",
                    })

                self.checked_urls.add(link_url)

        except Exception as e:
            self.logger.warning(f"Failed to validate URL {url}: {e}")

        return results

    def _validate_url(self, url: str) -> bool:
        """Validate a single URL."""
        # Note: This validates HTTP/HTTPS URLs from markdown links, which is safe
        for attempt in range(self.retries + 1):
            try:
                with urlopen(url, timeout=self.timeout) as response:
                    return response.status == 200
            except (URLError, HTTPError, OSError):
                if attempt == self.retries:
                    return False
                time.sleep(1)  # Wait before retry

        return False


class QualityReporter:
    """Comprehensive quality reporting system."""

    def __init__(self, output_dir: str = "docs/reports") -> None:
        """Initialize quality reporter with output directory."""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_comprehensive_report(
        self,
        metrics: DocumentationMetrics,
        issues: list[DocumentationIssue],
        link_results: dict[str, object],
    ) -> str:
        """Generate comprehensive quality report."""
        report_path = (
            self.output_dir
            / f"docs_quality_report_{datetime.now(UTC).strftime('%Y%m%d_%H%M%S')}.md"
        )

        with Path(report_path).open("w", encoding="utf-8") as f:
            f.write(self._generate_report_content(metrics, issues, link_results))

        return str(report_path)

    def _generate_report_header(self, metrics: DocumentationMetrics) -> str:
        """Generate the report header section."""
        return f"""# Documentation Quality Report

**Generated**: {datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S")}
**Quality Score**: {metrics.quality_score}/100

## 📊 Overview

- **Total Files**: {metrics.total_files}
- **Total Words**: {metrics.total_words:,}
- **Total Links**: {metrics.total_links}
- **External Links**: {metrics.external_links}
- **Internal Links**: {metrics.internal_links}
- **Images**: {metrics.images}
- **Code Blocks**: {metrics.code_blocks}

"""

    def _generate_link_validation_section(self, link_results: dict[str, object]) -> str:
        """Generate the link validation results section."""
        return f"""## 🔗 Link Validation Results

- **Links Checked**: {len(cast("list[object]", link_results.get("checked_links", [])))}
- **Valid Links**: {cast("int", link_results.get("valid_links", 0))}
- **Broken Links**: {cast("int", link_results.get("broken_links", 0))}
- **Link Health**: {cast("float", link_results.get("link_health_percentage", 0)):.1f}%

"""

    def _generate_issues_section(self, issues: list[DocumentationIssue]) -> str:
        """Generate the issues summary section."""
        severity_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for issue in issues:
            severity_counts[issue.severity] += 1

        report = "## ⚠️ Issues Summary\n\n"
        report += f"- **Total Issues**: {len(issues)}\n"
        report += f"- **Critical**: {severity_counts['critical']}\n"
        report += f"- **High**: {severity_counts['high']}\n"
        report += f"- **Medium**: {severity_counts['medium']}\n"
        report += f"- **Low**: {severity_counts['low']}\n\n"

        # Show top issues
        if issues:
            report += "### Top Issues\n\n"
            for issue in issues[:5]:
                severity_icon = {
                    "critical": "🔴",
                    "high": "🟠",
                    "medium": "🟡",
                    "low": "🟢",
                }.get(issue.severity, "⚪")
                report += f"{severity_icon} **{issue.type}**: {issue.message}\n"
                if issue.file_path:
                    report += f"   *File*: {issue.file_path}\n"
                report += "\n"

        return report

    def _generate_recommendations_section(
        self, metrics: DocumentationMetrics, severity_counts: dict[str, int]
    ) -> str:
        """Generate the recommendations section."""
        report = "## 💡 Recommendations\n\n"

        if severity_counts.get("critical", 0) > 0:
            report += "### 🔴 Critical Actions Required\n"
            report += "- Address all critical issues immediately\n"
            report += "- Fix broken links and missing content\n"
            report += "- Review content accuracy and completeness\n\n"

        if severity_counts.get("high", 0) > 0:
            report += "### 🟠 High Priority Actions\n"
            report += "- Fix broken internal links and missing images\n"
            report += "- Update stale content\n"
            report += "- Resolve structural issues\n\n"

        if metrics.quality_score < 80:
            report += "### 📈 Quality Improvements\n"
            report += "- Implement automated quality checks in CI/CD\n"
            report += "- Set up regular content review cycles\n"
            report += "- Establish documentation maintenance procedures\n\n"

        report += "### 🔄 Continuous Improvement\n"
        report += "- Schedule regular documentation audits\n"
        report += "- Monitor link health and content freshness\n"
        report += "- Track quality metrics over time\n"
        report += "- Implement automated fixes where possible\n"

        return report

    def _generate_report_content(
        self,
        metrics: DocumentationMetrics,
        issues: list[DocumentationIssue],
        link_results: dict[str, object],
    ) -> str:
        """Generate report content."""
        # Calculate severity counts for use in multiple sections
        severity_counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
        for issue in issues:
            severity_counts[issue.severity] += 1

        # Build report from sections
        report = self._generate_report_header(metrics)
        report += self._generate_link_validation_section(link_results)
        report += self._generate_issues_section(issues)
        report += self._generate_recommendations_section(metrics, severity_counts)

        return report


def main() -> None:
    """Main entry point for documentation maintenance."""
    parser = argparse.ArgumentParser(
        description="Documentation Maintenance and Quality Assurance"
    )
    parser.add_argument("--audit", action="store_true", help="Run documentation audit")
    parser.add_argument(
        "--validate", action="store_true", help="Validate external links"
    )
    parser.add_argument(
        "--report", action="store_true", help="Generate quality reports"
    )
    parser.add_argument(
        "--comprehensive", action="store_true", help="Run all maintenance tasks"
    )
    parser.add_argument(
        "--output-dir",
        default="docs/reports",
        help="Output directory for reports (default: docs/reports)",
    )

    args = parser.parse_args()

    if not any([args.audit, args.validate, args.report, args.comprehensive]):
        parser.print_help()
        return

    # Initialize components
    auditor = DocumentationAuditor()
    validator = LinkValidator()
    reporter = QualityReporter(args.output_dir)

    # Run requested operations
    metrics = None
    link_results = None

    if args.audit or args.comprehensive:
        audit_result = auditor.audit_all_files()
        if audit_result.is_success:
            metrics = audit_result.unwrap()
        else:
            return

    if args.validate or args.comprehensive:
        link_results = validator.validate_all_links()

    if args.report or args.comprehensive:
        if not metrics:
            audit_result = auditor.audit_all_files()
            if audit_result.is_success:
                metrics = audit_result.unwrap()
            else:
                return

        if not link_results:
            link_results = validator.validate_all_links()

        # Generate reports
        reporter.generate_comprehensive_report(metrics, auditor.issues, link_results)
        reporter.generate_summary_report(metrics, auditor.issues)


if __name__ == "__main__":
    main()
