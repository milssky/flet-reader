from __future__ import annotations

from pathlib import Path
from types import MappingProxyType
from typing import Final, final

import attrs
from lxml import etree

from flet_reader.infra.dtos import Book, Chapter

FB2_NS: Final = 'http://www.gribuser.ru/xml/fictionbook/2.0'
XLINK_NS: Final = 'http://www.w3.org/1999/xlink'

NS = MappingProxyType({
    'fb': FB2_NS,
    'xlink': XLINK_NS,
})


@final
@attrs.define(frozen=True)
class FBFileReader:
    """FB2 book file reader."""

    _parser: etree.XMLParser

    def __call__(self, file_path: Path) -> Book:
        """Conver file to DTO."""
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
        chapters = []
        if body is None:
            return []
        for section in body.iter():
            chapters.append(section)  # noqa: PERF402
            # TODO: extract blocks from sections
        return chapters

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
