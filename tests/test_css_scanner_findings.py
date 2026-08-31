from pathlib import Path

from scanner.css_scanner import CSSScanner


def test_css_scanner_collects_declaration_findings(tmp_path: Path):

    css_file = tmp_path / "style.css"

    css_file.write_text(
        """
        .card {
            color: red !important;
        }
        """,
        encoding="utf-8"
    )

    result = CSSScanner().scan([css_file])

    assert len(result.declaration_findings) == 1

    finding = result.declaration_findings[0]

    assert finding.selectors == [".card"]
    assert finding.property == "color"
    assert finding.issue == "important_declaration"


def test_css_scanner_collects_rule_findings(tmp_path: Path):

    css_file = tmp_path / "style.css"

    css_file.write_text(
        """
        .card {
            color: red;
        }

        .card {
            color: red;
        }
        """,
        encoding="utf-8"
    )

    result = CSSScanner().scan([css_file])

    assert len(result.rule_findings) == 1

    finding = result.rule_findings[0]

    assert finding.selectors == [".card"]
    assert finding.issue == "duplicate_rule"