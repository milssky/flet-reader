from typing import Final

from flet_reader.common.di import Resolve
from flet_reader.logic.usecases import ConvertBookToSql
from tests.plugins.reader import FILES_DIR

_BOOK_FILE: Final = FILES_DIR / 'sample.fb2'


def test_converts_book_to_sql(implemented_resolve: Resolve) -> None:
    """Read an FB2 file and save the parsed book."""
    convert_book = implemented_resolve(ConvertBookToSql)

    book_id = convert_book(_BOOK_FILE)

    assert book_id == 1
