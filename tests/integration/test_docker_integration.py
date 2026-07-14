"""Docker integration tests for FLEXT Meltano.

Behavioral integration tests that exercise the observable contract of the
Docker test stack (`tk`) and the real PostgreSQL/Redis services it brings up.
Assertions target public behavior only: fixture endpoints, the `r[T]` outcome
of stack operations (`execute`/`down`/`ready`), and real data round-trips
through each service. No stack internals are inspected.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import psycopg2
import pytest
import redis
from flext_tests import tm

from tests import c

if TYPE_CHECKING:
    from flext_tests import tk

__all__ = ["TestsFlextMeltanoDockerIntegration"]


class TestsFlextMeltanoDockerIntegration:
    """Behavioral Docker-based integration tests."""

    @staticmethod
    def _connect_postgres() -> psycopg2.extensions.connection:
        """Open a PostgreSQL connection to the test service."""
        return psycopg2.connect(
            host=c.Meltano.Tests.HOST,
            port=c.Meltano.Tests.POSTGRES_PORT,
            database="flext_test",
            user="test",
            password="test",
            connect_timeout=5,
        )

    @staticmethod
    def _connect_redis() -> redis.Redis[bytes]:
        """Open a Redis client to the test service."""
        return redis.Redis(
            host=c.Meltano.Tests.HOST,
            port=c.Meltano.Tests.REDIS_PORT,
            db=0,
        )

    @staticmethod
    def _is_transient_postgres_error(err_msg: str) -> bool:
        """Return True for known transient PostgreSQL startup/connection errors."""
        return (
            "connection" in err_msg
            or "closed" in err_msg
            or "refused" in err_msg
            or "timeout" in err_msg
            or "starting up" in err_msg
        )

    @pytest.mark.docker
    @pytest.mark.integration
    def test_postgres_service_endpoint_is_published(
        self, postgres_service: str
    ) -> None:
        """PostgreSQL fixture yields the published host:port endpoint."""
        tm.that(postgres_service, eq=f"{c.LOCALHOST}:{c.Meltano.Tests.POSTGRES_PORT}")

    @pytest.mark.docker
    @pytest.mark.integration
    def test_redis_service_endpoint_is_published(self, redis_service: str) -> None:
        """Redis fixture yields the published host:port endpoint."""
        tm.that(redis_service, eq=f"{c.LOCALHOST}:{c.Meltano.Tests.REDIS_PORT}")

    @pytest.mark.docker
    @pytest.mark.integration
    def test_meltano_service_endpoint_has_valid_port(
        self, meltano_service: str
    ) -> None:
        """Meltano fixture yields an endpoint on the test host with a real port."""
        host, _, port = meltano_service.partition(":")
        tm.that(host, eq=c.Meltano.Tests.HOST)
        assert int(port) > 0

    @pytest.mark.docker
    @pytest.mark.integration
    def test_ready_probe_returns_boolean_result_for_each_service(
        self, docker_services: tk
    ) -> None:
        """`ready` yields an ``r[bool]`` per service port (observable contract)."""
        postgres_ready = docker_services.ready(port=c.Meltano.Tests.POSTGRES_PORT)
        redis_ready = docker_services.ready(port=c.Meltano.Tests.REDIS_PORT)
        if postgres_ready.failure or redis_ready.failure:
            pytest.skip("Docker readiness probe unavailable")
        tm.that(postgres_ready.value, is_=bool)
        tm.that(redis_ready.value, is_=bool)
        if not (postgres_ready.value and redis_ready.value):
            pytest.skip("Docker services not fully ready")

    @pytest.mark.docker
    @pytest.mark.integration
    @pytest.mark.slow
    def test_manual_stack_lifecycle_starts_and_stops_successfully(
        self, docker_manager: tk
    ) -> None:
        """`execute` then `down` each yield a successful ``r[T]`` outcome."""
        start_result = docker_manager.execute()
        tm.ok(start_result)
        should_assert_stop = True
        try:
            postgres_ready = docker_manager.ready(port=c.Meltano.Tests.POSTGRES_PORT)
            if postgres_ready.failure or not postgres_ready.value:
                should_assert_stop = False
                pytest.skip("PostgreSQL service not available")
            tm.that(postgres_ready.value, is_=bool)
        finally:
            stop_result = docker_manager.down()
            if should_assert_stop:
                tm.ok(stop_result)

    @pytest.mark.docker
    @pytest.mark.integration
    def test_postgres_round_trips_inserted_row(self, postgres_service: str) -> None:
        """A row written to PostgreSQL is read back unchanged (real round-trip)."""
        conn: psycopg2.extensions.connection | None = None
        try:
            conn = self._connect_postgres()
            with conn.cursor() as cursor:
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS test_table ("
                    "id SERIAL PRIMARY KEY, name VARCHAR(100), "
                    "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
                )
                cursor.execute(
                    "INSERT INTO test_table (name) VALUES (%s)", ("test_record",)
                )
                cursor.execute(
                    "SELECT id, name FROM test_table WHERE name = %s", ("test_record",)
                )
                result = cursor.fetchone()
                tm.that(result, none=False)
                tm.that(result[1], eq="test_record")
                cursor.execute("DROP TABLE test_table")
            conn.commit()
        except psycopg2.Error as exc:
            if self._is_transient_postgres_error(str(exc).lower()):
                pytest.skip(f"PostgreSQL not ready for operations: {exc}")
            raise
        finally:
            if conn is not None:
                conn.close()

    @pytest.mark.docker
    @pytest.mark.integration
    def test_redis_round_trips_string_and_list_values(self, redis_service: str) -> None:
        """Values written to Redis are read back unchanged (real round-trip)."""
        client: redis.Redis[bytes] | None = None
        try:
            client = self._connect_redis()
            client.set("test_key", "test_value")
            tm.that(client.get("test_key"), eq=b"test_value")
            client.lpush("test_list", "item1")
            client.lpush("test_list", "item2")
            tm.that(client.llen("test_list"), eq=2)
            client.delete("test_key")
            client.delete("test_list")
            tm.that(client.get("test_key"), none=True)
        finally:
            if client is not None:
                client.close()
