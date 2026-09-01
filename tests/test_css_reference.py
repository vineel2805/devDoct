from pathlib import Path

from models.css_reference import CSSReference


def test_css_reference_stores_basic_reference():

    source = Path("index.php")
    target = Path("css/style.css")

    reference = CSSReference(
        source_file=source,
        target_file=target,
        reference_type="stylesheet",
        source_line=10,
        source_column=5,
    )

    assert reference.source_file == source
    assert reference.target_file == target
    assert reference.reference_type == "stylesheet"
    assert reference.source_line == 10
    assert reference.source_column == 5
    assert reference.confidence == "high"
    assert reference.resolved is False


def test_css_reference_can_represent_import():

    source = Path("css/main.css")
    target = Path("css/components.css")

    reference = CSSReference(
        source_file=source,
        target_file=target,
        reference_type="import",
        source_line=3,
        source_column=1,
    )

    assert reference.reference_type == "import"
    assert reference.source_file == source
    assert reference.target_file == target


def test_css_reference_can_represent_unresolved_dynamic_reference():

    reference = CSSReference(
        source_file=Path("templates/header.php"),
        target_file=None,
        reference_type="dynamic_stylesheet",
        source_line=15,
        confidence="low",
        resolved=False,
    )

    assert reference.target_file is None
    assert reference.reference_type == "dynamic_stylesheet"
    assert reference.confidence == "low"
    assert reference.resolved is False
    