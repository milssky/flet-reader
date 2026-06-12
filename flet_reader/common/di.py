import importlib
import types
from typing import ClassVar, Protocol, final


class Resolve(Protocol):
    """Resolve protocol for regular types."""

    def __call__[Thing](self, thing: type[Thing]) -> Thing:
        """Returns resolved type with deps."""


class HasContainer:
    """Base class for all parts that use ``resolve()`` function."""

    #: Speed up the resolution, do not import module twice.
    _resolved: ClassVar[types.ModuleType | None] = None

    @final
    @classmethod
    def _get_resolve(cls) -> Resolve:
        if cls._resolved is None:  # pragma: no cover
            cls._resolved = importlib.import_module('flet_reader.implemented')
        return cls._resolved.resolve  # type: ignore[no-any-return]  # pragma: no cover

    @final
    def _resolve[Thing](self, thing: type[Thing]) -> Thing:
        return self._get_resolve()(thing)  # pragma: no cover
