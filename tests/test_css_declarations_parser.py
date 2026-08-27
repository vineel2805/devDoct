from parsers.css_parser import CSSParser


def test_parser_extracts_css_declaration():

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

    properties = [
        declaration.property
        for declaration in result.declarations
    ]

    assert properties == [
        "color",
        "padding",
        "display",
    ]