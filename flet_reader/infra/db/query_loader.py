from enum import StrEnum
from pathlib import Path
from typing import Final, final

_QUERIES_DIR: Final = Path(__file__).parent / 'queries'


class SqlQuery(StrEnum):
    """Supported SQL query file names."""

    INSERT_BOOK = 'insert_book.sql'
    INSERT_BOOK_AUTHOR = 'insert_book_author.sql'
    INSERT_CHAPTER = 'insert_chapter.sql'
    INSERT_BLOCK = 'insert_block.sql'


@final
class SqlQueryLoader:
    """Load SQL queries from files."""

    def __call__(self, query_name: SqlQuery) -> str:
        """Return a query by its file name."""
        return (_QUERIES_DIR / query_name.value).read_text(encoding='utf-8')
