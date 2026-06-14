from typing import final

import attrs

from flet_reader.infra.db.connection import DBConnection
from flet_reader.infra.db.query_loader import SqlQuery, SqlQueryLoader
from flet_reader.infra.dtos import ShortBookInfo


@final
@attrs.define(frozen=True)
class LoadBooksInfo:
    """Load book info."""

    _query: SqlQueryLoader
    _connection: DBConnection

    def __call__(self) -> list[ShortBookInfo]:
        """Call load script."""
        with self._connection() as connection:
            cursor = connection.execute(self._query(SqlQuery.LOAD_BOOKS_INFO))
            return [
                ShortBookInfo(
                    title=row['title'],
                    author=row['name'],
                )
                for row in cursor.fetchall()
            ]
