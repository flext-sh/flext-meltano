"""FLEXT Meltano Executor - Base class with core command execution.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import importlib
import os
import time
from collections.abc import Mapping, Sequence
from contextlib import redirect_stderr, redirect_stdout, suppress
from io import StringIO
from pathlib import Path
from typing import TYPE_CHECKING, override

import meltano
from click import Abort, ClickException
from flext_core import r
from meltano.cli.cli import cli as meltano_cli
from meltano.cli.utils import CliError
from meltano.core.error import EmptyMeltanoFileException, MeltanoError, ProjectNotFound
from meltano.core.plugin.error import PluginNotFoundError
from meltano.core.project import Project
from meltano.core.project_init_service import (
    ProjectInitService,
    ProjectInitServiceError,
)
from sqlalchemy.exc import SQLAlchemyError

from flext_meltano import FlextMeltanoServiceBase, c, m, t, u

if TYPE_CHECKING:
    from flext_meltano import FlextMeltanoCLI
else:
    FlextMeltanoCLI = object


class FlextMeltanoExecutorBase(FlextMeltanoServiceBase):
    """Base executor providing Meltano command execution with error handling."""

    service_name: str = "FlextMeltanoExecutor"

    @property
    def project_root(self) -> Path:
        """Get project root directory - delegates to settings."""
        return u.Meltano.resolve_project_root(self.settings) or Path.cwd()

    @staticmethod
    def create_flext_cli() -> r[FlextMeltanoCLI]:
        """Create FLEXT CLI instance - delegates to CLI module."""
        return u.try_(
            lambda: getattr(
                importlib.import_module("flext_meltano.cli"),
                "FlextMeltanoCLI",
            )(),
            catch=(ValueError, TypeError, KeyError, AttributeError, OSError),
        ).map_error(lambda e: f"Failed to create CLI: {e}")

    @staticmethod
    def get_version() -> r[str]:
        """Get version information from the imported Meltano package."""
        return u.try_(
            lambda: getattr(
                meltano,
                "__version__",
                c.Meltano.Defaults.SERVICE_VERSION,
            ),
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

    @staticmethod
    def _normalize_exit_code(raw_exit_code: object) -> int:
        """Normalize runtime exit codes into integers."""
        if raw_exit_code is None:
            return 0
        if isinstance(raw_exit_code, int):
            return raw_exit_code
        try:
            return int(str(raw_exit_code))
        except (TypeError, ValueError):
            return 1

    def _project_search_root(self, _cwd: Path | None = None) -> Path | None:
        """Resolve the project root used for project-scoped Meltano operations."""
        configured_root = u.Meltano.resolve_project_root(self.settings)
        if configured_root is not None:
            return configured_root
        if _cwd is not None:
            return m.Meltano.PathPayload(value=_cwd).value
        return None

    @staticmethod
    def initialize_project_root(
        project_root: Path,
        *,
        force: bool = False,
    ) -> r[Project]:
        """Initialize a Meltano project using the library service."""
        return u.try_(
            lambda: ProjectInitService(project_root).init(
                activate=False,
                force=force,
            ),
            catch=(
                ProjectInitServiceError,
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
            ),
        ).map_error(lambda e: f"Failed to initialize Meltano project: {e}")

    def load_project(self, _cwd: Path | None = None) -> r[Project]:
        """Load a Meltano project using the imported runtime."""
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

    def get_project_plugins(
        self,
        plugin_type: str | None = None,
        _cwd: Path | None = None,
    ) -> r[list[dict[str, str]]]:
        """Return project-scoped plugin definitions from Meltano runtime state."""
        project_result = self.load_project(_cwd)
        if project_result.is_failure:
            return r[list[dict[str, str]]].fail(
                project_result.error or "Failed to load Meltano project",
            )
        selected_type = u.Meltano.normalize_plugin_group(plugin_type)
        discovered: list[dict[str, str]] = []
        current_plugins = project_result.value.plugins.current_plugins
        if hasattr(current_plugins, "canonical"):
            current_plugins = current_plugins.canonical()
        if not isinstance(current_plugins, Mapping):
            return r[list[dict[str, str]]].ok(discovered)
        for raw_type, raw_plugins in current_plugins.items():
            if not isinstance(raw_plugins, list):
                continue
            for raw_plugin in raw_plugins:
                if not isinstance(raw_plugin, Mapping):
                    continue
                plugin_data = u.Meltano.build_discovered_plugin(
                    u.to_str(raw_type),
                    raw_plugin,
                )
                if plugin_data is None:
                    continue
                if selected_type is not None and plugin_data["type"] != selected_type:
                    continue
                discovered.append(plugin_data)
        return r[list[dict[str, str]]].ok(discovered)

    def _runtime_environment_args(self, _cwd: Path | None = None) -> list[str]:
        """Select a runtime environment explicitly to avoid leaking test env vars."""
        selected_environment = u.Meltano.normalize_environment_name(
            u.to_str(getattr(self.settings, "environment", "")),
        )
        if not selected_environment:
            return [c.Meltano.Commands.NO_ENVIRONMENT_OPTION]
        project_result = self.load_project(_cwd)
        if project_result.is_failure:
            return [c.Meltano.Commands.NO_ENVIRONMENT_OPTION]
        available_environments = {
            environment.name
            for environment in project_result.value.meltano.environments
        }
        if selected_environment not in available_environments:
            return [c.Meltano.Commands.NO_ENVIRONMENT_OPTION]
        return [
            c.Meltano.Commands.ENVIRONMENT_OPTION,
            selected_environment,
        ]

    @override
    def execute(self) -> r[t.Meltano.ExecutionResultDict]:
        """Execute the Meltano executor service."""
        config_data: t.Meltano.ExecutionResultDict = u.Meltano.build_status_payload(
            c.Meltano.Enums.OperationStatus.READY,
            extra_fields={
                "executor_type": "flext_meltano_executor",
                "execution_timestamp": str(time.time()),
            },
            config=self.settings,
            config_field="config",
        )
        self.logger.info("FlextMeltanoExecutor executed successfully")
        return r[t.Meltano.ExecutionResultDict].ok(config_data)

    def execute_meltano_command(
        self,
        command: Sequence[str],
        timeout: int = c.Meltano.Network.MELTANO_DEFAULT_TIMEOUT,
        _cwd: Path | None = None,
    ) -> r[m.Meltano.CommandExecutionResult]:
        """Execute a Meltano runtime command in-process and capture its output."""
        if timeout <= 0:
            return r[m.Meltano.CommandExecutionResult].fail(
                "Command timeout must be greater than zero",
            )
        try:
            start_time = time.monotonic()
            normalized_command: list[str] = list(
                u.Meltano.normalize_runtime_command(command),
            )
            if not normalized_command:
                return r[m.Meltano.CommandExecutionResult].fail(
                    "Command cannot be empty",
                )
            needs_project_context = normalized_command[0] not in {
                c.Meltano.Commands.HELP_OPTION,
                c.Meltano.Commands.VERSION_OPTION,
            }
            working_dir = self.project_root if _cwd is None else _cwd
            cwd = m.Meltano.PathPayload(value=working_dir).value
            runtime_args: list[str] = list(normalized_command)
            if needs_project_context:
                runtime_args = [
                    *self._runtime_environment_args(cwd),
                    c.Meltano.Commands.CWD_OPTION,
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
            try:
                with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                    meltano_cli.main(
                        args=runtime_args,
                        prog_name=c.Meltano.Commands.BINARY,
                        standalone_mode=False,
                    )
            except SystemExit as e:
                exit_code = self._normalize_exit_code(e.code)
            except (
                Abort,
                ClickException,
                CliError,
                EmptyMeltanoFileException,
                MeltanoError,
                PluginNotFoundError,
                ProjectNotFound,
                ValueError,
                TypeError,
                KeyError,
                AttributeError,
                OSError,
                RuntimeError,
                ImportError,
                SQLAlchemyError,
            ) as e:
                exit_code = 1
                runtime_error = str(e)
            finally:
                with suppress(OSError):
                    os.chdir(prior_cwd)
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
        except (
            ValueError,
            TypeError,
            KeyError,
            AttributeError,
            OSError,
            RuntimeError,
            ImportError,
            SQLAlchemyError,
        ) as e:
            error_msg = f"Command execution failed: {e}"
            self.logger.exception(error_msg)
            return r[m.Meltano.CommandExecutionResult].fail(error_msg)

    def execute_dbt_command(
        self,
        dbt_command: str,
        args: Sequence[str] | None = None,
    ) -> r[m.Meltano.CommandExecutionResult]:
        """Execute a DBT command."""
        try:
            return self.execute_meltano_command(
                u.Meltano.build_dbt_runtime_command(dbt_command, args),
            )
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[m.Meltano.CommandExecutionResult].fail(f"DBT command failed: {e}")

    def execute_pipeline(
        self,
        tap_name: str,
        target_name: str,
        _config: t.Meltano.MeltanoConfigDict | None = None,
    ) -> r[m.Meltano.CommandExecutionResult]:
        """Execute a complete ELT pipeline."""
        try:
            return self.execute_meltano_command(
                u.Meltano.build_pipeline_runtime_command(tap_name, target_name),
            )
        except (ValueError, TypeError, KeyError, AttributeError, OSError) as e:
            return r[m.Meltano.CommandExecutionResult].fail(
                f"Pipeline execution failed: {e}",
            )
