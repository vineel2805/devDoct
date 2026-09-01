"""
Aggregates CSS findings for reporting.
"""

from collections import defaultdict
from pathlib import Path

from models.css_declaration_finding import CSSDeclarationFinding


class ReportAggregator:
    """Organizes findings by file and issue type."""

    def __init__(
        self,
        findings: list[CSSDeclarationFinding],
    ):
        self.findings = findings

    def findings_by_file(
        self,
    ) -> dict[Path, list[CSSDeclarationFinding]]:
        """Group findings by source file."""

        grouped = defaultdict(list)

        for finding in self.findings:
            if finding.file is not None:
                grouped[finding.file].append(finding)

        return dict(grouped)

    def findings_by_issue(
        self,
    ) -> dict[str, list[CSSDeclarationFinding]]:
        """Group findings by issue type."""

        grouped = defaultdict(list)

        for finding in self.findings:
            grouped[finding.issue].append(finding)

        return dict(grouped)

    def file_finding_counts(
        self,
    ) -> dict[Path, int]:
        """Return files ordered by number of findings."""

        counts = {
            file: len(findings)
            for file, findings in self.findings_by_file().items()
        }

        return dict(
            sorted(
                counts.items(),
                key=lambda item: item[1],
                reverse=True,
            )
        )