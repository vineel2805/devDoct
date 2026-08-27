"""
Integration tests for CSS usage analysis.

Tests the complete flow:

CSS source
    ↓
CSSScanner / CSSParser
    ↓
CSSScanResult
    ↓
UsageAnalyzer
    ↓
CSSMatcher
    ↓
HTMLScanResult
"""

from pathlib import Path

from scanner.css_scanner import CSSScanner
from scanner.html_scanner import HTMLScanner
from analyzers.usage import UsageAnalyzer


def create_html_file(tmp_path: Path, name: str, content: str) -> Path:
    """Create a temporary HTML file."""

    path = tmp_path / name
    path.write_text(
        content,
        encoding="utf-8"
    )

    return path


def create_css_file(tmp_path: Path, name: str, content: str) -> Path:
    """Create a temporary CSS file."""

    path = tmp_path / name
    path.write_text(
        content,
        encoding="utf-8"
    )

    return path


def analyze_project(
    tmp_path: Path,
    html_content: str,
    css_content: str
):
    """Scan HTML/CSS and run UsageAnalyzer."""

    html_file = create_html_file(
        tmp_path,
        "index.html",
        html_content
    )

    css_file = create_css_file(
        tmp_path,
        "style.css",
        css_content
    )

    html_result = HTMLScanner().scan(
        [html_file],
        tmp_path
    )

    css_result = CSSScanner().scan(
        [css_file]
    )

    usage_result = UsageAnalyzer().analyze(
        html_result,
        css_result
    )

    return usage_result


# ============================================================
# BASIC SELECTOR MATCHING
# ============================================================


