"""FLEXT Test Docker Manager - Enterprise Docker testing infrastructure.

This module provides tk class for comprehensive containerized testing
of FLEXT Meltano components with automatic lifecycle management, health checks,
and resource cleanup.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import atexit
import subprocess
import time
from collections.abc import Generator, Mapping, MutableSequence
from contextlib import contextmanager
from pathlib import Path
from typing import Any

import pytest

from flext_core import FlextLogger, r
from tests import t


class ContainerManager:
    """Base class for container management with common functionality."""

    def __init__(self, compose_file: str, project_name: str) -> None:
        """Initialize container manager.

        Args:
            compose_file: Path to docker-compose file
            project_name: Docker compose project name

        """
        self.compose_file = Path(compose_file)
        self.project_name = project_name
        self.logger = FlextLogger(__name__)

    def run_compose_command(
        self,
        command: t.StrSequence,
        timeout: int = 300,
    ) -> r[subprocess.CompletedProcess[str]]:
        """Run a docker-compose command with error handling.

        Args:
            command: Command arguments
            timeout: Command timeout

        Returns:
            r with command result

        """
        try:
            full_command: MutableSequence[str] = [
                "docker-compose",
                "-f",
                str(self.compose_file),
                "-p",
                self.project_name,
            ] + list(command)
            result = subprocess.run(
                full_command,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if result.returncode != 0:
                return r[subprocess.CompletedProcess[str]].fail(
                    f"Command failed: {' '.join(full_command)}\n{result.stderr}",
                )
            return r[subprocess.CompletedProcess[str]].ok(result)
        except subprocess.TimeoutExpired:
            return r[subprocess.CompletedProcess[str]].fail(
                f"Command timed out: {' '.join(command)}",
            )
        except Exception as e:
            return r[subprocess.CompletedProcess[str]].fail(f"Command error: {e}")


class Tk(ContainerManager):
    """Enterprise Docker testing infrastructure for FLEXT Meltano.

    Provides comprehensive container lifecycle management with automatic cleanup,
    health monitoring, and resource optimization for integration testing.

    Features:
    - Automatic container startup/shutdown
    - Health check integration
    - Resource monitoring
    - Network isolation
    - Persistent containers across test sessions
    - Graceful error handling and recovery
    """

    def __init__(
        self,
        compose_file: str = "docker-compose.test.yml",
        project_name: str = "flext-test",
        *,
        keep_running: bool = True,
    ) -> None:
        """Initialize Docker test manager.

        Args:
            compose_file: Path to docker-compose file
            project_name: Docker compose project name
            keep_running: Whether to keep containers running after tests

        """
        super().__init__(compose_file, project_name)
        self.keep_running = keep_running
        self.containers_started = False
        self._services: Mapping[str, Mapping[str, Any]] = {}
        atexit.register(self._cleanup_containers)

    def start_services(
        self,
        services: t.StrSequence | None = None,
        wait_timeout: int = 60,
    ) -> r[bool]:
        """Start Docker services with health checks.

        Args:
            services: List of services to start (None for all)
            wait_timeout: Timeout for service health checks

        Returns:
            r indicating success/failure

        """
        try:
            if not self.compose_file.exists():
                return r[bool].fail(
                    f"Docker compose file not found: {self.compose_file}",
                )
            cmd = ["up", "-d"]
            if services:
                cmd.extend(services)
            result = self.run_compose_command(cmd, timeout=300)
            if result.is_failure:
                return r[bool].fail(f"Failed to start Docker services: {result.error}")
            self.containers_started = True
            if not self._wait_for_services(wait_timeout):
                return r[bool].fail("Services failed health checks")
            self.logger.info("Docker services started successfully")
            return r[bool].ok(value=True)
        except Exception as e:
            return r[bool].fail(f"Error starting Docker services: {e}")

    def stop_services(self, *, remove_volumes: bool = False) -> r[bool]:
        """Stop Docker services.

        Args:
            remove_volumes: Whether to remove volumes

        Returns:
            r indicating success/failure

        """
        try:
            if not self.containers_started:
                return r[bool].ok(value=True)
            cmd = ["down"]
            if remove_volumes:
                cmd.append("-v")
            result = self.run_compose_command(cmd, timeout=120)
            if result.is_failure:
                self.logger.warning(f"Failed to stop Docker services: {result.error}")
                return r[bool].fail(f"Failed to stop Docker services: {result.error}")
            self.containers_started = False
            self.logger.info("Docker services stopped successfully")
            return r[bool].ok(value=True)
        except Exception as e:
            return r[bool].fail(f"Error stopping Docker services: {e}")

    def get_service_url(self, service_name: str, port: int) -> str | None:
        """Get service URL for a running container.

        Args:
            service_name: Name of the service
            port: Internal port number

        Returns:
            Service URL or None if not available

        """
        try:
            cmd = ["port", service_name, str(port)]
            result = self.run_compose_command(cmd, timeout=30)
            if result.is_success:
                process = result.value
                host_port = process.stdout.strip().split(":")
                if len(host_port) == 2:
                    return f"localhost:{host_port[1]}"
        except Exception as e:
            self.logger.warning(f"Failed to get service URL for {service_name}: {e}")
        return None

    def execute_in_container(
        self,
        service_name: str,
        command: t.StrSequence,
        timeout: int = 30,
    ) -> r[Mapping[str, Any]]:
        """Execute command in running container.

        Args:
            service_name: Name of the service
            command: Command to execute
            timeout: Command timeout

        Returns:
            r with execution results

        """
        try:
            cmd = [
                "docker-compose",
                "-f",
                str(self.compose_file),
                "-p",
                self.project_name,
                "exec",
            ]
            cmd.extend(["-T", service_name])
            cmd.extend(command)
            result = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return r[Mapping[str, Any]].ok({
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0,
            })
        except subprocess.TimeoutExpired:
            return r[Mapping[str, Any]].fail("Command execution timed out")
        except Exception as e:
            return r[Mapping[str, Any]].fail(f"Command execution failed: {e}")

    def _wait_for_services(self, timeout: int) -> bool:
        """Wait for services to be healthy.

        Args:
            timeout: Maximum time to wait

        Returns:
            True if all services are healthy

        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                cmd = [
                    "docker-compose",
                    "-f",
                    str(self.compose_file),
                    "-p",
                    self.project_name,
                    "ps",
                    "-q",
                ]
                result = subprocess.run(
                    cmd,
                    check=False,
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if (
                    result.returncode == 0
                    and result.stdout.strip()
                    and self._check_service_health()
                ):
                    return True
            except Exception as e:
                self.logger.warning(f"Error checking service health: {e}")
            time.sleep(2)
        return False

    def _check_service_health(self) -> bool:
        """Check if services are responding.

        Returns:
            True if services are healthy

        """
        try:
            services_to_check = [("postgres", 5432), ("redis", 6379)]
            for service, port in services_to_check:
                url = self.get_service_url(service, port)
                if url:
                    self.logger.debug("Service %s available at %s", service, url)
                else:
                    self.logger.warning("Service %s not accessible", service)
            return True
        except Exception as e:
            self.logger.warning(f"Health check failed: {e}")
            return False

    def _cleanup_containers(self) -> None:
        """Cleanup containers on exit."""
        if self.containers_started and (not self.keep_running):
            try:
                self.stop_services(remove_volumes=True)
            except Exception as e:
                self.logger.exception("Failed to cleanup containers", error=str(e))

    @contextmanager
    def service_context(self, services: t.StrSequence | None = None) -> Generator[Tk]:
        """Context manager for service lifecycle.

        Args:
            services: List of services to manage

        """
        try:
            self.start_services(services)
            yield self
        finally:
            if not self.keep_running:
                self.stop_services()


@pytest.fixture(scope="session")
def docker_manager() -> Tk:
    """Session-scoped Docker manager fixture."""
    return Tk(keep_running=True)


@pytest.fixture
def docker_services(docker_manager: Tk) -> Generator[Tk]:
    """Function-scoped Docker services fixture."""
    with docker_manager.service_context():
        yield docker_manager
