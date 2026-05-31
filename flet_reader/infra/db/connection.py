from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from typing import final

import attrs


@final
@attrs.define(frozen=True)
class DBConfig:
    """SQLite database configuration."""

    path: str
    uri: bool = False


@final
@attrs.define(frozen=True)
class DBConnection:
    """Provide connection to sqlite DB."""

    _config: DBConfig

    @contextmanager
    def __call__(self) -> Iterator[sqlite3.Connection]:
        """Returns connection iterator."""
        conn = sqlite3.connect(self._config.path, uri=self._config.uri)
        conn.row_factory = sqlite3.Row

        conn.execute('PRAGMA foreign_keys = ON')

        try:
            yield conn
        finally:
            conn.close()
