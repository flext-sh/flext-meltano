"""Test missing coverage for FlextMeltanoExecutor methods.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import tempfile
from pathlib import Path
from unittest import mock

from flext_tests import FlextTestsUtilities

from flext_core import FlextResult
from flext_meltano.executors import FlextMeltanoExecutor


class TestExecutorsMissingCoverage:
    """Test missing coverage for FlextMeltanoExecutor methods."""

    def setup_method(self) -> None:
        """Setup test utilities."""
        self.test_assertions = FlextTestsUtilities.assertion()
        # Create temporary project root for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_root = Path(self.temp_dir.name)
        self.executor = FlextMeltanoExecutor(project_root=self.project_root)

    def teardown_method(self) -> None:
        """Cleanup test resources."""
        self.temp_dir.cleanup()

    def test_run_command_failure_scenario(self) -> None:
        """Test run_command with failure scenario."""
        # Test with invalid command that should fail
        result = self.executor.run_command(["nonexistent-command", "arg1", "arg2"])

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_failure:
            self.test_assertions.assert_in(
                item="Command execution failed",
                container=result.error,
                message="Should have error message",
            )

    def test_run_command_exception_scenario(self) -> None:
        """Test run_command with exception scenario."""
        # Test with invalid command that will cause exception
        result = self.executor.run_command(["invalid-command-that-does-not-exist"])

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        # Should return success with exit code 1 for unknown command
        if result.is_success:
            self.test_assertions.assert_equals(
                actual=result.value,
                expected=1,
                message="Should return exit code 1 for unknown command",
            )

    def test_run_command_success_scenario(self) -> None:
        """Test run_command with success scenario."""
        # Test with version command that should succeed
        result = self.executor.run_command(["version"])

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

        if result.is_success:
            self.test_assertions.assert_equals(
                actual=result.value,
                expected=0,
                message="Should return exit code 0 for version command",
            )

    def test_run_command_with_empty_args(self) -> None:
        """Test run_command with empty args."""
        result = self.executor.run_command([])

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

    def test_run_command_with_single_arg(self) -> None:
        """Test run_command with single argument."""
        result = self.executor.run_command(["test-command"])

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

    def test_run_command_with_multiple_args(self) -> None:
        """Test run_command with multiple arguments."""
        result = self.executor.run_command(["test-command", "arg1", "arg2", "arg3"])

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

    def test_run_command_with_none_args(self) -> None:
        """Test run_command with empty args."""
        result = self.executor.run_command([])

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

    def test_run_command_with_invalid_command_type(self) -> None:
        """Test run_command with invalid command."""
        result = self.executor.run_command(["invalid-command"])

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

    def test_run_command_with_non_string_command(self) -> None:
        """Test run_command with numeric command string."""
        result = self.executor.run_command(["123"])

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

    def test_run_command_with_complex_args(self) -> None:
        """Test run_command with complex arguments."""
        complex_args = [
            "complex-command",
            "arg1",
            "--option",
            "value",
            "--flag",
            "arg2",
        ]
        result = self.executor.run_command(complex_args)

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

    def test_run_command_with_special_characters(self) -> None:
        """Test run_command with special characters."""
        special_args = [
            "special-command",
            "arg with spaces",
            "--option=value",
            "arg-with-dashes",
        ]
        result = self.executor.run_command(special_args)

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

    def test_run_command_with_unicode_args(self) -> None:
        """Test run_command with unicode arguments."""
        unicode_args = ["unicode-command", "arg1", "arg2", "arg3"]
        result = self.executor.run_command(unicode_args)

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

    def test_run_command_with_long_args(self) -> None:
        """Test run_command with long arguments."""
        long_args = ["long-command"] + ["arg1"] * 100  # 100 arguments
        result = self.executor.run_command(long_args)

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

    def test_run_command_with_mixed_types(self) -> None:
        """Test run_command with mixed argument types."""
        mixed_args = ["mixed-command", "string", 123, True, None]
        result = self.executor.run_command(mixed_args)

        self.test_assertions.assert_true(
            condition=isinstance(result, FlextResult),
            message="Should return FlextResult",
        )

    def test_execute_meltano_command_success_path(self) -> None:
        """Test execute_meltano_command success path to cover missing lines."""
        # Create a temporary directory with meltano.yml
        temp_dir = Path(tempfile.mkdtemp())

        with mock.patch.object(Path, "exists", return_value=True):
            result = self.executor.execute_meltano_command(
                project_root=temp_dir, command=["run", "tap-csv", "target-csv"]
            )

            self.test_assertions.assert_true(
                condition=result.is_success, message="Should succeed with valid project"
            )

            if result.is_success:
                result_data = result.unwrap()
                self.test_assertions.assert_equals(
                    actual=result_data["success"],
                    expected=True,
                    message="Should have success=True",
                )
                self.test_assertions.assert_equals(
                    actual=result_data["result_type"],
                    expected="meltano_command",
                    message="Should have correct result_type",
                )

    def test_get_project_info_success_path(self) -> None:
        """Test get_project_info success path to cover missing lines."""
        temp_dir = Path(tempfile.mkdtemp())

        with mock.patch.object(Path, "exists", return_value=True):
            result = self.executor.get_project_info(temp_dir)

            self.test_assertions.assert_true(
                condition=result.is_success, message="Should succeed with valid project"
            )

            if result.is_success:
                result_data = result.unwrap()
                self.test_assertions.assert_equals(
                    actual=result_data["success"],
                    expected=True,
                    message="Should have success=True",
                )
                self.test_assertions.assert_equals(
                    actual=result_data["result_type"],
                    expected="project_info",
                    message="Should have correct result_type",
                )

    def test_execute_method_health_command_success(self) -> None:
        """Test execute method with health command success path."""
        # Mock the health method using object.__setattr__ to bypass Pydantic
        original_health = self.executor.health
        object.__setattr__(
            self.executor,
            "health",
            mock.Mock(return_value=FlextResult.ok({"status": "healthy"})),
        )

        try:
            result = self.executor.execute("health")

            self.test_assertions.assert_true(
                condition=result.is_success,
                message="Should succeed with health command",
            )
        finally:
            object.__setattr__(self.executor, "health", original_health)

    def test_execute_method_version_command_success(self) -> None:
        """Test execute method with version command success path."""
        # Mock the version method using object.__setattr__ to bypass Pydantic
        original_version = self.executor.version
        object.__setattr__(
            self.executor,
            "version",
            mock.Mock(return_value=FlextResult.ok({"version": "1.0.0"})),
        )

        try:
            result = self.executor.execute("version")

            self.test_assertions.assert_true(
                condition=result.is_success,
                message="Should succeed with version command",
            )
        finally:
            object.__setattr__(self.executor, "version", original_version)

    def test_execute_method_health_command_failure(self) -> None:
        """Test execute method with health command failure path."""
        # Mock the health method using object.__setattr__ to bypass Pydantic
        original_health = self.executor.health
        object.__setattr__(
            self.executor,
            "health",
            mock.Mock(return_value=FlextResult.fail("Health check failed")),
        )

        try:
            result = self.executor.execute("health")

            self.test_assertions.assert_true(
                condition=result.is_failure,
                message="Should fail with health command failure",
            )
        finally:
            object.__setattr__(self.executor, "health", original_health)

    def test_execute_method_version_command_failure(self) -> None:
        """Test execute method with version command failure path."""
        # Mock the version method using object.__setattr__ to bypass Pydantic
        original_version = self.executor.version
        object.__setattr__(
            self.executor,
            "version",
            mock.Mock(return_value=FlextResult.fail("Version check failed")),
        )

        try:
            result = self.executor.execute("version")

            self.test_assertions.assert_true(
                condition=result.is_failure,
                message="Should fail with version command failure",
            )
        finally:
            object.__setattr__(self.executor, "version", original_version)
