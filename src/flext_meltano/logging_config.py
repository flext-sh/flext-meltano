"""FlextMeltanoLoggingSettings - Consolidated logging configuration for pipeline operations.

Organizes 62+ logging boolean fields into coherent categories:
- Pipeline operations logging
- Extract/source operations logging
- Load/sink operations logging
- Transform/DBT operations logging
- Orchestration and monitoring logging
- Debugging and performance logging

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from pydantic import Field, computed_field

from flext import FlextModels


class FlextMeltanoLoggingSettings(FlextModels):
    """Consolidated logging configuration for all pipeline operations.

    Single responsibility: manage logging configuration across all domains.
    """

    # Pipeline Operations Logging (9 fields)
    pipeline_execution: bool = Field(
        default=True,
        description="Log pipeline execution details",
    )
    pipeline_stages: bool = Field(
        default=True,
        description="Log pipeline stage transitions",
    )
    pipeline_progress: bool = Field(
        default=True,
        description="Log pipeline progress updates",
    )
    pipeline_errors: bool = Field(
        default=True,
        description="Log pipeline errors and failures",
    )
    pipeline_warnings: bool = Field(default=True, description="Log pipeline warnings")
    pipeline_performance: bool = Field(
        default=True,
        description="Log pipeline performance metrics",
    )
    pipeline_timing: bool = Field(
        default=True,
        description="Log pipeline timing information",
    )
    pipeline_memory: bool = Field(default=True, description="Log pipeline memory usage")
    pipeline_throughput: bool = Field(
        default=True,
        description="Log pipeline throughput metrics",
    )

    # Extract/Source Operations Logging (8 fields)
    extract_operations: bool = Field(default=True, description="Log extract operations")
    extract_queries: bool = Field(default=True, description="Log extract queries")
    extract_results: bool = Field(default=True, description="Log extract results")
    extract_errors: bool = Field(default=True, description="Log extract errors")
    extract_performance: bool = Field(
        default=True,
        description="Log extract performance metrics",
    )
    extract_timing: bool = Field(
        default=True,
        description="Log extract timing information",
    )
    extract_memory: bool = Field(default=True, description="Log extract memory usage")
    extract_throughput: bool = Field(
        default=True,
        description="Log extract throughput metrics",
    )

    # Load/Sink Operations Logging (8 fields)
    load_operations: bool = Field(default=True, description="Log load operations")
    load_batches: bool = Field(default=True, description="Log load batches")
    load_results: bool = Field(default=True, description="Log load results")
    load_errors: bool = Field(default=True, description="Log load errors")
    load_performance: bool = Field(
        default=True,
        description="Log load performance metrics",
    )
    load_timing: bool = Field(default=True, description="Log load timing information")
    load_memory: bool = Field(default=True, description="Log load memory usage")
    load_throughput: bool = Field(
        default=True,
        description="Log load throughput metrics",
    )

    # Transform/DBT Operations Logging (8 fields)
    transform_operations: bool = Field(
        default=True,
        description="Log transform operations",
    )
    transform_sql: bool = Field(default=True, description="Log transform SQL queries")
    transform_results: bool = Field(default=True, description="Log transform results")
    transform_errors: bool = Field(default=True, description="Log transform errors")
    transform_performance: bool = Field(
        default=True,
        description="Log transform performance metrics",
    )
    transform_timing: bool = Field(
        default=True,
        description="Log transform timing information",
    )
    transform_memory: bool = Field(
        default=True,
        description="Log transform memory usage",
    )
    transform_lineage: bool = Field(
        default=True,
        description="Log transform lineage tracking",
    )

    # DBT Specific Logging (6 fields)
    dbt_parse: bool = Field(default=True, description="Log DBT parsing operations")
    dbt_compile: bool = Field(default=True, description="Log DBT compilation")
    dbt_execute: bool = Field(default=True, description="Log DBT execution")
    dbt_test: bool = Field(default=True, description="Log DBT test operations")
    dbt_snapshot: bool = Field(default=True, description="Log DBT snapshot operations")
    dbt_docs: bool = Field(default=True, description="Log DBT documentation generation")

    # Data Quality Logging (8 fields)
    data_quality: bool = Field(default=True, description="Log data quality checks")
    data_quality_checks: bool = Field(
        default=True,
        description="Log data quality check results",
    )
    data_quality_errors: bool = Field(
        default=True,
        description="Log data quality errors",
    )
    data_quality_warnings: bool = Field(
        default=True,
        description="Log data quality warnings",
    )
    data_quality_metrics: bool = Field(
        default=True,
        description="Log data quality metrics",
    )
    data_quality_timing: bool = Field(
        default=True,
        description="Log data quality timing information",
    )
    data_quality_memory: bool = Field(
        default=True,
        description="Log data quality memory usage",
    )
    data_quality_throughput: bool = Field(
        default=True,
        description="Log data quality throughput metrics",
    )

    # Plugin Logging (6 fields)
    plugin_operations: bool = Field(default=True, description="Log plugin operations")
    plugin_errors: bool = Field(default=True, description="Log plugin errors")
    plugin_performance: bool = Field(
        default=True,
        description="Log plugin performance metrics",
    )
    plugin_timing: bool = Field(
        default=True,
        description="Log plugin timing information",
    )
    plugin_memory: bool = Field(default=True, description="Log plugin memory usage")
    plugin_throughput: bool = Field(
        default=True,
        description="Log plugin throughput metrics",
    )

    # Source and Target Logging (14 fields)
    source_info: bool = Field(default=True, description="Log source information")
    target_info: bool = Field(default=True, description="Log target information")
    source_errors: bool = Field(default=True, description="Log source errors")
    target_errors: bool = Field(default=True, description="Log target errors")
    source_performance: bool = Field(
        default=True,
        description="Log source performance metrics",
    )
    target_performance: bool = Field(
        default=True,
        description="Log target performance metrics",
    )
    source_timing: bool = Field(
        default=True,
        description="Log source timing information",
    )
    target_timing: bool = Field(
        default=True,
        description="Log target timing information",
    )
    source_memory: bool = Field(default=True, description="Log source memory usage")
    target_memory: bool = Field(default=True, description="Log target memory usage")
    source_throughput: bool = Field(
        default=True,
        description="Log source throughput metrics",
    )
    target_throughput: bool = Field(
        default=True,
        description="Log target throughput metrics",
    )

    # Meltano Performance Tracking (1 field)
    track_meltano_performance: bool = Field(
        default=True,
        description="Track Meltano performance metrics",
    )

    # Orchestration Logging (5 fields)
    orchestration_scheduling: bool = Field(
        default=True,
        description="Log orchestration scheduling events",
    )
    orchestration_execution: bool = Field(
        default=True,
        description="Log orchestration execution",
    )
    orchestration_state: bool = Field(
        default=True,
        description="Log orchestration state changes",
    )
    orchestration_hooks: bool = Field(
        default=True,
        description="Log orchestration hook execution",
    )
    orchestration_dependencies: bool = Field(
        default=True,
        description="Log dependency resolution",
    )

    # Monitoring and Observability Logging (5 fields)
    monitoring_metrics: bool = Field(default=True, description="Log collected metrics")
    monitoring_alerts: bool = Field(default=True, description="Log alert generation")
    monitoring_health: bool = Field(default=True, description="Log health checks")
    monitoring_traces: bool = Field(default=True, description="Log distributed traces")
    monitoring_events: bool = Field(
        default=True,
        description="Log observability events",
    )

    # Debugging and Diagnostics Logging (5 fields)
    debug_verbose: bool = Field(
        default=False,
        description="Enable verbose debug logging",
    )
    debug_trace_calls: bool = Field(
        default=False,
        description="Log function call traces",
    )
    debug_variable_state: bool = Field(
        default=False,
        description="Log variable state changes",
    )
    debug_configuration: bool = Field(
        default=False,
        description="Log configuration details",
    )
    debug_performance_profile: bool = Field(
        default=False,
        description="Log performance profiling data",
    )

    @computed_field
    def pipeline_dict(self) -> dict[str, bool]:
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
    def extract_dict(self) -> dict[str, bool]:
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
    def load_dict(self) -> dict[str, bool]:
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
    def transform_dict(self) -> dict[str, bool]:
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


__all__ = ["FlextMeltanoLoggingSettings"]
