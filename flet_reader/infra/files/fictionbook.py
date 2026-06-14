from pathlib import Path
from types import MappingProxyType
from typing import Final, final

import attrs
from lxml import etree

from flet_reader.common.enums import BlockTypes
from flet_reader.infra.dtos import Block, Book, Chapter

FB2_NS: Final = 'http://www.gribuser.ru/xml/fictionbook/2.0'
XLINK_NS: Final = 'http://www.w3.org/1999/xlink'

NS = MappingProxyType({
    'fb': FB2_NS,
    'xlink': XLINK_NS,
})


@final
@attrs.define(frozen=True)
class FBFileReader:  # noqa: WPS214
    """FB2 book file reader."""

    _parser: etree.XMLParser

    def __call__(self, file_path: Path) -> Book:
        """Convert file to DTO."""
        root = etree.fromstring(self._open_book(file_path), parser=self._parser)
        return Book(
            title=self._get_title(root),
            chapters=self._get_chapters(root),
            authors=self._get_author(root),
        )

    def _open_book(self, file_path: Path) -> bytes:
        return file_path.read_bytes()

    def _get_title(self, root: etree.Element) -> str:
        return (
            root.findtext(
                './/fb:description/fb:title-info/fb:book-title',
                namespaces=NS,
            )
            or ''
        )

    def _get_chapters(self, root: etree.Element) -> list[Chapter]:
        body = root.find('fb:body', namespaces=NS)
        if body is None:
            return []

        sections = body.findall('fb:section', namespaces=NS)
        if not sections:
            blocks = self._get_blocks(body)
            if not blocks:
                return []
            return [
                Chapter(
                    blocks=blocks,
                    title=self._get_element_text(
                        body.find('fb:title', namespaces=NS),
                    ),
                    level=1,
                ),
            ]

        chapters = []
        for section in sections:
            chapters.extend(self._get_section_chapters(section, level=1))
        return chapters

    def _get_section_chapters(
        self,
        section: etree.Element,
        level: int,
    ) -> list[Chapter]:
        chapters = [
            Chapter(
                blocks=self._get_blocks(section),
                title=self._get_element_text(
                    section.find('fb:title', namespaces=NS),
                ),
                level=level,
            ),
        ]
        for nested_section in section.findall('fb:section', namespaces=NS):
            chapters.extend(
                self._get_section_chapters(
                    nested_section,
                    level=level + 1,
                ),
            )
        return chapters

    def _get_blocks(self, section: etree.Element) -> list[Block]:  # noqa: WPS231
        blocks = []
        for element in section:
            element_type = etree.QName(element).localname
            if element_type in {'title', 'subtitle'}:
                blocks.append(
                    Block(
                        type=BlockTypes.header,
                        content=self._get_element_text(element),
                    ),
                )
            elif element_type == 'p':
                blocks.append(
                    Block(
                        type=BlockTypes.text,
                        content=self._get_element_text(element),
                    ),
                )
            elif element_type == 'image':
                blocks.append(
                    Block(
                        type=BlockTypes.image,
                        content=element.get(
                            f'{{{XLINK_NS}}}href',
                            '',
                        ),
                    ),
                )
            elif element_type != 'section':
                blocks.extend(self._get_blocks(element))
        return blocks

    def _get_author(self, root: etree.Element) -> list[str]:
        authors = []
        for author in root.findall(
            './/fb:description/fb:title-info/fb:author',
            namespaces=NS,
        ):
            parts = [
                author.findtext('fb:first-name', namespaces=NS),
                author.findtext('fb:middle-name', namespaces=NS),
                author.findtext('fb:last-name', namespaces=NS),
                author.findtext('fb:nickname', namespaces=NS),
            ]
            name = ' '.join(
                name_part.strip()
                for name_part in parts
                if name_part and name_part.strip()
            )
            authors.append(name)
        return authors

    def _get_element_text(self, element: etree.Element | None) -> str:
        if element is None:
            return ''
        return ' '.join(''.join(element.itertext()).split())
