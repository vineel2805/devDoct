from pathlib import Path

from models.css_declaration_finding import CSSDeclarationFinding
from reports.aggregator import ReportAggregator
from reports.terminal import TerminalReport


def make_finding(
    file: Path,
    issue: str,
    line: int = 10,
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


def test_terminal_report_shows_files_by_finding_count(capsys):

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
            file_b,
            "conflicting_declaration",
        ),
    ]

    aggregator = ReportAggregator(findings)

    report = TerminalReport()

    report.show_file_analysis(
        aggregator
    )

    output = capsys.readouterr().out

    assert "CSS FILE ANALYSIS" in output
    assert "css/header.css" in output
    assert "css/cards.css" in output

    assert output.index(
        "css/header.css"
    ) < output.index(
        "css/cards.css"
    )


def test_terminal_report_shows_finding_count_per_file(
    capsys,
):

    file_a = Path("css/admin.css")

    findings = [
        make_finding(
            file_a,
            "duplicate_declaration",
        ),
        make_finding(
            file_a,
            "conflicting_declaration",
        ),
        make_finding(
            file_a,
            "important_declaration",
        ),
    ]

    aggregator = ReportAggregator(findings)

    report = TerminalReport()

    report.show_file_analysis(
        aggregator
    )

    output = capsys.readouterr().out

    assert "css/admin.css" in output
    assert "3" in output


def test_terminal_report_shows_findings_by_issue(
    capsys,
):

    file_a = Path("css/admin.css")

    findings = [
        make_finding(
            file_a,
            "duplicate_declaration",
        ),
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
    ]

    aggregator = ReportAggregator(findings)

    report = TerminalReport()

    report.show_issue_analysis(
        aggregator
    )

    output = capsys.readouterr().out

    assert "FINDINGS BY TYPE" in output

    assert "Duplicate declarations" in output
    assert "2" in output

    assert "Important declarations" in output
    assert "1" in output

    assert "Conflicting declarations" in output
    assert "1" in output


def test_terminal_report_handles_no_findings(
    capsys,
):

    aggregator = ReportAggregator([])

    report = TerminalReport()

    report.show_file_analysis(
        aggregator
    )

    output = capsys.readouterr().out

    assert "CSS FILE ANALYSIS" in output
    assert "No CSS findings" in output


def test_terminal_report_shows_file_details(
    capsys,
):

    file_a = Path("css/cards.css")

    findings = [
        make_finding(
            file_a,
            "duplicate_declaration",
            line=42,
        ),
        make_finding(
            file_a,
            "important_declaration",
            line=57,
        ),
    ]

    aggregator = ReportAggregator(findings)

    report = TerminalReport()

    report.show_file_details(
        file_a,
        aggregator,
    )

    output = capsys.readouterr().out

    assert "css/cards.css" in output
    assert "2 findings" in output

    assert "Duplicate declaration" in output
    assert "Important declaration" in output

    assert "42" in output
    assert "57" in output