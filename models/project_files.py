"""
Data models used throughout DevDoctor.
"""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ProjectFiles:
    """Stores all discovered project files."""

    php: list[Path] = field(default_factory=list)
    html: list[Path] = field(default_factory=list)
    css: list[Path] = field(default_factory=list)
    js: list[Path] = field(default_factory=list)

    @property
    def total(self) -> int:
        return (
            len(self.php)
            + len(self.html)
            + len(self.css)
            + len(self.js)
        )