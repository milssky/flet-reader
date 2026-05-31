from typing import Protocol


class Resolve(Protocol):
    """Resolve protocol for regular types."""

    def __call__[Thing](self, thing: type[Thing]) -> Thing:
        """Returns resolved type with deps."""
