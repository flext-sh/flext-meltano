"""Meltano executor for FLEXT integration."""

from __future__ import annotations

import subprocess
import time
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .config import MeltanoConfig


class MeltanoExecutor:
    """Executes Meltano operations via FLEXT integration."""

    def __init__(self, config: MeltanoConfig) -> None:
        """Initialize Meltano executor."""
        self.config = config

    def run_pipeline(
        self,
        extractor: str | None = None,
        loader: str | None = None,
        transform: str | None = None,
        environment: str = "dev",
        variables: dict[str, Any] | None = None,
        dry_run: bool = False,
        job_id: str | None = None,
    ) -> dict[str, Any]:
        """Run a Meltano pipeline."""
        if not job_id:
            job_id = f"meltano-run-{int(time.time())}"

        start_time = time.time()

        try:
            # Build meltano command
            cmd_args = [self.config.meltano_path, "run"]

            if extractor:
                cmd_args.append(extractor)
            if loader:
                cmd_args.append(loader)

            # Execute command
            env = {"MELTANO_ENVIRONMENT": environment}
            if variables:
                env.update(
                    {f"MELTANO_VAR_{k.upper()}": str(v) for k, v in variables.items()}
                )

            if dry_run:
                return {
                    "job_id": job_id,
                    "status": "success",
                    "exit_code": 0,
                    "output": f"DRY RUN: Would execute: {' '.join(filter(None, cmd_args))}",
                    "start_time": start_time,
                    "end_time": time.time(),
                }

            result = subprocess.run(
                [arg for arg in cmd_args if arg is not None],
                check=False,
                cwd=self.config.project_dir,
                capture_output=True,
                text=True,
                env=env,
                timeout=1800,  # 30 minutes timeout
            )

            return {
                "job_id": job_id,
                "status": "success" if result.returncode == 0 else "error",
                "exit_code": result.returncode,
                "output": result.stdout,
                "error_output": result.stderr if result.returncode != 0 else "",
                "start_time": start_time,
                "end_time": time.time(),
            }

        except subprocess.TimeoutExpired:
            return {
                "job_id": job_id,
                "status": "error",
                "exit_code": 124,
                "output": "",
                "error_output": "Pipeline execution timed out after 30 minutes",
                "start_time": start_time,
                "end_time": time.time(),
            }
        except Exception as e:
            return {
                "job_id": job_id,
                "status": "error",
                "exit_code": 1,
                "output": "",
                "error_output": str(e),
                "start_time": start_time,
                "end_time": time.time(),
            }

    def test_plugin(self, plugin_name: str, environment: str = "dev") -> dict[str, Any]:
        """Test a Meltano plugin."""
        job_id = f"meltano-test-{plugin_name}-{int(time.time())}"
        start_time = time.time()

        try:
            cmd_args = [self.config.meltano_path, "invoke", plugin_name, "--help"]

            result = subprocess.run(
                [arg for arg in cmd_args if arg is not None],
                check=False,
                cwd=self.config.project_dir,
                capture_output=True,
                text=True,
                env={"MELTANO_ENVIRONMENT": environment},
                timeout=300,  # 5 minutes timeout
            )

            return {
                "job_id": job_id,
                "status": "success" if result.returncode == 0 else "error",
                "exit_code": result.returncode,
                "output": result.stdout,
                "error_output": result.stderr if result.returncode != 0 else "",
                "plugin_name": plugin_name,
                "test_type": "help_command",
                "start_time": start_time,
                "end_time": time.time(),
            }

        except Exception as e:
            return {
                "job_id": job_id,
                "status": "error",
                "exit_code": 1,
                "output": "",
                "error_output": str(e),
                "plugin_name": plugin_name,
                "test_type": "help_command",
                "start_time": start_time,
                "end_time": time.time(),
            }

    def describe_plugin(self, plugin_name: str) -> dict[str, Any]:
        """Describe a Meltano plugin."""
        job_id = f"meltano-describe-{plugin_name}-{int(time.time())}"
        start_time = time.time()

        try:
            cmd_args = [self.config.meltano_path, "describe", plugin_name]

            result = subprocess.run(
                [arg for arg in cmd_args if arg is not None],
                check=False,
                cwd=self.config.project_dir,
                capture_output=True,
                text=True,
                timeout=120,  # 2 minutes timeout
            )

            return {
                "job_id": job_id,
                "status": "success" if result.returncode == 0 else "error",
                "exit_code": result.returncode,
                "output": result.stdout,
                "error_output": result.stderr if result.returncode != 0 else "",
                "plugin_name": plugin_name,
                "description_type": "meltano_describe",
                "start_time": start_time,
                "end_time": time.time(),
            }

        except Exception as e:
            return {
                "job_id": job_id,
                "status": "error",
                "exit_code": 1,
                "output": "",
                "error_output": str(e),
                "plugin_name": plugin_name,
                "description_type": "meltano_describe",
                "start_time": start_time,
                "end_time": time.time(),
            }
