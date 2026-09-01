"""
Project dependency graph.

Stores relationships between project files together with
the evidence that established each relationship.
"""

from collections import defaultdict
from pathlib import Path

from models.dependency_edge import DependencyEdge


class DependencyGraph:
    """Represents project file dependencies and their evidence."""

    def __init__(self):
        self._children: dict[Path, set[Path]] = defaultdict(set)
        self._parents: dict[Path, set[Path]] = defaultdict(set)

        self._edges: dict[tuple[Path, Path], set[DependencyEdge]] = (
            defaultdict(set)
        )

    def add_dependency(
        self,
        source: Path,
        target: Path,
    ) -> None:
        """Add a basic dependency without additional evidence."""

        source = Path(source).resolve()
        target = Path(target).resolve()

        self._children[source].add(target)
        self._parents[target].add(source)

    def add_edge(
        self,
        edge: DependencyEdge,
    ) -> None:
        """Add a dependency edge and preserve its evidence."""

        source = edge.source_file.resolve()

        if edge.target_file is None:
            return

        target = edge.target_file.resolve()

        self._children[source].add(target)
        self._parents[target].add(source)

        self._edges[(source, target)].add(edge)

    def children(
        self,
        source: Path,
    ) -> set[Path]:
        """Return files directly depended on by source."""

        return set(
            self._children.get(
                Path(source).resolve(),
                set(),
            )
        )

    def parents(
        self,
        target: Path,
    ) -> set[Path]:
        """Return files that directly depend on target."""

        return set(
            self._parents.get(
                Path(target).resolve(),
                set(),
            )
        )

    def edges(
        self,
        source: Path,
        target: Path,
    ) -> set[DependencyEdge]:
        """Return evidence connecting source to target."""

        key = (
            Path(source).resolve(),
            Path(target).resolve(),
        )

        return set(
            self._edges.get(
                key,
                set(),
            )
        )

    def outgoing_edges(
        self,
        source: Path,
    ) -> set[DependencyEdge]:
        """Return all dependency evidence originating from source."""

        source = Path(source).resolve()

        result: set[DependencyEdge] = set()

        for (
            edge_source,
            _,
        ), edges in self._edges.items():

            if edge_source == source:
                result.update(edges)

        return result

    def incoming_edges(
        self,
        target: Path,
    ) -> set[DependencyEdge]:
        """Return all dependency evidence pointing to target."""

        target = Path(target).resolve()

        result: set[DependencyEdge] = set()

        for (
            _,
            edge_target,
        ), edges in self._edges.items():

            if edge_target == target:
                result.update(edges)

        return result

    def dependencies(
        self,
        source: Path,
    ) -> set[Path]:
        """Return all files reachable from source."""

        source = Path(source).resolve()

        visited: set[Path] = set()
        stack = list(
            self.children(source)
        )

        while stack:

            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            stack.extend(
                self.children(current)
            )

        return visited

    def dependents(
        self,
        target: Path,
    ) -> set[Path]:
        """Return all files that can reach target."""

        target = Path(target).resolve()

        visited: set[Path] = set()
        stack = list(
            self.parents(target)
        )

        while stack:

            current = stack.pop()

            if current in visited:
                continue

            visited.add(current)

            stack.extend(
                self.parents(current)
            )

        return visited

    def has_cycle(self) -> bool:
        """Return True if the graph contains a cycle."""

        visiting: set[Path] = set()
        visited: set[Path] = set()

        def visit(node: Path) -> bool:

            if node in visiting:
                return True

            if node in visited:
                return False

            visiting.add(node)

            for child in self.children(node):

                if visit(child):
                    return True

            visiting.remove(node)
            visited.add(node)

            return False

        nodes = (
            set(self._children)
            | set(self._parents)
        )

        return any(
            visit(node)
            for node in nodes
        )