"""
Analyzes CSS declarations.
"""

from models.css_rule import CSSRule
from models.css_declaration_finding import CSSDeclarationFinding


class CSSDeclarationAnalyzer:
    """Analyzes CSS declarations for potential issues."""

    def analyze(
        self,
        rules: list[CSSRule]
    ) -> list[CSSDeclarationFinding]:

        findings = []

        for rule in rules:

            seen_properties = set()
            seen_declarations = set()

            for declaration in rule.declarations:

                # -----------------------------
                # !important detection
                # -----------------------------

                if declaration.important:

                    findings.append(
                        CSSDeclarationFinding(
                            selectors=rule.selectors,
                            property=declaration.property,
                            value=declaration.value,
                            issue="important_declaration",
                            source_line=declaration.source_line,
                            source_column=declaration.source_column
                        )
                    )

                # -----------------------------
                # Duplicate property detection
                # -----------------------------

                declaration_key = (
                    declaration.property,
                    declaration.value
                )

                if declaration.property in seen_properties:

                    if declaration_key in seen_declarations:
                        issue = "duplicate_declaration"
                    else:
                        issue = "conflicting_declaration"

                    findings.append(
                        CSSDeclarationFinding(
                            selectors=rule.selectors,
                            property=declaration.property,
                            value=declaration.value,
                            issue=issue,
                            source_line=declaration.source_line,
                            source_column=declaration.source_column
                        )
                    )

                seen_properties.add(
                    declaration.property
                )

                seen_declarations.add(
                    declaration_key
                )

        return findings