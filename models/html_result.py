"""
Stores HTML scanning results.
"""

from pathlib import Path
from dataclasses import dataclass, field


@dataclass
class FileHTMLResult:
    """Stores HTML information for a single file."""

    classes: set[str] = field(default_factory=set)
    ids: set[str] = field(default_factory=set)
    elements: set[str] = field(default_factory=set)

    total_elements: int = 0


@dataclass
class HTMLScanResult:
    """Stores project-wide HTML scan results."""

    # Project-wide unique selectors
    classes: set[str] = field(default_factory=set)
    ids: set[str] = field(default_factory=set)
    elements: set[str] = field(default_factory=set)

    # Per-file scan results
    files: dict[Path, FileHTMLResult] = field(default_factory=dict)

    @property
    def total_classes(self) -> int:
        return len(self.classes)

    @property
    def total_ids(self) -> int:
        return len(self.ids)

    @property
    def total_elements(self) -> int:
        return len(self.elements)

    @property
    def total_files(self) -> int:
        return len(self.files)