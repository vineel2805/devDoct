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

    # Cleaned HTML source used by CSSMatcher.
    document: str = ""


@dataclass
class HTMLScanResult:
    """Project-wide HTML scan results."""

    root: Path

    classes: set[str] = field(default_factory=set)
    ids: set[str] = field(default_factory=set)
    elements: set[str] = field(default_factory=set)

    files: dict[Path, FileHTMLResult] = field(
        default_factory=dict
    )

    @property
    def total_classes(self) -> int:
        return len(self.classes)

    @property
    def total_ids(self) -> int:
        return len(self.ids)

    @property
    def total_elements(self) -> int:
        return sum(
            file_result.total_elements
            for file_result in self.files.values()
        )

    @property
    def total_files(self) -> int:
        return len(self.files)