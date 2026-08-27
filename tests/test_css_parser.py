"""
Tests for the DevDoctor CSS parser.
"""

from parsers.css_parser import CSSParser


def test_simple_class_selector():

    css = """
    .card {
        padding: 10px;
    }
    """

    result = CSSParser().parse(css)

    assert "card" in result.classes
    assert result.total_rules == 1
    assert result.total_selectors == 1
    assert result.invalid_selectors == 0


def test_simple_id_selector():

    css = """
    #header {
        background: black;
    }
    """

    result = CSSParser().parse(css)

    assert "header" in result.ids
    assert result.total_rules == 1
    assert result.invalid_selectors == 0


def test_element_selector():

    css = """
    body {
        margin: 0;
    }

    button {
        cursor: pointer;
    }
    """

    result = CSSParser().parse(css)

    assert "body" in result.elements
    assert "button" in result.elements

    assert result.total_rules == 2
    assert result.invalid_selectors == 0


def test_multiple_classes():

    css = """
    .card.feature-box {
        padding: 10px;
    }
    """

    result = CSSParser().parse(css)

    assert "card" in result.classes
    assert "feature-box" in result.classes

    assert result.invalid_selectors == 0


def test_descendant_selector():

    css = """
    .container .card {
        padding: 10px;
    }
    """

    result = CSSParser().parse(css)

    assert "container" in result.classes
    assert "card" in result.classes

    assert result.invalid_selectors == 0


def test_child_selector():

    css = """
    .container > .card {
        padding: 10px;
    }
    """

    result = CSSParser().parse(css)

    assert "container" in result.classes
    assert "card" in result.classes

    assert result.invalid_selectors == 0


def test_element_with_class():

    css = """
    button.primary-btn {
        cursor: pointer;
    }
    """

    result = CSSParser().parse(css)

    assert "button" in result.elements
    assert "primary-btn" in result.classes

    assert result.invalid_selectors == 0


def test_id_with_class():

    css = """
    #contact-section.contact-page {
        display: block;
    }
    """

    result = CSSParser().parse(css)

    assert "contact-section" in result.ids
    assert "contact-page" in result.classes

    assert result.invalid_selectors == 0


def test_selector_list():

    css = """
    .card,
    .box,
    .panel {
        padding: 10px;
    }
    """

    result = CSSParser().parse(css)

    assert "card" in result.classes
    assert "box" in result.classes
    assert "panel" in result.classes

    assert result.total_rules == 1
    assert result.total_selectors == 3
    assert result.invalid_selectors == 0


def test_pseudo_class():

    css = """
    .btn:hover {
        opacity: 0.8;
    }
    """

    result = CSSParser().parse(css)

    assert "btn" in result.classes
    assert result.invalid_selectors == 0


def test_pseudo_element():

    css = """
    .card::before {
        content: "";
    }
    """

    result = CSSParser().parse(css)

    assert "card" in result.classes
    assert result.invalid_selectors == 0


def test_not_selector():

    css = """
    .card:not(.unused-card) {
        display: block;
    }
    """

    result = CSSParser().parse(css)

    assert "card" in result.classes
    assert "unused-card" in result.classes

    assert result.invalid_selectors == 0


def test_is_selector():

    css = """
    :is(.card, .feature-box) {
        margin: 10px;
    }
    """

    result = CSSParser().parse(css)

    assert "card" in result.classes
    assert "feature-box" in result.classes

    assert result.invalid_selectors == 0


def test_where_selector():

    css = """
    :where(.container, .wrapper) {
        max-width: 1200px;
    }
    """

    result = CSSParser().parse(css)

    assert "container" in result.classes
    assert "wrapper" in result.classes

    assert result.invalid_selectors == 0


def test_attribute_selector():

    css = """
    input[type="text"] {
        padding: 8px;
    }
    """

    result = CSSParser().parse(css)

    assert "input" in result.elements
    assert result.invalid_selectors == 0


def test_attribute_selector_with_class():

    css = """
    input.form-control[type="email"] {
        width: 100%;
    }
    """

    result = CSSParser().parse(css)

    assert "input" in result.elements
    assert "form-control" in result.classes

    assert result.invalid_selectors == 0


