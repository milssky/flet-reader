from pathlib import Path
from typing import Final

from flet_reader.common.di import Resolve
from flet_reader.infra import db
from flet_reader.logic.usecases import ConvertBookToSql
from tests.plugins.reader import FILES_DIR

_CREATE_TABLES: Final = (
    Path(__file__).parent.parent.parent
    / 'flet_reader'
    / 'infra'
    / 'db'
    / 'queries'
    / 'create_tables.sql'
)
_BOOK_FILE: Final = FILES_DIR / 'sample.fb2'


def test_converts_book_to_sql(implemented_resolve: Resolve) -> None:
    """Read an FB2 file and save the parsed book."""
    implemented_resolve(db.SqlScriptRunner)(_CREATE_TABLES)
    convert_book = implemented_resolve(ConvertBookToSql)

    book_id = convert_book(_BOOK_FILE)

    assert book_id == 1
