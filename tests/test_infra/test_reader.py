from __future__ import annotations

from pathlib import Path
from typing import Final

from flet_reader.common.di import Resolve
from flet_reader.infra.dtos import Book
from flet_reader.infra.files.fictionbook import FBFileReader

_BASE_DIR: Final = Path(__file__).parent.parent.parent


def test_fb2reader(implemented_resolve: Resolve) -> None:
    """Ensure FBFileReader parses .fb2 file."""
    reader = implemented_resolve(FBFileReader)
    book_path = Path(
        _BASE_DIR / 'tests' / 'test_infra' / 'files' / 'sample.fb2',
    )

    book = reader(book_path)

    assert isinstance(book, Book)
    assert book.title == 'A Study in Scarlet'
    assert isinstance(book.authors, list)
    assert book.authors == ['Arthur Conan Doyle']
