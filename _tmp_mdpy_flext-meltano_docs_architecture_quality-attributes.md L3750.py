# from flext-meltano/docs/architecture/quality-attributes.md:3750
from __future__ import annotations


class TestResultAnalyzer:
    """Analyze test results for insights and improvements."""

    def analyze_test_run(self, test_results: TestResults) -> TestAnalysis:
        """Analyze comprehensive test run results."""
        analysis = TestAnalysis()

        # Coverage analysis
        analysis.coverage_trends = self._analyze_coverage_trends(test_results)

        # Failure pattern analysis
        analysis.failure_patterns = self._analyze_failure_patterns(test_results)

        # Performance analysis
        analysis.performance_trends = self._analyze_performance_trends(test_results)

        # Reliability analysis
        analysis.reliability_metrics = self._analyze_reliability_metrics(test_results)

        # Generate recommendations
        analysis.recommendations = self._generate_test_recommendations(analysis)

        return analysis

    def _analyze_coverage_trends(self, results: TestResults) -> CoverageTrends:
        """Analyze test coverage trends."""
        # Calculate coverage by module
        module_coverage = {}
        for test_result in results.test_cases:
            module = test_result.module
            if module not in module_coverage:
                module_coverage[module] = {"covered": 0, "total": 0}

            # Aggregate coverage data
            module_coverage[module]["covered"] += test_result.lines_covered
            module_coverage[module]["total"] += test_result.lines_total

        # Calculate coverage percentages
        coverage_percentages = {}
        for module, coverage in module_coverage.items():
            if coverage["total"] > 0:
                coverage_percentages[module] = (
                    coverage["covered"] / coverage["total"]
                ) * 100

        return CoverageTrends(
            overall_coverage=sum(coverage_percentages.values())
            / len(coverage_percentages),
            module_coverage=coverage_percentages,
            uncovered_lines=self._identify_uncovered_lines(results),
        )

    def _analyze_failure_patterns(self, results: TestResults) -> FailurePatterns:
        """Analyze patterns in test failures."""
        failure_patterns = FailurePatterns()

        # Group failures by type
        failure_types = {}
        for test_result in results.test_cases:
            if test_result.failure:
                failure_type = self._classify_failure(test_result.error_message)
                failure_types[failure_type] = failure_types.get(failure_type, 0) + 1

        failure_patterns.failure_types = failure_types

        # Identify flaky tests
        flaky_tests = []
        for test_name, test_runs in results.test_runs.items():
            if len(test_runs) > 1:
                success_count = sum(1 for run in test_runs if run.passed)
                if 0 < success_count < len(test_runs):  # Mixed results
                    flaky_tests.append(test_name)

        failure_patterns.flaky_tests = flaky_tests

        # Identify slow tests
        slow_tests = [
            test.name
            for test in results.test_cases
            if test.execution_time > results.slow_test_threshold
        ]
        failure_patterns.slow_tests = slow_tests

        return failure_patterns

    def _generate_test_recommendations(self, analysis: TestAnalysis) -> t.StringList:
        """Generate recommendations based on test analysis."""
        recommendations = []

        # Coverage recommendations
        if analysis.coverage_trends.overall_coverage < 95:
            low_coverage_modules = [
                module
                for module, coverage in analysis.coverage_trends.module_coverage.items()
                if coverage < 90
            ]
            if low_coverage_modules:
                recommendations.append(
                    f"Improve test coverage for modules: {', '.join(low_coverage_modules)}"
                )

        # Failure pattern recommendations
        if analysis.failure_patterns.flaky_tests:
            recommendations.append(
                f"Address flaky tests: {', '.join(analysis.failure_patterns.flaky_tests[:5])}"
            )

        # Performance recommendations
        if analysis.performance_trends.average_test_time > 1.0:  # seconds
            recommendations.append(
                "Consider optimizing slow tests or running them separately"
            )

        # Reliability recommendations
        if analysis.reliability_metrics.test_flakiness_rate > 0.05:
            recommendations.append(
                "High test flakiness detected - investigate test stability"
            )

        return recommendations```
______________________________________________________________________

## 🔄 Cross-Cutting Concerns

### Logging Architecture

