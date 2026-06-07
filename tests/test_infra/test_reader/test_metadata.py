from flet_reader.infra.dtos import Book


def test_fb2reader_metadata(parsed_book: Book) -> None:
    """Ensure FBFileReader parses book metadata."""
    assert parsed_book.title == 'A Study in Scarlet'
    assert parsed_book.authors == ['Arthur Conan Doyle']
