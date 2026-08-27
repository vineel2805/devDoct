"""
Stores CSS usage analysis results.
"""

from dataclasses import dataclass, field


@dataclass
class SelectorUsage:
    """Stores usage information for a single CSS selector."""

    selector: str

    used: bool = False

    matched_files: list[str] = field(
        default_factory=list
    )
    source_file: str = ""

    source_line: int = 0
    source_column: int = 0

    error: str | None = None


@dataclass
class UsageResult:
    """Stores CSS usage analysis results."""

    # ---------------------------------
    # CSS classes
    # ---------------------------------

    used_classes: set[str] = field(
        default_factory=set
    )

    unused_classes: set[str] = field(
        default_factory=set
    )

    missing_classes: set[str] = field(
        default_factory=set
    )

    # ---------------------------------
    # CSS IDs
    # ---------------------------------

    used_ids: set[str] = field(
        default_factory=set
    )

    unused_ids: set[str] = field(
        default_factory=set
    )

    missing_ids: set[str] = field(
        default_factory=set
    )

    # ---------------------------------
    # CSS selectors
    # ---------------------------------

    selectors: list[SelectorUsage] = field(
        default_factory=list
    )

    @property
    def total_selectors(self) -> int:
        """Return total CSS selectors analyzed."""

        return len(self.selectors)

    @property
    def used_selectors(self) -> int:
        """Return number of selectors matching HTML."""

        return sum(
            selector.used
            for selector in self.selectors
        )

    @property
    def unused_selectors(self) -> int:
        """Return number of selectors not matching HTML."""

        return sum(
            not selector.used
            for selector in self.selectors
        )