def test_media_query():

    css = """
    @media (max-width: 768px) {

        .container {
            padding: 10px;
        }

        .mobile-menu {
            display: block;
        }
    }
    """

    result = CSSParser().parse(css)

    assert "container" in result.classes
    assert "mobile-menu" in result.classes

    assert result.invalid_selectors == 0


def test_multiple_at_rules():

    css = """
    @media (max-width: 768px) {

        .mobile-menu {
            display: block;
        }
    }

    @supports (display: grid) {

        .grid {
            display: grid;
        }
    }
    """

    result = CSSParser().parse(css)

    assert "mobile-menu" in result.classes
    assert "grid" in result.classes

    assert result.invalid_selectors == 0


def test_escaped_class_selector():

    css = r"""
    .user\:active {
        color: red;
    }
    """

    result = CSSParser().parse(css)

    assert "user:active" in result.classes
    assert result.invalid_selectors == 0


def test_multiple_combinators():

    css = """
    .container > .row .card + .button {
        display: block;
    }
    """

    result = CSSParser().parse(css)

    assert "container" in result.classes
    assert "row" in result.classes
    assert "card" in result.classes
    assert "button" in result.classes

    assert result.invalid_selectors == 0


def test_multiple_id_and_classes():

    css = """
    #main.container.active {
        display: block;
    }
    """

    result = CSSParser().parse(css)

    assert "main" in result.ids
    assert "container" in result.classes
    assert "active" in result.classes

    assert result.invalid_selectors == 0


def test_universal_selector():

    css = """
    *.card {
        box-sizing: border-box;
    }
    """

    result = CSSParser().parse(css)

    assert "card" in result.classes
    assert result.invalid_selectors == 0


def test_attribute_prefix_selector():

    css = """
    input[name^="user"] {
        padding: 8px;
    }
    """

    result = CSSParser().parse(css)

    assert "input" in result.elements
    assert result.invalid_selectors == 0


def test_attribute_contains_selector():

    css = """
    input[class*="form"] {
        width: 100%;
    }
    """

    result = CSSParser().parse(css)

    assert "input" in result.elements
    assert result.invalid_selectors == 0


def test_has_selector():

    css = """
    .card:has(.price) {
        border: 1px solid black;
    }
    """

    result = CSSParser().parse(css)

    assert "card" in result.classes
    assert "price" in result.classes

    assert result.invalid_selectors == 0


def test_nested_function_selector():

    css = """
    :not(:is(.card, .box)) {
        display: block;
    }
    """

    result = CSSParser().parse(css)

    assert "card" in result.classes
    assert "box" in result.classes

    assert result.invalid_selectors == 0


def test_complex_selector_list():

    css = """
    .card:hover,
    #modal .button,
    input.form-control[type="email"] {
        display: block;
    }
    """

    result = CSSParser().parse(css)

    assert "card" in result.classes
    assert "button" in result.classes
    assert "modal" in result.ids
    assert "input" in result.elements
    assert "form-control" in result.classes

    assert result.total_rules == 1
    assert result.total_selectors == 3
    assert result.invalid_selectors == 0


def test_invalid_selector():

    css = """
    .card {
        display: block;
    }

    .button:::invalid {
        color: red;
    }
    """

    result = CSSParser().parse(css)

    assert "card" in result.classes
    assert result.invalid_selectors >= 1
def test_selector_list_stores_individual_selector_names():

    css = """
    .card,
    .feature-box,
    .highlight {
        padding: 10px;
    }
    """

    result = CSSParser().parse(css)

    selectors = [
        selector.selector
        for selector in result.selectors
    ]

    assert ".card" in selectors
    assert ".feature-box" in selectors
    assert ".highlight" in selectors

    assert len(selectors) == 3

def test_selector_list_does_not_duplicate_full_selector_text():

    css = """
    .card,
    .feature-box,
    .highlight {
        padding: 10px;
    }
    """

    result = CSSParser().parse(css)

    selectors = [
        selector.selector
        for selector in result.selectors
    ]

    assert ".card,\n.feature-box,\n.highlight" not in selectors




def test_selector_list_preserves_same_source_location():

    css = """
    .card,
    .feature-box,
    .highlight {
        padding: 10px;
    }
    """

    result = CSSParser().parse(css)

    assert len(result.selectors) == 3

    lines = {
        selector.source_line
        for selector in result.selectors
    }

    columns = {
        selector.source_column
        for selector in result.selectors
    }

    assert len(lines) == 1
    assert len(columns) == 1