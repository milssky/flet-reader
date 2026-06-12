from typing import final

import flet as ft

from flet_reader.common.di import HasContainer


@final
class ReaderApp(ft.Container, HasContainer):
    """Main app class."""


def main(page: ft.Page) -> None:  # pragma: no cover
    """Entrypoint."""
    page.title = 'Flet Reader'
    reader = ReaderApp()
    page.add(reader)


if __name__ == '__main__':  # pragma: no cover
    ft.run(main)
