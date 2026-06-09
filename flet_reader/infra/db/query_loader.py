from pathlib import Path
from typing import Final, final

_QUERIES_DIR: Final = Path(__file__).parent / 'queries'


@final
class SqlQueryLoader:
    """Load SQL queries from files."""

    def __call__(self, query_name: str) -> str:
        """Return a query by its file name."""
        return (_QUERIES_DIR / query_name).read_text(encoding='utf-8')
