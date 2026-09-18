# from flext-meltano/docs/architecture.md:105
├── singer_types.py           # FlextMeltanoTypes (Singer protocol abstractions)
├── tap_abstractions.py       # FlextMeltanoTapAbstractions with TapConfig, StreamDefinition
├── target_abstractions.py   # FlextMeltanoTargetAbstractions for target operations
└── file_managers.py         # FlextMeltanoFileManagers for file operations```
**Purpose**: Provides type-safe abstractions for Singer protocol, data streams, and file operations.

### **Configuration Layer**

**Settings and Environment Management**

