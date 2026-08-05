"""
Scans HTML/PHP files for class and id attributes.
"""

from pathlib import Path

from bs4 import BeautifulSoup

from models.html_result import HTMLScanResult, FileHTMLResult
from parsers.php_cleaner import PHPCleaner


class HTMLScanner:
    """Extracts HTML classes and IDs."""

    def scan(self, files: list[Path]) -> HTMLScanResult:

        result = HTMLScanResult()

        for file in files:

            try:

                html = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                html = PHPCleaner.clean(html)

                soup = BeautifulSoup(html, "lxml")

                file_result = FileHTMLResult()

                #
                # Scan HTML elements
                #
                for tag in soup.find_all(True):

                    file_result.total_elements += 1

                    #
                    # Extract classes
                    #
                    classes = tag.get("class")

                    if classes:
                        for cls in classes:

                            cls = cls.strip()

                            if cls:

                                file_result.classes.add(cls)
                                result.classes.add(cls)

                    #
                    # Extract IDs
                    #
                    tag_id = tag.get("id")

                    if tag_id:

                        tag_id = tag_id.strip()

                        if tag_id:

                            file_result.ids.add(tag_id)
                            result.ids.add(tag_id)

                #
                # Store per-file result
                #
                result.files[file] = file_result

            except Exception as e:

                print(f"Failed to scan {file}: {e}")

        return result