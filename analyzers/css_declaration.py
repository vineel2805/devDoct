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

            for declaration in rule.declarations:

                # -----------------------------
                # !important detection
                # -----------------------------

                if declaration.value.endswith("!important"):

                    findings.append(
                        CSSDeclarationFinding(
                            selector=rule.selectors[0],
                            property=declaration.property,
                            value=declaration.value,
                            source_line=declaration.source_line,
                            source_column=declaration.source_column
                        )
                    )

                # -----------------------------
                # Duplicate property detection
                # -----------------------------

                if declaration.property in seen_properties:

                    findings.append(
                        CSSDeclarationFinding(
                            selector=rule.selectors[0],
                            property=declaration.property,
                            value=declaration.value,
                            source_line=declaration.source_line,
                            source_column=declaration.source_column
                        )
                    )

                seen_properties.add(
                    declaration.property
                )

        return findings