from typing import final, override

import flet as ft

from flet_reader.common.di import HasContainer
from flet_reader.infra.db import LoadBooksInfo


@final
class ReaderApp(ft.Container, HasContainer):
    """Main app class."""

    @override
    def init(self) -> None:
        """Init app layout."""
        self.books_list = ft.Text(
            value='\n'.join([
                f'{book_info.title} - {book_info.author}'
                for book_info in self._resolve(LoadBooksInfo)()
            ]),
        )
        self.content = ft.Column(  # noqa: WPS110
            controls=[ft.Row(controls=[self.books_list])],
        )


def main(page: ft.Page) -> None:
    """Entrypoint."""
    page.title = 'Flet Reader'
    reader = ReaderApp()
    page.add(reader)


if __name__ == '__main__':  # pragma: no cover
    ft.run(main)
