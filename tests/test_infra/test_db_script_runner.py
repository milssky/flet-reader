from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Final

from flet_reader.common.di import Resolve
from flet_reader.infra import db

_BASE_DIR: Final = Path(__file__).parent.parent.parent


def test_create_tables_script(
    db_connection: sqlite3.Connection,
    implemented_resolve: Resolve,
) -> None:
    """Runs the real create-tables script and checks DB schema behavior."""
    query = (
        _BASE_DIR
        / 'flet_reader'
        / 'infra'
        / 'db'
        / 'queries'
        / 'create_tables.sql'
    )
    script_runner = implemented_resolve(db.SqlScriptRunner)

    script_runner(query)
    table_names = {
        row['name']
        for row in db_connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """,
        ).fetchall()
    }

    assert table_names == {'books', 'chapters', 'blocks'}
