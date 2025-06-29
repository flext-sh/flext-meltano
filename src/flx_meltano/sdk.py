"""Meltano SDK for FLX.

This module provides a high-level SDK for interacting with Meltano,
including custom exception classes for better error handling.
"""

from __future__ import annotations


class MeltanoError(Exception):
    r"""MeltanoError - Custom Exception.

    Implementa exceção customizada para casos específicos do domínio. Fornece informações detalhadas sobre erros.

    Arquitetura: Enterprise Patterns
    Padrões: SOLID principles, clean code

    Attributes: Sem atributos públicos documentados.

    Methods: Sem métodos públicos.

    Examples: Uso típico da classe:

    ```python
    instance = MeltanoError()\n    result = instance.method()
    ```

    See Also
    --------
    - [Documentação da Arquitetura](../../docs/architecture/index.md)
    - [Padrões de Design](../../docs/architecture/001-clean-architecture-ddd.md)

    Note: Esta classe segue os padrões Enterprise Patterns estabelecidos no projeto.

    """

    """Base exception class for Meltano-related errors."""


class MeltanoProjectError(MeltanoError):
    """Raised for errors related to Meltano project management."""


class MeltanoExecutionError(MeltanoError):
    """Raised for errors during Meltano command execution."""

    def __init__(
        self,
        message: str,
        command: list[str] | None = None,
        returncode: int | None = None,
        stdout: str | None = None,
        stderr: str | None = None,
    ) -> None:
        """Initialize the Meltano execution exception.

        Creates a detailed exception for Meltano command execution failures,
        capturing command details, return codes, and output for debugging.

        Args:
        ----
            message: Description of the execution error.
            command: The Meltano command that failed.
            returncode: Process exit code if available.
            stdout: Standard output from the failed command.
            stderr: Standard error output from the failed command.

        Note:
        ----
            Provides comprehensive error context for debugging.

        """
        super().__init__(message)
        self.command = command
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = stderr
