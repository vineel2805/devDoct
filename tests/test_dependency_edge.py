from pathlib import Path

from models.dependency_edge import DependencyEdge


def test_dependency_edge_stores_basic_information():

    source = Path("index.php")
    target = Path("header.php")

    edge = DependencyEdge(
        source_file=source,
        target_file=target,
        dependency_type="include",
    )

    assert edge.source_file == source
    assert edge.target_file == target
    assert edge.dependency_type == "include"


def test_dependency_edge_stores_source_location():

    edge = DependencyEdge(
        source_file=Path("index.php"),
        target_file=Path("header.php"),
        dependency_type="include",
        source_line=15,
        source_column=9,
    )

    assert edge.source_line == 15
    assert edge.source_column == 9


def test_dependency_edge_stores_confidence():

    edge = DependencyEdge(
        source_file=Path("index.php"),
        target_file=Path("header.php"),
        dependency_type="include",
        confidence="high",
    )

    assert edge.confidence == "high"


def test_dependency_edge_can_be_unresolved():

    edge = DependencyEdge(
        source_file=Path("index.php"),
        target_file=None,
        dependency_type="include",
        confidence="low",
        resolved=False,
    )

    assert edge.target_file is None
    assert edge.resolved is False
    assert edge.confidence == "low"


def test_dependency_edge_is_hashable():

    edge = DependencyEdge(
        source_file=Path("index.php"),
        target_file=Path("header.php"),
        dependency_type="include",
    )

    edges = {edge}

    assert edge in edges


def test_different_reference_types_are_distinct():

    source = Path("main.css")
    target = Path("theme.css")

    import_edge = DependencyEdge(
        source_file=source,
        target_file=target,
        dependency_type="import",
    )

    stylesheet_edge = DependencyEdge(
        source_file=source,
        target_file=target,
        dependency_type="stylesheet",
    )

    assert import_edge != stylesheet_edge