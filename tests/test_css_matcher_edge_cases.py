"""
Hard/production-oriented CSS matcher tests.

These tests target selector combinations and edge cases
commonly encountered in larger web projects.
"""

from analyzers.css_matcher import CSSMatcher
from parsers.css_parser import CSSParser


def get_selector(css: str, index: int = 0):

    result = CSSParser().parse(css)

    assert result.invalid_selectors == 0
    assert len(result.selectors) > index

    return result.selectors[index]


def matcher_matches(css: str, html: str, index: int = 0):

    selector = get_selector(css, index)

    return CSSMatcher().matches(
        selector,
        html
    )


# ============================================================
# Deep combinators
# ============================================================


def test_deep_descendant_selector():

    html = """
    <main class="page">
        <section class="content">
            <div class="container">
                <article class="card">
                    <h2 class="title">
                        Product
                    </h2>
                </article>
            </div>
        </section>
    </main>
    """

    css = """
    .page .content .container .card .title {
        color: black;
    }
    """

    assert matcher_matches(css, html)


def test_deep_selector_wrong_structure():

    html = """
    <main class="page">
        <section class="sidebar">
            <div class="container">
                <article class="card">
                    <h2 class="title">
                        Product
                    </h2>
                </article>
            </div>
        </section>
    </main>
    """

    css = """
    .page .content .container .card .title {
        color: black;
    }
    """

    assert not matcher_matches(css, html)


# ============================================================
# Multiple combinators
# ============================================================


