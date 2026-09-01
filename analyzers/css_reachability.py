"""
Analyzes CSS file reachability using the project dependency graph.
"""

from dataclasses import dataclass
from pathlib import Path

from models.dependency_graph import DependencyGraph


@dataclass(frozen=True)
class CSSReachability:
    """Reachability result for a CSS file."""

    file: Path
    status: str
    confidence: int


class CSSReachabilityAnalyzer:
    """Classifies CSS files using dependency evidence."""

    def analyze(
        self,
        css_files: list[Path],
        graph: DependencyGraph,
    ) -> dict[Path, CSSReachability]:
        """
        Analyze CSS reachability.

        The returned dictionary preserves the exact Path objects supplied
        by the caller while dependency lookups use normalized paths.
        """

        results: dict[Path, CSSReachability] = {}

        for css_file in css_files:

            original_file = Path(css_file)
            resolved_file = original_file.resolve()

            incoming_edges = graph.incoming_edges(
                resolved_file
            )

            if not incoming_edges:

                results[original_file] = CSSReachability(
                    file=original_file,
                    status="low",
                    confidence=20,
                )

                continue

            resolved_edges = [
                edge
                for edge in incoming_edges
                if edge.resolved
            ]

            unresolved_edges = [
                edge
                for edge in incoming_edges
                if not edge.resolved
            ]

            # A direct stylesheet reference from PHP/HTML/template
            # is strong static evidence.
            direct_stylesheet_edges = [
                edge
                for edge in resolved_edges
                if edge.dependency_type == "stylesheet"
            ]

            if direct_stylesheet_edges:

                confidence = self._calculate_confidence(
                    direct_stylesheet_edges,
                    base=90,
                )

                results[original_file] = CSSReachability(
                    file=original_file,
                    status="high",
                    confidence=confidence,
                )

                continue

            # A CSS @import is an indirect dependency.
            import_edges = [
                edge
                for edge in resolved_edges
                if edge.dependency_type == "import"
            ]

            if import_edges:

                confidence = self._calculate_confidence(
                    import_edges,
                    base=70,
                )

                results[original_file] = CSSReachability(
                    file=original_file,
                    status="medium",
                    confidence=confidence,
                )

                continue

            # We found an unresolved reference. Do not call the
            # stylesheet dead because static analysis could not
            # resolve the reference.
            if unresolved_edges:

                results[original_file] = CSSReachability(
                    file=original_file,
                    status="unknown",
                    confidence=30,
                )

                continue

            # Other resolved dependency types still provide
            # evidence that the file participates in the graph.
            if resolved_edges:

                confidence = self._calculate_confidence(
                    resolved_edges,
                    base=60,
                )

                results[original_file] = CSSReachability(
                    file=original_file,
                    status="medium",
                    confidence=confidence,
                )

                continue

            results[original_file] = CSSReachability(
                file=original_file,
                status="low",
                confidence=20,
            )

        return results

    @staticmethod
    def _calculate_confidence(
        edges,
        base: int,
    ) -> int:
        """
        Calculate confidence from dependency evidence.

        Independent source files strengthen the evidence slightly.
        The result is always bounded between 0 and 100.
        """

        unique_sources = {
            edge.source_file.resolve()
            for edge in edges
        }

        confidence = base + min(
            max(len(unique_sources) - 1, 0),
            5,
        )

        return max(
            0,
            min(confidence, 100),
        )