"""
Scans CSS files and extracts selectors.
"""

from pathlib import Path

from models.css_result import CSSScanResult, FileCSSResult
from parsers.css_parser import CSSParser

from analyzers.css_declaration import CSSDeclarationAnalyzer
from analyzers.css_rule import CSSRuleAnalyzer


class CSSScanner:
    """Extracts CSS selectors and analyzes CSS rules."""

    def __init__(self):
        self.parser = CSSParser()
        self.declaration_analyzer = CSSDeclarationAnalyzer()
        self.rule_analyzer = CSSRuleAnalyzer()

    def scan(
        self,
        files: list[Path]
    ) -> CSSScanResult:

        result = CSSScanResult()

        for file in files:

            try:

                css = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                parsed = self.parser.parse(css)

                declaration_findings = self.declaration_analyzer.analyze(
                    parsed.rules
                )

                rule_findings = self.rule_analyzer.analyze(
                    parsed.rules
                )

                file_result = FileCSSResult()
                for finding in declaration_findings:
                    finding.file = file

                for finding in rule_findings:
                    finding.file = file
                # -----------------------------
                # Store file data
                # -----------------------------

                file_result.classes = parsed.classes
                file_result.ids = parsed.ids
                file_result.elements = parsed.elements

                file_result.selectors = parsed.selectors
                file_result.declarations = parsed.declarations
                file_result.total_rules = parsed.total_rules

                file_result.declaration_findings = declaration_findings
                file_result.rule_findings = rule_findings

                # -----------------------------
                # Store project-wide data
                # -----------------------------

                result.classes.update(
                    parsed.classes
                )

                result.ids.update(
                    parsed.ids
                )

                result.elements.update(
                    parsed.elements
                )
                result.declaration_findings.extend(
                    declaration_findings
                )

                result.rule_findings.extend(
                    rule_findings
                )

                # -----------------------------
                # Store file result
                # -----------------------------

                result.files[file] = file_result

            except Exception as e:

                print(
                    f"Failed to scan {file}: {e}"
                )

        return result