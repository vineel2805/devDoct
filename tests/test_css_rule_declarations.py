from parsers.css_parser import CSSParser


def test_parser_associates_declarations_with_selector():

    css = """
    .card {
        color: red;
        padding: 20px;
    }
    """

    result = CSSParser().parse(css)

    rule = result.rules[0]

    assert rule.selectors == [".card"]

    assert len(rule.declarations) == 2

    assert rule.declarations[0].property == "color"
    assert rule.declarations[0].value == "red"

    assert rule.declarations[1].property == "padding"
    assert rule.declarations[1].value == "20px"


def test_parser_associates_multiple_rules():

    css = """
    .card {
        color: red;
    }

    .button {
        display: flex;
    }
    """

    result = CSSParser().parse(css)

    assert len(result.rules) == 2

    assert result.rules[0].selectors == [".card"]
    assert result.rules[0].declarations[0].property == "color"

    assert result.rules[1].selectors == [".button"]
    assert result.rules[1].declarations[0].property == "display"