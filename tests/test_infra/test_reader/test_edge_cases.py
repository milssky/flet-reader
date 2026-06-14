from pathlib import Path

from flet_reader.common.enums import BlockTypes
from flet_reader.infra.files.fictionbook import FBFileReader


def test_fb2reader_without_body(
    reader: FBFileReader,
    tmp_path: Path,
) -> None:
    """Ensure a book without body has no chapters."""
    book_path = tmp_path / 'without-body.fb2'
    book_path.write_text(
        '<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0"/>',
    )

    assert reader(book_path).chapters == []


def test_fb2reader_body_without_readable_blocks(
    reader: FBFileReader,
    tmp_path: Path,
) -> None:
    """Ensure an empty body has no fallback chapter."""
    book_path = tmp_path / 'empty-body.fb2'
    book_path.write_text(
        '<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">'
        '<body><empty-line/></body>'
        '</FictionBook>',
    )

    assert reader(book_path).chapters == []


def test_fb2reader_image_block(
    reader: FBFileReader,
    tmp_path: Path,
) -> None:
    """Ensure an FB2 image becomes an image block."""
    book_path = tmp_path / 'with-image.fb2'
    book_path.write_text(
        '<FictionBook '
        'xmlns="http://www.gribuser.ru/xml/fictionbook/2.0" '
        'xmlns:xlink="http://www.w3.org/1999/xlink">'
        '<body><section><image xlink:href="#cover"/></section></body>'
        '</FictionBook>',
    )

    image_block = reader(book_path).chapters[0].blocks[0]
    assert image_block.type is BlockTypes.image
    assert image_block.content == '#cover'


def test_fb2reader_blocks_inside_container(
    reader: FBFileReader,
    tmp_path: Path,
) -> None:
    """Ensure blocks inside FB2 containers are retained."""
    book_path = tmp_path / 'with-cite.fb2'
    book_path.write_text(
        '<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">'
        '<body><section><cite><p>Quoted text.</p></cite></section></body>'
        '</FictionBook>',
    )

    blocks = reader(book_path).chapters[0].blocks

    assert [(block.type, block.content) for block in blocks] == [
        (BlockTypes.text, 'Quoted text.'),
    ]


def test_fb2reader_body_paragraphs_wo_sections(
    reader: FBFileReader,
    tmp_path: Path,
) -> None:
    """Ensure direct body paragraphs become a fallback chapter."""
    book_path = tmp_path / 'without-sections.fb2'
    book_path.write_text(
        '<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">'
        '<body>'
        '<title><p>Fallback chapter</p></title>'
        '<p>First paragraph.</p>'
        '<p>Second <emphasis>paragraph</emphasis>.</p>'
        '</body>'
        '</FictionBook>',
    )

    chapters = reader(book_path).chapters

    assert len(chapters) == 1
    assert chapters[0].title == 'Fallback chapter'
    assert chapters[0].level == 1
    assert [(block.type, block.content) for block in chapters[0].blocks] == [
        (BlockTypes.header, 'Fallback chapter'),
        (BlockTypes.text, 'First paragraph.'),
        (BlockTypes.text, 'Second paragraph.'),
    ]
