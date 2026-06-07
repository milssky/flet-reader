from __future__ import annotations

from pathlib import Path
from typing import Final

import pytest

from flet_reader.common.di import Resolve
from flet_reader.common.enums import BlockTypes
from flet_reader.infra.dtos import Book
from flet_reader.infra.files.fictionbook import FBFileReader

_BASE_DIR: Final = Path(__file__).parent.parent.parent


@pytest.fixture
def reader(implemented_resolve: Resolve) -> FBFileReader:
    """Create an FB2 reader."""
    return implemented_resolve(FBFileReader)


@pytest.fixture
def parsed_book(reader: FBFileReader) -> Book:
    """Read the sample FB2 book."""
    book_path = Path(
        _BASE_DIR / 'tests' / 'test_infra' / 'files' / 'sample.fb2',
    )
    return reader(book_path)


def test_fb2reader_metadata(parsed_book: Book) -> None:
    """Ensure FBFileReader parses book metadata."""
    assert parsed_book.title == 'A Study in Scarlet'
    assert parsed_book.authors == ['Arthur Conan Doyle']


def test_fb2reader_chapters(parsed_book: Book) -> None:
    """Ensure FBFileReader preserves the section hierarchy."""
    assert [
        (chapter.title, chapter.level, len(chapter.blocks))
        for chapter in parsed_book.chapters
    ] == [
        ('', 1, 1),
        ('PART I.', 1, 1),
        ('', 2, 1),
        ('CHAPTER I. MR. SHERLOCK HOLMES.', 2, 3),
    ]


def test_fb2reader_blocks(parsed_book: Book) -> None:
    """Ensure FBFileReader extracts text blocks."""
    first_block = parsed_book.chapters[0].blocks[0]
    assert first_block.type is BlockTypes.text
    assert isinstance(first_block.content, str)
    assert first_block.content.startswith(
        'Frontispiece, with the caption:',
    )
    nested_block = parsed_book.chapters[2].blocks[0]
    assert isinstance(nested_block.content, str)
    assert nested_block.content == (
        '(Being a reprint from the reminiscences of JOHN H. WATSON, M.D.,'
        ' late of the Army Medical Department.) 2'
    )


def test_fb2reader_section_title_block(parsed_book: Book) -> None:
    """Ensure section title becomes its first block."""
    title_block = parsed_book.chapters[1].blocks[0]
    assert title_block.type is BlockTypes.header
    assert title_block.content == 'PART I.'


def test_fb2reader_without_body(
    reader: FBFileReader,
    tmp_path: Path,
) -> None:
    """Ensure a book without body has no chapters."""
    book_path = tmp_path / 'without-body.fb2'
    book_path.write_text(
        '<FictionBook '
        'xmlns="http://www.gribuser.ru/xml/fictionbook/2.0"/>',
    )

    assert reader(book_path).chapters == []


def test_fb2reader_image_block(
    reader: FBFileReader,
    tmp_path: Path,
) -> None:
    """Ensure an FB2 image becomes an image block."""
    book_path = tmp_path / 'with-image.fb2'
    book_path.write_text(
        '<FictionBook '
        'xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" '
        'xmlns:xlink="http://www.w3.org/1999/xlink">'
        '<body><section><image xlink:href="#cover"/></section></body>'
        '</FictionBook>',
    )

    image_block = reader(book_path).chapters[0].blocks[0]
    assert image_block.type is BlockTypes.image
    assert image_block.content == '#cover'
