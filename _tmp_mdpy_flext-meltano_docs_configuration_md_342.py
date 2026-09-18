# from flext-meltano_docs/configuration.md:342
from flext_meltano import FlextMeltanoSettings

settings = FlextMeltanoSettings()

# Load development configuration
dev_config = settings.load_configuration("dev")

# Load production configuration
prod_config = settings.load_configuration("prod")```
______________________________________________________________________

## 🔧 Configuration File Management

### Reading Configuration Files

