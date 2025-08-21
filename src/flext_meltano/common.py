"""Common utilities for flext-meltano."""

from __future__ import annotations


def injectable[T](cls: type[T]) -> type[T]:
    """Decorator to mark classes as injectable for dependency injection.

    This is a simple marker decorator that can be used by DI containers.
    For now, it's a no-op that just returns the class unchanged.
    """
    return cls


__all__ = ["injectable"]
