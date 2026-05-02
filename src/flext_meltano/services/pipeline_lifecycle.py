"""FLEXT Meltano Pipeline Lifecycle - Status, stop, and delete operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import os
import shutil
import signal
import time
from pathlib import Path

from flext_meltano import FlextMeltanoPipelinePaths, c, p, r


class FlextMeltanoPipelineLifecycleOperations(FlextMeltanoPipelinePaths):
    """Static lifecycle operations for pipelines - status, stop, delete."""

    @staticmethod
    def _is_process_running(pid: int) -> bool:
        """Check if a process with the given PID is running."""
        if pid <= 0:
            return False
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        except PermissionError:
            return True
        except OSError:
            return False
        return True

    @staticmethod
    def _check_pipeline_dir(pipeline_name: str) -> p.Result[Path]:
        """Validate pipeline directory exists and return it."""
        pipeline_dir = FlextMeltanoPipelinePaths.pipeline_dir(pipeline_name)
        if not pipeline_dir.exists() or not pipeline_dir.is_dir():
            return r[Path].fail(f"Pipeline '{pipeline_name}' not found")
        return r[Path].ok(pipeline_dir)

    @staticmethod
    def _read_pid(pipeline_name: str) -> p.Result[tuple[int, Path]]:
        """Read PID from pipeline pid file, return (pid, pid_path)."""
        pid_path = FlextMeltanoPipelinePaths.pipeline_pid_path(pipeline_name)
        if not pid_path.exists():
            return r[tuple[int, Path]].fail(
                f"Pipeline '{pipeline_name}' is not running",
            )
        try:
            pid = int(pid_path.read_text(encoding=c.Cli.ENCODING_DEFAULT).strip())
        except c.EXC_OS_VALUE as exc:
            return r[tuple[int, Path]].fail(
                f"Failed to read PID for pipeline '{pipeline_name}': {exc}",
            )
        return r[tuple[int, Path]].ok((pid, pid_path))

    @staticmethod
    def get_pipeline_status(pipeline_name: str) -> p.Result[str]:
        """Get the status of a specific Meltano pipeline."""
        dir_check = FlextMeltanoPipelineLifecycleOperations._check_pipeline_dir(
            pipeline_name,
        )
        if dir_check.failure:
            return r[str].fail(dir_check.error)
        pid_path = FlextMeltanoPipelinePaths.pipeline_pid_path(pipeline_name)
        if not pid_path.exists():
            return r[str].ok("stopped")
        pid_result = FlextMeltanoPipelineLifecycleOperations._read_pid(pipeline_name)
        if pid_result.failure:
            return r[str].fail(
                f"Failed to read status for pipeline '{pipeline_name}': "
                f"{pid_result.error}",
            )
        pid, _ = pid_result.value
        if FlextMeltanoPipelineLifecycleOperations._is_process_running(pid):
            return r[str].ok("running")
        pid_path.unlink(missing_ok=True)
        return r[str].ok("stopped")

    @staticmethod
    def stop_pipeline(
        pipeline_name: str, timeout_seconds: float = 10.0
    ) -> p.Result[str]:
        """Stop a running Meltano pipeline."""
        dir_check = FlextMeltanoPipelineLifecycleOperations._check_pipeline_dir(
            pipeline_name,
        )
        if dir_check.failure:
            return r[str].fail(dir_check.error)
        pid_result = FlextMeltanoPipelineLifecycleOperations._read_pid(pipeline_name)
        if pid_result.failure:
            return r[str].fail(pid_result.error)
        pid, pid_path = pid_result.value
        if not FlextMeltanoPipelineLifecycleOperations._is_process_running(pid):
            pid_path.unlink(missing_ok=True)
            return r[str].fail(f"Pipeline '{pipeline_name}' is not running")
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pid_path.unlink(missing_ok=True)
            return r[str].fail(f"Pipeline '{pipeline_name}' is not running")
        except OSError as exc:
            return r[str].fail(f"Failed to stop pipeline '{pipeline_name}': {exc}")
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            if not FlextMeltanoPipelineLifecycleOperations._is_process_running(pid):
                pid_path.unlink(missing_ok=True)
                return r[str].ok("stopped")
            time.sleep(0.1)
        return r[str].fail(
            f"Pipeline '{pipeline_name}' did not stop within"
            f" {timeout_seconds:.1f} seconds",
        )

    @staticmethod
    def delete_pipeline(pipeline_name: str) -> p.Result[str]:
        """Delete a Meltano pipeline."""
        dir_check = FlextMeltanoPipelineLifecycleOperations._check_pipeline_dir(
            pipeline_name,
        )
        if dir_check.failure:
            return r[str].fail(dir_check.error)
        pipeline_dir = dir_check.value
        status_result = FlextMeltanoPipelineLifecycleOperations.get_pipeline_status(
            pipeline_name,
        )
        if status_result.failure:
            return r[str].fail(status_result.error)
        if status_result.value == c.Meltano.OperationStatus.RUNNING.value:
            return r[str].fail(
                f"Pipeline '{pipeline_name}' is running. Stop it before deletion",
            )
        try:
            shutil.rmtree(pipeline_dir)
        except OSError as exc:
            return r[str].fail(f"Failed to delete pipeline '{pipeline_name}': {exc}")
        if pipeline_dir.exists():
            return r[str].fail(f"Pipeline '{pipeline_name}' deletion was not confirmed")
        return r[str].ok("deleted")
