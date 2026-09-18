# from flext-meltano_docs/architecture/system-context.md:291
from __future__ import annotations


class MeltanoAdapter:
    """Meltano CLI integration with proper error handling."""

    def run_meltano_command(self, command: str, **kwargs) -> p.Result[MeltanoResult]:
        """Execute Meltano CLI command safely."""
        # Build command with proper escaping
        cmd = ["meltano", command]
        if kwargs:
            for key, value in kwargs.items():
                cmd.extend([f"--{key}", str(value)])

        try:
            # Execute with timeout and proper error handling
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.command_timeout,
                cwd=self.project_root,
            )

            if result.returncode == 0:
                return r.ok(
                    MeltanoResult(success=True, output=result.stdout, command=cmd)
                )
            return r.fail(
                MeltanoExecutionError(
                    f"Meltano command failed: {result.stderr}",
                    command=cmd,
                    return_code=result.returncode,
                )
            )

        except subprocess.TimeoutExpired:
            return r.fail(
                MeltanoTimeoutError(
                    f"Meltano command timed out after {self.command_timeout}s",
                    command=cmd,
                )
            )```
#### Singer SDK Integration

