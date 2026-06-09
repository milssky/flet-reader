import contextlib
from typing import Any, Protocol

import pytest
from diwire import Container

from flet_reader import implemented
from flet_reader.common.di import Resolve
from flet_reader.infra import db

_DEFAULT_FACTORY = object()


class ImplementedOverride(Protocol):
    """
    Protocol to use in tests where `implemented_override` fixture is used.

    Importing this type is only allowed under ``if TYPE_CHECKING`` in tests.
    """

    def __call__(
        self,
        dependency: type[Any],
        factory: type[Any] | object = _DEFAULT_FACTORY,
        *,
        scope: Any = ...,
        lifetime: Any = ...,
        **kwargs: Any,
    ) -> contextlib.AbstractContextManager[Resolve]:
        """Dependency override factory protocol."""


@pytest.fixture
def implemented_container(
    db_config: db.DBConfig,
    monkeypatch: pytest.MonkeyPatch,
) -> Container:
    """Provide app DI container configured for tests."""
    container = implemented.create_container(db_config)
    monkeypatch.setattr(implemented, '_container', container)
    return container


@pytest.fixture
def implemented_resolve(
    implemented_container: Container,
) -> Resolve:
    """Provide sync DI resolver configured for tests."""

    def _resolve[Thing](thing: type[Thing]) -> Thing:  # noqa: WPS430
        return implemented_container.resolve(thing)

    return _resolve
