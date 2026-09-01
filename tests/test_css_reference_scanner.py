from pathlib import Path

from scanner.css_reference_scanner import CSSReferenceScanner


def test_finds_stylesheet_link(tmp_path: Path):

    html_file = tmp_path / "index.php"
    css_file = tmp_path / "css" / "style.css"

    css_file.parent.mkdir()

    html_file.write_text(
        """
        <html>
            <head>
                <link rel="stylesheet" href="css/style.css">
            </head>
        </html>
        """,
        encoding="utf-8",
    )

    scanner = CSSReferenceScanner()

    result = scanner.scan(
        [html_file],
        [css_file],
        tmp_path,
    )

    assert len(result) == 1

    reference = result[0]

    assert reference.source_file == html_file
    assert reference.target_file == css_file
    assert reference.reference_type == "stylesheet"
    assert reference.resolved is True


def test_finds_relative_stylesheet_link(
    tmp_path: Path,
):

    pages = tmp_path / "pages"
    css_dir = tmp_path / "css"

    pages.mkdir()
    css_dir.mkdir()

    html_file = pages / "index.php"
    css_file = css_dir / "style.css"

    html_file.write_text(
        """
        <link rel="stylesheet" href="../css/style.css">
        """,
        encoding="utf-8",
    )

    css_file.write_text(
        ".card { color: red; }",
        encoding="utf-8",
    )

    scanner = CSSReferenceScanner()

    result = scanner.scan(
        [html_file],
        [css_file],
        tmp_path,
    )

    assert len(result) == 1

    reference = result[0]

    assert reference.target_file == css_file
    assert reference.resolved is True


def test_finds_css_import(tmp_path: Path):

    css_dir = tmp_path / "css"
    css_dir.mkdir()

    main_css = css_dir / "main.css"
    components_css = css_dir / "components.css"

    main_css.write_text(
        """
        @import "components.css";

        .card {
            color: red;
        }
        """,
        encoding="utf-8",
    )

    components_css.write_text(
        """
        .button {
            display: flex;
        }
        """,
        encoding="utf-8",
    )

    scanner = CSSReferenceScanner()

    result = scanner.scan(
        [main_css],
        [main_css, components_css],
        tmp_path,
    )

    assert len(result) == 1

    reference = result[0]

    assert reference.source_file == main_css
    assert reference.target_file == components_css
    assert reference.reference_type == "import"
    assert reference.resolved is True


def test_finds_import_using_url_function(
    tmp_path: Path,
):

    css_dir = tmp_path / "css"
    css_dir.mkdir()

    main_css = css_dir / "main.css"
    reset_css = css_dir / "reset.css"

    main_css.write_text(
        """
        @import url("reset.css");
        """,
        encoding="utf-8",
    )

    reset_css.write_text(
        """
        body {
            margin: 0;
        }
        """,
        encoding="utf-8",
    )

    scanner = CSSReferenceScanner()

    result = scanner.scan(
        [main_css],
        [main_css, reset_css],
        tmp_path,
    )

    assert len(result) == 1

    reference = result[0]

    assert reference.target_file == reset_css
    assert reference.reference_type == "import"
    assert reference.resolved is True


def test_handles_missing_stylesheet_reference(
    tmp_path: Path,
):

    html_file = tmp_path / "index.php"
    existing_css = tmp_path / "style.css"

    html_file.write_text(
        """
        <link rel="stylesheet" href="missing.css">
        """,
        encoding="utf-8",
    )

    existing_css.write_text(
        ".card { color: red; }",
        encoding="utf-8",
    )

    scanner = CSSReferenceScanner()

    result = scanner.scan(
        [html_file],
        [existing_css],
        tmp_path,
    )

    assert len(result) == 1

    reference = result[0]

    assert reference.target_file is None
    assert reference.reference_type == "stylesheet"
    assert reference.resolved is False


def test_ignores_non_stylesheet_links(
    tmp_path: Path,
):

    html_file = tmp_path / "index.php"
    css_file = tmp_path / "style.css"

    html_file.write_text(
        """
        <link rel="icon" href="favicon.ico">
        <link rel="preload" href="font.woff2">
        """,
        encoding="utf-8",
    )

    css_file.write_text(
        ".card { color: red; }",
        encoding="utf-8",
    )

    scanner = CSSReferenceScanner()

    result = scanner.scan(
        [html_file],
        [css_file],
        tmp_path,
    )

    assert result == []


def test_handles_query_string_in_stylesheet(
    tmp_path: Path,
):

    html_file = tmp_path / "index.php"
    css_file = tmp_path / "style.css"

    html_file.write_text(
        """
        <link
            rel="stylesheet"
            href="style.css?v=42"
        >
        """,
        encoding="utf-8",
    )

    css_file.write_text(
        ".card { color: red; }",
        encoding="utf-8",
    )

    scanner = CSSReferenceScanner()

    result = scanner.scan(
        [html_file],
        [css_file],
        tmp_path,
    )

    assert len(result) == 1

    reference = result[0]

    assert reference.target_file == css_file
    assert reference.resolved is True