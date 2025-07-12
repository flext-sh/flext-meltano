"""Command-line interface for FLEXT Meltano.

This module provides CLI commands for Meltano operations.
Uses flext-cli patterns for consistency.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml
from loguru import logger


def info_command(_args: argparse.Namespace) -> int:
    """Show FLEXT Meltano information."""
    logger.info("FLEXT Meltano - Enterprise ETL/ELT Pipeline Engine")
    logger.info("Version: 0.7.0")
    logger.info("Singer Protocol Support: Yes")
    return 0


def init_command(args: argparse.Namespace) -> int:
    """Initialize a new Meltano project."""
    try:
        project_name = args.name
        project_dir = Path(args.directory) if args.directory else Path(project_name)

        # Create project directory
        project_dir.mkdir(parents=True, exist_ok=True)

        # Create meltano.yml
        meltano_config = {
            "version": 1,
            "default_environment": "dev",
            "project_id": f"flext-{project_name}",
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

        logger.success(f"Initialized Meltano project: {project_name}")
        logger.info(f"Project directory: {project_dir}")
        return 0

    except Exception as e:
        logger.error(f"Failed to initialize project: {e}")
        return 1


def run_command(args: argparse.Namespace) -> int:
    """Run a Meltano command."""
    try:
        # Build meltano command
        cmd = ["meltano"]

        if hasattr(args, "environment") and args.environment:
            cmd.extend(["--environment", args.environment])

        cmd.extend(args.command)

        logger.info(f"Running: {' '.join(cmd)}")

        # Execute command
        result = subprocess.run(
            cmd,
            cwd=args.project_dir if hasattr(args, "project_dir") else None,
            capture_output=False, check=False,
        )

        return result.returncode

    except Exception as e:
        logger.error(f"Failed to run command: {e}")
        return 1


def install_command(args: argparse.Namespace) -> int:
    """Install a Meltano plugin."""
    try:
        cmd = ["meltano", "add", args.plugin_type, args.plugin_name]

        if hasattr(args, "variant") and args.variant:
            cmd.extend(["--variant", args.variant])

        logger.info(f"Installing {args.plugin_type}: {args.plugin_name}")

        result = subprocess.run(
            cmd,
            cwd=args.project_dir if hasattr(args, "project_dir") else None, check=False,
        )

        if result.returncode == 0:
            logger.success(f"Installed {args.plugin_name}")
        else:
            logger.error(f"Failed to install {args.plugin_name}")

        return result.returncode

    except Exception as e:
        logger.error(f"Failed to install plugin: {e}")
        return 1


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="flext-meltano",
        description="FLEXT Meltano CLI - Enterprise ETL/ELT Pipeline Engine",
    )

    parser.add_argument(
        "--project-dir",
        type=Path,
        help="Meltano project directory",
    )

    parser.add_argument(
        "--environment", "-e",
        help="Meltano environment",
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Info command
    info_parser = subparsers.add_parser("info", help="Show FLEXT Meltano information")
    info_parser.set_defaults(func=info_command)

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize new Meltano project")
    init_parser.add_argument("name", help="Project name")
    init_parser.add_argument("--directory", help="Project directory")
    init_parser.set_defaults(func=init_command)

    # Run command
    run_parser = subparsers.add_parser("run", help="Run Meltano command")
    run_parser.add_argument("command", nargs="+", help="Meltano command to run")
    run_parser.set_defaults(func=run_command)

    # Install command
    install_parser = subparsers.add_parser("install", help="Install plugin")
    install_parser.add_argument("plugin_type", choices=["extractor", "loader", "transformer"])
    install_parser.add_argument("plugin_name", help="Plugin name")
    install_parser.add_argument("--variant", help="Plugin variant")
    install_parser.set_defaults(func=install_command)

    return parser


def main() -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()

    # Set up logging
    if args.verbose:
        logger.add(sys.stderr, level="DEBUG")
    else:
        logger.add(sys.stderr, level="INFO")

    # Execute command
    if hasattr(args, "func"):
        return args.func(args)
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
