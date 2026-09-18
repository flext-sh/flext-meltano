# from flext-meltano_docs/configuration.md:183
from flext_meltano import StreamDefinition

# Define stream configuration
stream = StreamDefinition(
    name="users",
    schema={
        "type": "object",
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"},
            "email": {"type": "string"},
        },
    },
    metadata={
        "selected": True,
        "replication-method": "INCREMENTAL",
        "replication-key": "updated_at",
    },
)```
______________________________________________________________________

## 🛠️ dbt Configuration

### dbt Project Structure```
transform/
├── dbt_project.yml
├── profiles/
│   └── profiles.yml
├── models/
│   ├── staging/
│   │   └── stg_users.sql
│   └── marts/
│       └── dim_users.sql
├── tests/
│   └── assert_user_id_unique.sql
└── macros/
    └── custom_macros.sql```
### dbt Project Configuration (dbt_project.yml)

