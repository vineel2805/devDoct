"""
Stores CSS usage analysis results.
"""

from dataclasses import dataclass, field


@dataclass
class UsageResult:
    """Stores CSS usage analysis results."""

    # CSS classes
    used_classes: set[str] = field(default_factory=set)
    unused_classes: set[str] = field(default_factory=set)
    missing_classes: set[str] = field(default_factory=set)

    # CSS IDs
    used_ids: set[str] = field(default_factory=set)
    unused_ids: set[str] = field(default_factory=set)
    missing_ids: set[str] = field(default_factory=set)