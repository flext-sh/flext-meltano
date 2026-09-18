# from flext-meltano_docs/configuration.md:395
from flext_meltano import FlextMeltanoValidators

validators = FlextMeltanoValidators()

# Validate Singer schema
schema_validation = validators.validate_singer_schema({
    "type": "object",
    "properties": {"id": {"type": "integer"}, "name": {"type": "string"}},
})

# Validate dbt models
model_validation = validators.validate_dbt_models([
    {"name": "stg_users", "path": "models/staging/stg_users.sql"},
    {"name": "dim_users", "path": "models/marts/dim_users.sql"},
])```
### Runtime Validation

