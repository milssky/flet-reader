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
