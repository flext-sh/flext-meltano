# from flext-meltano_docs/api-reference.md:1108
from flext_meltano import FlextMeltanoService

# Initialize service
service = FlextMeltanoService()

# Execute tap
tap_result = service.execute_tap(
    tap_name="tap-csv", settings={"files": ["data/sales.csv"]}
)

if tap_result.success:
    records = tap_result.unwrap().records

    # Execute target
    target_result = service.execute_target(
        target_name="target-jsonl",
        records=records,
        settings={"destination_path": "output/sales.jsonl"},
    )```
### Advanced Pipeline Orchestration

