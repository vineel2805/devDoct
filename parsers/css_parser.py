"""
CSS Parser.

Parses CSS using tinycss2 and extracts selectors.
"""

from dataclasses import dataclass, field

import tinycss2


@dataclass
class ParsedCSS:
    """Selectors extracted from a CSS file."""

    classes: set[str] = field(default_factory=set)
    ids: set[str] = field(default_factory=set)
    elements: set[str] = field(default_factory=set)

    total_rules: int = 0


class CSSParser:
    """Parses CSS source code."""

    def parse(self, css: str) -> ParsedCSS:

        result = ParsedCSS()

        stylesheet = tinycss2.parse_stylesheet(
            css,
            skip_comments=True,
            skip_whitespace=True
        )

        for rule in stylesheet:

            if rule.type != "qualified-rule":
                continue

            result.total_rules += 1

            selector = tinycss2.serialize(rule.prelude)

            self._extract_selectors(
                selector,
                result
            )

        return result

    def _extract_selectors(
        self,
        selector: str,
        result: ParsedCSS
    ) -> None:

        token = ""

        i = 0

        while i < len(selector):

            c = selector[i]

            #
            # Class
            #
            if c == ".":

                i += 1

                token = ""

                while (
                    i < len(selector)
                    and (
                        selector[i].isalnum()
                        or selector[i] in "-_"
                    )
                ):

                    token += selector[i]
                    i += 1

                if token:
                    result.classes.add(token)

                continue

            #
            # ID
            #
            if c == "#":

                i += 1

                token = ""

                while (
                    i < len(selector)
                    and (
                        selector[i].isalnum()
                        or selector[i] in "-_"
                    )
                ):

                    token += selector[i]
                    i += 1

                if token:
                    result.ids.add(token)

                continue

            #
            # Element
            #
            if c.isalpha():

                token = c

                i += 1

                while (
                    i < len(selector)
                    and (
                        selector[i].isalnum()
                        or selector[i] == "-"
                    )
                ):

                    token += selector[i]
                    i += 1

                if token.lower() not in {
                    "hover",
                    "focus",
                    "active",
                    "before",
                    "after",
                    "root",
                    "not",
                    "is",
                    "where",
                    "has"
                }:

                    result.elements.add(token)

                continue

            i += 1