"""
Scans CSS files and extracts selectors.
"""

from pathlib import Path

from models.css_result import CSSScanResult, FileCSSResult
from parsers.css_parser import CSSParser


class CSSScanner:
    """Extracts CSS selectors."""

    def __init__(self):
        self.parser = CSSParser()

    def scan(
        self,
        files: list[Path]
    ) -> CSSScanResult:

        result = CSSScanResult()

        for file in files:

            try:

                css = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                parsed = self.parser.parse(css)

                file_result = FileCSSResult()

                # -----------------------------
                # Store file data
                # -----------------------------

                file_result.classes = parsed.classes
                file_result.ids = parsed.ids
                file_result.elements = parsed.elements

                file_result.selectors = parsed.selectors
                file_result.declarations = parsed.declarations
                file_result.total_rules = parsed.total_rules

                # -----------------------------
                # Store project-wide data
                # -----------------------------

                result.classes.update(
                    parsed.classes
                )

                result.ids.update(
                    parsed.ids
                )

                result.elements.update(
                    parsed.elements
                )

                # -----------------------------
                # Store file result
                # -----------------------------

                result.files[file] = file_result

            except Exception as e:

                print(
                    f"Failed to scan {file}: {e}"
                )

        return result