def test_complex_combinator_chain():

    html = """
    <div class="container">
        <section class="content">
            <div class="card">
                <button class="buy-button">
                    Buy
                </button>
            </div>
        </section>
    </div>
    """

    css = """
    .container > .content .card > .buy-button {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_adjacent_sibling():

    html = """
    <div class="card">
        Product
    </div>

    <button class="buy-button">
        Buy
    </button>
    """

    css = """
    .card + .buy-button {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_adjacent_sibling_wrong_order():

    html = """
    <button class="buy-button">
        Buy
    </button>

    <div class="card">
        Product
    </div>
    """

    css = """
    .card + .buy-button {
        display: block;
    }
    """

    assert not matcher_matches(css, html)


def test_general_sibling_with_intermediate_elements():

    html = """
    <div class="card">
        Product
    </div>

    <span>
        Separator
    </span>

    <button class="buy-button">
        Buy
    </button>
    """

    css = """
    .card ~ .buy-button {
        display: block;
    }
    """

    assert matcher_matches(css, html)


# ============================================================
# Multiple classes / IDs
# ============================================================


def test_multiple_classes_and_id():

    html = """
    <div
        id="product"
        class="card featured active"
    >
        Product
    </div>
    """

    css = """
    #product.card.featured.active {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_multiple_classes_missing_one():

    html = """
    <div
        id="product"
        class="card featured"
    >
        Product
    </div>
    """

    css = """
    #product.card.featured.active {
        display: block;
    }
    """

    assert not matcher_matches(css, html)


# ============================================================
# :not()
# ============================================================


def test_multiple_not_conditions():

    html = """
    <div class="card">
        Product
    </div>
    """

    css = """
    .card:not(.disabled):not(.hidden) {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_multiple_not_conditions_fail():

    html = """
    <div class="card disabled">
        Product
    </div>
    """

    css = """
    .card:not(.disabled):not(.hidden) {
        display: block;
    }
    """

    assert not matcher_matches(css, html)


# ============================================================
# :is() / :where()
# ============================================================


def test_is_selector_with_multiple_options():

    html = """
    <div class="product-card">
        Product
    </div>
    """

    css = """
    :is(.card, .product-card, .item) {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_is_selector_no_option_matches():

    html = """
    <div class="product">
        Product
    </div>
    """

    css = """
    :is(.card, .product-card, .item) {
        display: block;
    }
    """

    assert not matcher_matches(css, html)


def test_where_selector_with_complex_options():

    html = """
    <section class="container">
        <div class="card">
            Product
        </div>
    </section>
    """

    css = """
    :where(.container, .wrapper) .card {
        display: block;
    }
    """

    assert matcher_matches(css, html)


# ============================================================
# :has()
# ============================================================


def test_has_direct_child():

    html = """
    <article class="card">
        <span class="price">
            ₹999
        </span>
    </article>
    """

    css = """
    .card:has(> .price) {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_has_nested_descendant():

    html = """
    <article class="card">
        <div class="content">
            <span class="price">
                ₹999
            </span>
        </div>
    </article>
    """

    css = """
    .card:has(.content .price) {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_has_wrong_descendant():

    html = """
    <article class="card">
        <div class="content">
            <span class="title">
                Product
            </span>
        </div>
    </article>
    """

    css = """
    .card:has(.content .price) {
        display: block;
    }
    """

    assert not matcher_matches(css, html)


# ============================================================
# Attribute selectors
# ============================================================


def test_attribute_equals():

    html = """
    <input name="username">
    """

    css = """
    input[name="username"] {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_attribute_prefix():

    html = """
    <input name="user-email">
    """

    css = """
    input[name^="user"] {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_attribute_suffix():

    html = """
    <input name="email">
    """

    css = """
    input[name$="mail"] {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_attribute_contains():

    html = """
    <input class="form-control-large">
    """

    css = """
    input[class*="form-control"] {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_attribute_word_match():

    html = """
    <div class="card featured">
        Product
    </div>
    """

    css = """
    div[class~="featured"] {
        display: block;
    }
    """

    assert matcher_matches(css, html)


# ============================================================
# Pseudo classes
# ============================================================


def test_first_child():

    html = """
    <div class="container">
        <div class="card">
            First
        </div>

        <div class="card">
            Second
        </div>
    </div>
    """

    css = """
    .card:first-child {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_last_child():

    html = """
    <div class="container">
        <div class="card">
            First
        </div>

        <div class="card">
            Last
        </div>
    </div>
    """

    css = """
    .card:last-child {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_nth_child():

    html = """
    <ul>
        <li class="item">One</li>
        <li class="item">Two</li>
        <li class="item">Three</li>
    </ul>
    """

    css = """
    .item:nth-child(2) {
        display: block;
    }
    """

    assert matcher_matches(css, html)


# ============================================================
# Pseudo elements
# ============================================================


def test_pseudo_element():

    html = """
    <div class="card">
        Product
    </div>
    """

    css = """
    .card::before {
        content: "";
    }
    """

    assert matcher_matches(css, html)


# ============================================================
# Universal selectors
# ============================================================


def test_universal_selector_with_class():

    html = """
    <div class="card">
        Product
    </div>
    """

    css = """
    *.card {
        display: block;
    }
    """

    assert matcher_matches(css, html)


# ============================================================
# Complex selector lists
# ============================================================


def test_complex_selector_list_second_selector_matches():

    html = """
    <button class="primary-button">
        Buy
    </button>
    """

    css = """
    .card,
    .product,
    button.primary-button {
        display: block;
    }
    """

    assert matcher_matches(css, html, index=2)


def test_complex_selector_list_no_selector_matches():

    html = """
    <div class="other">
        Product
    </div>
    """

    css = """
    .card,
    .product,
    button.primary-button {
        display: block;
    }
    """

    assert not matcher_matches(css, html, index=0)


# ============================================================
# HTML structure edge cases
# ============================================================


def test_same_class_multiple_elements():

    html = """
    <div class="card">One</div>
    <div class="card">Two</div>
    <div class="card">Three</div>
    """

    css = """
    .card {
        display: block;
    }
    """

    assert matcher_matches(css, html)


def test_class_on_wrong_element():

    html = """
    <span class="button">
        Click
    </span>
    """

    css = """
    button.button {
        display: block;
    }
    """

    assert not matcher_matches(css, html)


def test_nested_same_class():

    html = """
    <div class="card">
        <div class="card">
            Inner
        </div>
    </div>
    """

    css = """
    .card .card {
        display: block;
    }
    """

    assert matcher_matches(css, html)


# ============================================================
# HTML comments / irrelevant nodes
# ============================================================


def test_comment_does_not_match_selector():

    html = """
    <!--
        <div class="card"></div>
    -->

    <div class="product">
        Product
    </div>
    """

    css = """
    .card {
        display: block;
    }
    """

    assert not matcher_matches(css, html)


# ============================================================
# Case sensitivity
# ============================================================


def test_class_case_sensitivity():

    html = """
    <div class="Card">
        Product
    </div>
    """

    css = """
    .card {
        display: block;
    }
    """

    assert not matcher_matches(css, html)


# ============================================================
# Multiple matching possibilities
# ============================================================


def test_selector_matches_any_element():

    html = """
    <div class="product">
        One
    </div>

    <div class="card">
        Two
    </div>

    <div class="product">
        Three
    </div>
    """

    css = """
    .card {
        display: block;
    }
    """

    assert matcher_matches(css, html)


# ============================================================
# Deep real-world selector
# ============================================================


def test_real_world_product_selector():

    html = """
    <main id="shop" class="page">

        <section class="products">

            <div class="product-grid">

                <article class="product-card featured">

                    <div class="product-image">
                        <img
                            src="product.jpg"
                            alt="Product"
                        >
                    </div>

                    <div class="product-content">

                        <h2 class="product-title">
                            Product
                        </h2>

                        <span class="product-price">
                            ₹999
                        </span>

                        <button class="add-to-cart">
                            Add
                        </button>

                    </div>

                </article>

            </div>

        </section>

    </main>
    """

    css = """
    #shop.page
    .products
    .product-grid
    .product-card.featured
    .product-content
    .add-to-cart {
        display: block;
    }
    """

    assert matcher_matches(css, html)