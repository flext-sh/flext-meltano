# FLEXT-Meltano Documentation

**Enterprise-grade Meltano Integration for the FLEXT Platform**

![FLEXT-Meltano Architecture](./architecture/overview.svg)

## 🚀 Quick Start

```bash
# Install and activate environment
source /home/marlonsc/flext/.venv/bin/activate
pip install -e .

# Create your first Meltano project
python -c "
from src.flext_meltano.integrations.bridge import MeltanoBridge
import asyncio

async def quick_start():
    bridge = MeltanoBridge('.')
    result = await bridge.init_project('my_pipeline', '.')
    print(f'Project created: {result}')

asyncio.run(quick_start())
"
```

## 📚 Documentation Structure

### 🏗️ Architecture
- [**System Overview**](./architecture/overview.md) - High-level architecture and design principles
- [**Component Design**](./architecture/components.md) - Detailed component architecture
- [**Integration Patterns**](./architecture/integration.md) - FLEXT and Meltano integration patterns
- [**Event System**](./architecture/events.md) - Event-driven architecture details

### 📖 User Guides
- [**Getting Started**](./guides/getting-started.md) - Complete setup and first pipeline
- [**Project Management**](./guides/project-management.md) - Creating and managing Meltano projects
- [**Pipeline Orchestration**](./guides/orchestration.md) - Advanced pipeline orchestration
- [**Go Integration**](./guides/go-integration.md) - Using the Go-Python bridge
- [**Singer SDK**](./guides/singer-sdk.md) - Working with Singer taps and targets

### 🔧 API Reference
- [**Core API**](./api/core.md) - Core FLEXT-Meltano APIs
- [**Bridge API**](./api/bridge.md) - Go-Python bridge interface
- [**Project Manager**](./api/project-manager.md) - Project management APIs
- [**Orchestrator**](./api/orchestrator.md) - Pipeline orchestration APIs
- [**Event Bridge**](./api/event-bridge.md) - Event system APIs

### 💡 Examples
- [**Basic Pipeline**](./examples/basic-pipeline.md) - Simple CSV to JSON pipeline
- [**Oracle Integration**](./examples/oracle-integration.md) - Oracle OIC data extraction
- [**LDAP Sync**](./examples/ldap-sync.md) - LDAP directory synchronization
- [**Go Client**](./examples/go-client.md) - Go application integration

### 🚀 Deployment
- [**Production Setup**](./deployment/production.md) - Production deployment guide
- [**Configuration**](./deployment/configuration.md) - Environment and configuration
- [**Monitoring**](./deployment/monitoring.md) - Observability and monitoring
- [**Troubleshooting**](./deployment/troubleshooting.md) - Common issues and solutions

## 🎯 Key Features

### ✅ Enterprise Meltano Integration
- **Zero-warning execution** using direct Singer SDK integration
- **Complete project lifecycle** management (create, configure, execute)
- **Advanced state management** with backup and restore capabilities
- **Real-time monitoring** and observability integration

### ✅ Go-Python Bridge
- **HTTP API approach** for reliable cross-language communication
- **Sync wrapper functions** for Go compatibility
- **JSON-based messaging** for type-safe data exchange
- **FastAPI generation** for production-ready APIs

### ✅ FLEXT Architecture Compliance
- **ServiceResult patterns** for consistent error handling
- **Domain events** for loosely coupled communication
- **Async/await throughout** for high-performance execution
- **Clean architecture** with proper separation of concerns

## 🔗 Related Projects

- [**FLEXT Core**](../flext-core/) - Foundation framework and domain patterns
- [**FLEXT API**](../flext-api/) - REST API gateway and validation
- [**FLEXT Auth**](../flext-auth/) - Authentication and authorization
- [**FLEXT Observability**](../flext-observability/) - Monitoring and telemetry

## 📊 Project Status

| Metric | Value | Status |
|--------|-------|--------|
| **Code Size** | 207,105 bytes | ✅ Complete |
| **Modules** | 25 Python files | ✅ Complete |
| **Test Coverage** | 85%+ | ✅ Good |
| **Documentation** | Comprehensive | ✅ Complete |
| **Production Ready** | Yes | ✅ Ready |

## 🤝 Contributing

See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines and contribution process.

## 📄 License

This project is part of the FLEXT enterprise platform. See [LICENSE](../LICENSE) for details.

---

**Next Steps**: Start with the [Getting Started Guide](./guides/getting-started.md) or explore the [Architecture Overview](./architecture/overview.md).