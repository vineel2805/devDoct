"""
Iksha CLI entry point.
"""

import argparse

from scanner.file_scanner import FileScanner
from scanner.html_scanner import HTMLScanner
from scanner.css_scanner import CSSScanner
from analyzers.usage import UsageAnalyzer
from reports.terminal import TerminalReport
from reports.aggregator import ReportAggregator


def build_parser() -> argparse.ArgumentParser:
    """Build the Iksha command-line parser."""

    parser = argparse.ArgumentParser(
        prog="iksha",
        description="Project Intelligence CLI",
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan a project",
    )

    scan_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Project path to scan",
    )

    return parser


def scan_project(path: str) -> None:
    """Scan and analyze a project."""

    report = TerminalReport()

    report.show_banner()
    report.show_scan_start(path)

    # ----------------------------------------
    # File scan
    # ----------------------------------------

    file_scanner = FileScanner(path)
    project = file_scanner.scan()

    report.show_success(
        "Files discovered"
    )

    # ----------------------------------------
    # HTML scan
    # ----------------------------------------

    html_scanner = HTMLScanner()

    html_result = html_scanner.scan(
        project.php + project.html,
        project.root,
    )

    report.show_success(
        "HTML analysis complete"
    )

    # ----------------------------------------
    # CSS scan
    # ----------------------------------------

    css_scanner = CSSScanner()

    css_result = css_scanner.scan(
        project.css,
    )

    report.show_success(
        "CSS analysis complete"
    )
    

    

    # ----------------------------------------
    # Usage analysis
    # ----------------------------------------

    usage_analyzer = UsageAnalyzer()

    usage_result = usage_analyzer.analyze(
        html_result,
        css_result,
    )

    report.show_success(
        "Usage analysis complete"
    )

    # ----------------------------------------
    # Summary
    # ----------------------------------------

    report.show_summary(
        project,
        html_result,
        css_result,
        usage_result,
    )
    # ----------------------------------------
    # CSS findings
    # ----------------------------------------

    findings = (
            css_result.declaration_findings
            + css_result.rule_findings
        )
    
    aggregator = ReportAggregator(findings)
    report.show_file_analysis(aggregator)
    report.show_issue_analysis(aggregator)


def main() -> None:
    """Run the Iksha CLI."""

    parser = build_parser()

    args = parser.parse_args()

    if args.command == "scan":
        scan_project(args.path)
        return

    parser.print_help()


if __name__ == "__main__":
    main()