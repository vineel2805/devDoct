"""
Scans JavaScript files for references to CSS classes and IDs.
"""

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class JSReference:
    """A CSS-related reference discovered in JavaScript."""

    value: str
    reference_type: str
    source_file: Path
    source_line: int
    source_column: int
    confidence: str = "high"


class JSScanner:
    """Extracts CSS class and ID references from JavaScript."""

    # Examples:
    #
    # document.querySelector(".card")
    # document.querySelector("#modal")
    # document.querySelectorAll(".product")
    QUERY_SELECTOR_PATTERN = re.compile(
        r"""
        \b
        (?:document|window|element|this)
        \s*
        \.
        querySelector(?:All)?
        \s*
        \(
        \s*
        ["']
        ([.#])
        ([A-Za-z_][A-Za-z0-9_-]*)
        ["']
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    # Examples:
    #
    # classList.add("active")
    # classList.remove("hidden")
    # classList.toggle("open")
    CLASS_LIST_PATTERN = re.compile(
        r"""
        \b
        classList
        \s*
        \.
        (?:add|remove|toggle|contains|replace)
        \s*
        \(
        \s*
        ["']
        ([A-Za-z_][A-Za-z0-9_-]*)
        ["']
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    def scan(
        self,
        files: list[Path],
    ) -> list[JSReference]:
        """
        Scan JavaScript files for CSS class and ID references.
        """

        references: list[JSReference] = []

        for file in files:

            file = Path(file)

            # Only scan JavaScript files.
            if file.suffix.lower() != ".js":
                continue

            if not file.exists():
                continue

            try:
                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except OSError:
                continue

            references.extend(
                self._scan_query_selectors(
                    file,
                    content,
                )
            )

            references.extend(
                self._scan_class_list(
                    file,
                    content,
                )
            )

        return references

    def _scan_query_selectors(
        self,
        file: Path,
        content: str,
    ) -> list[JSReference]:

        references: list[JSReference] = []

        for match in self.QUERY_SELECTOR_PATTERN.finditer(
            content
        ):

            prefix = match.group(1)
            value = match.group(2)

            line = (
                content.count(
                    "\n",
                    0,
                    match.start(),
                )
                + 1
            )

            column = (
                match.start()
                - content.rfind(
                    "\n",
                    0,
                    match.start(),
                )
            )

            reference_type = (
                "class"
                if prefix == "."
                else "id"
            )

            references.append(
                JSReference(
                    value=value,
                    reference_type=reference_type,
                    source_file=file,
                    source_line=line,
                    source_column=column,
                    confidence="high",
                )
            )

        return references

    def _scan_class_list(
        self,
        file: Path,
        content: str,
    ) -> list[JSReference]:

        references: list[JSReference] = []

        for match in self.CLASS_LIST_PATTERN.finditer(
            content
        ):

            value = match.group(1)

            line = (
                content.count(
                    "\n",
                    0,
                    match.start(),
                )
                + 1
            )

            column = (
                match.start()
                - content.rfind(
                    "\n",
                    0,
                    match.start(),
                )
            )

            references.append(
                JSReference(
                    value=value,
                    reference_type="class",
                    source_file=file,
                    source_line=line,
                    source_column=column,
                    confidence="high",
                )
            )

        return references