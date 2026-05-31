from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import closing
from uuid import uuid4

import pytest

from flet_reader.infra import db


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
