"""
Stores CSS rule information.
"""

from dataclasses import dataclass, field

from models.css_declaration import CSSDeclaration


@dataclass
class CSSRule:
    """Stores one CSS rule and its declarations."""

    selectors: list[str] = field(
        default_factory=list
    )

    declarations: list[CSSDeclaration] = field(
        default_factory=list
    )

    source_line: int = 0
    source_column: int = 0