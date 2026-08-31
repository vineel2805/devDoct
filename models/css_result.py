"""
Stores CSS scanning results.
"""

from pathlib import Path
from dataclasses import dataclass, field

from parsers.css_parser import ParsedSelector
from models.css_declaration import CSSDeclaration

from models.css_declaration_finding import CSSDeclarationFinding

@dataclass
class FileCSSResult:
    """Stores CSS information for a single file."""

    classes: set[str] = field(default_factory=set)
    ids: set[str] = field(default_factory=set)
    elements: set[str] = field(default_factory=set)

    # Parsed CSS selectors from this file.
    selectors: list[ParsedSelector] = field(
        default_factory=list
    )

    declarations: list[CSSDeclaration] = field(
        default_factory=list
    )
    
    declaration_findings: list[CSSDeclarationFinding] = field(
        default_factory=list
    )

    rule_findings: list[CSSDeclarationFinding] = field(
        default_factory=list
    )

    total_rules: int = 0



@dataclass
class CSSScanResult:
    """Stores project-wide CSS scan results."""

    # Project-wide unique selectors.
    classes: set[str] = field(default_factory=set)
    ids: set[str] = field(default_factory=set)
    elements: set[str] = field(default_factory=set)

    # Per-file scan results.
    files: dict[Path, FileCSSResult] = field(
        default_factory=dict
    )

    declaration_findings: list[CSSDeclarationFinding] = field(
        default_factory=list
    )

    rule_findings: list[CSSDeclarationFinding] = field(
        default_factory=list
    )

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

    @property
    def total_selectors(self) -> int:
        """Return total parsed CSS selectors."""

        return sum(
            len(file_result.selectors)
            for file_result in self.files.values()
        )