# from flext-meltano_docs/configuration.md:358
from flext_meltano import FlextMeltanoFileManagers

file_manager = FlextMeltanoFileManagers()

# Read meltano.yml
meltano_config = file_manager.read_meltano_config()

# Read Singer catalog
catalog_result = file_manager.read_singer_catalog("catalog.json")

# Read dbt profiles
dbt_profiles = file_manager.read_dbt_profiles()```
### Writing Configuration Files

