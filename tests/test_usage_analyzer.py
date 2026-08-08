"""
Tests for UsageAnalyzer.

Tests:
- Used classes
- Unused classes
- Missing classes
- Used IDs
- Unused IDs
- Missing IDs
- Empty inputs
- Complete overlap
- No overlap
- Duplicate values
- Input immutability
"""

from pathlib import Path

from analyzers.usage import UsageAnalyzer
from models.html_result import HTMLScanResult
from models.css_result import CSSScanResult


def make_html(classes=None, ids=None):
    """Create an HTMLScanResult for testing."""

    return HTMLScanResult(
        root=Path("."),
        classes=set(classes or []),
        ids=set(ids or []),
    )


def make_css(classes=None, ids=None):
    """Create a CSSScanResult for testing."""

    return CSSScanResult(
        classes=set(classes or []),
        ids=set(ids or []),
    )


# ============================================================
# BASIC CLASS TESTS
# ============================================================


def test_used_classes():
    html = make_html(
        classes={"card", "button", "header"}
    )

    css = make_css(
        classes={"card", "button", "footer"}
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_classes == {
        "card",
        "button",
    }


def test_unused_classes():
    html = make_html(
        classes={"card", "button"}
    )

    css = make_css(
        classes={"card", "button", "footer", "sidebar"}
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.unused_classes == {
        "footer",
        "sidebar",
    }


def test_missing_classes():
    html = make_html(
        classes={"card", "button", "header"}
    )

    css = make_css(
        classes={"card", "button"}
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.missing_classes == {
        "header",
    }


# ============================================================
# BASIC ID TESTS
# ============================================================


def test_used_ids():
    html = make_html(
        ids={"header", "content", "footer"}
    )

    css = make_css(
        ids={"header", "content", "sidebar"}
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_ids == {
        "header",
        "content",
    }


def test_unused_ids():
    html = make_html(
        ids={"header", "content"}
    )

    css = make_css(
        ids={"header", "content", "sidebar", "modal"}
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.unused_ids == {
        "sidebar",
        "modal",
    }


def test_missing_ids():
    html = make_html(
        ids={"header", "content", "footer"}
    )

    css = make_css(
        ids={"header", "content"}
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.missing_ids == {
        "footer",
    }


# ============================================================
# COMPLETE ANALYSIS
# ============================================================


def test_complete_analysis():
    html = make_html(
        classes={
            "card",
            "button",
            "header",
        },
        ids={
            "main",
            "footer",
        },
    )

    css = make_css(
        classes={
            "card",
            "button",
            "sidebar",
        },
        ids={
            "main",
            "modal",
        },
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_classes == {
        "card",
        "button",
    }

    assert result.unused_classes == {
        "sidebar",
    }

    assert result.missing_classes == {
        "header",
    }

    assert result.used_ids == {
        "main",
    }

    assert result.unused_ids == {
        "modal",
    }

    assert result.missing_ids == {
        "footer",
    }


# ============================================================
# EMPTY INPUTS
# ============================================================


def test_empty_html_and_css():
    html = make_html()
    css = make_css()

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_classes == set()
    assert result.unused_classes == set()
    assert result.missing_classes == set()

    assert result.used_ids == set()
    assert result.unused_ids == set()
    assert result.missing_ids == set()


def test_empty_html():
    html = make_html()

    css = make_css(
        classes={"card", "button"},
        ids={"main", "footer"},
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_classes == set()
    assert result.unused_classes == {
        "card",
        "button",
    }
    assert result.missing_classes == set()

    assert result.used_ids == set()
    assert result.unused_ids == {
        "main",
        "footer",
    }
    assert result.missing_ids == set()


def test_empty_css():
    html = make_html(
        classes={"card", "button"},
        ids={"main", "footer"},
    )

    css = make_css()

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_classes == set()
    assert result.unused_classes == set()
    assert result.missing_classes == {
        "card",
        "button",
    }

    assert result.used_ids == set()
    assert result.unused_ids == set()
    assert result.missing_ids == {
        "main",
        "footer",
    }


# ============================================================
# COMPLETE OVERLAP
# ============================================================


def test_everything_is_used():
    html = make_html(
        classes={"card", "button"},
        ids={"main", "footer"},
    )

    css = make_css(
        classes={"card", "button"},
        ids={"main", "footer"},
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_classes == {
        "card",
        "button",
    }

    assert result.unused_classes == set()
    assert result.missing_classes == set()

    assert result.used_ids == {
        "main",
        "footer",
    }

    assert result.unused_ids == set()
    assert result.missing_ids == set()


# ============================================================
# NO OVERLAP
# ============================================================


def test_nothing_matches():
    html = make_html(
        classes={"html-card", "html-button"},
        ids={"html-main", "html-footer"},
    )

    css = make_css(
        classes={"css-card", "css-button"},
        ids={"css-main", "css-footer"},
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_classes == set()

    assert result.unused_classes == {
        "css-card",
        "css-button",
    }

    assert result.missing_classes == {
        "html-card",
        "html-button",
    }

    assert result.used_ids == set()

    assert result.unused_ids == {
        "css-main",
        "css-footer",
    }

    assert result.missing_ids == {
        "html-main",
        "html-footer",
    }


# ============================================================
# DUPLICATE VALUES
# ============================================================


def test_duplicate_classes_are_handled():
    html = make_html(
        classes=[
            "card",
            "card",
            "button",
            "button",
        ]
    )

    css = make_css(
        classes=[
            "card",
            "card",
            "button",
        ]
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_classes == {
        "card",
        "button",
    }

    assert result.unused_classes == set()
    assert result.missing_classes == set()


def test_duplicate_ids_are_handled():
    html = make_html(
        ids=[
            "main",
            "main",
            "footer",
        ]
    )

    css = make_css(
        ids=[
            "main",
            "main",
        ]
    )

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_ids == {
        "main",
    }

    assert result.unused_ids == set()

    assert result.missing_ids == {
        "footer",
    }


# ============================================================
# INPUT IMMUTABILITY
# ============================================================


def test_analyzer_does_not_modify_html_or_css():
    html_classes = {
        "card",
        "button",
        "header",
    }

    html_ids = {
        "main",
        "footer",
    }

    css_classes = {
        "card",
        "button",
        "sidebar",
    }

    css_ids = {
        "main",
        "modal",
    }

    html = make_html(
        classes=html_classes,
        ids=html_ids,
    )

    css = make_css(
        classes=css_classes,
        ids=css_ids,
    )

    UsageAnalyzer().analyze(html, css)

    assert html.classes == html_classes
    assert html.ids == html_ids

    assert css.classes == css_classes
    assert css.ids == css_ids


# ============================================================
# RESULT SET INDEPENDENCE
# ============================================================


def test_result_sets_are_independent_from_input():
    html = make_html(
        classes={"card", "button"},
        ids={"main"},
    )

    css = make_css(
        classes={"card", "sidebar"},
        ids={"main", "modal"},
    )

    result = UsageAnalyzer().analyze(html, css)

    result.used_classes.add("fake")

    result.unused_classes.add("fake")

    result.missing_classes.add("fake")

    result.used_ids.add("fake")

    result.unused_ids.add("fake")

    result.missing_ids.add("fake")

    assert "fake" not in html.classes
    assert "fake" not in html.ids

    assert "fake" not in css.classes
    assert "fake" not in css.ids


# ============================================================
# SINGLE VALUE CASES
# ============================================================


def test_single_matching_class():
    html = make_html(classes={"card"})
    css = make_css(classes={"card"})

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_classes == {"card"}
    assert result.unused_classes == set()
    assert result.missing_classes == set()


def test_single_unused_css_class():
    html = make_html(classes=set())
    css = make_css(classes={"card"})

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_classes == set()
    assert result.unused_classes == {"card"}
    assert result.missing_classes == set()


def test_single_missing_css_class():
    html = make_html(classes={"card"})
    css = make_css(classes=set())

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_classes == set()
    assert result.unused_classes == set()
    assert result.missing_classes == {"card"}


def test_single_matching_id():
    html = make_html(ids={"main"})
    css = make_css(ids={"main"})

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_ids == {"main"}
    assert result.unused_ids == set()
    assert result.missing_ids == set()


def test_single_unused_css_id():
    html = make_html(ids=set())
    css = make_css(ids={"main"})

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_ids == set()
    assert result.unused_ids == {"main"}
    assert result.missing_ids == set()


def test_single_missing_css_id():
    html = make_html(ids={"main"})
    css = make_css(ids=set())

    result = UsageAnalyzer().analyze(html, css)

    assert result.used_ids == set()
    assert result.unused_ids == set()
    assert result.missing_ids == {"main"}