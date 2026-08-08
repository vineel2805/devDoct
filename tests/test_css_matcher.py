"""
Tests for the DevDoctor CSS matcher.
"""

from analyzers.css_matcher import CSSMatcher
from parsers.css_parser import CSSParser


def get_selector(css: str):

    result = CSSParser().parse(css)

    assert result.total_selectors == 1

    return result.selectors[0]


def test_class_selector_matches():

    html = """
    <div class="card">
        Product
    </div>
    """

    selector = get_selector(
        ".card { color: red; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_class_selector_does_not_match():

    html = """
    <div class="product">
        Product
    </div>
    """

    selector = get_selector(
        ".card { color: red; }"
    )

    matcher = CSSMatcher()

    assert not matcher.matches(selector, html)


def test_descendant_selector_matches():

    html = """
    <div class="container">
        <div class="card">
            Product
        </div>
    </div>
    """

    selector = get_selector(
        ".container .card { color: red; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_child_selector_matches():

    html = """
    <div class="container">
        <div class="card">
            Product
        </div>
    </div>
    """

    selector = get_selector(
        ".container > .card { color: red; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_child_selector_does_not_match():

    html = """
    <div class="container">
        <section>
            <div class="card">
                Product
            </div>
        </section>
    </div>
    """

    selector = get_selector(
        ".container > .card { color: red; }"
    )

    matcher = CSSMatcher()

    assert not matcher.matches(selector, html)


def test_id_selector_matches():

    html = """
    <section id="contact-section">
        Contact
    </section>
    """

    selector = get_selector(
        "#contact-section { padding: 10px; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_id_selector_does_not_match():

    html = """
    <section id="about-section">
        About
    </section>
    """

    selector = get_selector(
        "#contact-section { padding: 10px; }"
    )

    matcher = CSSMatcher()

    assert not matcher.matches(selector, html)


def test_element_selector_matches():

    html = """
    <button>
        Submit
    </button>
    """

    selector = get_selector(
        "button { cursor: pointer; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_element_and_class_selector():

    html = """
    <button class="primary-btn">
        Submit
    </button>
    """

    selector = get_selector(
        "button.primary-btn { cursor: pointer; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_element_and_class_selector_does_not_match():

    html = """
    <a class="primary-btn">
        Submit
    </a>
    """

    selector = get_selector(
        "button.primary-btn { cursor: pointer; }"
    )

    matcher = CSSMatcher()

    assert not matcher.matches(selector, html)


def test_multiple_classes():

    html = """
    <div class="card featured">
        Product
    </div>
    """

    selector = get_selector(
        ".card.featured { display: block; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_multiple_classes_does_not_match():

    html = """
    <div class="card">
        Product
    </div>
    """

    selector = get_selector(
        ".card.featured { display: block; }"
    )

    matcher = CSSMatcher()

    assert not matcher.matches(selector, html)


def test_attribute_selector():

    html = """
    <input
        type="email"
        class="form-control"
    >
    """

    selector = get_selector(
        'input[type="email"] { width: 100%; }'
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_attribute_selector_does_not_match():

    html = """
    <input
        type="text"
        class="form-control"
    >
    """

    selector = get_selector(
        'input[type="email"] { width: 100%; }'
    )

    matcher = CSSMatcher()

    assert not matcher.matches(selector, html)


def test_attribute_selector_with_class():

    html = """
    <input
        type="email"
        class="form-control"
    >
    """

    selector = get_selector(
        'input.form-control[type="email"] { width: 100%; }'
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_not_selector():

    html = """
    <div class="card">
        Product
    </div>
    """

    selector = get_selector(
        ".card:not(.disabled) { display: block; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_not_selector_does_not_match():

    html = """
    <div class="card disabled">
        Product
    </div>
    """

    selector = get_selector(
        ".card:not(.disabled) { display: block; }"
    )

    matcher = CSSMatcher()

    assert not matcher.matches(selector, html)


def test_is_selector():

    html = """
    <div class="card">
        Product
    </div>
    """

    selector = get_selector(
        ":is(.card, .product) { display: block; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_where_selector():

    html = """
    <div class="container">
        Content
    </div>
    """

    selector = get_selector(
        ":where(.container, .wrapper) { display: block; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_has_selector():

    html = """
    <div class="card">
        <span class="price">
            ₹100
        </span>
    </div>
    """

    selector = get_selector(
        ".card:has(.price) { display: block; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_has_selector_does_not_match():

    html = """
    <div class="card">
        <span class="title">
            Product
        </span>
    </div>
    """

    selector = get_selector(
        ".card:has(.price) { display: block; }"
    )

    matcher = CSSMatcher()

    assert not matcher.matches(selector, html)


def test_adjacent_sibling_selector():

    html = """
    <div class="card">
        Product
    </div>

    <button class="button">
        Buy
    </button>
    """

    selector = get_selector(
        ".card + .button { display: block; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_general_sibling_selector():

    html = """
    <div class="card">
        Product
    </div>

    <div class="spacer">
        Spacer
    </div>

    <button class="button">
        Buy
    </button>
    """

    selector = get_selector(
        ".card ~ .button { display: block; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_complex_selector():

    html = """
    <main id="main" class="container">
        <section class="content">
            <div class="card">
                Product
            </div>
        </section>
    </main>
    """

    selector = get_selector(
        "#main.container > .content .card"
        " { display: block; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)


def test_complex_selector_does_not_match():

    html = """
    <main id="main" class="container">
        <section class="sidebar">
            <div class="card">
                Product
            </div>
        </section>
    </main>
    """

    selector = get_selector(
        "#main.container > .content .card"
        " { display: block; }"
    )

    matcher = CSSMatcher()

    assert not matcher.matches(selector, html)


def test_unused_selector():

    html = """
    <div class="product">
        Product
    </div>
    """

    selector = get_selector(
        ".unused-card { display: block; }"
    )

    matcher = CSSMatcher()

    assert not matcher.matches(selector, html)


def test_empty_html():

    html = ""

    selector = get_selector(
        ".card { display: block; }"
    )

    matcher = CSSMatcher()

    assert not matcher.matches(selector, html)


def test_malformed_html():

    html = """
    <div class="container">
        <div class="card">
            Product
    """

    selector = get_selector(
        ".container .card { display: block; }"
    )

    matcher = CSSMatcher()

    assert matcher.matches(selector, html)