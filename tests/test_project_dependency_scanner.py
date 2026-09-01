from pathlib import Path

from scanner.project_dependency_scanner import (
    ProjectDependencyScanner,
)


def test_finds_php_to_php_dependency(tmp_path: Path):

    index = tmp_path / "index.php"
    header = tmp_path / "header.php"

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
        <header>Header</header>
        """,
        encoding="utf-8",
    )

    scanner = ProjectDependencyScanner()

    result = scanner.scan(
        [index, header],
        tmp_path,
    )

    assert result.children(index) == {
        header.resolve()
    }


def test_finds_php_to_css_dependency(tmp_path: Path):

    index = tmp_path / "index.php"
    css = tmp_path / "style.css"

    index.write_text(
        """
        <link rel="stylesheet" href="style.css">
        """,
        encoding="utf-8",
    )

    css.write_text(
        """
        .card {
            color: red;
        }
        """,
        encoding="utf-8",
    )

    scanner = ProjectDependencyScanner()

    result = scanner.scan(
        [index, css],
        tmp_path,
    )

    assert result.children(index) == {
        css.resolve()
    }


def test_finds_css_import(tmp_path: Path):

    main_css = tmp_path / "main.css"
    component_css = tmp_path / "component.css"

    main_css.write_text(
        """
        @import "component.css";

        body {
            margin: 0;
        }
        """,
        encoding="utf-8",
    )

    component_css.write_text(
        """
        .button {
            display: flex;
        }
        """,
        encoding="utf-8",
    )

    scanner = ProjectDependencyScanner()

    result = scanner.scan(
        [main_css, component_css],
        tmp_path,
    )

    assert result.children(main_css) == {
        component_css.resolve()
    }


def test_finds_complete_php_to_css_chain(tmp_path: Path):

    index = tmp_path / "index.php"
    header = tmp_path / "header.php"
    css = tmp_path / "header.css"

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
        <link rel="stylesheet" href="header.css">
        """,
        encoding="utf-8",
    )

    css.write_text(
        """
        .header {
            background: black;
        }
        """,
        encoding="utf-8",
    )

    scanner = ProjectDependencyScanner()

    result = scanner.scan(
        [index, header, css],
        tmp_path,
    )

    assert result.children(index) == {
        header.resolve()
    }

    assert result.children(header) == {
        css.resolve()
    }

    assert result.dependencies(index) == {
        header.resolve(),
        css.resolve(),
    }


def test_handles_multiple_entry_files(tmp_path: Path):

    index = tmp_path / "index.php"
    admin = tmp_path / "admin.php"

    index_css = tmp_path / "index.css"
    admin_css = tmp_path / "admin.css"

    index.write_text(
        '<link rel="stylesheet" href="index.css">',
        encoding="utf-8",
    )

    admin.write_text(
        '<link rel="stylesheet" href="admin.css">',
        encoding="utf-8",
    )

    index_css.write_text(
        ".home { color: red; }",
        encoding="utf-8",
    )

    admin_css.write_text(
        ".admin { color: blue; }",
        encoding="utf-8",
    )

    scanner = ProjectDependencyScanner()

    result = scanner.scan(
        [
            index,
            admin,
            index_css,
            admin_css,
        ],
        tmp_path,
    )

    assert result.children(index) == {
        index_css.resolve()
    }

    assert result.children(admin) == {
        admin_css.resolve()
    }


def test_missing_dependency_does_not_crash(
    tmp_path: Path,
):

    index = tmp_path / "index.php"

    index.write_text(
        """
        <?php
        include "missing.php";
        ?>
        """,
        encoding="utf-8",
    )

    scanner = ProjectDependencyScanner()

    result = scanner.scan(
        [index],
        tmp_path,
    )

    assert result.children(index) == set()


def test_handles_circular_php_dependencies(
    tmp_path: Path,
):

    first = tmp_path / "first.php"
    second = tmp_path / "second.php"

    first.write_text(
        """
        <?php
        include "second.php";
        ?>
        """,
        encoding="utf-8",
    )

    second.write_text(
        """
        <?php
        include "first.php";
        ?>
        """,
        encoding="utf-8",
    )

    scanner = ProjectDependencyScanner()

    result = scanner.scan(
        [first, second],
        tmp_path,
    )

    assert result.children(first) == {
        second.resolve()
    }

    assert result.children(second) == {
        first.resolve()
    }

    assert result.has_cycle() is True


def test_preserves_dependency_evidence(
    tmp_path: Path,
):

    index = tmp_path / "index.php"
    css = tmp_path / "style.css"

    index.write_text(
        """
        <html>
            <head>
                <link rel="stylesheet" href="style.css">
            </head>
        </html>
        """,
        encoding="utf-8",
    )

    css.write_text(
        ".card { color: red; }",
        encoding="utf-8",
    )

    scanner = ProjectDependencyScanner()

    result = scanner.scan(
        [index, css],
        tmp_path,
    )

    edges = result.edges(
        index,
        css,
    )

    assert len(edges) == 1

    edge = next(iter(edges))

    assert edge.dependency_type == "stylesheet"
    assert edge.source_line == 4
    assert edge.confidence == "high"
    assert edge.resolved is True