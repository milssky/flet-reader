from pathlib import Path
from typing import final

import attrs


@final
@attrs.define(frozen=True)
class ConvertBookToSql:
    """Parse book file and save it to database."""

    def __call__(self, book: Path) -> None:
        """Save book file to database."""
