from flet_reader.common.enums import BlockTypes
from flet_reader.infra.dtos import Book


def test_fb2reader_blocks(parsed_book: Book) -> None:
    """Ensure FBFileReader extracts text blocks."""
    first_block = parsed_book.chapters[0].blocks[0]
    assert first_block.type is BlockTypes.text
    assert isinstance(first_block.content, str)
    assert first_block.content.startswith(
        'Frontispiece, with the caption:',
    )
    nested_block = parsed_book.chapters[2].blocks[0]
    assert isinstance(nested_block.content, str)
    assert nested_block.content == (
        '(Being a reprint from the reminiscences of JOHN H. WATSON, M.D.,'
        ' late of the Army Medical Department.) 2'
    )


def test_fb2reader_section_title_block(parsed_book: Book) -> None:
    """Ensure section title becomes its first block."""
    title_block = parsed_book.chapters[1].blocks[0]
    assert title_block.type is BlockTypes.header
    assert title_block.content == 'PART I.'
