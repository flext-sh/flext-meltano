"""Docker integration tests for FLEXT Meltano.

Tests that use real Docker containers for comprehensive integration testing.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import psycopg2
import pytest
import redis
from flext_tests import tk

from tests.constants import c


class TestsFlextMeltanoDockerIntegration:
    """Docker-based integration tests."""

    @staticmethod
    def _connect_postgres() -> psycopg2.extensions.connection:
        """Create a PostgreSQL test connection."""
        return psycopg2.connect(
            host=c.Meltano.Tests.HOST,
            port=c.Meltano.Tests.POSTGRES_PORT,
            database="flext_test",
            user="test",
            password="test",
            connect_timeout=5,
        )

    @staticmethod
    def _assert_postgres_operations(conn: psycopg2.extensions.connection) -> None:
        """Assert canonical PostgreSQL create/insert/select/drop flow."""
        with conn.cursor() as cursor:
            cursor.execute(
                "\n                    CREATE TABLE IF NOT EXISTS test_table (\n                        id SERIAL PRIMARY KEY,\n                        name VARCHAR(100),\n                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n                    )\n                ",
            )
            cursor.execute(
                "INSERT INTO test_table (name) VALUES (%s)",
                ("test_record",),
            )
            cursor.execute(
                "SELECT id, name FROM test_table WHERE name = %s",
                ("test_record",),
            )
            result = cursor.fetchone()
            assert result is not None
            assert result[1] == "test_record"
            cursor.execute("DROP TABLE test_table")
        conn.commit()

    @staticmethod
    def _is_transient_postgres_error(err_msg: str) -> bool:
        """Return True for known transient PostgreSQL connection errors."""
        return (
            "connection" in err_msg
            or "closed" in err_msg
            or "refused" in err_msg
            or "timeout" in err_msg
            or "starting up" in err_msg
        )

    @staticmethod
    def _connect_redis() -> redis.Redis[bytes]:
        """Create a Redis test client."""
        return redis.Redis(
            host=c.Meltano.Tests.HOST,
            port=c.Meltano.Tests.REDIS_PORT,
            db=0,
        )

    @staticmethod
    def _assert_redis_operations(client: redis.Redis[bytes]) -> None:
        """Assert canonical Redis set/list/delete flow."""
        client.set("test_key", "test_value")
        value = client.get("test_key")
        assert value == b"test_value"
        client.lpush("test_list", "item1")
        client.lpush("test_list", "item2")
        length = client.llen("test_list")
        assert length == 2
        client.delete("test_key")
        client.delete("test_list")

    @pytest.mark.docker
    @pytest.mark.integration
    def test_postgres_service_available(self, postgres_service: str) -> None:
        """Test that PostgreSQL service is available and responsive."""
        assert postgres_service == f"{c.LOCALHOST}:{c.Meltano.Tests.POSTGRES_PORT}"
        try:
            conn = psycopg2.connect(
                host=c.Meltano.Tests.HOST,
                port=c.Meltano.Tests.POSTGRES_PORT,
                database="flext_test",
                user="test",
                password="test",
                connect_timeout=5,
            )
            conn.close()
        except Exception as e:
            err_msg = str(e).lower()
            if (
                "starting up" in err_msg
                or "connection refused" in err_msg
                or "timeout" in err_msg
            ):
                pytest.skip(f"PostgreSQL not ready: {e}")
            pytest.fail(f"Failed to connect to PostgreSQL: {e}")

    @pytest.mark.docker
    @pytest.mark.integration
    def test_redis_service_available(self, redis_service: str) -> None:
        """Test that Redis service is available and responsive."""
        assert redis_service == f"{c.LOCALHOST}:{c.Meltano.Tests.REDIS_PORT}"
        try:
            r = redis.Redis(
                host=c.Meltano.Tests.HOST,
                port=c.Meltano.Tests.REDIS_PORT,
                db=0,
            )
            r.ping()
            r.close()
        except Exception as e:
            pytest.fail(f"Failed to connect to Redis: {e}")

    @pytest.mark.docker
    @pytest.mark.integration
    def test_meltano_service_available(self, meltano_service: str) -> None:
        """Test that Meltano service is available."""
        host, _, port = meltano_service.partition(":")
        assert host == c.Meltano.Tests.HOST
        assert int(port) > 0

    @pytest.mark.docker
    @pytest.mark.integration
    def test_docker_services_health(self, docker_services: tk) -> None:
        """Test overall Docker services health."""
        postgres_ready = docker_services.ready(port=c.Meltano.Tests.POSTGRES_PORT)
        redis_ready = docker_services.ready(port=c.Meltano.Tests.REDIS_PORT)
        if postgres_ready.failure or not postgres_ready.value:
            pytest.skip("PostgreSQL service not available")
        if redis_ready.failure or not redis_ready.value:
            pytest.skip("Redis service not available")

    @pytest.mark.docker
    @pytest.mark.integration
    @pytest.mark.slow
    def test_container_lifecycle(self, docker_manager: tk) -> None:
        """Test complete container lifecycle management."""
        start_result = docker_manager.execute()
        assert start_result.success
        should_assert_stop = True
        try:
            postgres_ready = docker_manager.ready(port=c.Meltano.Tests.POSTGRES_PORT)
            if postgres_ready.failure or not postgres_ready.value:
                should_assert_stop = False
                pytest.skip("PostgreSQL service not available")
        finally:
            stop_result = docker_manager.down()
            if should_assert_stop:
                assert stop_result.success

    @pytest.mark.docker
    @pytest.mark.integration
    def test_postgres_database_operations(self, postgres_service: str) -> None:
        """Test actual database operations with PostgreSQL."""
        conn = None
        try:
            conn = self._connect_postgres()
            self._assert_postgres_operations(conn)
        except Exception as e:
            err_msg = str(e).lower()
            if self._is_transient_postgres_error(err_msg):
                pytest.skip(f"PostgreSQL not ready for operations: {e}")
            pytest.fail(f"Database operation failed: {e}")
        finally:
            if conn:
                conn.close()

    @pytest.mark.docker
    @pytest.mark.integration
    def test_redis_operations(self, redis_service: str) -> None:
        """Test actual Redis operations."""
        r = None
        try:
            r = self._connect_redis()
            self._assert_redis_operations(r)
        except Exception as e:
            pytest.fail(f"Redis operation failed: {e}")
        finally:
            if r:
                r.close()