def test_class_selector_is_used(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <html>
            <body>
                <div class="card">
                    Product
                </div>
            </body>
        </html>
        """,

        """
        .card {
            padding: 10px;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card"
    )

    assert selector.used
    assert "index.html" in selector.matched_files


def test_class_selector_is_unused(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <html>
            <body>
                <div class="product">
                    Product
                </div>
            </body>
        </html>
        """,

        """
        .card {
            padding: 10px;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card"
    )

    assert not selector.used
    assert selector.matched_files == []


# ============================================================
# ID SELECTOR
# ============================================================


def test_id_selector_is_used(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <section id="contact">
            Contact
        </section>
        """,

        """
        #contact {
            padding: 20px;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == "#contact"
    )

    assert selector.used
    assert "index.html" in selector.matched_files


def test_id_selector_is_unused(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <section id="about">
            About
        </section>
        """,

        """
        #contact {
            padding: 20px;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == "#contact"
    )

    assert not selector.used
    assert selector.matched_files == []


# ============================================================
# DESCENDANT SELECTOR
# ============================================================


def test_descendant_selector_matches(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <div class="container">
            <div class="card">
                Product
            </div>
        </div>
        """,

        """
        .container .card {
            padding: 10px;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".container .card"
    )

    assert selector.used


# ============================================================
# CHILD SELECTOR
# ============================================================


def test_child_selector_matches(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <div class="container">
            <div class="card">
                Product
            </div>
        </div>
        """,

        """
        .container > .card {
            padding: 10px;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".container > .card"
    )

    assert selector.used


def test_child_selector_does_not_match_wrong_structure(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <div class="container">
            <section>
                <div class="card">
                    Product
                </div>
            </section>
        </div>
        """,

        """
        .container > .card {
            padding: 10px;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".container > .card"
    )

    assert not selector.used


# ============================================================
# CRITICAL FALSE-POSITIVE TEST
# ============================================================


def test_existing_classes_do_not_mean_selector_is_used(
    tmp_path
):

    result = analyze_project(
        tmp_path,

        """
        <div class="container">
            <section>
                <div class="card">
                    Product
                </div>
            </section>
        </div>
        """,

        """
        .container > .card {
            padding: 10px;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".container > .card"
    )

    assert not selector.used


# ============================================================
# MULTIPLE SELECTORS
# ============================================================


def test_multiple_selectors_are_analyzed(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <div class="card">
            <button class="btn">
                Buy
            </button>
        </div>
        """,

        """
        .card {
            padding: 10px;
        }

        .btn {
            padding: 5px;
        }

        .unused {
            display: none;
        }
        """
    )

    card = next(
        item
        for item in result.selectors
        if item.selector == ".card"
    )

    btn = next(
        item
        for item in result.selectors
        if item.selector == ".btn"
    )

    unused = next(
        item
        for item in result.selectors
        if item.selector == ".unused"
    )

    assert card.used
    assert btn.used
    assert not unused.used


# ============================================================
# MULTIPLE HTML FILES
# ============================================================


def test_selector_matches_second_html_file(tmp_path):

    html_one = create_html_file(
        tmp_path,
        "index.html",
        """
        <div class="home">
            Home
        </div>
        """
    )

    html_two = create_html_file(
        tmp_path,
        "about.html",
        """
        <div class="card">
            About
        </div>
        """
    )

    css_file = create_css_file(
        tmp_path,
        "style.css",
        """
        .card {
            padding: 10px;
        }
        """
    )

    html_result = HTMLScanner().scan(
        [html_one, html_two],
        tmp_path
    )

    css_result = CSSScanner().scan(
        [css_file]
    )

    result = UsageAnalyzer().analyze(
        html_result,
        css_result
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card"
    )

    assert selector.used
    assert "about.html" in selector.matched_files
    assert "index.html" not in selector.matched_files


# ============================================================
# MULTIPLE HTML FILES MATCHING
# ============================================================


def test_selector_matches_multiple_html_files(tmp_path):

    html_one = create_html_file(
        tmp_path,
        "index.html",
        """
        <div class="card">
            Home
        </div>
        """
    )

    html_two = create_html_file(
        tmp_path,
        "about.html",
        """
        <div class="card">
            About
        </div>
        """
    )

    css_file = create_css_file(
        tmp_path,
        "style.css",
        """
        .card {
            padding: 10px;
        }
        """
    )

    html_result = HTMLScanner().scan(
        [html_one, html_two],
        tmp_path
    )

    css_result = CSSScanner().scan(
        [css_file]
    )

    result = UsageAnalyzer().analyze(
        html_result,
        css_result
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card"
    )

    assert selector.used

    assert "index.html" in selector.matched_files
    assert "about.html" in selector.matched_files


# ============================================================
# ATTRIBUTE SELECTOR
# ============================================================


def test_attribute_selector_matches(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <input
            type="email"
            class="form-control"
        >
        """,

        """
        input[type="email"] {
            width: 100%;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == 'input[type="email"]'
    )

    assert selector.used


# ============================================================
# MULTIPLE CLASSES
# ============================================================


def test_multiple_class_selector_matches(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <div class="card featured">
            Product
        </div>
        """,

        """
        .card.featured {
            border: 1px solid black;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card.featured"
    )

    assert selector.used


def test_multiple_class_selector_fails_when_class_missing(
    tmp_path
):

    result = analyze_project(
        tmp_path,

        """
        <div class="card">
            Product
        </div>
        """,

        """
        .card.featured {
            border: 1px solid black;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card.featured"
    )

    assert not selector.used


# ============================================================
# :NOT()
# ============================================================


def test_not_selector_matches(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <div class="card">
            Product
        </div>
        """,

        """
        .card:not(.disabled) {
            display: block;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card:not(.disabled)"
    )

    assert selector.used


def test_not_selector_does_not_match_excluded_element(
    tmp_path
):

    result = analyze_project(
        tmp_path,

        """
        <div class="card disabled">
            Product
        </div>
        """,

        """
        .card:not(.disabled) {
            display: block;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card:not(.disabled)"
    )

    assert not selector.used


# ============================================================
# :IS()
# ============================================================


def test_is_selector_matches(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <div class="card">
            Product
        </div>
        """,

        """
        :is(.card, .product) {
            display: block;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ":is(.card, .product)"
    )

    assert selector.used


# ============================================================
# :HAS()
# ============================================================


def test_has_selector_matches(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <article class="card">
            <span class="price">
                ₹999
            </span>
        </article>
        """,

        """
        .card:has(.price) {
            display: block;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card:has(.price)"
    )

    assert selector.used


def test_has_selector_does_not_match_without_child(
    tmp_path
):

    result = analyze_project(
        tmp_path,

        """
        <article class="card">
            Product
        </article>
        """,

        """
        .card:has(.price) {
            display: block;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card:has(.price)"
    )

    assert not selector.used


# ============================================================
# SIBLING SELECTORS
# ============================================================


def test_adjacent_sibling_selector_matches(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <h2>Title</h2>
        <p class="description">
            Description
        </p>
        """,

        """
        h2 + .description {
            margin-top: 10px;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == "h2 + .description"
    )

    assert selector.used


def test_general_sibling_selector_matches(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <h2>Title</h2>
        <div></div>
        <p class="description">
            Description
        </p>
        """,

        """
        h2 ~ .description {
            margin-top: 10px;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == "h2 ~ .description"
    )

    assert selector.used


# ============================================================
# MEDIA QUERY
# ============================================================


def test_media_query_selector_is_analyzed(tmp_path):

    result = analyze_project(
        tmp_path,

        """
        <div class="mobile-menu">
            Menu
        </div>
        """,

        """
        @media (max-width: 768px) {

            .mobile-menu {
                display: block;
            }
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".mobile-menu"
    )

    assert selector.used


# ============================================================
# EMPTY HTML
# ============================================================


def test_empty_html_produces_unused_selector(tmp_path):

    result = analyze_project(
        tmp_path,
        "",
        """
        .card {
            display: block;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card"
    )

    assert not selector.used
    assert selector.matched_files == []


# ============================================================
# SELECTOR SOURCE INFORMATION
# ============================================================


def test_selector_source_information_is_preserved(
    tmp_path
):

    result = analyze_project(
        tmp_path,

        """
        <div class="card">
            Product
        </div>
        """,

        """
        
        .card {
            padding: 10px;
        }
        """
    )

    selector = next(
        item
        for item in result.selectors
        if item.selector == ".card"
    )

    assert selector.source_line > 0
    assert selector.source_column > 0