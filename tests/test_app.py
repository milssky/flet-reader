import flet as ft

from flet_reader.main import main


def test_main_sets_window_title(mock_page: ft.Page) -> None:
    """Ensure that the application sets the expected window title."""
    main(mock_page)

    assert mock_page.title == 'Flet Reader'
