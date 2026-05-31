# NOTE: simple layers go on top!

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import punq

if TYPE_CHECKING:
    from flet_reader.infra import db

DEFAULT_DB_PATH = 'flet-reader.sqlite3'


def create_injector[Thing](
    container: punq.Container,
    localns: dict[str, Any],
) -> Callable[[Thing], Thing]:
    # We need to provide the same string names as we do in the definition.
    localns.pop('container')
    container.registrations._localns.update(localns)  # noqa: SLF001
    return lambda service: service


def create_container(
    db_config: db.DBConfig | None = None,
) -> punq.Container:
    """Creates `punq` container, which can be re-created in tests."""
    from flet_reader.infra import db

    container = punq.Container()

    container.register(
        db.DBConfig,
        instance=db_config or db.DBConfig(path=DEFAULT_DB_PATH),
        scope=punq.Scope.singleton,
    )
    container.register(db.DBConnection)
    container.register(db.SqlScriptRunner)

    return container


_container = create_container()


def resolve[Thing](thing: type[Thing]) -> Thing:
    """Type-safe resolution for `punq`."""
    return _container.resolve(thing)  # type: ignore[no-any-return]  # pragma: no cover
