from typing import final, override

import flet as ft

from flet_reader.common.di import HasContainer
from flet_reader.components.book_catalog import BookCatalog
from flet_reader.infra.db import BooksInfoLoader


@final
class ReaderApp(ft.Container, HasContainer):
    """Main app class."""

    @override
    def init(self) -> None:
        """Init app layout."""
        self.content = BookCatalog(  # noqa: WPS110(
            books=self._resolve(BooksInfoLoader)(),
        )


def main(page: ft.Page) -> None:
    """Entrypoint."""
    page.title = 'Flet Reader'
    reader = ReaderApp()
    page.add(reader)


if __name__ == '__main__':  # pragma: no cover
    ft.run(main)
