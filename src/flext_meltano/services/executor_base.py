"""FLEXT Meltano Executor - Base class with core command execution.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import time
from collections.abc import (
    Sequence,
)
from contextlib import redirect_stderr, redirect_stdout, suppress
from io import StringIO
from pathlib import Path
from typing import override

import meltano
from click import Abort, ClickException
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

from flext_meltano import (
    FlextMeltanoServiceBase,
    FlextMeltanoSettings,
    c,
    m,
    p,
    r,
    t,
    u,
)


class FlextMeltanoExecutorBase(FlextMeltanoServiceBase):
    """Base executor providing Meltano command execution with error handling."""

    service_name: t.NonEmptyStr = u.Field(
        default="FlextMeltanoExecutor",
        description="Canonical Meltano executor service name.",
        validate_default=True,
    )

    def __init__(
        self,
        settings: FlextMeltanoSettings | t.JsonMapping | None = None,
        *,
        service_name: t.NonEmptyStr | None = None,
        service_version: t.NonEmptyStr | None = None,
        source_name: str | None = None,
        sink_name: str | None = None,
        transformation_name: str | None = None,
    ) -> None:
        """Expose a minimal typed constructor for executor callers."""
        super().__init__(
            settings=settings,
            service_name=service_name,
            service_version=service_version,
            source_name=source_name,
            sink_name=sink_name,
            transformation_name=transformation_name,
        )

    @property
    def project_root(self) -> Path:
        """Get project root directory - delegates to settings."""
        return u.Meltano.resolve_project_root(self.settings) or Path.cwd()

    @staticmethod
    def fetch_version() -> p.Result[str]:
        """Get version information from the imported Meltano package."""
        return u.try_(
            lambda: meltano.__version__,
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
    def _normalize_exit_code(raw_exit_code: int | str | None) -> int:
        """Normalize runtime exit codes into integers."""
        if raw_exit_code is None:
            return 0
        if isinstance(raw_exit_code, int):
            return raw_exit_code
        try:
            return int(raw_exit_code)
        except ValueError:
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
    ) -> p.Result[Project]:
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

    def load_project(self, _cwd: Path | None = None) -> p.Result[Project]:
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

    def fetch_project_plugins(
        self,
        plugin_type: str | None = None,
        _cwd: Path | None = None,
    ) -> p.Result[Sequence[t.StrMapping]]:
        """Return project-scoped plugin definitions from Meltano runtime state."""
        project_result = self.load_project(_cwd)
        if project_result.failure:
            return r[Sequence[t.StrMapping]].fail(
                project_result.error or "Failed to load Meltano project",
            )
        selected_type = u.Meltano.normalize_plugin_group(plugin_type)
        current_plugins_raw = project_result.value.plugins.current_plugins
        discovered = u.Meltano.discover_project_plugins(
            current_plugins_raw,
            selected_type=selected_type,
        )
        return r[Sequence[t.StrMapping]].ok(discovered)

    def _runtime_environment_args(self, _cwd: Path | None = None) -> t.StrSequence:
        """Select a runtime environment explicitly to avoid leaking test env vars."""
        selected_environment = u.Meltano.normalize_environment_name(
            self.settings.environment,
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
        return [
            c.Meltano.CMD_ENVIRONMENT_OPTION,
            selected_environment,
        ]

    @override
    def execute(self) -> p.Result[t.JsonMapping]:
        """Execute the Meltano executor service."""
        config_data: t.JsonMapping = {
            "status": c.Meltano.OperationStatus.READY,
            "executor_type": "flext_meltano_executor",
            "execution_timestamp": str(time.time()),
            "settings": self.settings.model_dump(mode="json"),
        }
        self.logger.info("FlextMeltanoExecutor executed successfully")
        return r[t.JsonMapping].ok(config_data)

    def execute_meltano_command(
        self,
        command: t.StrSequence,
        timeout: int = c.Meltano.NETWORK_MELTANO_DEFAULT_TIMEOUT,
        _cwd: Path | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
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
            try:
                Project.deactivate()
                with redirect_stdout(stdout_buffer), redirect_stderr(stderr_buffer):
                    meltano_cli.main(
                        args=runtime_args,
                        prog_name=c.Meltano.CMD_BINARY,
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
                Project.deactivate()
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
            self.logger.exception("Command execution failed", error=str(e))
            return r[m.Meltano.CommandExecutionResult].fail(str(e))

    def execute_dbt_command(
        self,
        dbt_command: str,
        args: t.StrSequence | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Execute a DBT command."""
        try:
            return self.execute_meltano_command(
                u.Meltano.build_dbt_runtime_command(dbt_command, args),
            )
        except c.Meltano.OPERATION_ERRORS as e:
            return r[m.Meltano.CommandExecutionResult].fail(str(e))

    def execute_pipeline(
        self,
        tap_name: str,
        target_name: str,
        config: t.JsonMapping | None = None,
    ) -> p.Result[m.Meltano.CommandExecutionResult]:
        """Execute a complete ELT pipeline."""
        try:
            command = list(
                u.Meltano.build_pipeline_runtime_command(tap_name, target_name)
            )
            if config is not None:
                command.extend(
                    f"--{u.to_str(key).strip()}={u.to_str(value)}"
                    for key, value in config.items()
                )
            return self.execute_meltano_command(
                command,
            )
        except c.Meltano.OPERATION_ERRORS as e:
            return r[m.Meltano.CommandExecutionResult].fail(str(e))
