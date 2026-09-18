# from flext-meltano/docs/architecture.md:271
from __future__ import annotations


# All operations return r[T] for railway-oriented programming
def process_elt_pipeline(
    tap_config: TapConfig, target_config: m.Dict
) -> p.Result[m.Dict]:
    """Process ELT pipeline with comprehensive error handling."""
    # Validation phase
    validation_result = validate_configuration(tap_config)
    if validation_result.failure:
        return r[m.Dict].fail(
            f"Configuration validation failed: {validation_result.error}"
        )

    # Execution phase
    execution_result = execute_pipeline(tap_config, target_config)
    if execution_result.failure:
        return r[m.Dict].fail(f"Pipeline execution failed: {execution_result.error}")

    return r[m.Dict].ok(execution_result.unwrap())```
### **Exception Hierarchy**

