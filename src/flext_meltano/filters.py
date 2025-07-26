"""FlextMeltano Helper - Output Filters and Cleaners.

Utilities for filtering warnings and cleaning output from various tools.
"""

from __future__ import annotations


def filter_singer_warnings(stderr_text: str) -> str:
    """Filter out Singer SDK deprecation warnings from stderr to achieve zero warnings.

    Args:
        stderr_text: Raw stderr text from Singer SDK commands

    Returns:
        Filtered stderr text with warnings removed

    """
    if not stderr_text:
        return stderr_text

    lines = stderr_text.split("\n")
    filtered_lines = []
    warning_patterns = [
        "SingerSDKDeprecationWarning:",
        "DeprecationWarning:",
        "PendingDeprecationWarning:",
        "Invalid -W option ignored:",
        "Warning:",
        "UserWarning:",
        # Specific Singer SDK warning patterns
        "schema_translator.py:",
        "singer_sdk/batch.py:",
        "singer_sdk/streams/core.py:",
        # Meltano specific warnings
        "meltano.cli.cli:",
        "meltano.core.runner:",
    ]

    for line in lines:
        # Skip lines that contain warning patterns
        should_filter = any(pattern in line for pattern in warning_patterns)
        if not should_filter:
            filtered_lines.append(line)

    return "\n".join(filtered_lines)


def filter_meltano_warnings(output: str) -> str:
    """Filter out Meltano CLI warnings and info messages.

    Args:
        output: Raw output from Meltano CLI commands

    Returns:
        Filtered output with warnings removed

    """
    if not output:
        return output

    lines = output.split("\n")
    filtered_lines = []
    warning_patterns = [
        "meltano.cli.cli:WARNING",
        "meltano.core.runner:INFO",
        "urllib3.connectionpool:INFO",
        "requests.packages.urllib3:INFO",
        # Remove timestamp prefixed lines that are just informational
        "[20",  # Matches lines starting with timestamps like [2024-
    ]

    for line in lines:
        # Skip lines that contain warning patterns
        should_filter = any(pattern in line for pattern in warning_patterns)
        if not should_filter and line.strip():  # Also skip empty lines
            filtered_lines.append(line)

    return "\n".join(filtered_lines)
