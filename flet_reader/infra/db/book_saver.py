import sqlite3
from typing import final

import attrs

from flet_reader.infra.db.connection import DBConnection
from flet_reader.infra.db.query_loader import SqlQueryLoader
from flet_reader.infra.dtos import Block, Book, Chapter


@final
@attrs.define(frozen=True)
class BookSaver:
    """Save a book DTO to SQLite."""

    _connection: DBConnection
    _query: SqlQueryLoader

    def __call__(self, book: Book) -> int:
        """Save the complete book in one transaction and return its ID."""
        with self._connection() as connection, connection:
            book_id = self._insert_book(connection, book)
            self._insert_authors(connection, book_id, book.authors)
            self._insert_chapters(connection, book_id, book.chapters)
        return book_id

    def _insert_book(
        self,
        connection: sqlite3.Connection,
        book: Book,
    ) -> int:
        cursor = connection.execute(
            self._query('insert_book.sql'),
            {'title': book.title},
        )
        book_id = cursor.lastrowid
        if book_id is None:  # pragma: no cover
            raise RuntimeError('SQLite did not return a book ID')
        return book_id

    def _insert_authors(
        self,
        connection: sqlite3.Connection,
        book_id: int,
        authors: list[str],
    ) -> None:
        connection.executemany(
            self._query('insert_book_author.sql'),
            (
                {
                    'book_id': book_id,
                    'order_index': order_index,
                    'name': author,
                }
                for order_index, author in enumerate(authors)
            ),
        )

    def _insert_chapters(
        self,
        connection: sqlite3.Connection,
        book_id: int,
        chapters: list[Chapter],
    ) -> None:
        parent_ids: list[int] = []
        for order_index, chapter in enumerate(chapters):
            self._validate_level(chapter.level, parent_ids)
            parent_ids = parent_ids[: chapter.level - 1]
            parent_id = parent_ids[-1] if parent_ids else None
            chapter_id = self._insert_chapter(
                connection,
                book_id,
                parent_id,
                order_index,
                chapter,
            )
            parent_ids.append(chapter_id)
            self._insert_blocks(
                connection,
                book_id,
                chapter_id,
                chapter.blocks,
            )

    def _insert_chapter(
        self,
        connection: sqlite3.Connection,
        book_id: int,
        parent_id: int | None,
        order_index: int,
        chapter: Chapter,
    ) -> int:
        cursor = connection.execute(
            self._query('insert_chapter.sql'),
            {
                'book_id': book_id,
                'parent_id': parent_id,
                'title': chapter.title,
                'order_index': order_index,
                'level': chapter.level,
            },
        )
        chapter_id = cursor.lastrowid
        if chapter_id is None:  # pragma: no cover
            raise RuntimeError('SQLite did not return a chapter ID')
        return chapter_id

    def _insert_blocks(
        self,
        connection: sqlite3.Connection,
        book_id: int,
        chapter_id: int,
        blocks: list[Block],
    ) -> None:
        connection.executemany(
            self._query('insert_block.sql'),
            (
                {
                    'book_id': book_id,
                    'chapter_id': chapter_id,
                    'order_index': order_index,
                    'type': block.type.value,
                    'content': (
                        block.content
                        if isinstance(block.content, str)
                        else None
                    ),
                    'payload': (
                        block.content
                        if isinstance(block.content, bytes)
                        else None
                    ),
                }
                for order_index, block in enumerate(blocks)
            ),
        )

    def _validate_level(
        self,
        level: int,
        parent_ids: list[int],
    ) -> None:
        if level < 1 or level > len(parent_ids) + 1:
            raise ValueError(f'Invalid chapter level: {level}')
