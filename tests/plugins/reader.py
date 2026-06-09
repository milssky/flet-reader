from pathlib import Path
from typing import Final

import pytest

from flet_reader.common.di import Resolve
from flet_reader.infra.dtos import Book
from flet_reader.infra.files.fictionbook import FBFileReader

FILES_DIR: Final = Path(__file__).parent.parent / 'fixtures' / 'files'


@pytest.fixture
def reader(implemented_resolve: Resolve) -> FBFileReader:
    """Create an FB2 reader."""
    return implemented_resolve(FBFileReader)


@pytest.fixture
def parsed_book(reader: FBFileReader) -> Book:
    """Read the sample FB2 book."""
    return reader(FILES_DIR / 'sample.fb2')
