from pathlib import Path

from models.dependency_graph import DependencyGraph


def test_add_dependency():

    graph = DependencyGraph()

    source = Path("index.php")
    target = Path("header.php")

    graph.add_dependency(source, target)

    assert graph.children(source) == {
        target.resolve()
    }


def test_find_parents():

    graph = DependencyGraph()

    index = Path("index.php")
    header = Path("header.php")

    graph.add_dependency(index, header)

    assert graph.parents(header) == {
        index.resolve()
    }


def test_finds_transitive_dependencies():

    graph = DependencyGraph()

    index = Path("index.php")
    header = Path("header.php")
    navigation = Path("navigation.php")

    graph.add_dependency(index, header)
    graph.add_dependency(header, navigation)

    dependencies = graph.dependencies(index)

    assert dependencies == {
        header.resolve(),
        navigation.resolve(),
    }


def test_finds_transitive_dependents():

    graph = DependencyGraph()

    index = Path("index.php")
    header = Path("header.php")
    navigation = Path("navigation.php")

    graph.add_dependency(index, header)
    graph.add_dependency(header, navigation)

    dependents = graph.dependents(navigation)

    assert dependents == {
        index.resolve(),
        header.resolve(),
    }


def test_does_not_duplicate_dependency():

    graph = DependencyGraph()

    source = Path("index.php")
    target = Path("header.php")

    graph.add_dependency(source, target)
    graph.add_dependency(source, target)

    assert graph.children(source) == {
        target.resolve()
    }


def test_handles_missing_target_node():

    graph = DependencyGraph()

    source = Path("index.php")
    target = Path("missing.php")

    graph.add_dependency(source, target)

    assert graph.children(source) == {
        target.resolve()
    }


def test_detects_circular_dependency():

    graph = DependencyGraph()

    first = Path("first.php")
    second = Path("second.php")

    graph.add_dependency(first, second)
    graph.add_dependency(second, first)

    assert graph.has_cycle() is True


def test_does_not_report_cycle_for_normal_graph():

    graph = DependencyGraph()

    index = Path("index.php")
    header = Path("header.php")
    footer = Path("footer.php")

    graph.add_dependency(index, header)
    graph.add_dependency(index, footer)

    assert graph.has_cycle() is False


def test_handles_long_dependency_chain():

    graph = DependencyGraph()

    first = Path("a.php")
    second = Path("b.php")
    third = Path("c.php")
    fourth = Path("d.php")

    graph.add_dependency(first, second)
    graph.add_dependency(second, third)
    graph.add_dependency(third, fourth)

    assert graph.dependencies(first) == {
        second.resolve(),
        third.resolve(),
        fourth.resolve(),
    }


def test_cycle_safe_transitive_traversal():

    graph = DependencyGraph()

    first = Path("a.php")
    second = Path("b.php")
    third = Path("c.php")

    graph.add_dependency(first, second)
    graph.add_dependency(second, third)
    graph.add_dependency(third, first)

    assert graph.dependencies(first) == {
        second.resolve(),
        third.resolve(),
        first.resolve(),
    }