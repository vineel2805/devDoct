"""
Scans PHP/template files for file dependencies.

Supported PHP dependency statements:

    include
    require
    include_once
    require_once
"""

from pathlib import Path
import re

from models.template_dependency import TemplateDependency


class TemplateDependencyScanner:
    """Finds PHP/template file dependencies."""

    DEPENDENCY_PATTERN = re.compile(
        r"""
        \b(
            include_once
            |require_once
            |include
            |require
        )
        \s*
        (?:\(\s*)?
        ["']([^"']+)["']
        \s*\)?
        """,
        re.IGNORECASE | re.VERBOSE,
    )

    def scan(
        self,
        source_files: list[Path],
        project_root: Path,
    ) -> list[TemplateDependency]:
        """
        Scan PHP/template files for include and require dependencies.
        """

        dependencies: list[TemplateDependency] = []

        project_root = project_root.resolve()

        for source_file in source_files:

            source_file = Path(source_file)

            if not source_file.exists():
                continue

            if source_file.suffix.lower() not in {
                ".php",
                ".phtml",
                ".inc",
            }:
                continue

            try:
                content = source_file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                )
            except OSError:
                continue

            dependencies.extend(
                self._scan_file(
                    source_file.resolve(),
                    content,
                    project_root,
                )
            )

        return dependencies

    def _scan_file(
        self,
        source_file: Path,
        content: str,
        project_root: Path,
    ) -> list[TemplateDependency]:
        """Extract dependencies from one PHP/template file."""

        dependencies: list[TemplateDependency] = []

        for match in self.DEPENDENCY_PATTERN.finditer(content):

            dependency_type = match.group(1).lower()
            target = match.group(2).strip()

            if not target:
                continue

            source_line = (
                content.count(
                    "\n",
                    0,
                    match.start(),
                )
                + 1
            )

            target_file = self._resolve_target(
                source_file=source_file,
                target=target,
                project_root=project_root,
            )

            dependencies.append(
                TemplateDependency(
                    source_file=source_file,
                    target_file=target_file,
                    dependency_type=dependency_type,
                    source_line=source_line,
                    source_column=match.start()
                    - content.rfind(
                        "\n",
                        0,
                        match.start(),
                    ),
                    confidence=(
                        "high"
                        if target_file is not None
                        else "low"
                    ),
                    resolved=target_file is not None,
                )
            )

        return dependencies

    def _resolve_target(
        self,
        source_file: Path,
        target: str,
        project_root: Path,
    ) -> Path | None:
        """
        Resolve a template dependency.

        Supports:

        - relative paths
        - project-root paths
        - normalized paths
        """

        target = target.strip()

        if not target:
            return None

        # Ignore PHP expressions for now.
        #
        # Example:
        # include $header;
        # include $base . "/header.php";
        #
        # These require runtime-aware analysis and cannot
        # be safely resolved statically.
        if any(
            character in target
            for character in (
                "$",
                "{",
                "}",
            )
        ):
            return None

        # Remove query strings/fragments if present.
        target = target.split("?", 1)[0]
        target = target.split("#", 1)[0]

        if not target:
            return None

        # Project-root-relative dependency.
        if target.startswith("/"):

            candidate = (
                project_root
                / target.lstrip("/")
            )

        else:

            # Normal relative dependency.
            candidate = (
                source_file.parent
                / target
            )

        candidate = candidate.resolve()

        # Make sure the resolved file remains inside
        # the scanned project.
        try:
            candidate.relative_to(project_root)
        except ValueError:
            return None

        if candidate.is_file():
            return candidate

        return None