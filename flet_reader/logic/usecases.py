from pathlib import Path
from typing import final

import attrs

from flet_reader.infra.db import BookSaver
from flet_reader.infra.files.fictionbook import FBFileReader


@final
@attrs.define(frozen=True)
class ConvertBookToSql:
    """Parse book file and save it to database."""

    _saver: BookSaver
    _reader: FBFileReader

    def __call__(self, book_path: Path) -> int:
        """Save book file to database."""
        book = self._reader(book_path)
        return self._saver(book)
