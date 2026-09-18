# from flext-meltano/docs/architecture.md:94
├── executors.py              # FlextMeltanoExecutor (command orchestration)
├── executors_bridge.py       # FlextMeltanoBridge (Go ↔ Python communication)
├── executors_cli.py          # FlextMeltanoCli (CLI command processing)
└── executors_meltano.py      # Simplified executor implementations```
**Purpose**: Handles execution of ELT operations, CLI commands, and bridge communication with external systems.

### **Abstraction Layer**

**Protocol and Data Integration**

