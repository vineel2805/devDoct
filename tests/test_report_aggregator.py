from pathlib import Path

from models.css_declaration_finding import CSSDeclarationFinding
from reports.aggregator import ReportAggregator


def make_finding(
    file: Path,
    issue: str,
    line: int = 1,
):
    return CSSDeclarationFinding(
        file=file,
        selectors=[".card"],
        property="color",
        value="red",
        issue=issue,
        source_line=line,
        source_column=5,
    )


def test_aggregator_groups_findings_by_file():

    file_a = Path("css/header.css")
    file_b = Path("css/cards.css")

    findings = [
        make_finding(
            file_a,
            "duplicate_declaration",
            10,
        ),
        make_finding(
            file_a,
            "important_declaration",
            20,
        ),
        make_finding(
            file_b,
            "conflicting_declaration",
            30,
        ),
    ]

    aggregator = ReportAggregator(findings)

    result = aggregator.findings_by_file()

    assert result[file_a] == [
        findings[0],
        findings[1],
    ]

    assert result[file_b] == [
        findings[2],
    ]


def test_aggregator_groups_findings_by_issue():

    file_a = Path("css/header.css")

    findings = [
        make_finding(
            file_a,
            "duplicate_declaration",
            10,
        ),
        make_finding(
            file_a,
            "duplicate_declaration",
            20,
        ),
        make_finding(
            file_a,
            "important_declaration",
            30,
        ),
    ]

    aggregator = ReportAggregator(findings)

    result = aggregator.findings_by_issue()

    assert result["duplicate_declaration"] == [
        findings[0],
        findings[1],
    ]

    assert result["important_declaration"] == [
        findings[2],
    ]


def test_aggregator_counts_findings_per_file():

    file_a = Path("css/header.css")
    file_b = Path("css/cards.css")

    findings = [
        make_finding(
            file_a,
            "duplicate_declaration",
        ),
        make_finding(
            file_a,
            "important_declaration",
        ),
        make_finding(
            file_a,
            "conflicting_declaration",
        ),
        make_finding(
            file_b,
            "duplicate_rule",
        ),
    ]

    aggregator = ReportAggregator(findings)

    result = aggregator.file_finding_counts()

    assert result[file_a] == 3
    assert result[file_b] == 1


def test_aggregator_sorts_files_by_finding_count():

    file_a = Path("css/header.css")
    file_b = Path("css/cards.css")
    file_c = Path("css/footer.css")

    findings = [
        make_finding(file_a, "duplicate_declaration"),
        make_finding(file_a, "important_declaration"),

        make_finding(file_b, "conflicting_declaration"),
        make_finding(file_b, "duplicate_rule"),
        make_finding(file_b, "important_declaration"),

        make_finding(file_c, "duplicate_declaration"),
    ]

    aggregator = ReportAggregator(findings)

    result = aggregator.file_finding_counts()

    assert list(result.items()) == [
        (file_b, 3),
        (file_a, 2),
        (file_c, 1),
    ]


def test_aggregator_handles_empty_findings():

    aggregator = ReportAggregator([])

    assert aggregator.findings_by_file() == {}
    assert aggregator.findings_by_issue() == {}
    assert aggregator.file_finding_counts() == {}