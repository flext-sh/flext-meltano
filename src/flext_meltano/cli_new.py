"""Command-line interface for FLEXT Meltano using centralized CLI framework.

Copyright (c) 2025 FLEXT Team. All rights reserved.
"""

from __future__ import annotations

import subprocess
from pathlib import Path

import click
import yaml


@click.group()
@click.version_option(version="0.7.0")
def cli() -> None:
    """FLEXT Meltano - Enterprise ETL/ELT Pipeline Engine."""


@cli.command()
@click.option("--format", "output_format", default="table", help="Output format")
@click.option("--quiet", is_flag=True, help="Quiet mode")
def info(output_format: str, quiet: bool) -> None:
    """Show FLEXT Meltano information."""
    info_data = {
        "name": "FLEXT Meltano",
        "version": "0.7.0",
        "description": "Enterprise ETL/ELT Pipeline Engine",
        "singer_protocol": True,
        "features": [
            "Singer Protocol Support",
            "State Management",
            "Pipeline Execution",
            "Plugin Management",
        ],
    }

    if not quiet:
        click.echo(f"Name: {info_data['name']}")
        click.echo(f"Version: {info_data['version']}")
        click.echo(f"Description: {info_data['description']}")
        click.echo(f"Singer Protocol: {info_data['singer_protocol']}")
        click.echo("Features:")
        for feature in info_data["features"]:
            click.echo(f"  - {feature}")


@cli.command()
@click.argument("name")
@click.option("--directory", help="Project directory")
@click.option("--template", default="default", help="Project template")
def init(name: str, directory: str | None, template: str) -> None:
    """Initialize a new Meltano project."""
    try:
        project_dir = Path(directory) if directory else Path(name)
        project_dir.mkdir(parents=True, exist_ok=True)

        # Create meltano.yml
        meltano_config = {
            "version": 1,
            "default_environment": "dev",
            "project_id": f"flext-{name}",
            "environments": [
                {"name": "dev"},
                {"name": "staging"},
                {"name": "prod"},
            ],
            "plugins": {
                "extractors": [],
                "loaders": [],
                "transformers": [],
            },
        }

        meltano_yml = project_dir / "meltano.yml"
        with meltano_yml.open("w") as f:
            yaml.safe_dump(meltano_config, f, default_flow_style=False, indent=2)

        click.echo(f"✅ Initialized Meltano project: {name}")
        click.echo(f"📁 Project directory: {project_dir}")

    except Exception as e:
        click.echo(f"❌ Failed to initialize project: {e}", err=True)
        raise click.Abort


@cli.command()
@click.argument("command", nargs=-1, required=True)
@click.option("--environment", "-e", help="Meltano environment")
@click.option("--project-dir", type=click.Path(exists=True), help="Project directory")
def run(command: tuple[str, ...], environment: str | None, project_dir: str | None) -> None:
    """Run a Meltano command."""
    try:
        cmd = ["meltano"]

        if environment:
            cmd.extend(["--environment", environment])

        cmd.extend(command)

        click.echo(f"🚀 Running: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            cwd=project_dir,
            capture_output=False, check=False,
        )

        if result.returncode != 0:
            click.echo(f"❌ Command failed with exit code {result.returncode}", err=True)
            raise click.Abort
        click.echo("✅ Command completed successfully")

    except Exception as e:
        click.echo(f"❌ Failed to run command: {e}", err=True)
        raise click.Abort


@cli.command()
@click.argument("plugin_type", type=click.Choice(["extractor", "loader", "transformer"]))
@click.argument("plugin_name")
@click.option("--variant", help="Plugin variant")
@click.option("--project-dir", type=click.Path(exists=True), help="Project directory")
def install(plugin_type: str, plugin_name: str, variant: str | None, project_dir: str | None) -> None:
    """Install a Meltano plugin."""
    try:
        cmd = ["meltano", "add", plugin_type, plugin_name]

        if variant:
            cmd.extend(["--variant", variant])

        click.echo(f"📦 Installing {plugin_type}: {plugin_name}")

        result = subprocess.run(
            cmd,
            cwd=project_dir, check=False,
        )

        if result.returncode == 0:
            click.echo(f"✅ Installed {plugin_name}")
        else:
            click.echo(f"❌ Failed to install {plugin_name}", err=True)
            raise click.Abort

    except Exception as e:
        click.echo(f"❌ Failed to install plugin: {e}", err=True)
        raise click.Abort


if __name__ == "__main__":
    cli()
