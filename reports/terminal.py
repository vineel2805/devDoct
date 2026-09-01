"""
Terminal presentation for Iksha.
"""

from pathlib import Path

from rich.console import Console
from rich.text import Text

from reports.aggregator import ReportAggregator


class TerminalReport:
    """Renders Iksha analysis results in the terminal."""

    def __init__(self):
        self.console = Console()

    def show_banner(self) -> None:
        """Display Iksha identity."""

        logo = Text(
            "IKSHA",
            style="bold blue",
        )

        self.console.print()
        self.console.print(logo)
        self.console.print(
            "Project Intelligence",
            style="dim",
        )
        self.console.print(
            "See. Understand. Improve.",
            style="dim",
        )
        self.console.print()

    def show_scan_start(
        self,
        project_path: str,
    ) -> None:
        """Display scan start."""

        self.console.print(
            f"[blue]→[/blue] Scanning "
            f"[bold]{project_path}[/bold]"
        )

    def show_success(
        self,
        message: str,
    ) -> None:
        """Display successful operation."""

        self.console.print(
            f"[blue]✓[/blue] {message}"
        )

    def show_info(
        self,
        message: str,
    ) -> None:
        """Display informational text."""

        self.console.print(
            f"[dim]• {message}[/dim]"
        )

    def show_summary(
        self,
        project,
        html_result,
        css_result,
        usage_result,
    ) -> None:
        """Display project scan summary."""

        self.console.print()
        self.console.print(
            "─" * 48,
            style="dim",
        )

        self.console.print(
            "Scan Summary",
            style="bold",
        )

        self.console.print()

        self.console.print(
            f"  PHP Files       {len(project.php)}"
        )

        self.console.print(
            f"  HTML Files      {len(project.html)}"
        )

        self.console.print(
            f"  CSS Files       {len(project.css)}"
        )

        self.console.print(
            f"  JS Files        {len(project.js)}"
        )

        self.console.print()

        self.console.print(
            "HTML",
            style="bold blue",
        )

        self.console.print(
            f"  Classes         "
            f"{html_result.total_classes}"
        )

        self.console.print(
            f"  IDs             "
            f"{html_result.total_ids}"
        )

        self.console.print(
            f"  Elements        "
            f"{html_result.total_elements}"
        )

        self.console.print()

        self.console.print(
            "CSS",
            style="bold blue",
        )

        self.console.print(
            f"  Classes         "
            f"{css_result.total_classes}"
        )

        self.console.print(
            f"  IDs             "
            f"{css_result.total_ids}"
        )

        self.console.print(
            f"  Elements        "
            f"{css_result.total_elements}"
        )

        self.console.print(
            f"  Selectors       "
            f"{css_result.total_selectors}"
        )

        self.console.print(
            f"  Files           "
            f"{css_result.total_files}"
        )

        self.console.print()

        self.console.print(
            "Usage",
            style="bold blue",
        )

        self.console.print(
            f"  Used Classes    "
            f"{len(usage_result.used_classes)}"
        )

        self.console.print(
            f"  Unused Classes  "
            f"{len(usage_result.unused_classes)}"
        )

        self.console.print(
            f"  Missing Classes "
            f"{len(usage_result.missing_classes)}"
        )

        self.console.print(
            f"  Used IDs        "
            f"{len(usage_result.used_ids)}"
        )

        self.console.print(
            f"  Unused IDs      "
            f"{len(usage_result.unused_ids)}"
        )

        self.console.print(
            f"  Missing IDs     "
            f"{len(usage_result.missing_ids)}"
        )

        self.console.print()

        self.console.print(
            "Findings",
            style="bold blue",
        )

        self.console.print(
            f"  CSS declarations "
            f"{len(css_result.declaration_findings)}"
        )

        self.console.print(
            f"  CSS rules         "
            f"{len(css_result.rule_findings)}"
        )

        self.console.print()

        self.console.print(
            "─" * 48,
            style="dim",
        )

    def show_file_analysis(
        self,
        aggregator: ReportAggregator,
    ) -> None:
        """Display CSS files ordered by finding count."""

        self.console.print()
        self.console.print(
            "CSS FILE ANALYSIS",
            style="bold blue",
        )
        self.console.print()

        counts = aggregator.file_finding_counts()

        if not counts:
            self.console.print(
                "  No CSS findings.",
                style="dim",
            )
            return

        for file, count in counts.items():
            self.console.print(
            f"  {count:>3}  {file.as_posix()}"
            )

    def show_issue_analysis(
        self,
        aggregator: ReportAggregator,
    ) -> None:
        """Display findings grouped by issue type."""

        self.console.print()
        self.console.print(
            "FINDINGS BY TYPE",
            style="bold blue",
        )
        self.console.print()

        grouped = aggregator.findings_by_issue()

        if not grouped:
            self.console.print(
                "  No CSS findings.",
                style="dim",
            )
            return

        labels = {
            "duplicate_declaration":
                "Duplicate declarations",

            "conflicting_declaration":
                "Conflicting declarations",

            "important_declaration":
                "Important declarations",

            "duplicate_property":
                "Duplicate properties",

            "duplicate_rule":
                "Duplicate rules",
        }

        for issue, findings in grouped.items():

            label = labels.get(
                issue,
                issue.replace("_", " ").title(),
            )

            self.console.print(
                f"  {len(findings):>3}  {label}"
            )

    def show_file_details(
        self,
        file: Path,
        aggregator: ReportAggregator,
    ) -> None:
        """Display findings belonging to one CSS file."""

        findings_by_file = (
            aggregator.findings_by_file()
        )

        findings = findings_by_file.get(
            file,
            [],
        )

        self.console.print()
        self.console.print(
            file.as_posix(),
            style="bold blue",
        )

        self.console.print()

        if not findings:
            self.console.print(
                "  No CSS findings.",
                style="dim",
            )
            return

        count = len(findings)

        self.console.print(
            f"{count} "
            f"{'finding' if count == 1 else 'findings'}"
        )

        self.console.print()

        labels = {
            "duplicate_declaration":
                "Duplicate declaration",

            "conflicting_declaration":
                "Conflicting declaration",

            "important_declaration":
                "Important declaration",

            "duplicate_property":
                "Duplicate property",

            "duplicate_rule":
                "Duplicate rule",
        }

        for finding in findings:

            label = labels.get(
                finding.issue,
                finding.issue.replace(
                    "_",
                    " ",
                ).title(),
            )

            self.console.print(
                f"  {label}",
                style="bold",
            )

            self.console.print(
                f"    Selector: "
                f"{', '.join(finding.selectors)}"
            )

            if finding.property:
                self.console.print(
                    f"    Property: "
                    f"{finding.property}"
                )

            if finding.value:
                self.console.print(
                    f"    Value: "
                    f"{finding.value}"
                )

            self.console.print(
                f"    Line: "
                f"{finding.source_line}"
            )

            self.console.print()