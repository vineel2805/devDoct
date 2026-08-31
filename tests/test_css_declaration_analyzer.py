from analyzers.css_declaration import CSSDeclarationAnalyzer
from models.css_declaration import CSSDeclaration
from models.css_rule import CSSRule
from parsers.css_parser import CSSParser

def test_analyzer_finds_important_declaration():

    rule = CSSRule(
        selectors=[".card"],
        declarations=[
            CSSDeclaration(
                property="color",
                value="red",
                important=True,
                source_line=3,
                source_column=9
            )
        ],
        source_line=2,
        source_column=5
    )

    result = CSSDeclarationAnalyzer().analyze(
        [rule]
    )

    assert len(result) == 1

    finding = result[0]

    assert finding.selector == ".card"
    assert finding.property == "color"
    assert finding.value == "red"
    assert finding.issue == "important_declaration"
def test_analyzer_ignores_normal_declaration():

    rule = CSSRule(
        selectors=[".card"],
        declarations=[
            CSSDeclaration(
                property="color",
                value="red",
                source_line=3,
                source_column=9
            )
        ]
    )

    result = CSSDeclarationAnalyzer().analyze(
        [rule]
    )

    assert result == []



def test_analyzer_finds_multiple_important_declarations():

    rule = CSSRule(
        selectors=[".card"],
        declarations=[
            CSSDeclaration(
                property="color",
                value="red",
                important=True,
                source_line=3,
                source_column=9
            ),
            CSSDeclaration(
                property="padding",
                value="20px",
                source_line=4,
                source_column=9
            ),
            CSSDeclaration(
                property="display",
                value="flex",
                important=True,
                source_line=5,
                source_column=9
            )
        ]
    )

    result = CSSDeclarationAnalyzer().analyze(
        [rule]
    )

    assert len(result) == 2

    assert result[0].selector == ".card"
    assert result[0].property == "color"

    assert result[1].selector == ".card"
    assert result[1].property == "display"


def test_analyzer_finding_includes_selector():

    rule = CSSRule(
        selectors=[".card"],
        declarations=[
            CSSDeclaration(
                property="color",
                value="red",
                important=True,
                source_line=3,
                source_column=9
            )
        ],
        source_line=2,
        source_column=5
    )

    result = CSSDeclarationAnalyzer().analyze(
        [rule]
    )

    assert len(result) == 1

    finding = result[0]

    assert finding.selector == ".card"
    assert finding.property == "color"
    assert finding.value == "red"
    assert finding.issue == "important_declaration"
def test_analyzer_finds_duplicate_property():

    rule = CSSRule(
        selectors=[".card"],
        declarations=[
            CSSDeclaration(
                property="color",
                value="red",
                source_line=3,
                source_column=9
            ),
            CSSDeclaration(
                property="color",
                value="blue",
                source_line=4,
                source_column=9
            )
        ]
    )

    result = CSSDeclarationAnalyzer().analyze(
        [rule]
    )

    assert len(result) == 1

    finding = result[0]

    assert finding.selector == ".card"
    assert finding.property == "color"
    assert finding.source_line == 4
    assert finding.issue == "conflicting_declaration"
def test_analyzer_does_not_flag_property_in_different_rules():

    rules = [
        CSSRule(
            selectors=[".card"],
            declarations=[
                CSSDeclaration(
                    property="color",
                    value="red",
                    source_line=3,
                    source_column=9
                )
            ]
        ),
        CSSRule(
            selectors=[".button"],
            declarations=[
                CSSDeclaration(
                    property="color",
                    value="blue",
                    source_line=7,
                    source_column=9
                )
            ]
        )
    ]

    result = CSSDeclarationAnalyzer().analyze(rules)

    assert result == []
def test_analyzer_detects_identical_duplicate_declaration():

    rule = CSSRule(
        selectors=[".card"],
        declarations=[
            CSSDeclaration(
                property="color",
                value="red",
                source_line=3,
                source_column=9
            ),
            CSSDeclaration(
                property="color",
                value="red",
                source_line=4,
                source_column=9
            )
        ]
    )

    result = CSSDeclarationAnalyzer().analyze(
        [rule]
    )

    assert len(result) == 1

    finding = result[0]

    assert finding.selector == ".card"
    assert finding.property == "color"
    assert finding.value == "red"
    assert finding.source_line == 4
def test_analyzer_reports_only_one_finding_for_identical_duplicate():

    rule = CSSRule(
        selectors=[".card"],
        declarations=[
            CSSDeclaration(
                property="color",
                value="red",
                source_line=3,
                source_column=9
            ),
            CSSDeclaration(
                property="color",
                value="red",
                source_line=4,
                source_column=9
            )
        ]
    )

    result = CSSDeclarationAnalyzer().analyze([rule])

    assert len(result) == 1



def test_parser_preserves_important_flag():

    css = """
    .card {
        color: red !important;
    }
    """

    result = CSSParser().parse(css)

    declaration = result.declarations[0]

    assert declaration.important is True


def test_parser_marks_normal_declaration_as_not_important():

    css = """
    .card {
        color: red;
    }
    """

    result = CSSParser().parse(css)

    declaration = result.declarations[0]

    assert declaration.important is False

def test_analyzer_finding_identifies_issue_type():

    rule = CSSRule(
        selectors=[".card"],
        declarations=[
            CSSDeclaration(
                property="color",
                value="red !important",
                important=True,
                source_line=3,
                source_column=9
            )
        ]
    )

    result = CSSDeclarationAnalyzer().analyze([rule])

    assert len(result) == 1
    assert result[0].issue == "important_declaration"
def test_analyzer_distinguishes_identical_duplicate_declaration():

    rule = CSSRule(
        selectors=[".card"],
        declarations=[
            CSSDeclaration(
                property="color",
                value="red",
                source_line=3,
                source_column=9
            ),
            CSSDeclaration(
                property="color",
                value="red",
                source_line=4,
                source_column=9
            )
        ]
    )

    result = CSSDeclarationAnalyzer().analyze([rule])

    assert len(result) == 1

    finding = result[0]

    assert finding.issue == "duplicate_declaration"
    assert finding.property == "color"
    assert finding.value == "red"
    assert finding.source_line == 4
def test_analyzer_identifies_conflicting_declaration():

    rule = CSSRule(
        selectors=[".card"],
        declarations=[
            CSSDeclaration(
                property="display",
                value="block",
                source_line=3,
                source_column=9
            ),
            CSSDeclaration(
                property="display",
                value="flex",
                source_line=4,
                source_column=9
            )
        ]
    )

    result = CSSDeclarationAnalyzer().analyze([rule])

    assert len(result) == 1

    finding = result[0]

    assert finding.selector == ".card"
    assert finding.property == "display"
    assert finding.value == "flex"
    assert finding.issue == "conflicting_declaration"
    assert finding.source_line == 4