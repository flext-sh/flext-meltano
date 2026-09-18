# from flext-meltano/docs/architecture/quality-attributes.md:280
from __future__ import annotations


class ConnectionPoolManager:
    """Intelligent connection pooling for external services."""

    def __init__(self, pool_configs: Dict[str, PoolConfig]):
        self.pools: Dict[str, ConnectionPool] = {}
        self.pool_configs = pool_configs
        self.metrics = PoolMetrics()

    def get_connection(self, service_name: str) -> Connection:
        """Get connection from appropriate pool."""
        if service_name not in self.pools:
            self._create_pool(service_name)

        pool = self.pools[service_name]

        try:
            connection = pool.get_connection()
            self.metrics.connection_acquired(service_name)
            return connection

        except PoolExhaustedError:
            self.metrics.pool_exhausted(service_name)
            # Implement backoff and retry logic
            raise PoolExhaustedError(f"Pool exhausted for {service_name}")

    def release_connection(self, service_name: str, connection: Connection) -> None:
        """Release connection back to pool."""
        if service_name in self.pools:
            self.pools[service_name].release_connection(connection)
            self.metrics.connection_released(service_name)

    def _create_pool(self, service_name: str) -> None:
        """Create connection pool for service."""
        settings = self.pool_configs.get(service_name)
        if not settings:
            raise ConfigurationError(f"No pool settings for {service_name}")

        pool = ConnectionPool(
            host=settings.host,
            port=settings.port,
            max_connections=settings.max_connections,
            min_connections=settings.min_connections,
            max_idle_time=settings.max_idle_time,
            health_check_interval=settings.health_check_interval,
        )

        self.pools[service_name] = pool
        self.metrics.pool_created(service_name)

    def health_check(self) -> Dict[str, PoolHealth]:
        """Perform health check on all pools."""
        health_status = {}

        for service_name, pool in self.pools.items():
            try:
                # Test connection
                conn = pool.get_connection()
                # Perform simple operation
                conn.ping()
                pool.release_connection(conn)

                health_status[service_name] = PoolHealth.HEALTHY

            except Exception as e:
                self.metrics.pool_health_check_failed(service_name, str(e))
                health_status[service_name] = PoolHealth.UNHEALTHY

        return health_status```
#### 3. Async Processing

