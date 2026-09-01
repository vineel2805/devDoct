from pathlib import Path

from models.dependency_graph import DependencyGraph
from models.dependency_edge import DependencyEdge
from analyzers.css_reachability import CSSReachabilityAnalyzer


def make_edge(
    source: Path,
    target: Path,
    dependency_type: str = "stylesheet",
    confidence: str = "high",
    resolved: bool = True,
):
    return DependencyEdge(
        source_file=source,
        target_file=target,
        dependency_type=dependency_type,
        source_line=10,
        source_column=1,
        confidence=confidence,
        resolved=resolved,
    )


def test_direct_css_reference_is_high_confidence():

    graph = DependencyGraph()

    page = Path("index.php")
    css = Path("style.css")

    graph.add_edge(
        make_edge(
            page,
            css,
            dependency_type="stylesheet",
        )
    )

    analyzer = CSSReachabilityAnalyzer()

    result = analyzer.analyze(
        [css],
        graph,
    )

    assert result[css].status == "high"
    assert result[css].confidence >= 90


def test_css_import_is_medium_confidence():

    graph = DependencyGraph()

    main_css = Path("main.css")
    component_css = Path("component.css")

    graph.add_edge(
        make_edge(
            main_css,
            component_css,
            dependency_type="import",
        )
    )

    analyzer = CSSReachabilityAnalyzer()

    result = analyzer.analyze(
        [main_css, component_css],
        graph,
    )

    assert result[component_css].status == "medium"
    assert result[component_css].confidence >= 70


def test_php_to_css_is_high_confidence():

    graph = DependencyGraph()

    php = Path("header.php")
    css = Path("header.css")

    graph.add_edge(
        make_edge(
            php,
            css,
            dependency_type="stylesheet",
        )
    )

    analyzer = CSSReachabilityAnalyzer()

    result = analyzer.analyze(
        [css],
        graph,
    )

    assert result[css].status == "high"


def test_unreferenced_css_is_low_confidence():

    graph = DependencyGraph()

    css = Path("legacy.css")

    analyzer = CSSReachabilityAnalyzer()

    result = analyzer.analyze(
        [css],
        graph,
    )

    assert result[css].status == "low"
    assert result[css].confidence < 70


def test_transitive_css_dependency_is_reachable():

    graph = DependencyGraph()

    page = Path("index.php")
    main_css = Path("main.css")
    component_css = Path("component.css")

    graph.add_edge(
        make_edge(
            page,
            main_css,
            dependency_type="stylesheet",
        )
    )

    graph.add_edge(
        make_edge(
            main_css,
            component_css,
            dependency_type="import",
        )
    )

    analyzer = CSSReachabilityAnalyzer()

    result = analyzer.analyze(
        [main_css, component_css],
        graph,
    )

    assert result[main_css].status == "high"
    assert result[component_css].status == "medium"


def test_multiple_parents_are_supported():

    graph = DependencyGraph()

    page_one = Path("index.php")
    page_two = Path("admin.php")
    css = Path("shared.css")

    graph.add_edge(
        make_edge(
            page_one,
            css,
            dependency_type="stylesheet",
        )
    )

    graph.add_edge(
        make_edge(
            page_two,
            css,
            dependency_type="stylesheet",
        )
    )

    analyzer = CSSReachabilityAnalyzer()

    result = analyzer.analyze(
        [css],
        graph,
    )

    assert result[css].status == "high"
    assert result[css].confidence >= 90


def test_unresolved_reference_produces_unknown():

    graph = DependencyGraph()

    page = Path("index.php")
    css = Path("dynamic.css")

    # An unresolved edge should not be treated as
    # proof that the CSS file is reachable.
    unresolved_edge = DependencyEdge(
        source_file=page,
        target_file=css,
        dependency_type="dynamic_stylesheet",
        source_line=20,
        source_column=1,
        confidence="low",
        resolved=False,
    )

    graph.add_edge(unresolved_edge)

    analyzer = CSSReachabilityAnalyzer()

    result = analyzer.analyze(
        [css],
        graph,
    )

    assert result[css].status == "unknown"


def test_confidence_is_bounded():

    graph = DependencyGraph()

    page = Path("index.php")
    css = Path("style.css")

    graph.add_edge(
        make_edge(
            page,
            css,
        )
    )

    analyzer = CSSReachabilityAnalyzer()

    result = analyzer.analyze(
        [css],
        graph,
    )

    assert 0 <= result[css].confidence <= 100


def test_circular_dependencies_do_not_crash():

    graph = DependencyGraph()

    first = Path("first.css")
    second = Path("second.css")

    graph.add_edge(
        make_edge(
            first,
            second,
            dependency_type="import",
        )
    )

    graph.add_edge(
        make_edge(
            second,
            first,
            dependency_type="import",
        )
    )

    analyzer = CSSReachabilityAnalyzer()

    result = analyzer.analyze(
        [first, second],
        graph,
    )

    assert first in result
    assert second in result


def test_all_css_files_receive_a_result():

    graph = DependencyGraph()

    used = Path("used.css")
    unused = Path("unused.css")

    page = Path("index.php")

    graph.add_edge(
        make_edge(
            page,
            used,
        )
    )

    analyzer = CSSReachabilityAnalyzer()

    result = analyzer.analyze(
        [used, unused],
        graph,
    )

    assert set(result.keys()) == {
        used,
        unused,
    }