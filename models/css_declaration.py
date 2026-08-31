"""
Stores CSS declaration information.
"""

from dataclasses import dataclass


@dataclass
class CSSDeclaration:
    """Stores one CSS property declaration."""

    property: str
    value: str
    important: bool = False

    source_line: int = 0
    source_column: int = 0