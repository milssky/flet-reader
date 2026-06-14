import sqlite3

import pytest

from flet_reader.common.di import Resolve
from flet_reader.common.enums import BlockTypes
from flet_reader.infra import db
from flet_reader.infra.dtos import Block, Book, Chapter


def test_saves_complete_book(
    implemented_resolve: Resolve,
    db_connection: sqlite3.Connection,
) -> None:
    """Saves metadata, chapter hierarchy, and block payloads."""
    book_saver = implemented_resolve(db.BookSaver)
    book = Book(
        title='Test book',
        authors=['First Author', 'Second Author'],
        chapters=[
            Chapter(
                title='Parent',
                level=1,
                blocks=[
                    Block(type=BlockTypes.text, content='Text'),
                    Block(type=BlockTypes.image, content=b'image'),
                ],
            ),
            Chapter(
                title='Child',
                level=2,
                blocks=[],
            ),
            Chapter(
                title='Next parent',
                level=1,
                blocks=[],
            ),
        ],
    )

    book_id = book_saver(book)

    _assert_metadata(db_connection, book_id)
    _assert_chapters(db_connection)
    _assert_blocks(db_connection)


def _assert_metadata(
    db_connection: sqlite3.Connection,
    book_id: int,
) -> None:
    saved_book = db_connection.execute(
        'SELECT id, title FROM books',
    ).fetchone()
    saved_authors = db_connection.execute(
        """
        SELECT order_index, name
        FROM book_authors
        ORDER BY order_index
        """,
    ).fetchall()

    assert dict(saved_book) == {'id': book_id, 'title': 'Test book'}
    assert [tuple(row) for row in saved_authors] == [
        (0, 'First Author'),
        (1, 'Second Author'),
    ]


def _assert_chapters(db_connection: sqlite3.Connection) -> None:
    saved_chapters = db_connection.execute(
        """
        SELECT id, parent_id, title, order_index, level
        FROM chapters
        ORDER BY order_index
        """,
    ).fetchall()

    assert [tuple(row)[1:] for row in saved_chapters] == [
        (None, 'Parent', 0, 1),
        (saved_chapters[0]['id'], 'Child', 1, 2),
        (None, 'Next parent', 2, 1),
    ]


def _assert_blocks(db_connection: sqlite3.Connection) -> None:
    saved_blocks = db_connection.execute(
        """
        SELECT order_index, type, content, payload
        FROM blocks
        ORDER BY order_index
        """,
    ).fetchall()

    assert [tuple(row) for row in saved_blocks] == [
        (0, 'text', 'Text', None),
        (1, 'image', None, b'image'),
    ]


def test_rolls_back_invalid_chapter_level(
    implemented_resolve: Resolve,
    db_connection: sqlite3.Connection,
) -> None:
    """Does not leave a partial book after invalid hierarchy."""
    book_saver = implemented_resolve(db.BookSaver)
    book = Book(
        title='Invalid book',
        authors=[],
        chapters=[
            Chapter(
                title='Invalid child',
                level=2,
                blocks=[],
            ),
        ],
    )

    with pytest.raises(ValueError, match='Invalid chapter level: 2'):
        book_saver(book)

    saved_books = db_connection.execute(
        'SELECT COUNT(*) FROM books',
    ).fetchone()[0]
    assert saved_books == 0
