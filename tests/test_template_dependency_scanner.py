from pathlib import Path

from scanner.template_dependency_scanner import (
    TemplateDependencyScanner,
)


def test_finds_include(tmp_path: Path):

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

    scanner = TemplateDependencyScanner()

    result = scanner.scan(
        [index],
        tmp_path,
    )

    assert len(result) == 1

    dependency = result[0]

    assert dependency.source_file == index
    assert dependency.target_file == header
    assert dependency.dependency_type == "include"
    assert dependency.resolved is True


def test_finds_require(tmp_path: Path):

    index = tmp_path / "index.php"
    config = tmp_path / "config.php"

    index.write_text(
        """
        <?php
        require "config.php";
        ?>
        """,
        encoding="utf-8",
    )

    config.write_text(
        """
        <?php
        $app = "Iksha";
        ?>
        """,
        encoding="utf-8",
    )

    scanner = TemplateDependencyScanner()

    result = scanner.scan(
        [index],
        tmp_path,
    )

    assert len(result) == 1

    dependency = result[0]

    assert dependency.source_file == index
    assert dependency.target_file == config
    assert dependency.dependency_type == "require"
    assert dependency.resolved is True


def test_finds_include_once(tmp_path: Path):

    index = tmp_path / "index.php"
    header = tmp_path / "header.php"

    index.write_text(
        """
        <?php
        include_once "header.php";
        ?>
        """,
        encoding="utf-8",
    )

    header.write_text(
        "",
        encoding="utf-8",
    )

    scanner = TemplateDependencyScanner()

    result = scanner.scan(
        [index],
        tmp_path,
    )

    assert len(result) == 1

    dependency = result[0]

    assert dependency.dependency_type == "include_once"
    assert dependency.target_file == header
    assert dependency.resolved is True


def test_finds_require_once(tmp_path: Path):

    index = tmp_path / "index.php"
    database = tmp_path / "database.php"

    index.write_text(
        """
        <?php
        require_once "database.php";
        ?>
        """,
        encoding="utf-8",
    )

    database.write_text(
        "",
        encoding="utf-8",
    )

    scanner = TemplateDependencyScanner()

    result = scanner.scan(
        [index],
        tmp_path,
    )

    assert len(result) == 1

    dependency = result[0]

    assert dependency.dependency_type == "require_once"
    assert dependency.target_file == database
    assert dependency.resolved is True


def test_resolves_relative_include(tmp_path: Path):

    pages = tmp_path / "pages"
    includes = tmp_path / "includes"

    pages.mkdir()
    includes.mkdir()

    index = pages / "index.php"
    header = includes / "header.php"

    index.write_text(
        """
        <?php
        include "../includes/header.php";
        ?>
        """,
        encoding="utf-8",
    )

    header.write_text(
        "",
        encoding="utf-8",
    )

    scanner = TemplateDependencyScanner()

    result = scanner.scan(
        [index],
        tmp_path,
    )

    assert len(result) == 1

    dependency = result[0]

    assert dependency.target_file == header
    assert dependency.resolved is True


def test_records_missing_dependency(tmp_path: Path):

    index = tmp_path / "index.php"

    index.write_text(
        """
        <?php
        include "missing.php";
        ?>
        """,
        encoding="utf-8",
    )

    scanner = TemplateDependencyScanner()

    result = scanner.scan(
        [index],
        tmp_path,
    )

    assert len(result) == 1

    dependency = result[0]

    assert dependency.source_file == index
    assert dependency.target_file is None
    assert dependency.dependency_type == "include"
    assert dependency.resolved is False


def test_finds_multiple_dependencies(tmp_path: Path):

    index = tmp_path / "index.php"
    header = tmp_path / "header.php"
    footer = tmp_path / "footer.php"

    index.write_text(
        """
        <?php

        include "header.php";
        require "footer.php";

        ?>
        """,
        encoding="utf-8",
    )

    header.write_text("", encoding="utf-8")
    footer.write_text("", encoding="utf-8")

    scanner = TemplateDependencyScanner()

    result = scanner.scan(
        [index],
        tmp_path,
    )

    assert len(result) == 2

    targets = {
        dependency.target_file
        for dependency in result
    }

    assert header in targets
    assert footer in targets


def test_records_source_line(tmp_path: Path):

    index = tmp_path / "index.php"
    header = tmp_path / "header.php"

    index.write_text(
        """
        <?php

        echo "Hello";

        include "header.php";

        ?>
        """,
        encoding="utf-8",
    )

    header.write_text("", encoding="utf-8")

    scanner = TemplateDependencyScanner()

    result = scanner.scan(
        [index],
        tmp_path,
    )

    assert len(result) == 1

    dependency = result[0]

    assert dependency.source_line == 6


def test_ignores_non_php_files(tmp_path: Path):

    html_file = tmp_path / "index.html"
    php_file = tmp_path / "header.php"

    html_file.write_text(
        """
        include "header.php";
        """,
        encoding="utf-8",
    )

    php_file.write_text(
        "",
        encoding="utf-8",
    )

    scanner = TemplateDependencyScanner()

    result = scanner.scan(
        [html_file],
        tmp_path,
    )

    assert result == []


def test_finds_nested_dependencies(tmp_path: Path):

    index = tmp_path / "index.php"
    header = tmp_path / "header.php"
    navigation = tmp_path / "navigation.php"

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
        <?php
        include "navigation.php";
        ?>
        """,
        encoding="utf-8",
    )

    navigation.write_text(
        """
        <nav>Navigation</nav>
        """,
        encoding="utf-8",
    )

    scanner = TemplateDependencyScanner()

    result = scanner.scan(
        [index, header],
        tmp_path,
    )

    assert len(result) == 2

    dependencies = {
        (
            dependency.source_file,
            dependency.target_file,
        )
        for dependency in result
    }

    assert (
        index,
        header,
    ) in dependencies

    assert (
        header,
        navigation,
    ) in dependencies


def test_handles_circular_dependencies(tmp_path: Path):

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

    scanner = TemplateDependencyScanner()

    result = scanner.scan(
        [first, second],
        tmp_path,
    )

    assert len(result) == 2

    dependencies = {
        (
            dependency.source_file,
            dependency.target_file,
        )
        for dependency in result
    }

    assert (
        first,
        second,
    ) in dependencies

    assert (
        second,
        first,
    ) in dependencies