from pathlib import Path

from scanner.js_scanner import JSScanner


def test_finds_query_selector_class(tmp_path: Path):

    js = tmp_path / "app.js"

    js.write_text(
        """
        const card = document.querySelector(".card");
        """,
        encoding="utf-8",
    )

    result = JSScanner().scan([js])

    assert len(result) == 1
    assert result[0].value == "card"
    assert result[0].reference_type == "class"


def test_finds_query_selector_id(tmp_path: Path):

    js = tmp_path / "app.js"

    js.write_text(
        """
        const modal = document.querySelector("#login-modal");
        """,
        encoding="utf-8",
    )

    result = JSScanner().scan([js])

    assert len(result) == 1
    assert result[0].value == "login-modal"
    assert result[0].reference_type == "id"


def test_finds_query_selector_all(tmp_path: Path):

    js = tmp_path / "app.js"

    js.write_text(
        """
        document.querySelectorAll(".product");
        """,
        encoding="utf-8",
    )

    result = JSScanner().scan([js])

    assert len(result) == 1
    assert result[0].value == "product"
    assert result[0].reference_type == "class"


def test_finds_class_list_add(tmp_path: Path):

    js = tmp_path / "app.js"

    js.write_text(
        """
        element.classList.add("active");
        """,
        encoding="utf-8",
    )

    result = JSScanner().scan([js])

    assert len(result) == 1
    assert result[0].value == "active"
    assert result[0].reference_type == "class"


def test_finds_class_list_remove(tmp_path: Path):

    js = tmp_path / "app.js"

    js.write_text(
        """
        element.classList.remove("hidden");
        """,
        encoding="utf-8",
    )

    result = JSScanner().scan([js])

    assert len(result) == 1
    assert result[0].value == "hidden"
    assert result[0].reference_type == "class"


def test_records_source_location(tmp_path: Path):

    js = tmp_path / "app.js"

    js.write_text(
        """
        const x = 1;

        document.querySelector(".card");
        """,
        encoding="utf-8",
    )

    result = JSScanner().scan([js])

    assert len(result) == 1

    reference = result[0]

    assert reference.source_file == js
    assert reference.source_line == 4


def test_ignores_non_js_files(tmp_path: Path):

    css = tmp_path / "style.css"

    css.write_text(
        ".card { color: red; }",
        encoding="utf-8",
    )

    result = JSScanner().scan([css])

    assert result == []


def test_finds_multiple_references(tmp_path: Path):

    js = tmp_path / "app.js"

    js.write_text(
        """
        document.querySelector(".card");
        document.querySelector("#modal");
        element.classList.add("active");
        """,
        encoding="utf-8",
    )

    result = JSScanner().scan([js])

    values = {
        reference.value
        for reference in result
    }

    assert values == {
        "card",
        "modal",
        "active",
    }