"""FLEXT Meltano Executor - Base class with core command execution.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import time
from collections.abc import Mapping, Sequence
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
from pydantic import Field, TypeAdapter, ValidationError
from sqlalchemy.exc import SQLAlchemyError

from flext_core import r
from flext_meltano.base import FlextMeltanoServiceBase
from flext_meltano.constants import FlextMeltanoConstants as c
from flext_meltano.models import FlextMeltanoModels as m
from flext_meltano.typings import FlextMeltanoTypes as t
from flext_meltano.utilities import FlextMeltanoUtilities as u


class FlextMeltanoExecutorBase(FlextMeltanoServiceBase):
    """Base executor providing Meltano command execution with error handling."""

    _container_mapping_list_adapter = TypeAdapter(list[t.ContainerMapping])
    service_name: str = Field(
        default="FlextMeltanoExecutor",
        description="Canonical executor service instance name",
    )

    @property
    def project_root(self) -> Path:
        """Get project root directory - delegates to settings."""
        return u.Meltano.resolve_project_root(self.settings) or Path.cwd()

    @staticmethod
    def _coerce_container_mapping(
        value: t.ContainerMapping | None,
    ) -> t.ContainerMapping | None:
        """Normalize runtime objects to canonical container mappings when possible."""
        if not isinstance(value, Mapping):
            return None
        try:
            return t.Meltano.CONTAINER_MAP_ADAPTER.validate_python(value)
        except ValidationError:
            return None

    @classmethod
    def _coerce_mapping_list(
        cls,
        value: list[t.ContainerMapping] | t.NormalizedValue,
    ) -> list[t.ContainerMapping] | None:
        """Normalize runtime plugin lists to canonical mapping lists."""
        if not isinstance(value, list):
            return None
        try:
            return cls._container_mapping_list_adapter.validate_python(value)
        except ValidationError:
            return None

    @staticmethod
    def get_version() -> r[str]:
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
            return t.Meltano.INTEGER_ADAPTER.validate_python(raw_exit_code)
        except ValidationError:
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
    ) -> r[Sequence[t.StrMapping]]:
        """Return project-scoped plugin definitions from Meltano runtime state."""
        project_result = self.load_project(_cwd)
        if project_result.failure:
            return r[Sequence[t.StrMapping]].fail(
                project_result.error or "Failed to load Meltano project",
            )
        selected_type = u.Meltano.normalize_plugin_group(plugin_type)
        discovered: list[t.StrMapping] = []
        current_plugins_raw = project_result.value.plugins.current_plugins
        canonical_fn = getattr(current_plugins_raw, "canonical", None)
        raw_canonical = (
            canonical_fn() if callable(canonical_fn) else current_plugins_raw
        )
        try:
            coerced_input = t.Meltano.CONTAINER_MAP_ADAPTER.validate_python(
                raw_canonical,
            )
        except ValidationError:
            coerced_input = None
        current_plugins = self._coerce_container_mapping(coerced_input)
        if current_plugins is None:
            return r[Sequence[t.StrMapping]].ok(discovered)
        for raw_type, raw_plugins_value in current_plugins.items():
            raw_plugins = self._coerce_mapping_list(raw_plugins_value)
            if raw_plugins is None:
                continue
            for raw_plugin in raw_plugins:
                plugin_data = u.Meltano.build_discovered_plugin(
                    u.to_str(raw_type),
                    raw_plugin,
                )
                if plugin_data is None:
                    continue
                if selected_type is not None and plugin_data["type"] != selected_type:
                    continue
                discovered.append(plugin_data)
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
    def execute(self) -> r[t.ContainerMapping]:
        """Execute the Meltano executor service."""
        config_data: t.ContainerMapping = {
            "status": c.Meltano.OperationStatus.READY,
            "executor_type": "flext_meltano_executor",
            "execution_timestamp": str(time.time()),
            "settings": self.settings.model_dump(),
        }
        self.logger.info("FlextMeltanoExecutor executed successfully")
        return r[t.ContainerMapping].ok(config_data)

    def execute_meltano_command(
        self,
        command: t.StrSequence,
        timeout: int = c.Meltano.NETWORK_MELTANO_DEFAULT_TIMEOUT,
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
    ) -> r[m.Meltano.CommandExecutionResult]:
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
        _config: t.ContainerMapping | None = None,
    ) -> r[m.Meltano.CommandExecutionResult]:
        """Execute a complete ELT pipeline."""
        try:
            return self.execute_meltano_command(
                u.Meltano.build_pipeline_runtime_command(tap_name, target_name),
            )
        except c.Meltano.OPERATION_ERRORS as e:
            return r[m.Meltano.CommandExecutionResult].fail(str(e))
