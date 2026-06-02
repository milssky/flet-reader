import enum
from typing import final


@final
@enum.verify(enum.UNIQUE)
class BlockTypes(enum.StrEnum):
    """Represent available types of book block."""

    text = 'text'
    header = 'header'
    image = 'image'
