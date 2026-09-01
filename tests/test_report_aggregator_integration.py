from pathlib import Path

from scanner.css_scanner import CSSScanner
from reports.aggregator import ReportAggregator


def test_aggregator_accepts_real_css_scanner_findings(tmp_path: Path):

    css_file = tmp_path / "style.css"

    css_file.write_text(
        """
        .card {
            color: red !important;
            display: block;
            display: flex;
        }
        """,
        encoding="utf-8",
    )

    css_result = CSSScanner().scan([css_file])

    findings = (
        css_result.declaration_findings
        + css_result.rule_findings
    )

    aggregator = ReportAggregator(findings)

    result = aggregator.findings_by_file()

    assert css_file in result
    assert len(result[css_file]) == 2


def test_aggregator_groups_real_findings_by_issue(
    tmp_path: Path,
):

    css_file = tmp_path / "style.css"

    css_file.write_text(
        """
        .card {
            color: red !important;
            display: block;
            display: flex;
        }
        """,
        encoding="utf-8",
    )

    css_result = CSSScanner().scan([css_file])

    findings = (
        css_result.declaration_findings
        + css_result.rule_findings
    )

    aggregator = ReportAggregator(findings)

    result = aggregator.findings_by_issue()

    assert "important_declaration" in result
    assert "conflicting_declaration" in result

    assert len(
        result["important_declaration"]
    ) == 1

    assert len(
        result["conflicting_declaration"]
    ) == 1


def test_aggregator_ranks_real_css_files_by_findings(
    tmp_path: Path,
):

    header = tmp_path / "header.css"
    cards = tmp_path / "cards.css"

    header.write_text(
        """
        .header {
            color: red !important;
            display: block;
            display: flex;
        }
        """,
        encoding="utf-8",
    )

    cards.write_text(
        """
        .card {
            color: red !important;
        }
        """,
        encoding="utf-8",
    )

    scanner = CSSScanner()

    header_result = scanner.scan([header])
    cards_result = scanner.scan([cards])

    findings = (
        header_result.declaration_findings
        + header_result.rule_findings
        + cards_result.declaration_findings
        + cards_result.rule_findings
    )

    aggregator = ReportAggregator(findings)

    result = aggregator.file_finding_counts()

    assert result[header] == 2
    assert result[cards] == 1

    assert list(result.keys()) == [
        header,
        cards,
    ]


def test_aggregator_handles_project_with_no_css_findings(
    tmp_path: Path,
):

    css_file = tmp_path / "clean.css"

    css_file.write_text(
        """
        .card {
            color: red;
            display: flex;
        }
        """,
        encoding="utf-8",
    )

    css_result = CSSScanner().scan([css_file])

    findings = (
        css_result.declaration_findings
        + css_result.rule_findings
    )

    aggregator = ReportAggregator(findings)

    assert aggregator.findings_by_file() == {}
    assert aggregator.findings_by_issue() == {}
    assert aggregator.file_finding_counts() == {}