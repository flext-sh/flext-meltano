"""FLEXT Meltano Project Manager - Enterprise Meltano Integration.

Modern Python 3.13 implementation using flext-core patterns.
Zero tolerance for legacy code or duplicated implementations.
"""

from __future__ import annotations

import asyncio
import shutil
from datetime import UTC
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any

import yaml
from structlog import get_logger

from flext_core import ServiceResult
from flext_core.domain.pydantic_base import DomainEvent

logger = get_logger(__name__)


class ProjectInitializationMode(StrEnum):
    """Project initialization behavior modes."""

    CREATE_NEW = "create_new"
    FORCE_RECREATE = "force_recreate"
    OVERWRITE_EXISTING = "overwrite_existing"


class MeltanoProjectError(Exception):
    """Meltano project operation error."""


class MeltanoExecutionError(Exception):
    """Meltano command execution error."""

    def __init__(self, message: str, command: list[str] | None = None, returncode: int | None = None, stderr: str | None = None) -> None:
        super().__init__(message)
        self.command = command
        self.returncode = returncode
        self.stderr = stderr


class MeltanoProjectManager:
    """Enterprise Meltano project manager using flext-core patterns."""

    def __init__(self, project_root: Path | str) -> None:
        self.project_root = Path(project_root)
        self.logger = logger.bind(project_root=str(self.project_root))

    async def create_project(self, project_name: str, environment: str = "dev") -> ServiceResult[dict[str, Any]]:
        """Create new Meltano project with enterprise configuration."""
        self.logger.info("Creating Meltano project", project_name=project_name, environment=environment)

        try:
            project_path = self.project_root / project_name

            if project_path.exists():
                return ServiceResult.fail(f"Project already exists at {project_path}")

            # Create project directory
            project_path.mkdir(parents=True, exist_ok=True)

            # Initialize basic Meltano project structure
            meltano_yml_content = {
                "version": 1,
                "default_environment": environment,
                "project_id": f"{project_name}-{datetime.now(UTC).strftime('%Y%m%d')}",
                "environments": [
                    {"name": environment},
                ],
                "plugins": {
                    "extractors": [],
                    "loaders": [],
                    "transformers": [],
                    "orchestrators": [],
                    "utilities": [],
                },
            }

            # Write meltano.yml
            meltano_yml_path = project_path / "meltano.yml"
            with meltano_yml_path.open("w", encoding="utf-8") as f:
                yaml.safe_dump(meltano_yml_content, f, default_flow_style=False, indent=2)

            # Create .meltano directory
            (project_path / ".meltano").mkdir(exist_ok=True)

            result = {
                "project_name": project_name,
                "project_path": str(project_path),
                "environment": environment,
                "created_at": datetime.now(UTC).isoformat(),
            }

            self.logger.info("Meltano project created successfully", **result)
            return ServiceResult.success(result)

        except Exception as e:
            error_msg = f"Failed to create Meltano project: {e}"
            self.logger.exception(error_msg, error=str(e))
            return ServiceResult.fail(error_msg)

    async def load_project_config(self, project_name: str) -> ServiceResult[dict[str, Any]]:
        """Load Meltano project configuration."""
        try:
            project_path = self.project_root / project_name
            meltano_yml = project_path / "meltano.yml"

            if not meltano_yml.exists():
                return ServiceResult.fail(f"Project config not found: {meltano_yml}")

            with meltano_yml.open("r", encoding="utf-8") as f:
                config = yaml.safe_load(f)

            if not config:
                return ServiceResult.fail("Invalid or empty meltano.yml")

            return ServiceResult.success(config)

        except Exception as e:
            error_msg = f"Failed to load project config: {e}"
            self.logger.exception(error_msg, error=str(e))
            return ServiceResult.fail(error_msg)

    async def save_project_config(self, project_name: str, config: dict[str, Any]) -> ServiceResult[None]:
        """Save Meltano project configuration."""
        try:
            project_path = self.project_root / project_name
            meltano_yml = project_path / "meltano.yml"

            # Create backup
            if meltano_yml.exists():
                backup_path = meltano_yml.with_suffix(".yml.backup")
                shutil.copy2(meltano_yml, backup_path)

            # Save configuration
            with meltano_yml.open("w", encoding="utf-8") as f:
                yaml.safe_dump(config, f, default_flow_style=False, indent=2)

            return ServiceResult.success(None)

        except Exception as e:
            error_msg = f"Failed to save project config: {e}"
            self.logger.exception(error_msg, error=str(e))
            return ServiceResult.fail(error_msg)

    async def run_command(self, project_name: str, command_args: list[str], environment: str = "dev") -> ServiceResult[dict[str, Any]]:
        """Execute Meltano command in project context."""
        try:
            project_path = self.project_root / project_name

            if not project_path.exists():
                return ServiceResult.fail(f"Project not found: {project_path}")

            # Build command
            cmd = ["meltano"]
            if environment != "dev":
                cmd.extend(["--environment", environment])
            cmd.extend(command_args)

            self.logger.info("Executing Meltano command", command=cmd, project_path=str(project_path))

            # Execute command
            process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=project_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )

            stdout, stderr = await process.communicate()

            result = {
                "command": " ".join(cmd),
                "returncode": process.returncode,
                "stdout": stdout.decode() if stdout else "",
                "stderr": stderr.decode() if stderr else "",
                "success": process.returncode == 0,
            }

            if process.returncode != 0:
                self.logger.error("Meltano command failed", **result)
                return ServiceResult.fail(f"Command failed: {result['stderr']}")

            self.logger.info("Meltano command completed successfully", **result)
            return ServiceResult.success(result)

        except Exception as e:
            error_msg = f"Failed to execute command: {e}"
            self.logger.exception(error_msg, error=str(e))
            return ServiceResult.fail(error_msg)

    async def add_plugin(self, project_name: str, plugin_type: str, plugin_name: str, **plugin_config: Any) -> ServiceResult[dict[str, Any]]:
        """Add plugin to Meltano project."""
        try:
            # Load current config
            config_result = await self.load_project_config(project_name)
            if not config_result.is_success:
                return ServiceResult.fail(config_result.error)

            config = config_result.value

            # Add plugin to config
            if plugin_type not in config["plugins"]:
                config["plugins"][plugin_type] = []

            plugin_entry = {
                "name": plugin_name,
                **plugin_config,
            }

            config["plugins"][plugin_type].append(plugin_entry)

            # Save config
            save_result = await self.save_project_config(project_name, config)
            if not save_result.is_success:
                return save_result

            result = {
                "plugin_type": plugin_type,
                "plugin_name": plugin_name,
                "plugin_config": plugin_entry,
            }

            self.logger.info("Plugin added successfully", **result)
            return ServiceResult.success(result)

        except Exception as e:
            error_msg = f"Failed to add plugin: {e}"
            self.logger.exception(error_msg, error=str(e))
            return ServiceResult.fail(error_msg)

    async def validate_project(self, project_name: str) -> ServiceResult[dict[str, Any]]:
        """Validate Meltano project structure and configuration."""
        try:
            project_path = self.project_root / project_name

            validation_results = {
                "project_exists": project_path.exists(),
                "config_exists": (project_path / "meltano.yml").exists(),
                "meltano_dir_exists": (project_path / ".meltano").exists(),
                "config_valid": False,
                "errors": [],
            }

            if not validation_results["project_exists"]:
                validation_results["errors"].append("Project directory does not exist")
                return ServiceResult.success(validation_results)

            if not validation_results["config_exists"]:
                validation_results["errors"].append("meltano.yml not found")
                return ServiceResult.success(validation_results)

            # Validate config structure
            config_result = await self.load_project_config(project_name)
            if config_result.is_success:
                config = config_result.value

                required_fields = ["version", "project_id", "plugins"]
                missing_fields = [field for field in required_fields if field not in config]

                if missing_fields:
                    validation_results["errors"].extend([f"Missing field: {field}" for field in missing_fields])
                else:
                    validation_results["config_valid"] = True
            else:
                validation_results["errors"].append(f"Config validation failed: {config_result.error}")

            validation_results["is_valid"] = (
                validation_results["project_exists"] and
                validation_results["config_exists"] and
                validation_results["config_valid"] and
                not validation_results["errors"]
            )

            return ServiceResult.success(validation_results)

        except Exception as e:
            error_msg = f"Failed to validate project: {e}"
            self.logger.exception(error_msg, error=str(e))
            return ServiceResult.fail(error_msg)


