from typing import cast
from unittest.mock import Mock

import flet as ft
import pytest


@pytest.fixture
def mock_page() -> ft.Page:
    """Provide an isolated page mock for application unit tests."""
    return cast(ft.Page, Mock(spec=ft.Page))
