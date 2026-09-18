# from flext-meltano_docs/architecture/quality-attributes.md:817
from __future__ import annotations


class DataScaler:
    """Data layer scaling with sharding and replication."""

    def __init__(self, database_client, sharding_config: ShardingConfig):
        self.db = database_client
        self.settings = sharding_config
        self.shard_manager = ShardManager(self.settings)

    def evaluate_data_scaling(self, metrics: DataMetrics) -> List[DataScalingAction]:
        """Evaluate data growth and determine scaling actions."""
        actions = []

        # Check table sizes
        for table_name, table_metrics in metrics.table_sizes.items():
            if table_metrics.size_gb > self.settings.max_table_size_gb:
                actions.append(
                    DataScalingAction(
                        action_type="shard_table",
                        table_name=table_name,
                        reason=f"Table size: {table_metrics.size_gb:.1f}GB exceeds limit",
                        shard_key=self._select_shard_key(table_name),
                    )
                )

        # Check query performance
        for query_name, query_metrics in metrics.query_performance.items():
            if query_metrics.avg_execution_time > self.settings.max_query_time_seconds:
                if query_metrics.table_size > self.settings.partition_threshold_gb:
                    actions.append(
                        DataScalingAction(
                            action_type="add_partition",
                            table_name=query_metrics.table_name,
                            reason=f"Slow query: {query_metrics.avg_execution_time:.2f}s",
                            partition_key=self._select_partition_key(query_metrics),
                        )
                    )

        # Check read/write ratios
        for table_name, rw_metrics in metrics.read_write_ratios.items():
            if rw_metrics.read_ratio > self.settings.read_replica_threshold:
                actions.append(
                    DataScalingAction(
                        action_type="add_read_replica",
                        table_name=table_name,
                        reason=f"High read ratio: {rw_metrics.read_ratio:.2f}",
                        replica_count=self._calculate_replica_count(rw_metrics),
                    )
                )

        return actions

    def execute_data_scaling(
        self, actions: List[DataScalingAction]
    ) -> List[DataScalingResult]:
        """Execute data scaling actions."""
        results = []

        for action in actions:
            try:
                if action.action_type == "shard_table":
                    result = self._execute_table_sharding(action)
                elif action.action_type == "add_partition":
                    result = self._execute_partitioning(action)
                elif action.action_type == "add_read_replica":
                    result = self._execute_read_replica(action)
                else:
                    raise ValueError(f"Unknown action type: {action.action_type}")

                results.append(
                    DataScalingResult(action=action, success=True, result=result)
                )

            except Exception as e:
                results.append(
                    DataScalingResult(action=action, success=False, error=str(e))
                )

        return results

    def _execute_table_sharding(self, action: DataScalingAction) -> ShardingResult:
        """Execute table sharding."""
        # Create shard key index if needed
        self.db.create_index(action.table_name, action.shard_key)

        # Calculate shard distribution
        shard_count = self._calculate_shard_count(action.table_name)
        shards = self.shard_manager.create_shards(action.table_name, shard_count)

        # Redistribute data
        redistribution_result = self._redistribute_data(action.table_name, shards)

        return ShardingResult(
            table_name=action.table_name,
            shard_count=shard_count,
            shards=shards,
            redistribution_result=redistribution_result,
        )

    def _calculate_shard_count(self, table_name: str) -> int:
        """Calculate optimal shard count based on data size and access patterns."""
        table_size = self.db.get_table_size(table_name)
        access_patterns = self.db.get_access_patterns(table_name)

        # Base calculation on data size
        base_shards = max(2, table_size // self.settings.shard_size_gb)

        # Adjust for access patterns
        if access_patterns.is_write_heavy:
            # Fewer, larger shards for write-heavy workloads
            shard_count = max(2, base_shards // 2)
        else:
            # More shards for read-heavy workloads
            shard_count = base_shards * 2

        return min(shard_count, self.settings.max_shards_per_table)```
#### 3. Functional Scaling

