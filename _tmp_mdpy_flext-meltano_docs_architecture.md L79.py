# from flext-meltano/docs/architecture.md:79
├── services.py                    # FlextMeltanoService (core orchestration)
├── service_implementations.py     # Specialized service implementations
├── adapters.py                   # FlextMeltanoAdapter (external integration)
└── plugin_protocols.py          # Protocol definitions for plugins```
**Key Components**:

- **FlextMeltanoService**: Unified service following s pattern
- **Service Implementations**: FlextMeltanoTapService, FlextTargetService, FlextDbtService
- **Plugin Protocols**: TapService, TargetService, DbtService

### **Execution Layer**

**Command Processing and Integration**

