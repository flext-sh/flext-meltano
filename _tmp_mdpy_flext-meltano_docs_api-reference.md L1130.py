# from flext-meltano/docs/api-reference.md:1130
from flext_meltano import FlextMeltanoExecutor

# Initialize executor
executor = FlextMeltanoExecutor()

# Execute pipeline with advanced options
result = executor.execute_pipeline_advanced(
    FlextMeltanoModels.PipelineOptions(
        tap="tap-salesforce",
        target="target-snowflake",
        incremental=True,
        parallelism=4,
        state_file="state/salesforce_state.json",
    )
)

if result.success:
    u.Cli.print(f"Pipeline completed in {result.unwrap().execution_time}s")```
### Plugin Management

