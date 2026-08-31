from analyzers.css_rule import CSSRuleAnalyzer
from models.css_declaration import CSSDeclaration
from models.css_rule import CSSRule


def test_analyzer_finds_duplicate_rule():

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
            ],
            source_line=2,
            source_column=5
        ),
        CSSRule(
            selectors=[".card"],
            declarations=[
                CSSDeclaration(
                    property="color",
                    value="red",
                    source_line=8,
                    source_column=9
                )
            ],
            source_line=7,
            source_column=5
        )
    ]

    result = CSSRuleAnalyzer().analyze(rules)

    assert len(result) == 1

    finding = result[0]

    assert finding.selector == ".card"
    assert finding.issue == "duplicate_rule"
    assert finding.source_line == 7


def test_analyzer_does_not_flag_different_rules():

    rules = [
        CSSRule(
            selectors=[".card"],
            declarations=[
                CSSDeclaration(
                    property="color",
                    value="red"
                )
            ]
        ),
        CSSRule(
            selectors=[".card"],
            declarations=[
                CSSDeclaration(
                    property="color",
                    value="blue"
                )
            ]
        )
    ]

    result = CSSRuleAnalyzer().analyze(rules)

    assert result == []