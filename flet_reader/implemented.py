# NOTE: simple layers go on top!

from __future__ import annotations

from typing import TYPE_CHECKING

from diwire import Container, Lifetime

if TYPE_CHECKING:
    from flet_reader.infra import db

DEFAULT_DB_PATH = 'flet-reader.sqlite3'


def create_container(
    db_config: db.DBConfig | None = None,
) -> Container:
    """Creates DI container, which can be re-created in tests."""
    from lxml import etree

    from flet_reader.infra import db
    from flet_reader.logic import usacases

    container = Container(default_lifetime=Lifetime.TRANSIENT)

    container.add_instance(
        db_config or db.DBConfig(path=DEFAULT_DB_PATH),
        provides=db.DBConfig,
    )
    container.add_instance(
        etree.XMLParser(
            resolve_entities=False,
            no_network=True,
            load_dtd=False,
            dtd_validation=False,
            huge_tree=False,
            recover=False,
            remove_blank_text=False,
        ),
    )
    container.add(db.DBConnection)
    container.add(db.SqlScriptRunner)

    container.add(usacases.ConvertBookToSql)

    return container


_container = create_container()


def resolve[Thing](thing: type[Thing]) -> Thing:
    """Type-safe resolution."""
    return _container.resolve(thing)  # pragma: no cover
