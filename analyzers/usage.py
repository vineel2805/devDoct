"""
Analyzes CSS selector usage against HTML documents.
"""

from pathlib import Path

from models.html_result import HTMLScanResult
from models.css_result import CSSScanResult
from models.usage_result import UsageResult, SelectorUsage

from analyzers.css_matcher import CSSMatcher


class UsageAnalyzer:
    """Analyzes whether CSS selectors are actually used by HTML."""

    def __init__(self):
        self.matcher = CSSMatcher()

    def analyze(
        self,
        html: HTMLScanResult,
        css: CSSScanResult,
    ) -> UsageResult:

        result = UsageResult()

        # ---------------------------------
        # Selector-level analysis
        # ---------------------------------

        for css_path, css_file in css.files.items():

            for selector in css_file.selectors:

                matched_files = []

                for html_path, html_file in html.files.items():

                    if self.matcher.matches(
                        selector,
                        html_file.document,
                    ):
                        matched_files.append(
                            self._display_path(
                                html_path,
                                html.root,
                            )
                        )

                result.selectors.append(
                    SelectorUsage(
                        selector=selector.selector,
                        used=bool(matched_files),
                        matched_files=matched_files,
                        source_file=str(css_path),
                        source_line=selector.source_line,
                        source_column=selector.source_column,
                        error=selector.error,
                    )
                )

        # ---------------------------------
        # Class summary
        # ---------------------------------

        result.used_classes = (
            html.classes & css.classes
        )

        result.unused_classes = (
            css.classes - html.classes
        )

        result.missing_classes = (
            html.classes - css.classes
        )

        # ---------------------------------
        # ID summary
        # ---------------------------------

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

    @staticmethod
    def _display_path(
        file: Path,
        root: Path,
    ) -> str:
        """
        Convert an internal project path into a
        project-relative path suitable for reports.

        Example:

            C:/project/pages/index.html
                ↓
            pages/index.html
        """

        file = Path(file)
        root = Path(root)

        try:
            return file.resolve().relative_to(
                root.resolve()
            ).as_posix()

        except ValueError:
            # Fallback for files outside the project root.
            return file.as_posix()