class FlextProjectManager(MeltanoProjectManager):
    """Enhanced project manager with FLEXT enterprise features."""

    def __init__(self, project_root: Path | str, event_bus: Any | None = None) -> None:
        super().__init__(project_root)
        self.event_bus = event_bus

    async def create_project_with_events(self, project_name: str, environment: str = "dev") -> ServiceResult[dict[str, Any]]:
        """Create project and publish domain events."""
        result = await self.create_project(project_name, environment)

        if result.is_success and self.event_bus:
            await self.event_bus.publish(
                DomainEvent(
                    event_type="meltano.project.created",
                    data={
                        "project_name": project_name,
                        "environment": environment,
                        "created_at": datetime.now(UTC).isoformat(),
                    },
                ),
            )

        return result

    async def backup_project(self, project_name: str, backup_path: Path) -> ServiceResult[Path]:
        """Create project backup archive."""
        try:
            project_path = self.project_root / project_name

            if not project_path.exists():
                return ServiceResult.fail(f"Project not found: {project_path}")

            # Ensure backup directory exists
            backup_path.parent.mkdir(parents=True, exist_ok=True)

            # Create backup archive
            await asyncio.to_thread(
                shutil.make_archive,
                str(backup_path.with_suffix("")),
                "zip",
                project_path,
            )

            backup_file = backup_path.with_suffix(".zip")

            if self.event_bus:
                await self.event_bus.publish(
                    DomainEvent(
                        event_type="meltano.project.backup_created",
                        data={
                            "project_name": project_name,
                            "backup_path": str(backup_file),
                            "backup_size": backup_file.stat().st_size,
                            "created_at": datetime.now(UTC).isoformat(),
                        },
                    ),
                )

            return ServiceResult.success(backup_file)

        except Exception as e:
            error_msg = f"Failed to backup project: {e}"
            self.logger.exception(error_msg, error=str(e))
            return ServiceResult.fail(error_msg)
