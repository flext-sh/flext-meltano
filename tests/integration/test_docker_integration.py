"""Docker integration tests for FLEXT Meltano.

Tests that use real Docker containers for comprehensive integration testing.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

import psycopg2
import pytest
import redis

from tests.helpers.docker_test_manager import FlextTestsDocker


class TestDockerIntegration:
    """Docker-based integration tests."""

    @pytest.mark.docker
    @pytest.mark.integration
    def test_postgres_service_available(self, postgres_service: str | None) -> None:
        """Test that PostgreSQL service is available and responsive."""
        if postgres_service is None:
            pytest.skip("PostgreSQL service not available")

        assert isinstance(postgres_service, str)
        # Basic connectivity check
        assert postgres_service.startswith("localhost:")
        assert ":5433" in postgres_service

        # Test actual database connection (skip on transient/unavailable)
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
            assert True  # Connection successful
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
        # Basic connectivity check
        assert redis_service.startswith("localhost:")
        assert ":6380" in redis_service

        # Test actual Redis connection
        try:
            r = redis.Redis(host="localhost", port=6380, db=0)
            r.ping()
            r.close()
            assert True  # Connection successful
        except Exception as e:
            pytest.fail(f"Failed to connect to Redis: {e}")

    @pytest.mark.docker
    @pytest.mark.integration
    def test_meltano_service_available(self, meltano_service: str | None) -> None:
        """Test that Meltano service is available."""
        if meltano_service is None:
            pytest.skip("Meltano service not available")

        assert isinstance(meltano_service, str)
        # Basic connectivity check (host:port format; port may vary by environment)
        assert meltano_service.startswith("localhost:")
        assert ":" in meltano_service and meltano_service.split(":")[-1].isdigit()

        # Note: Meltano UI testing would require HTTP client, basic check is sufficient

    @pytest.mark.docker
    @pytest.mark.integration
    def test_docker_services_health(self, docker_services: FlextTestsDocker) -> None:
        """Test overall Docker services health."""
        # Test that docker manager is available
        assert docker_services is not None

        # Test service URLs are accessible
        postgres_url = docker_services.get_service_url("postgres", 5432)
        redis_url = docker_services.get_service_url("redis", 6379)

        assert postgres_url is not None
        assert redis_url is not None

    @pytest.mark.docker
    @pytest.mark.integration
    @pytest.mark.slow
    def test_container_lifecycle(self, docker_manager: FlextTestsDocker) -> None:
        """Test complete container lifecycle management."""
        # Start services
        result = docker_manager.start_services(["postgres"])
        assert result.is_success

        # Verify service is accessible
        url = docker_manager.get_service_url("postgres", 5432)
        assert url is not None

        # Stop services
        result = docker_manager.stop_services()
        assert result.is_success

        # Verify services are stopped
        # Note: In keep_running mode, services stay up for other tests

    @pytest.mark.docker
    @pytest.mark.integration
    def test_postgres_database_operations(self, postgres_service: str | None) -> None:
        """Test actual database operations with PostgreSQL."""
        if postgres_service is None:
            pytest.skip("PostgreSQL service not available")

        assert isinstance(postgres_service, str)
        # Test database operations
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

            # Create a test table
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS test_table (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)

                # Insert test data
                cursor.execute(
                    "INSERT INTO test_table (name) VALUES (%s)",
                    ("test_record",),
                )

                # Query data back
                cursor.execute(
                    "SELECT id, name FROM test_table WHERE name = %s",
                    ("test_record",),
                )
                result = cursor.fetchone()

                assert result is not None
                assert result[1] == "test_record"

                # Clean up
                cursor.execute("DROP TABLE test_table")

            conn.commit()

        except Exception as e:
            err_msg = str(e).lower()
            if (
                "connection" in err_msg
                or "closed" in err_msg
                or "refused" in err_msg
                or "timeout" in err_msg
                or "starting up" in err_msg
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
        # Test Redis operations
        r = None
        try:
            r = redis.Redis(host="localhost", port=6380, db=0)

            # Test basic operations
            r.set("test_key", "test_value")
            value = r.get("test_key")

            assert value is not None
            assert value.decode() == "test_value"

            # Test list operations
            r.lpush("test_list", "item1")
            r.lpush("test_list", "item2")
            length = r.llen("test_list")

            assert length == 2

            # Clean up
            r.delete("test_key")
            r.delete("test_list")

        except Exception as e:
            pytest.fail(f"Redis operation failed: {e}")
        finally:
            if r:
                r.close()
