"""
Tests for CSS selector source information.
"""

from pathlib import Path

from models.html_result import HTMLScanResult, FileHTMLResult
from models.css_result import CSSScanResult, FileCSSResult
from parsers.css_parser import CSSParser
from analyzers.usage import UsageAnalyzer


def build_html(files: dict[str, str]) -> HTMLScanResult:
    """
    Build an HTMLScanResult from filename -> HTML source.
    """

    result = HTMLScanResult(root=Path("."))

    for filename, document in files.items():

        file_path = Path(filename)

        file_result = FileHTMLResult(
            document=document
        )

        result.files[file_path] = file_result

    return result


def build_css(files: dict[str, str]) -> CSSScanResult:
    """
    Build a CSSScanResult from filename -> CSS source.
    """

    result = CSSScanResult()

    parser = CSSParser()

    for filename, source in files.items():

        parsed = parser.parse(source)

        file_path = Path(filename)

        file_result = FileCSSResult()

        file_result.classes = parsed.classes
        file_result.ids = parsed.ids
        file_result.elements = parsed.elements
        file_result.total_rules = parsed.total_rules
        file_result.selectors = parsed.selectors

        result.files[file_path] = file_result

        result.classes.update(parsed.classes)
        result.ids.update(parsed.ids)
        result.elements.update(parsed.elements)

    return result


def test_selector_source_line_is_preserved():
    """
    CSS selector should retain its original source line.
    """

    css = """
    /* comment */

    .card {
        padding: 10px;
    }
    """

    html = {
        "index.html": """
        <div class="card"></div>
        """
    }

    css_result = build_css({
        "style.css": css
    })

    html_result = build_html(html)

    result = UsageAnalyzer().analyze(
        html_result,
        css_result
    )

    assert len(result.selectors) == 1

    selector = result.selectors[0]

    assert selector.selector == ".card"
    assert selector.used is True
    assert selector.source_line > 0


def test_selector_source_column_is_preserved():

    css = """
.card {
    padding: 10px;
}
"""

    css_result = build_css({
        "style.css": css
    })

    html_result = build_html({
        "index.html": '<div class="card"></div>'
    })

    result = UsageAnalyzer().analyze(
        html_result,
        css_result
    )

    selector = result.selectors[0]

    assert selector.source_line > 0
    assert selector.source_column >= 0


def test_unused_selector_preserves_source_information():

    css = """
.header {
    display: block;
}

.unused-card {
    display: none;
}
"""

    css_result = build_css({
        "style.css": css
    })

    html_result = build_html({
        "index.html": '<div class="header"></div>'
    })

    result = UsageAnalyzer().analyze(
        html_result,
        css_result
    )

    assert len(result.selectors) == 2

    unused = next(
        selector
        for selector in result.selectors
        if selector.selector == ".unused-card"
    )

    assert unused.used is False
    assert unused.source_line > 0
    assert unused.source_column >= 0


def test_multiple_css_files_preserve_selector_sources():

    css_result = build_css({
        "header.css": """
        .header {
            display: flex;
        }
        """,

        "footer.css": """
        .footer {
            display: block;
        }
        """
    })

    html_result = build_html({
        "index.html": """
        <header class="header"></header>
        <footer class="footer"></footer>
        """
    })

    result = UsageAnalyzer().analyze(
        html_result,
        css_result
    )

    assert len(result.selectors) == 2

    selectors = {
        selector.selector
        for selector in result.selectors
    }

    assert ".header" in selectors
    assert ".footer" in selectors


def test_selector_order_is_preserved():

    css = """
.first {
    color: red;
}

.second {
    color: blue;
}

.third {
    color: green;
}
"""

    css_result = build_css({
        "style.css": css
    })

    html_result = build_html({
        "index.html": """
        <div class="first"></div>
        <div class="second"></div>
        <div class="third"></div>
        """
    })

    result = UsageAnalyzer().analyze(
        html_result,
        css_result
    )

    selectors = [
        selector.selector
        for selector in result.selectors
    ]

    assert selectors == [
        ".first",
        ".second",
        ".third",
    ]


def test_duplicate_selector_is_analyzed_separately():

    css = """
.card {
    padding: 10px;
}

.card {
    margin: 10px;
}
"""

    css_result = build_css({
        "style.css": css
    })

    html_result = build_html({
        "index.html": '<div class="card"></div>'
    })

    result = UsageAnalyzer().analyze(
        html_result,
        css_result
    )

    assert len(result.selectors) == 2

    assert all(
        selector.used
        for selector in result.selectors
    )

    assert all(
        selector.selector == ".card"
        for selector in result.selectors
    )