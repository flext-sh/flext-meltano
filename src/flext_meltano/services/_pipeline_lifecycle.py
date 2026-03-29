"""FLEXT Meltano Pipeline Lifecycle - Status, stop, and delete operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import contextlib
import os
import shutil
import signal
import time
from pathlib import Path

from flext_core import r

from flext_meltano import u
from flext_meltano.services._pipeline_ops import FlextMeltanoPipelinePaths


class FlextMeltanoPipelineLifecycleOperations(FlextMeltanoPipelinePaths):
    """Static lifecycle operations for pipelines - status, stop, delete."""

    @staticmethod
    def _safe_unlink(path: Path) -> None:
        """Remove a file, ignoring missing or inaccessible errors."""
        with contextlib.suppress(FileNotFoundError, OSError):
            path.unlink()

    @staticmethod
    def _check_pipeline_dir(pipeline_name: str) -> r[Path]:
        """Validate pipeline directory exists and return it."""
        pipeline_dir = FlextMeltanoPipelinePaths.pipeline_dir(pipeline_name)
        if not pipeline_dir.exists() or not pipeline_dir.is_dir():
            return r[Path].fail(f"Pipeline '{pipeline_name}' not found")
        return r[Path].ok(pipeline_dir)

    @staticmethod
    def _read_pid(pipeline_name: str) -> r[tuple[int, Path]]:
        """Read PID from pipeline pid file, return (pid, pid_path)."""
        pid_path = FlextMeltanoPipelinePaths.pipeline_pid_path(pipeline_name)
        if not pid_path.exists():
            return r[tuple[int, Path]].fail(
                f"Pipeline '{pipeline_name}' is not running",
            )
        try:
            pid = int(pid_path.read_text(encoding="utf-8").strip())
        except (ValueError, OSError) as exc:
            return r[tuple[int, Path]].fail(
                f"Failed to read PID for pipeline '{pipeline_name}': {exc}",
            )
        return r[tuple[int, Path]].ok((pid, pid_path))

    @staticmethod
    def get_pipeline_status(pipeline_name: str) -> r[str]:
        """Get the status of a specific Meltano pipeline."""
        dir_check = FlextMeltanoPipelineLifecycleOperations._check_pipeline_dir(
            pipeline_name,
        )
        if dir_check.is_failure:
            return r[str].fail(dir_check.error)
        pid_path = FlextMeltanoPipelinePaths.pipeline_pid_path(pipeline_name)
        if not pid_path.exists():
            return r[str].ok("stopped")
        pid_result = FlextMeltanoPipelineLifecycleOperations._read_pid(pipeline_name)
        if pid_result.is_failure:
            return r[str].fail(
                f"Failed to read status for pipeline '{pipeline_name}': "
                f"{pid_result.error}",
            )
        pid, _ = pid_result.value
        if u.Meltano.is_process_running(pid):
            return r[str].ok("running")
        pid_path.unlink(missing_ok=True)
        return r[str].ok("stopped")

    @staticmethod
    def stop_pipeline(pipeline_name: str, timeout_seconds: float = 10.0) -> r[str]:
        """Stop a running Meltano pipeline."""
        dir_check = FlextMeltanoPipelineLifecycleOperations._check_pipeline_dir(
            pipeline_name,
        )
        if dir_check.is_failure:
            return r[str].fail(dir_check.error)
        pid_result = FlextMeltanoPipelineLifecycleOperations._read_pid(pipeline_name)
        if pid_result.is_failure:
            return r[str].fail(pid_result.error)
        pid, pid_path = pid_result.value
        if not u.Meltano.is_process_running(pid):
            FlextMeltanoPipelineLifecycleOperations._safe_unlink(pid_path)
            return r[str].fail(f"Pipeline '{pipeline_name}' is not running")
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            FlextMeltanoPipelineLifecycleOperations._safe_unlink(pid_path)
            return r[str].fail(f"Pipeline '{pipeline_name}' is not running")
        except OSError as exc:
            return r[str].fail(f"Failed to stop pipeline '{pipeline_name}': {exc}")
        deadline = time.monotonic() + timeout_seconds
        while time.monotonic() < deadline:
            if not u.Meltano.is_process_running(pid):
                FlextMeltanoPipelineLifecycleOperations._safe_unlink(pid_path)
                return r[str].ok("stopped")
            time.sleep(0.1)
        return r[str].fail(
            f"Pipeline '{pipeline_name}' did not stop within"
            f" {timeout_seconds:.1f} seconds",
        )

    @staticmethod
    def delete_pipeline(pipeline_name: str) -> r[str]:
        """Delete a Meltano pipeline."""
        dir_check = FlextMeltanoPipelineLifecycleOperations._check_pipeline_dir(
            pipeline_name,
        )
        if dir_check.is_failure:
            return r[str].fail(dir_check.error)
        pipeline_dir = dir_check.value
        status_result = FlextMeltanoPipelineLifecycleOperations.get_pipeline_status(
            pipeline_name,
        )
        if status_result.is_failure:
            return r[str].fail(status_result.error)
        if status_result.value == "running":
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
