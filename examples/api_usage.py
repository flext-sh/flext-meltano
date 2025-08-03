"""FLEXT Meltano API Usage Examples - Modern Enterprise API Patterns.

**Purpose**: Demonstrate modern FLEXT Meltano API usage following flext-core patterns
**Scope**: FlextMeltanoAPI integration, enterprise patterns, production workflows
**Target Audience**: Developers implementing production FLEXT Meltano integration
**Dependencies**: flext-core enterprise patterns, FlextMeltanoAPI service layer

## Overview

This example demonstrates the **modern FLEXT Meltano API** usage patterns for
enterprise applications, focusing on:

1. **FlextMeltanoAPI Integration**: Modern service-oriented API usage
2. **Enterprise Configuration**: Production-ready configuration management
3. **Pipeline Orchestration**: Complete pipeline lifecycle management
4. **Error Handling**: Comprehensive error management with FlextResult patterns
5. **Production Patterns**: Real-world usage scenarios and best practices

## Usage

```bash
python api_usage.py
```

## Architecture Alignment

Examples follow FLEXT Meltano's modern API architecture:
- **Service Layer**: FlextMeltanoAPI as primary integration point
- **Enterprise Patterns**: flext-core integration throughout
- **Production Ready**: Real-world configuration and error handling
- **Bridge Compatible**: API designed for Go service integration
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from flext_meltano.api import (
    FlextMeltanoAPI,
)


def example_basic_api_usage() -> None:
    """Basic example of FlextMeltanoAPI usage."""
    # Create temporary directory for the example
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "example_project"
        project_root.mkdir()

        # Initialize API
        FlextMeltanoAPI(
            project_root=project_root,
            environment="dev",
            auto_install=True,
        )

        # Example plugin configuration (would be used in real project)

        # Example catalog discovery (would be used in real project)

        # Example connection testing (would be used in real project)

        # Example pipeline execution (would be used in real project)


def example_one_liner_functions() -> None:
    """Example usage of one-liner functions."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "oneliner_project"
        project_root.mkdir()

        # Conceptual examples of one-liner functions


def example_advanced_usage() -> None:
    """Example of advanced API usage."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "advanced_project"
        project_root.mkdir()

        # API com configurações customizadas
        FlextMeltanoAPI(
            project_root=project_root,
            environment="prod",
            auto_install=False,  # Controle manual de plugins
            state_backend="filesystem",
        )


def example_error_handling() -> None:
    """Example of error handling with FlextResult."""
    with tempfile.TemporaryDirectory() as temp_dir:
        project_root = Path(temp_dir) / "error_handling"
        project_root.mkdir()

        FlextMeltanoAPI(project_root=project_root)


if __name__ == "__main__":
    example_basic_api_usage()
    example_one_liner_functions()
    example_advanced_usage()
    example_error_handling()
