import flet as ft

from flet_reader.app import ReaderApp


def main(page: ft.Page) -> None:  # pragma: no cover
    """Entrypoint."""
    ReaderApp(page).run()


if __name__ == '__main__':  # pragma: no cover
    ft.run(main)
