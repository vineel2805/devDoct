"""
Terminal presentation for Iksha.
"""

from rich.console import Console
from rich.text import Text


class TerminalReport:
    """Renders Iksha scan results in the terminal."""

    def __init__(self):
        self.console = Console()

    def show_banner(self) -> None:
        """Display Iksha identity."""

        logo = Text("IKSHA", style="bold blue")

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