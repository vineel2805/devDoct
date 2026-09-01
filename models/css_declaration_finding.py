"""
Stores CSS declaration analysis findings.
"""

from dataclasses import dataclass, field
from pathlib import Path

@dataclass
class CSSDeclarationFinding:
    """Stores one CSS declaration analysis finding."""
    file: Path | None =None
    selectors: list[str] = field(default_factory=list)

    property: str = ""
    value: str = ""
    issue: str = ""

    source_line: int = 0
    source_column: int = 0