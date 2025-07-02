"""Command-line interface for FLEXT Meltano."""

from __future__ import annotations

import argparse
import shlex
import subprocess
import sys
from pathlib import Path

import yaml
from loguru import logger


def info_command(_args: argparse.Namespace) -> int:
    """Show FLEXT Meltano information."""
    logger.info("FLEXT Meltano - Enterprise ETL/ELT Pipeline Engine")
    logger.info("Version: 0.2.0")
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
            "project_id": project_name,
            "environments": [
                {
                    "name": "dev",
                    "config": {
                        "plugins": {"extractors": [], "loaders": [], "transformers": []}
                    },
                },
                {
                    "name": "prod",
                    "config": {
                        "plugins": {"extractors": [], "loaders": [], "transformers": []}
                    },
                },
            ],
            "plugins": {"extractors": [], "loaders": [], "transformers": []},
        }

        meltano_file = project_dir / "meltano.yml"
        with meltano_file.open("w", encoding="utf-8") as f:
            yaml.dump(meltano_config, f, default_flow_style=False)

        # Create .gitignore
        gitignore_content = """
# Meltano
.meltano/
meltano.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
        """.strip()

        gitignore_file = project_dir / ".gitignore"
        with gitignore_file.open("w", encoding="utf-8") as f:
            f.write(gitignore_content)

        # Create README
        readme_content = f"""# {project_name}

FLEXT Meltano ETL Project

## Setup

1. Install Meltano:
   ```bash
   pip install meltano
   ```

2. Initialize the project:
   ```bash
   cd {project_name}
   meltano install
   ```

3. Add extractors and loaders:
   ```bash
   meltano add extractor tap-csv
   meltano add loader target-postgres
   ```

4. Run ETL pipeline:
   ```bash
   meltano run tap-csv target-postgres
   ```

## Configuration

- `meltano.yml`: Main configuration file
- `.env`: Environment variables
- `transform/`: dbt transformations

## Commands

- `meltano run <extractor> <loader>`: Run ETL pipeline
- `meltano invoke <plugin> <command>`: Invoke plugin command
- `meltano test <plugin>`: Test plugin configuration

"""

        readme_file = project_dir / "README.md"
        with readme_file.open("w", encoding="utf-8") as f:
            f.write(readme_content)

    except (OSError, ValueError, yaml.YAMLError) as e:
        logger.error(f"Failed to initialize project: {e}")
        return 1
    else:
        return 0


def list_plugins_command(_args: argparse.Namespace) -> int:
    """List available Meltano plugins."""
    try:
        plugins = {
            "extractors": [
                "tap-oracle-oic",
                "tap-oracle-wms",
                "tap-ldap",
                "tap-csv",
                "tap-postgres",
                "tap-mysql",
                "tap-sqlite",
            ],
            "loaders": [
                "target-oracle-oic",
                "target-oracle-wms",
                "target-ldap",
                "target-csv",
                "target-postgres",
                "target-mysql",
                "target-sqlite",
            ],
            "transformers": ["dbt-ldap", "dbt-postgres", "dbt-oracle"],
        }

        for plugin_type, plugin_list in plugins.items():
            logger.info(f"\n{plugin_type.capitalize()}:")
            for plugin in plugin_list:
                status = "✅ Available" if plugin.startswith(
                    (
                        "tap-oracle",
                        "target-oracle",
                        "tap-ldap",
                        "target-ldap",
                        "dbt-ldap",
                    )
                ) else "📦 Standard"
                logger.info(f"  {plugin}: {status}")

    except (ImportError, AttributeError) as e:
        logger.error(f"Failed to list plugins: {e}")
        return 1
    else:
        return 0


def _validate_meltano_args(extractor: str, loader: str, environment: str | None = None) -> list[str]:
    """Validate and sanitize Meltano command arguments.
    
    Args:
        extractor: The extractor (tap) name to validate
        loader: The loader (target) name to validate  
        environment: Optional environment name to validate
        
    Returns:
        List of validated command arguments
        
    Raises:
        ValueError: If any argument contains invalid characters

    """
    # Validate plugin names - only allow alphanumeric, hyphens, underscores
    import re
    plugin_pattern = re.compile(r"^[a-zA-Z0-9_-]+$")

    if not plugin_pattern.match(extractor):
        raise ValueError(f"Invalid extractor name: {extractor}")
    if not plugin_pattern.match(loader):
        raise ValueError(f"Invalid loader name: {loader}")
    if environment and not plugin_pattern.match(environment):
        raise ValueError(f"Invalid environment name: {environment}")

    # Build command with validated arguments
    cmd = ["meltano", "run", extractor, loader]
    if environment:
        cmd.extend(["--environment", environment])

    return cmd


