"""
Analyzes CSS selector usage against HTML selectors.
"""

from models.html_result import HTMLScanResult
from models.css_result import CSSScanResult
from models.usage_result import UsageResult


class UsageAnalyzer:
    """Compares HTML classes and IDs with CSS selectors."""

    def analyze(
        self,
        html: HTMLScanResult,
        css: CSSScanResult
    ) -> UsageResult:

        result = UsageResult()

        # -----------------------------
        # Classes
        # -----------------------------

        result.used_classes = (
            html.classes & css.classes
        )

        result.unused_classes = (
            css.classes - html.classes
        )

        result.missing_classes = (
            html.classes - css.classes
        )

        # -----------------------------
        # IDs
        # -----------------------------

        result.used_ids = (
            html.ids & css.ids
        )

        result.unused_ids = (
            css.ids - html.ids
        )

        result.missing_ids = (
            html.ids - css.ids
        )

        return result