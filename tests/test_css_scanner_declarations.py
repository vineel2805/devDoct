from pathlib import Path

from scanner.css_scanner import CSSScanner


def test_css_scanner_preserves_declarations(tmp_path: Path):

    css_file = tmp_path / "style.css"

    css_file.write_text(
        """
        .card {
            color: red;
            padding: 20px;
        }
        """,
        encoding="utf-8"
    )

    result = CSSScanner().scan([css_file])

    file_result = result.files[css_file]

    assert len(file_result.declarations) == 2

    assert file_result.declarations[0].property == "color"
    assert file_result.declarations[0].value == "red"

    assert file_result.declarations[1].property == "padding"
    assert file_result.declarations[1].value == "20px"