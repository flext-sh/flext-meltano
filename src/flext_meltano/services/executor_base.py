"""FLEXT Meltano Executor - Base class with core command execution.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import os
import time
from collections.abc import Mapping, Sequence
from contextlib import redirect_stderr, redirect_stdout
from importlib import metadata
from io import StringIO
from pathlib import Path
from typing import Annotated, override

from meltano.cli.cli import cli as meltano_cli
from meltano.cli.utils import CliError
from meltano.core.error import EmptyMeltanoFileException, MeltanoError, ProjectNotFound
from meltano.core.project import Project

from flext_meltano import (
    FlextMeltanoServiceBase,
    FlextMeltanoSettings,
    c,
    cli,
    m,
    p,
    r,
    settings,
    t,
    u,
)


class FlextMeltanoExecutorBase(FlextMeltanoServiceBase):
    """Base executor providing Meltano command execution with error handling."""

    service_name: Annotated[
        t.NonEmptyStr,
        m.Field(
            default="FlextMeltanoExecutor",
            description="Canonical Meltano executor service name",
        ),
    ] = "FlextMeltanoExecutor"

    @property
    def project_root(self) -> Path:
        """The project root directory - delegates to settings."""
        active_settings = (
            self.runtime_settings
            if isinstance(self.runtime_settings, FlextMeltanoSettings)
            else settings
        )
        return (
            u.Meltano.resolve_project_root(active_settings.Meltano.project_root)
            or Path.cwd()
        )

    @staticmethod
    def fetch_version() -> p.Result[str]:
        """Return the installed Meltano distribution version."""
        return u.try_(
            lambda: metadata.version("meltano"),
            catch=(
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ),
        ).map_error(lambda e: f"Failed to get version: {e}")

    def _project_search_root(self, _cwd: Path | None = None) -> Path | None:
        """Resolve the project root used for project-scoped Meltano operations.

        Returns:
            The resulting ``Path | None``.

        """
        active_settings = (
            self.runtime_settings
            if isinstance(self.runtime_settings, FlextMeltanoSettings)
            else settings
        )
        configured_root = u.Meltano.resolve_project_root(
            active_settings.Meltano.project_root,
        )
        if configured_root is not None:
            return configured_root
        if _cwd is not None:
            return m.Meltano.PathPayload(value=_cwd).value
        return None

    def load_project(self, _cwd: Path | None = None) -> p.Result[Project]:
        """Load a Meltano project using the imported runtime.

        Returns:
            The resulting ``p.Result[Project]``.

        """
        search_root = self._project_search_root(_cwd)
        return u.try_(
            lambda: Project.find(search_root, activate=False),
            catch=(
                ProjectNotFound,
                EmptyMeltanoFileException,
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ),
        ).map_error(lambda e: f"Failed to load Meltano project: {e}")

    def fetch_project_plugins(
        self,
        plugin_type: str | None = None,
        _cwd: Path | None = None,
    ) -> p.Result[Sequence[Mapping[str, str]]]:
        """Return the project-scoped plugin definitions from Meltano runtime state."""
        project_result = self.load_project(_cwd)
        if project_result.failure:
            return r[Sequence[Mapping[str, str]]].from_failure(project_result)
        selected_type = u.Meltano.normalize_plugin_group(plugin_type)
        current_plugins_raw = project_result.value.plugins.plugins_by_type(
            ensure_parent=False,
        )
        discovered = u.Meltano.discover_project_plugins(
            current_plugins_raw,
            selected_type=selected_type,
        )
        return r[Sequence[Mapping[str, str]]].ok(discovered)

    def discover_installed_plugins(self) -> p.Result[Sequence[str]]:
        """Discover installed Meltano plugins from the active project runtime.

        Returns:
            The resulting ``p.Result[Sequence[str]]``.

        """
        return self.fetch_project_plugins().map(
            lambda plugins: [
                plugin["name"] for plugin in plugins if plugin.get("name")
            ],
        )

    def _runtime_environment_args(self, _cwd: Path | None = None) -> Sequence[str]:
        """Select a runtime environment explicitly to avoid leaking test env vars.

        Returns:
            The resulting ``Sequence[str]``.

        """
        active_settings = (
            self.runtime_settings
            if isinstance(self.runtime_settings, FlextMeltanoSettings)
            else settings
        )
        selected_environment = u.Meltano.normalize_environment_name(
            active_settings.Meltano.environment,
        )
        if not selected_environment:
            return [c.Meltano.CMD_NO_ENVIRONMENT_OPTION]
        project_result = self.load_project(_cwd)
        if project_result.failure:
            return [c.Meltano.CMD_NO_ENVIRONMENT_OPTION]
        available_environments = {
            environment.name
            for environment in project_result.value.meltano.environments
        }
        if selected_environment not in available_environments:
            return [c.Meltano.CMD_NO_ENVIRONMENT_OPTION]
        return [c.Meltano.CMD_ENVIRONMENT_OPTION, selected_environment]

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute the Meltano executor service.

        Returns:
            The resulting ``p.Result[t.JsonMapping]``.

        """
        config_data: t.JsonMapping = {
            "status": c.Meltano.OperationStatus.READY,
            "executor_type": "flext_meltano_executor",
            "execution_timestamp": str(time.time()),
            "settings": settings.model_dump(mode="json"),
        }
        self.logger.info("FlextMeltanoExecutor executed successfully")
        return r[t.JsonMapping].ok(config_data)

    def execute_meltano_command(
        self,
        command: Sequence[str],
        timeout: int = c.Meltano.DEFAULT_TIMEOUT_SECONDS,
        _cwd: Path | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Execute a Meltano runtime command in-process and capture its output.

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.

        """
        if timeout <= 0:
            return r[m.Meltano.CommandExecutionResult].fail(
                "Command timeout must be greater than zero",
            )

        def _run_execute_meltano_command() -> p.Result[
            m.Meltano.CommandExecutionResult
        ]:
            start_time = time.monotonic()
            normalized_command: list[str] = list(
                u.Meltano.normalize_runtime_command(command),
            )
            if not normalized_command:
                return r[m.Meltano.CommandExecutionResult].fail(
                    "Command cannot be empty",
                )
            needs_project_context = normalized_command[0] not in {
                c.Meltano.CMD_HELP_OPTION,
                c.Meltano.CMD_VERSION_OPTION,
            }
            working_dir = self.project_root if _cwd is None else _cwd
            cwd = m.Meltano.PathPayload(value=working_dir).value
            runtime_args: list[str] = list(normalized_command)
            if needs_project_context:
                runtime_args = [
                    *self._runtime_environment_args(cwd),
                    c.Meltano.CMD_CWD_OPTION,
                    str(cwd),
                    *normalized_command,
                ]
            stdout_buffer = StringIO()
            stderr_buffer = StringIO()
            exit_code = 0
            self.logger.info(
                "Executing command",
                command=str(runtime_args),
                timeout=timeout,
                cwd=str(cwd),
            )
            prior_cwd = Path.cwd()
            runtime_error = ""
            Project.deactivate()
            try:
                with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                    command_result = cli.execute_external_command(
                        meltano_cli,
                        args=runtime_args,
                        prog_name=c.Meltano.CMD_BINARY,
                    )
                if command_result.failure:
                    exit_code = 1
                    runtime_error = command_result.error or "Meltano CLI command failed"
            except (
                CliError,
                EmptyMeltanoFileException,
                MeltanoError,
                ProjectNotFound,
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ) as e:
                exit_code = 1
                runtime_error = str(e)
            finally:
                Project.deactivate()
                try:
                    os.chdir(prior_cwd)
                except OSError as restore_error:
                    self.logger.warning(
                        "Failed to restore working directory",
                        path=prior_cwd,
                        error=str(restore_error),
                    )
            execution_time = time.monotonic() - start_time
            error_output = stderr_buffer.getvalue()
            if runtime_error and not error_output.strip():
                error_output = runtime_error
            result = m.Meltano.CommandExecutionResult(
                command=normalized_command,
                success=exit_code == 0,
                exit_code=exit_code,
                output=stdout_buffer.getvalue(),
                error=error_output,
                execution_time=execution_time,
            )
            return r[m.Meltano.CommandExecutionResult].ok(result)

        try:
            return _run_execute_meltano_command()
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
        ) as e:
            self.logger.exception("Command execution failed", error=str(e))
            return r[m.Meltano.CommandExecutionResult].fail(str(e), exception=e)

    def execute_dbt_command(
        self,
        dbt_command: str,
        args: Sequence[str] | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Execute a DBT command.

        Returns:
            The resulting ``p.Result[m.Meltano.CommandExecutionResult]``.

        """
        try:
            return self.execute_meltano_command(
                u.Meltano.build_dbt_runtime_command(dbt_command, args),
            )
        except c.EXC_ATTR_KEY_OS_TYPE_VALUE as e:
            return r[m.Meltano.CommandExecutionResult].fail(str(e), exception=e)


__all__: list[str] = ["FlextMeltanoExecutorBase"]
