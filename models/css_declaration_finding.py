"""
Stores CSS declaration analysis findings.
"""

from dataclasses import dataclass


@dataclass
class CSSDeclarationFinding:
    """Stores one CSS declaration analysis finding."""

    selector: str
    
    property: str
    value: str

    source_line: int = 0
    source_column: int = 0