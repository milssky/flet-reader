from flet_reader.common.di import Resolve
from flet_reader.infra import db
from flet_reader.infra.dtos import Book, ShortBookInfo


def test_loads_short_book_info(implemented_resolve: Resolve) -> None:
    """Load saved book metadata for the catalog."""
    book_id = implemented_resolve(db.BookSaver)(
        Book(
            title='Test book',
            authors=['Test author'],
            chapters=[],
        ),
    )

    books = implemented_resolve(db.BooksInfoLoader)()

    assert books == [
        ShortBookInfo(
            id=book_id,
            title='Test book',
            author='Test author',
        ),
    ]
