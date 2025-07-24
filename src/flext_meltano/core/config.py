"""Configuration management for FLEXT Meltano integration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass
class FlextMeltanoConfig:
    """Configuration for Meltano executor."""

    project_dir: str = "."
    python_path: str = "/home/marlonsc/flext/.venv/bin/python3"
    workspace_dir: str = "/home/marlonsc/flext"
    meltano_path: str | None = None
    environment: str = "dev"

    def __post_init__(self) -> None:
        """Initialize configuration after creation."""
        if self.meltano_path is None:
            # Auto-detect meltano path
            venv_meltano = Path(self.workspace_dir) / ".venv" / "bin" / "meltano"
            if venv_meltano.exists():
                self.meltano_path = str(venv_meltano)
            else:
                self.meltano_path = "meltano"  # fallback to PATH
