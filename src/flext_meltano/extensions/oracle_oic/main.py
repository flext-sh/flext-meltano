"""Main entry point for Oracle OIC extension.

REFACTORED: Uses flext-core patterns.
Zero tolerance for code duplication.
"""

from __future__ import annotations

import json
import logging

import typer
from meltano.edk.logging import default_logging_config, parse_log_level

from flext_meltano.extensions.oracle_oic.extension import OracleOICExtension


def get_logger(name: str) -> logging.Logger:
    """Get logger for module."""
    return logging.getLogger(name)

APP_NAME = "flext_oracle_oic_extension"

default_logging_config(level=parse_log_level("INFO"))

logger = get_logger(__name__)

ext = OracleOICExtension()

app = typer.Typer(
    name=APP_NAME,
    help="Oracle Integration Cloud extension for Meltano.",
)


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    log_level: str = typer.Option("INFO", envvar="LOG_LEVEL"),  # noqa: ARG001
    *,
    log_json: bool = typer.Option(default=False, envvar="LOG_JSON"),  # noqa: ARG001
) -> None:
    """Configure extension main entry point."""
    if ctx.invoked_subcommand is None:
        # No subcommand was invoked, show help
        typer.echo(ctx.get_help())


@app.command()
def initialize(
    ctx: typer.Context,  # noqa: ARG001
    *,
    force: bool = typer.Option(default=False, help="Force initialization"),  # noqa: ARG001
) -> None:
    """Initialize Oracle OIC extension."""
    try:
        # Extension initialization logic
        logger.info("Initializing Oracle OIC extension...")
        # Extension does not need special initialization beyond configuration
        logger.info("Oracle OIC extension ready for use")
    except Exception as e:
        logger.exception("Failed to initialize extension", exc_info=e)
        raise typer.Exit(1) from e


@app.command()
def invoke(
    ctx: typer.Context,  # noqa: ARG001
    command_args: list[str] | None = None,
) -> None:
    """Invoke a command on the extension."""
    if command_args is None:
        command_args = []
    logger.info("Invoking command on the extension...")
    if not command_args:
        typer.echo("No command provided. Use --help for available commands.")
        raise typer.Exit(1)

    command = command_args[0] if command_args else None
    args = command_args[1:] if len(command_args) > 1 else []
    try:
        ext.invoke(command, *args)
    except Exception as e:
        logger.exception("Command failed", exc_info=e)
        raise typer.Exit(1) from e


@app.command()
def describe(
    ctx: typer.Context,  # noqa: ARG001
    output_format: str = typer.Option("json", help="Output format (json or text)"),
) -> None:
    """Describe the extension."""
    logger.info("Describing the extension...")
    description = ext.describe()

    if output_format == "json":
        # Output as JSON
        typer.echo(json.dumps(description.model_dump(), indent=2))
    else:
        # Output as text
        typer.echo("Oracle OIC Extension Commands:")
        typer.echo("")
        for cmd in description.commands:
            typer.echo(f"  {cmd.name}")
            typer.echo(f"    {cmd.description}")
            if hasattr(cmd, "args") and cmd.args:
                typer.echo(f"    Usage: {cmd.name} {cmd.args}")
            typer.echo("")


if __name__ == "__main__":
    app()
