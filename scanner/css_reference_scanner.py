"""
Scans project files for references to CSS files.
"""

from pathlib import Path
import re
from urllib.parse import urlsplit

from models.css_reference import CSSReference


class CSSReferenceScanner:
    """Finds references to CSS files in HTML/PHP and CSS imports."""

    STYLESHEET_LINK_PATTERN = re.compile(
        r"""<link\b
            (?=[^>]*\brel\s*=\s*["']stylesheet["'])
            (?=[^>]*\bhref\s*=\s*["']([^"']+)["'])
            [^>]*>
        """,
        re.IGNORECASE | re.DOTALL | re.VERBOSE,
    )

    IMPORT_PATTERN = re.compile(
        r"""@import\s+(?:url\(\s*)?["']([^"']+)["']""",
        re.IGNORECASE,
    )

    def scan(
        self,
        source_files: list[Path],
        css_files: list[Path],
        project_root: Path,
    ) -> list[CSSReference]:
        """Find CSS references from source files."""

        references: list[CSSReference] = []

        project_root = project_root.resolve()

        css_lookup = {
            css_file.resolve(): css_file
            for css_file in css_files
        }

        for source_file in source_files:

            if not source_file.exists():
                continue

            try:
                content = source_file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except OSError:
                continue

            source_file = source_file.resolve()

            # CSS files can reference other CSS files through @import.
            if source_file.suffix.lower() == ".css":

                references.extend(
                    self._scan_imports(
                        source_file,
                        content,
                        css_lookup,
                        project_root,
                    )
                )

            # HTML/PHP/template files can reference CSS
            # through <link rel="stylesheet">.
            else:

                references.extend(
                    self._scan_stylesheet_links(
                        source_file,
                        content,
                        css_lookup,
                        project_root,
                    )
                )

        return references

    def _scan_stylesheet_links(
        self,
        source_file: Path,
        content: str,
        css_lookup: dict[Path, Path],
        project_root: Path,
    ) -> list[CSSReference]:
        """Find stylesheet links in HTML/PHP files."""

        references: list[CSSReference] = []

        for match in self.STYLESHEET_LINK_PATTERN.finditer(content):

            target = match.group(1)

            if not target:
                continue

            line = (
                content.count(
                    "\n",
                    0,
                    match.start(),
                )
                + 1
            )

            target_path = self._resolve_target(
                source_file,
                target,
                css_lookup,
                project_root,
            )

            references.append(
                CSSReference(
                    source_file=source_file,
                    target_file=target_path,
                    reference_type="stylesheet",
                    source_line=line,
                    source_column=1,
                    confidence="high",
                    resolved=target_path is not None,
                )
            )

        return references

    def _scan_imports(
        self,
        source_file: Path,
        content: str,
        css_lookup: dict[Path, Path],
        project_root: Path,
    ) -> list[CSSReference]:
        """Find CSS @import references."""

        references: list[CSSReference] = []

        for match in self.IMPORT_PATTERN.finditer(content):

            target = match.group(1)

            if not target:
                continue

            line = (
                content.count(
                    "\n",
                    0,
                    match.start(),
                )
                + 1
            )

            target_path = self._resolve_target(
                source_file,
                target,
                css_lookup,
                project_root,
            )

            references.append(
                CSSReference(
                    source_file=source_file,
                    target_file=target_path,
                    reference_type="import",
                    source_line=line,
                    source_column=1,
                    confidence="high",
                    resolved=target_path is not None,
                )
            )

        return references

    def _resolve_target(
        self,
        source_file: Path,
        target: str,
        css_lookup: dict[Path, Path],
        project_root: Path,
    ) -> Path | None:
        """
        Resolve a CSS reference to a CSS file in the project.

        Supports:

        - relative paths
        - project-root paths
        - query strings
        - URL fragments
        - normalized paths
        """

        target = target.strip()

        if not target:
            return None

        parsed = urlsplit(target)

        # External resources are not project CSS files.
        if parsed.scheme.lower() in {
            "http",
            "https",
            "data",
        }:
            return None

        path_part = parsed.path.strip()

        if not path_part:
            return None

        # --------------------------------------------------
        # Project-root-relative path
        #
        # Example:
        #
        # /css/style.css
        #
        # resolves to:
        #
        # <project_root>/css/style.css
        # --------------------------------------------------

        if path_part.startswith("/"):

            candidate = (
                project_root
                / path_part.lstrip("/")
            )

        # --------------------------------------------------
        # Source-relative path
        #
        # Example:
        #
        # pages/index.php
        # ../css/style.css
        #
        # resolves relative to pages/
        # --------------------------------------------------

        else:

            candidate = (
                source_file.parent
                / path_part
            )

        candidate = candidate.resolve()

        return css_lookup.get(candidate)