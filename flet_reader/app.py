from typing import Final, final

import flet as ft

from flet_reader.common.di import HasContainer
from flet_reader.components.book_catalog import BookCatalog
from flet_reader.infra.db import BooksInfoLoader

BOOK_ROUTE_PREFIX: Final = '/books/'


@final
class ReaderApp(HasContainer):  # pragma: no cover
    """Main app class."""

    def __init__(self, page: ft.Page) -> None:
        """Create the application for a Flet page."""
        self._page = page

    def run(self) -> None:
        """Configure the page and render the current route."""
        self._page.title = 'Flet Reader'
        self._page.on_route_change = self._route_change
        self._page.on_view_pop = self._view_pop
        self._route_change()

    def _route_change(
        self,
        event: ft.RouteChangeEvent | None = None,
    ) -> None:
        """Rebuild the view stack for the current route."""
        route = self._page.route if event is None else event.route
        self._page.views = self._build_views(route)
        self._page.update()

    async def _view_pop(self, event: ft.ViewPopEvent) -> None:
        """Return to the view below the one being closed."""
        if event.view is not None:
            self._page.views.remove(event.view)
        await self._page.push_route(self._page.views[-1].route)

    def _open_book(self, book_id: int) -> None:
        """Open the selected book page."""
        self._page.navigate(f'{BOOK_ROUTE_PREFIX}{book_id}')

    def _close_book(self) -> None:
        """Return to the book catalog."""
        self._page.navigate('/')

    def _build_views(self, route: str) -> list[ft.View]:
        """Build the view stack for an application route."""
        views = [
            ft.View(
                route='/',
                appbar=ft.AppBar(title=ft.Text('Books')),
                controls=[
                    BookCatalog(
                        books=self._resolve(BooksInfoLoader)(),
                        on_book_selected=self._open_book,
                    ),
                ],
            ),
        ]

        if route.startswith(BOOK_ROUTE_PREFIX):
            book_id = route.removeprefix(BOOK_ROUTE_PREFIX)
            views.append(
                ft.View(
                    route=route,
                    appbar=ft.AppBar(
                        leading=ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            on_click=self._close_book,
                        ),
                    ),
                    controls=[ft.Text(f'Book ID: {book_id}')],
                    padding=24,
                ),
            )

        return views
