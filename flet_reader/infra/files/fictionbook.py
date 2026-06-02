from pathlib import Path
from typing import final

import attrs


@final
@attrs.define(frozen=True)
class FBFileReader:
    """FB2 book file reader."""

    def __call__(self, file_path: Path) -> Book:
        """Conver file to DTO."""
        return Book(
            title=self._get_title(),
            sections=self._get_sections(),
            author=self._get_author(),
        )

    def _get_title(self) -> str:
        ...

    def _get_sections(self) -> list[Section]:
        ...

    def _get_author(self) -> str:
        ...
