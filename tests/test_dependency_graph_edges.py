from pathlib import Path

from models.dependency_edge import DependencyEdge
from models.dependency_graph import DependencyGraph


def make_edge(
    source: Path,
    target: Path,
    dependency_type: str = "include",
    line: int = 10,
    confidence: str = "high",
):
    return DependencyEdge(
        source_file=source,
        target_file=target,
        dependency_type=dependency_type,
        source_line=line,
        source_column=1,
        confidence=confidence,
        resolved=True,
    )


def test_add_edge_creates_dependency():

    graph = DependencyGraph()

    source = Path("index.php")
    target = Path("header.php")

    edge = make_edge(source, target)

    graph.add_edge(edge)

    assert graph.children(source) == {
        target.resolve()
    }


def test_add_edge_preserves_evidence():

    graph = DependencyGraph()

    source = Path("index.php")
    target = Path("header.php")

    edge = make_edge(
        source,
        target,
        dependency_type="include",
        line=15,
    )

    graph.add_edge(edge)

    edges = graph.edges(source, target)

    assert len(edges) == 1

    stored = next(iter(edges))

    assert stored.dependency_type == "include"
    assert stored.source_line == 15
    assert stored.confidence == "high"


def test_outgoing_edges():

    graph = DependencyGraph()

    source = Path("index.php")
    header = Path("header.php")
    footer = Path("footer.php")

    header_edge = make_edge(source, header)
    footer_edge = make_edge(
        source,
        footer,
        dependency_type="require",
    )

    graph.add_edge(header_edge)
    graph.add_edge(footer_edge)

    edges = graph.outgoing_edges(source)

    assert len(edges) == 2
    assert header_edge in edges
    assert footer_edge in edges


def test_incoming_edges():

    graph = DependencyGraph()

    index = Path("index.php")
    layout = Path("layout.php")
    header = Path("header.php")

    edge_one = make_edge(index, header)
    edge_two = make_edge(layout, header)

    graph.add_edge(edge_one)
    graph.add_edge(edge_two)

    edges = graph.incoming_edges(header)

    assert len(edges) == 2
    assert edge_one in edges
    assert edge_two in edges


def test_multiple_evidence_edges_between_same_files():

    graph = DependencyGraph()

    source = Path("index.php")
    target = Path("header.php")

    include_edge = make_edge(
        source,
        target,
        dependency_type="include",
        line=10,
    )

    require_edge = make_edge(
        source,
        target,
        dependency_type="require",
        line=20,
    )

    graph.add_edge(include_edge)
    graph.add_edge(require_edge)

    edges = graph.edges(source, target)

    assert len(edges) == 2


def test_duplicate_edge_is_not_stored_twice():

    graph = DependencyGraph()

    source = Path("index.php")
    target = Path("header.php")

    edge = make_edge(source, target)

    graph.add_edge(edge)
    graph.add_edge(edge)

    edges = graph.edges(source, target)

    assert len(edges) == 1


def test_unresolved_edge_is_ignored():

    graph = DependencyGraph()

    edge = DependencyEdge(
        source_file=Path("index.php"),
        target_file=None,
        dependency_type="include",
        confidence="low",
        resolved=False,
    )

    graph.add_edge(edge)

    assert graph.outgoing_edges(
        Path("index.php")
    ) == set()


def test_edge_evidence_does_not_break_transitive_dependencies():

    graph = DependencyGraph()

    index = Path("index.php")
    header = Path("header.php")
    css = Path("header.css")

    graph.add_edge(
        make_edge(
            index,
            header,
            dependency_type="include",
        )
    )

    graph.add_edge(
        make_edge(
            header,
            css,
            dependency_type="stylesheet",
        )
    )

    assert graph.dependencies(index) == {
        header.resolve(),
        css.resolve(),
    }