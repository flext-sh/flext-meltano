# from flext-meltano/docs/architecture/data-architecture.md:338
from __future__ import annotations


class SchemaValidator:
    """Singer schema validation with FLEXT patterns."""

    def validate_record(self, record: dict, schema: dict) -> p.Result[ValidatedRecord]:
        """Validate record against Singer schema."""
        try:
            # JSON Schema validation
            validate(instance=record, schema=schema)
            return r.ok(ValidatedRecord(record=record, schema=schema))
        except c.ValidationError as e:
            return r.fail(ValidationError(f"Schema validation failed: {e.message}"))

    def validate_stream_schema(self, schema: dict) -> p.Result[ValidatedSchema]:
        """Validate Singer stream schema."""
        required_fields = ["type", "properties"]
        if not all(field in schema for field in required_fields):
            return r.fail(SchemaError("Invalid Singer schema structure"))

        return r.ok(ValidatedSchema(schema=schema))```
______________________________________________________________________

## 🔄 Data Processing Pipeline

### Pipeline Execution Flow

