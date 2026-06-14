from collections.abc import Callable, Sequence
from typing import final

import flet as ft

from flet_reader.infra.dtos import ShortBookInfo


@final
class BookCatalog(ft.Container):
    """Scrollable adaptive grid of book cards."""

    def __init__(
        self,
        books: Sequence[ShortBookInfo],
        on_book_selected: Callable[[int], None],
    ) -> None:
        """Create catalog from short book descriptions."""
        super().__init__(expand=True)
        self._on_book_selected = on_book_selected
        self.content = ft.GridView(  # noqa: WPS110
            controls=[self._build_card(book) for book in books],
            max_extent=220,
            child_aspect_ratio=0.72,
            spacing=16,
            run_spacing=16,
            padding=16,
            expand=True,
        )

    def _build_card(self, book: ShortBookInfo) -> ft.Control:
        """Build a single book card."""
        return ft.Card(
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Container(
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                padding=16,
                ink=True,
                on_click=lambda: self._on_book_selected(book.id),
                content=ft.Column(  # noqa: WPS110
                    controls=[
                        ft.Container(
                            expand=True,
                            alignment=ft.Alignment.CENTER,
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
                            border_radius=12,
                            content=ft.Icon(
                                ft.Icons.MENU_BOOK_ROUNDED,
                                size=56,
                                color=ft.Colors.ON_SURFACE_VARIANT,
                            ),
                        ),
                        ft.Text(
                            book.title,
                            max_lines=2,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            weight=ft.FontWeight.W_600,
                        ),
                        ft.Text(
                            book.author,
                            max_lines=1,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            color=ft.Colors.ON_SURFACE_VARIANT,
                        ),
                    ],
                ),
            ),
        )
