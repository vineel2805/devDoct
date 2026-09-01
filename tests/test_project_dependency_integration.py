from pathlib import Path

from scanner.file_scanner import FileScanner
from scanner.project_dependency_scanner import (
    ProjectDependencyScanner,
)


def test_dependency_scanner_works_with_file_scanner(
    tmp_path: Path,
):

    index = tmp_path / "index.php"
    header = tmp_path / "header.php"
    css = tmp_path / "css" / "header.css"

    css.parent.mkdir()

    index.write_text(
        """
        <?php
        include "header.php";
        ?>
        """,
        encoding="utf-8",
    )

    header.write_text(
        """
        <link rel="stylesheet" href="css/header.css">
        """,
        encoding="utf-8",
    )

    css.write_text(
        """
        .header {
            color: red;
        }
        """,
        encoding="utf-8",
    )

    # First discover files using the existing scanner.
    project = FileScanner(tmp_path).scan()

    assert index in project.php
    assert header in project.php
    assert css in project.css

    # Then build the dependency graph.
    scanner = ProjectDependencyScanner()

    graph = scanner.scan(
        project.php + project.html + project.css,
        project.root,
    )

    assert header.resolve() in graph.children(
        index
    )

    assert css.resolve() in graph.children(
        header
    )


def test_file_scanner_and_dependency_graph_handle_nested_templates(
    tmp_path: Path,
):

    index = tmp_path / "index.php"
    layout = tmp_path / "layout.php"
    header = tmp_path / "header.php"
    css = tmp_path / "header.css"

    index.write_text(
        'include "layout.php";',
        encoding="utf-8",
    )

    layout.write_text(
        'include "header.php";',
        encoding="utf-8",
    )

    header.write_text(
        '<link rel="stylesheet" href="header.css">',
        encoding="utf-8",
    )

    css.write_text(
        '.header { display: block; }',
        encoding="utf-8",
    )

    project = FileScanner(tmp_path).scan()

    scanner = ProjectDependencyScanner()

    graph = scanner.scan(
        project.php + project.html + project.css,
        project.root,
    )

    assert graph.dependencies(index) == {
        layout.resolve(),
        header.resolve(),
        css.resolve(),
    }


def test_dependency_graph_identifies_css_entrypoint(
    tmp_path: Path,
):

    index = tmp_path / "index.php"
    css = tmp_path / "main.css"

    index.write_text(
        '<link rel="stylesheet" href="main.css">',
        encoding="utf-8",
    )

    css.write_text(
        '.card { color: red; }',
        encoding="utf-8",
    )

    project = FileScanner(tmp_path).scan()

    graph = ProjectDependencyScanner().scan(
        project.php + project.html + project.css,
        project.root,
    )

    assert graph.parents(css) == {
        index.resolve()
    }


def test_unreferenced_css_has_no_dependency_parent(
    tmp_path: Path,
):

    index = tmp_path / "index.php"
    used_css = tmp_path / "used.css"
    dead_css = tmp_path / "dead.css"

    index.write_text(
        '<link rel="stylesheet" href="used.css">',
        encoding="utf-8",
    )

    used_css.write_text(
        '.used { color: red; }',
        encoding="utf-8",
    )

    dead_css.write_text(
        '.dead { color: blue; }',
        encoding="utf-8",
    )

    project = FileScanner(tmp_path).scan()

    graph = ProjectDependencyScanner().scan(
        project.php + project.html + project.css,
        project.root,
    )

    assert graph.parents(used_css) == {
        index.resolve()
    }

    assert graph.parents(dead_css) == set()