"""
Builds the project-wide dependency graph.

Combines:
    PHP/template dependencies
    CSS stylesheet references
    CSS @import references
"""

from pathlib import Path

from models.dependency_graph import DependencyGraph
from models.dependency_edge import DependencyEdge
from scanner.template_dependency_scanner import (
    TemplateDependencyScanner,
)
from scanner.css_reference_scanner import (
    CSSReferenceScanner,
)


class ProjectDependencyScanner:
    """Builds a dependency graph for the entire project."""

    def __init__(self):
        self.template_scanner = TemplateDependencyScanner()
        self.css_reference_scanner = CSSReferenceScanner()

    def scan(
        self,
        files: list[Path],
        project_root: Path,
    ) -> DependencyGraph:
        """
        Scan project files and build a dependency graph.

        The graph contains relationships between:

            PHP → PHP
            PHP → CSS
            CSS → CSS
        """

        project_root = Path(project_root).resolve()

        normalized_files = [
            Path(file).resolve()
            for file in files
        ]

        php_files = [
            file
            for file in normalized_files
            if file.suffix.lower() in {
                ".php",
                ".phtml",
                ".inc",
            }
        ]

        css_files = [
            file
            for file in normalized_files
            if file.suffix.lower() == ".css"
        ]

        graph = DependencyGraph()

        # --------------------------------------------------
        # PHP / template dependencies
        # --------------------------------------------------

        template_dependencies = (
            self.template_scanner.scan(
                php_files,
                project_root,
            )
        )

        for dependency in template_dependencies:

            if dependency.target_file is None:
                continue

            edge = DependencyEdge(
                source_file=dependency.source_file,
                target_file=dependency.target_file,
                dependency_type=dependency.dependency_type,
                source_line=dependency.source_line,
                source_column=dependency.source_column,
                confidence=dependency.confidence,
                resolved=dependency.resolved,
            )

            graph.add_edge(edge)

        # --------------------------------------------------
        # CSS references
        #
        # We scan PHP/template files for:
        #
        # <link rel="stylesheet" ...>
        #
        # and CSS files for:
        #
        # @import
        # --------------------------------------------------

        css_reference_sources = (
            php_files + css_files
        )

        css_references = (
            self.css_reference_scanner.scan(
                css_reference_sources,
                css_files,
                project_root,
            )
        )

        for reference in css_references:

            if reference.target_file is None:
                continue

            edge = DependencyEdge(
                source_file=reference.source_file,
                target_file=reference.target_file,
                dependency_type=reference.reference_type,
                source_line=reference.source_line,
                source_column=reference.source_column,
                confidence=reference.confidence,
                resolved=reference.resolved,
            )

            graph.add_edge(edge)

        return graph