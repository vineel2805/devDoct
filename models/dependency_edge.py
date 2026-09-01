"""
Represents a single dependency relationship between project files.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DependencyEdge:
    """Represents evidence of a dependency between two files."""

    source_file: Path
    target_file: Path | None

    dependency_type: str

    source_line: int = 0
    source_column: int = 0

    confidence: str = "high"

    resolved: bool = True