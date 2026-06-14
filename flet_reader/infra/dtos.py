from typing import final

from msgspec import Struct

from flet_reader.common.enums import BlockTypes


@final
class Block(Struct):
    """Represents block of chapter."""

    type: BlockTypes
    content: str | bytes  # noqa: WPS110


@final
class Chapter(Struct):
    """Represents book chapter."""

    blocks: list[Block]
    title: str
    level: int


@final
class Book(Struct):
    """Represents full book."""

    chapters: list[Chapter]
    title: str
    authors: list[str]  # TODO: Convert to Struct


@final
class ShortBookInfo(Struct):
    """Represent title and book name."""

    title: str
    author: str  # TODO: All authors joined in one str. Remove it
