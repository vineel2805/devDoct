"""
Represents a template/PHP file dependency.
"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class TemplateDependency:
    """Represents a dependency between project files."""

    source_file: Path
    target_file: Path | None

    dependency_type: str

    source_line: int = 0
    source_column: int = 0

    confidence: str = "high"

    resolved: bool = False