def run_pipeline_command(args: argparse.Namespace) -> int:
    """Run an ETL pipeline."""
    try:
        extractor = args.extractor
        loader = args.loader
        environment = args.environment

        # Check if meltano.yml exists
        if not Path("meltano.yml").exists():
            logger.error("meltano.yml not found in current directory")
            return 1

        # Validate and build meltano command with security checks
        try:
            cmd = _validate_meltano_args(extractor, loader, environment)
        except ValueError as e:
            logger.error(f"Invalid command arguments: {e}")
            return 1

        # Log command being executed (for debugging)
        logger.info(f"Executing command: {shlex.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
            timeout=300  # 5 minute timeout
        )

        if result.returncode == 0:
            if result.stdout:
                logger.info("Pipeline execution output:")
                logger.info(result.stdout)
        elif result.stderr:
            logger.error("Pipeline execution failed:")
            logger.error(result.stderr)

        return result.returncode

    except FileNotFoundError as e:
        logger.error(f"Meltano not found: {e}")
        return 1
    except subprocess.TimeoutExpired:
        logger.error("Pipeline execution timed out")
        return 1
    except (subprocess.SubprocessError, OSError) as e:
        logger.error(f"Failed to run pipeline: {e}")
        return 1


def validate_command(args: argparse.Namespace) -> int:
    """Validate Meltano configuration."""
    try:
        errors = 0

        # Check if meltano.yml exists
        meltano_file = Path("meltano.yml")
        if not meltano_file.exists():
            errors += 1
        else:
            # Try to parse meltano.yml
            try:
                with meltano_file.open(encoding="utf-8") as f:
                    config = yaml.safe_load(f)

                # Check required fields
                required_fields = ["version", "project_id"]
                for field in required_fields:
                    if field not in config:
                        logger.error(f"Missing required field in meltano.yml: {field}")
                        errors += 1

            except yaml.YAMLError:
                errors += 1

        # Check meltano installation
        try:
            result = subprocess.run(
                ["meltano", "--version"],
                capture_output=True,
                text=True,
                check=False,
                timeout=30  # 30 second timeout
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                logger.info(f"Meltano version: {version}")
            else:
                logger.error("Meltano version check failed")
                errors += 1
        except FileNotFoundError:
            logger.error("Meltano executable not found")
            errors += 1
        except subprocess.TimeoutExpired:
            logger.error("Meltano version check timed out")
            errors += 1

        if errors == 0:
            return 0
        return 1

    except (OSError, yaml.YAMLError) as e:
        logger.error(f"Validation failed: {e}")
        return 1


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="FLEXT Meltano - ETL Integration CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  flext-meltano info                           # Show Meltano information
  flext-meltano init my-project                # Initialize new project
  flext-meltano list-plugins                   # List available plugins
  flext-meltano run tap-csv target-postgres    # Run ETL pipeline
  flext-meltano validate                       # Validate configuration
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Info command
    info_parser = subparsers.add_parser("info", help="Show Meltano information")
    info_parser.set_defaults(func=info_command)

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize new Meltano project")
    init_parser.add_argument("name", help="Project name")
    init_parser.add_argument(
        "--directory", help="Project directory (default: project name)"
    )
    init_parser.set_defaults(func=init_command)

    # List plugins command
    list_plugins_parser = subparsers.add_parser(
        "list-plugins", help="List available plugins"
    )
    list_plugins_parser.set_defaults(func=list_plugins_command)

    # Run pipeline command
    run_parser = subparsers.add_parser("run", help="Run ETL pipeline")
    run_parser.add_argument("extractor", help="Extractor (tap) to use")
    run_parser.add_argument("loader", help="Loader (target) to use")
    run_parser.add_argument("--environment", "-e", help="Environment to use")
    run_parser.set_defaults(func=run_pipeline_command)

    # Validate command
    validate_parser = subparsers.add_parser("validate", help="Validate configuration")
    validate_parser.set_defaults(func=validate_command)

    # Parse arguments
    args = parser.parse_args()

    # Execute command
    if hasattr(args, "func"):
        result = args.func(args)
        return int(result) if result is not None else 0
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
