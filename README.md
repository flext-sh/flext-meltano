# FLEXT-Meltano

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**FLEXT-Meltano** is the enterprise integration framework for extending Meltano capabilities within the FLEXT ecosystem. It provides comprehensive tooling for Singer protocol implementation, plugin development scaffolding, and robust data pipeline orchestration.

## 🚀 Key Features

- **Singer Protocol Compliance**: Full support for building custom Taps (extractors) and Targets (loaders) adhering to the Singer spec.
- **Plugin Scaffolding**: Automated generation of new plugin projects with boilerplate, configuration, and testing infrastructure.
- **Pipeline Orchestration**: Manage complex ELT workflows with dependencies, retries, and monitoring.
- **Schema Discovery**: Automatic schema inference and catalog generation for data sources.
- **State Management**: Robust handling of incremental sync state and bookmarks.
- **FLEXT Integration**: Seamlessly integrates with `flext-cli` for command-line control and `flext-observability` for pipeline metrics.

## 📦 Installation

To install `flext-meltano`:

```bash
pip install flext-meltano
```

Or with Poetry:

```bash
poetry add flext-meltano
```

## 🛠️ Usage

### Discovering Plugins

Programmatically inspect available plugins in a Meltano project.

```python
from flext_meltano import FlextMeltanoService

# 1. Initialize Service
service = FlextMeltanoService(project_root="/path/to/project")

# 2. Discover Plugins
plugins_result = service.discover_plugins()

if plugins_result.is_success:
    plugins = plugins_result.unwrap()
    print(f"Found {len(plugins)} plugins:")
    for p in plugins:
        print(f" - {p.name} ({p.type})")
```

### Executing a Tap

Run a specific extractor with custom state and configuration.

```python
from flext_meltano import FlextMeltanoAdapter

# 1. Initialize Adapter
adapter = FlextMeltanoAdapter()

# 2. Run Tap
result = adapter.run_tap(
    tap_name="tap-postgres",
    config={"host": "localhost", "port": 5432},
    state={"bookmarks": {"users": {"last_updated": "2023-01-01"}}}
)

if result.is_success:
    print("Tap execution completed successfully.")
else:
    print(f"Tap failed: {result.error}")
```

### Orchestrating a Pipeline

Execute a full EL (Extract-Load) pipeline.

```python
from flext_meltano import FlextMeltanoExecutor

# 1. Initialize Executor
executor = FlextMeltanoExecutor()

# 2. Run Pipeline
pipeline_result = executor.execute_pipeline(
    tap="tap-gitlab",
    target="target-snowflake",
    options={"incremental": True}
)

if pipeline_result.is_success:
    metrics = pipeline_result.unwrap()
    print(f"Pipeline finished. Records processed: {metrics.record_count}")
```

## 🏗️ Architecture

FLEXT-Meltano bridges the gap between raw Singer components and enterprise requirements:

- **Plugin Layer**: Scaffolding and lifecycle management for custom connectors.
- **Protocol Layer**: Strict implementation of the Singer spec for interoperability.
- **Orchestration Layer**: Execution engine for managing data flows and error recovery.
- **Integration Layer**: Adapters for Meltano CLI and project configuration.

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](docs/development.md) for details on creating new plugins, enhancing the orchestration engine, and submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
