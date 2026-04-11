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


class TestDockerIntegration:
    """Docker-based integration tests."""

    @pytest.mark.docker
    @pytest.mark.integration
    def test_postgres_service_available(self, postgres_service: str | None) -> None:
        """Test that PostgreSQL service is available and responsive."""
        if postgres_service is None:
            pytest.skip("PostgreSQL service not available")
        assert isinstance(postgres_service, str)
        assert postgres_service.startswith("localhost:")
        assert ":5433" in postgres_service
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5433,
                database="flext_test",
                user="test",
                password="test",
                connect_timeout=5,
            )
            conn.close()
            assert True
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
    def test_redis_service_available(self, redis_service: str | None) -> None:
        """Test that Redis service is available and responsive."""
        if redis_service is None:
            pytest.skip("Redis service not available")
        assert isinstance(redis_service, str)
        assert redis_service.startswith("localhost:")
        assert ":6380" in redis_service
        try:
            r = redis.Redis(host="localhost", port=6380, db=0)
            r.ping()
            r.close()
            assert True
        except Exception as e:
            pytest.fail(f"Failed to connect to Redis: {e}")

    @pytest.mark.docker
    @pytest.mark.integration
    def test_meltano_service_available(self, meltano_service: str | None) -> None:
        """Test that Meltano service is available."""
        if meltano_service is None:
            pytest.skip("Meltano service not available")
        assert isinstance(meltano_service, str)
        assert meltano_service.startswith("localhost:")
        assert ":" in meltano_service and meltano_service.split(":")[-1].isdigit()

    @pytest.mark.docker
    @pytest.mark.integration
    def test_docker_services_health(self, docker_services: tk) -> None:
        """Test overall Docker services health."""
        postgres_ready = docker_services.wait_for_port_ready("localhost", 5433)
        redis_ready = docker_services.wait_for_port_ready("localhost", 6380)
        if postgres_ready.failure or not postgres_ready.value:
            pytest.skip("PostgreSQL service not available")
        if redis_ready.failure or not redis_ready.value:
            pytest.skip("Redis service not available")

    @pytest.mark.docker
    @pytest.mark.integration
    @pytest.mark.slow
    def test_container_lifecycle(self, docker_manager: tk) -> None:
        """Test complete container lifecycle management."""
        start_result = docker_manager.start_compose_stack("docker-compose.test.yml")
        assert start_result.success
        should_assert_stop = True
        try:
            postgres_ready = docker_manager.wait_for_port_ready("localhost", 5433)
            if postgres_ready.failure or not postgres_ready.value:
                should_assert_stop = False
                pytest.skip("PostgreSQL service not available")
        finally:
            stop_result = docker_manager.compose_down("docker-compose.test.yml")
            if should_assert_stop:
                assert stop_result.success

    @pytest.mark.docker
    @pytest.mark.integration
    def test_postgres_database_operations(self, postgres_service: str | None) -> None:
        """Test actual database operations with PostgreSQL."""
        if postgres_service is None:
            pytest.skip("PostgreSQL service not available")
        assert isinstance(postgres_service, str)
        conn = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5433,
                database="flext_test",
                user="test",
                password="test",
                connect_timeout=5,
            )
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
        except Exception as e:
            err_msg = str(e).lower()
            if (
                "connection" in err_msg
                or "closed" in err_msg
                or "refused" in err_msg
                or ("timeout" in err_msg)
                or ("starting up" in err_msg)
            ):
                pytest.skip(f"PostgreSQL not ready for operations: {e}")
            pytest.fail(f"Database operation failed: {e}")
        finally:
            if conn:
                conn.close()

    @pytest.mark.docker
    @pytest.mark.integration
    def test_redis_operations(self, redis_service: str | None) -> None:
        """Test actual Redis operations."""
        if redis_service is None:
            pytest.skip("Redis service not available")
        assert isinstance(redis_service, str)
        r = None
        try:
            r = redis.Redis(host="localhost", port=6380, db=0)
            r.set("test_key", "test_value")
            value = r.get("test_key")
            assert value == b"test_value"
            r.lpush("test_list", "item1")
            r.lpush("test_list", "item2")
            length = r.llen("test_list")
            assert length == 2
            r.delete("test_key")
            r.delete("test_list")
        except Exception as e:
            pytest.fail(f"Redis operation failed: {e}")
        finally:
            if r:
                r.close()
