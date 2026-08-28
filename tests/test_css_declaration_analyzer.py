from analyzers.css_declaration import CSSDeclarationAnalyzer
from models.css_declaration import CSSDeclaration
from models.css_rule import CSSRule


def test_analyzer_finds_important_declaration():

    rule = CSSRule(
        selectors=[".card"],
        declarations=[
            CSSDeclaration(
                property="color",
                value="red !important",
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
    assert finding.value == "red !important"
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
                value="red !important",
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
                value="flex !important",
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
                value="red !important",
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
    assert finding.value == "red !important"