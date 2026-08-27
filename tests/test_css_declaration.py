from parsers.css_parser import CSSParser


def test_parser_extracts_declaration_property_and_value():

    css = """
    .card {
        color: red;
    }
    """

    result = CSSParser().parse(css)

    assert len(result.declarations) == 1

    declaration = result.declarations[0]

    assert declaration.property == "color"
    assert declaration.value == "red"


def test_parser_extracts_multiple_declarations():

    css = """
    .card {
        color: red;
        padding: 20px;
        display: flex;
    }
    """

    result = CSSParser().parse(css)

    assert len(result.declarations) == 3

    assert result.declarations[0].property == "color"
    assert result.declarations[0].value == "red"

    assert result.declarations[1].property == "padding"
    assert result.declarations[1].value == "20px"

    assert result.declarations[2].property == "display"
    assert result.declarations[2].value == "flex"


def test_parser_preserves_declaration_source_information():

    css = """
    .card {
        color: red;
    }
    """

    result = CSSParser().parse(css)

    declaration = result.declarations[0]

    assert declaration.source_line > 0
    assert declaration.source_column > 0


    


def test_parser_handles_important_value():

    css = """
    .card {
        color: red !important;
    }
    """

    result = CSSParser().parse(css)

    declaration = result.declarations[0]

    assert declaration.property == "color"
    assert declaration.value == "red !important"


def test_parser_handles_custom_property():

    css = """
    .card {
        --primary-color: #333;
    }
    """

    result = CSSParser().parse(css)

    declaration = result.declarations[0]

    assert declaration.property == "--primary-color"
    assert declaration.value == "#333"


def test_parser_handles_complex_value():

    css = """
    .card {
        margin: 10px 20px;
        font-family: Arial, sans-serif;
    }
    """

    result = CSSParser().parse(css)

    assert len(result.declarations) == 2

    assert result.declarations[0].property == "margin"
    assert result.declarations[0].value == "10px 20px"

    assert result.declarations[1].property == "font-family"
    assert result.declarations[1].value == "Arial, sans-serif"