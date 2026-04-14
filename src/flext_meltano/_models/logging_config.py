"""FLEXT Meltano models - Logging configuration."""

from __future__ import annotations

from flext_cli import m
from pydantic import computed_field

from flext_meltano import t


class FlextMeltanoModelsLogging:
    """Logging configuration models."""

    class LoggingConfig(m.BaseModel):
        """Consolidated logging configuration for all pipeline operations.

        Organizes 62+ logging boolean fields into coherent categories:
        - Pipeline operations logging
        - Extract/source operations logging
        - Load/sink operations logging
        - Transform/DBT operations logging
        - Orchestration and monitoring logging
        - Debugging and performance logging

        Single responsibility: manage logging configuration across all domains.
        """

        # Pipeline Operations Logging (9 fields)
        pipeline_execution: bool = True
        pipeline_stages: bool = True
        pipeline_progress: bool = True
        pipeline_errors: bool = True
        pipeline_warnings: bool = True
        pipeline_performance: bool = True
        pipeline_timing: bool = True
        pipeline_memory: bool = True
        pipeline_throughput: bool = True

        # Extract/Source Operations Logging (8 fields)
        extract_operations: bool = True
        extract_queries: bool = True
        extract_results: bool = True
        extract_errors: bool = True
        extract_performance: bool = True
        extract_timing: bool = True
        extract_memory: bool = True
        extract_throughput: bool = True

        # Load/Sink Operations Logging (8 fields)
        load_operations: bool = True
        load_batches: bool = True
        load_results: bool = True
        load_errors: bool = True
        load_performance: bool = True
        load_timing: bool = True
        load_memory: bool = True
        load_throughput: bool = True

        # Transform/DBT Operations Logging (8 fields)
        transform_operations: bool = True
        transform_sql: bool = True
        transform_results: bool = True
        transform_errors: bool = True
        transform_performance: bool = True
        transform_timing: bool = True
        transform_memory: bool = True
        transform_lineage: bool = True

        # DBT Specific Logging (6 fields)
        dbt_parse: bool = True
        dbt_compile: bool = True
        dbt_execute: bool = True
        dbt_test: bool = True
        dbt_snapshot: bool = True
        dbt_docs: bool = True

        # Data Quality Logging (8 fields)
        data_quality: bool = True
        data_quality_checks: bool = True
        data_quality_errors: bool = True
        data_quality_warnings: bool = True
        data_quality_metrics: bool = True
        data_quality_timing: bool = True
        data_quality_memory: bool = True
        data_quality_throughput: bool = True

        # Plugin Logging (6 fields)
        plugin_operations: bool = True
        plugin_errors: bool = True
        plugin_performance: bool = True
        plugin_timing: bool = True
        plugin_memory: bool = True
        plugin_throughput: bool = True

        # Source and Target Logging (12 fields)
        source_info: bool = True
        target_info: bool = True
        source_errors: bool = True
        target_errors: bool = True
        source_performance: bool = True
        target_performance: bool = True
        source_timing: bool = True
        target_timing: bool = True
        source_memory: bool = True
        target_memory: bool = True
        source_throughput: bool = True
        target_throughput: bool = True

        # Meltano Performance Tracking (1 field)
        track_meltano_performance: bool = True

        # Orchestration Logging (5 fields)
        orchestration_scheduling: bool = True
        orchestration_execution: bool = True
        orchestration_state: bool = True
        orchestration_hooks: bool = True
        orchestration_dependencies: bool = True

        # Monitoring and Observability Logging (5 fields)
        monitoring_metrics: bool = True
        monitoring_alerts: bool = True
        monitoring_health: bool = True
        monitoring_traces: bool = True
        monitoring_events: bool = True

        # Debugging and Diagnostics Logging (5 fields)
        debug_verbose: bool = False
        debug_trace_calls: bool = False
        debug_variable_state: bool = False
        debug_configuration: bool = False
        debug_performance_profile: bool = False

        @computed_field
        @property
        def extract_dict(self) -> t.BoolMapping:
            """Extract logging as dictionary."""
            return {
                "operations": self.extract_operations,
                "queries": self.extract_queries,
                "results": self.extract_results,
                "errors": self.extract_errors,
                "performance": self.extract_performance,
                "timing": self.extract_timing,
                "memory": self.extract_memory,
                "throughput": self.extract_throughput,
            }

        @computed_field
        @property
        def load_dict(self) -> t.BoolMapping:
            """Load logging as dictionary."""
            return {
                "operations": self.load_operations,
                "batches": self.load_batches,
                "results": self.load_results,
                "errors": self.load_errors,
                "performance": self.load_performance,
                "timing": self.load_timing,
                "memory": self.load_memory,
                "throughput": self.load_throughput,
            }

        @computed_field
        @property
        def pipeline_dict(self) -> t.BoolMapping:
            """Pipeline logging as dictionary."""
            return {
                "execution": self.pipeline_execution,
                "stages": self.pipeline_stages,
                "progress": self.pipeline_progress,
                "errors": self.pipeline_errors,
                "warnings": self.pipeline_warnings,
                "performance": self.pipeline_performance,
                "timing": self.pipeline_timing,
                "memory": self.pipeline_memory,
                "throughput": self.pipeline_throughput,
            }

        @computed_field
        @property
        def transform_dict(self) -> t.BoolMapping:
            """Transform logging as dictionary."""
            return {
                "operations": self.transform_operations,
                "sql": self.transform_sql,
                "results": self.transform_results,
                "errors": self.transform_errors,
                "performance": self.transform_performance,
                "timing": self.transform_timing,
                "memory": self.transform_memory,
                "lineage": self.transform_lineage,
            }
