"""
Analyzes CSS rules.
"""

from models.css_rule import CSSRule
from models.css_declaration_finding import CSSDeclarationFinding


class CSSRuleAnalyzer:
    """Analyzes CSS rules for potential issues."""

    def analyze(
        self,
        rules: list[CSSRule]
    ) -> list[CSSDeclarationFinding]:

        findings = []

        seen_rules = set()

        for rule in rules:

            declaration_key = tuple(
                (
                    declaration.property,
                    declaration.value,
                    declaration.important
                )
                for declaration in rule.declarations
            )

            rule_key = (
                tuple(rule.selectors),
                declaration_key
            )

            if rule_key in seen_rules:

                findings.append(
                    CSSDeclarationFinding(
                        selectors=rule.selectors,
                        property="",
                        value="",
                        issue="duplicate_rule",
                        source_line=rule.source_line,
                        source_column=rule.source_column
                    )
                )

            seen_rules.add(rule_key)

        return findings