import sqlite3
from collections.abc import Iterator
from contextlib import closing
from pathlib import Path
from typing import Final
from uuid import uuid4

import pytest

from flet_reader.common.di import Resolve
from flet_reader.infra import db

_CREATE_TABLES: Final = (
    Path(__file__).parent.parent.parent
    / 'flet_reader'
    / 'infra'
    / 'db'
    / 'queries'
    / 'create_tables.sql'
)


@pytest.fixture
def db_config() -> db.DBConfig:
    """Provide an in-memory database config for each test."""
    database_uri = (
        f'file:flet-reader-test-{uuid4().hex}?mode=memory&cache=shared'
    )
    return db.DBConfig(path=database_uri, uri=True)


@pytest.fixture(autouse=True)
def db_connection(
    db_config: db.DBConfig,
) -> Iterator[sqlite3.Connection]:
    """Provide an in-memory database for each test."""
    with closing(
        sqlite3.connect(db_config.path, uri=db_config.uri),
    ) as connection:
        connection.row_factory = sqlite3.Row
        connection.execute('PRAGMA foreign_keys = ON')

        yield connection


@pytest.fixture(autouse=True)
def migrate_database(
    db_connection: sqlite3.Connection,
    implemented_resolve: Resolve,
) -> None:
    """Apply database migrations before each test."""
    implemented_resolve(db.SqlScriptRunner)(_CREATE_TABLES)
