"""
Represents a reference to a CSS file.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class CSSReference:
    """Represents evidence that a CSS file is referenced."""

    source_file: Path
    target_file: Path | None

    reference_type: str

    source_line: int = 0
    source_column: int = 0

    confidence: str = "high"

    resolved: bool = False