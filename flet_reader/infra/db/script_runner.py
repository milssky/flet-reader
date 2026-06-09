import sqlite3
from pathlib import Path
from typing import final

import attrs

from flet_reader.infra.db.connection import DBConnection


@final
@attrs.define(frozen=True)
class SqlScriptRunner:
    """Run single sql script."""

    _connection: DBConnection

    def __call__(self, script_path: Path) -> None:
        """Execute script."""
        with self._connection() as conn:
            self._run_script(conn, script_path)
            conn.commit()

    def _run_script(self, conn: sqlite3.Connection, script_path: Path) -> None:
        sql = script_path.read_text(encoding='utf-8')
        conn.executescript(sql)
