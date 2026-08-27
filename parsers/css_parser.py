"""
CSS Parser.

Parses CSS syntax with tinycss2 and validates selectors
with cssselect2.
"""

from dataclasses import dataclass, field

import cssselect2
import tinycss2


@dataclass
class ParsedSelector:
    """Stores information about one CSS selector."""

    selector: str
    compiled: object | None = None

    source_line: int = 0
    source_column: int = 0

    valid: bool = True
    error: str | None = None


@dataclass
class ParsedCSS:
    """Stores parsed CSS information."""

    classes: set[str] = field(default_factory=set)
    ids: set[str] = field(default_factory=set)
    elements: set[str] = field(default_factory=set)

    selectors: list[ParsedSelector] = field(default_factory=list)

    total_rules: int = 0
    total_selectors: int = 0
    invalid_selectors: int = 0


class CSSParser:
    """Parses CSS stylesheets."""

    def parse(self, css: str) -> ParsedCSS:

        result = ParsedCSS()

        stylesheet = tinycss2.parse_stylesheet(
            css,
            skip_comments=True,
            skip_whitespace=True
        )

        self._parse_rules(
            stylesheet,
            result
        )

        return result

    def _parse_rules(
        self,
        rules,
        result: ParsedCSS
    ) -> None:

        for rule in rules:

            #
            # Normal CSS rule
            #
            if rule.type == "qualified-rule":

                result.total_rules += 1

                self._parse_selector_rule(
                    rule,
                    result
                )

            #
            # At-rules such as @media
            #
            elif rule.type == "at-rule":

                if rule.content is not None:

                    nested_rules = tinycss2.parse_blocks_contents(
                        rule.content,
                        skip_comments=True,
                        skip_whitespace=True
                    )

                    self._parse_rules(
                        nested_rules,
                        result
                    )

    def _parse_selector_rule(
        self,
        rule,
        result: ParsedCSS
    ) -> None:

        selector_text = tinycss2.serialize(
            rule.prelude
        ).strip()

        if not selector_text:
            return

        try:

            compiled_selectors = (
                cssselect2.compile_selector_list(
                    rule.prelude
                )
            )

        except cssselect2.SelectorError as e:

            result.invalid_selectors += 1

            result.selectors.append(
                ParsedSelector(
                    selector=selector_text,
                    source_line=rule.source_line,
                    source_column=rule.source_column,
                    valid=False,
                    error=str(e)
                )
            )

            return
        #
        # Split the selector list into individual selectors.
        #
        selector_names = self._split_selector_list(
            selector_text
        )
        #
        # cssselect2 returns one compiled selector
        # for every selector in a selector list.
        #
        for compiled, selector_name in zip(
        compiled_selectors,
        selector_names):

            selector = ParsedSelector(
                selector=selector_name,
                compiled=compiled,
                source_line=rule.source_line,
                source_column=rule.source_column
            )

            result.selectors.append(selector)

            result.total_selectors += 1

            #
            # Maintain class / ID / element summaries.
            #
            self._extract_selector_tokens(
                selector_text,
                result
            )

    def _extract_selector_tokens(
        self,
        selector: str,
        result: ParsedCSS
    ) -> None:
        """
        Extract class, ID, and element names from a CSS selector.

        cssselect2 validates the selector.
        This method maintains the selector summary used
        by DevDoctor.
        """

        tokens = tinycss2.parse_component_value_list(
            selector,
            skip_comments=True
        )

        self._extract_tokens(
            tokens,
            result
        )

    def _extract_tokens(
        self,
        tokens,
        result: ParsedCSS
    ) -> None:
        """
        Recursively extract selector tokens.

        Handles selectors inside functions such as:

            :not(.card)
            :is(.card, .button)
            :where(.container, .wrapper)
            :has(.card)
        """

        previous_literal = None

        for token in tokens:

            #
            # Class selector
            #
            if (
                previous_literal == "."
                and token.type == "ident"
            ):
                result.classes.add(token.value)

                previous_literal = None
                continue

            #
            # ID selector
            #
            if token.type == "hash":

                if token.value:
                    result.ids.add(token.value)

                previous_literal = None
                continue

            #
            # Function selector
            #
            # :not(...)
            # :is(...)
            # :where(...)
            # :has(...)
            #
            if token.type == "function":

                self._extract_tokens(
                    token.arguments,
                    result
                )

                previous_literal = None
                continue

            #
            # Element selector
            #
            if token.type == "ident":

                value = token.value.strip()

                if value:
                    result.elements.add(
                        value.lower()
                    )

                previous_literal = None
                continue

            #
            # Track literal tokens such as "."
            #
            if token.type == "literal":

                previous_literal = token.value
                continue

            #
            # Other token types
            #
            previous_literal = None

    def _split_selector_list(
        self,
        selector_text: str
    ) -> list[str]:
        """
        Split a CSS selector list into individual selectors.

        Commas inside parentheses or brackets are not
        treated as selector separators.

        Example:

            .card, .button, .title

        becomes:

            [".card", ".button", ".title"]

        while:

            .card:not(.hidden, .disabled), .button

        becomes:

            [".card:not(.hidden, .disabled)", ".button"]
        """

        selectors = []

        current = []

        parentheses_depth = 0
        bracket_depth = 0

        for char in selector_text:

            if char == "(":
                parentheses_depth += 1

            elif char == ")":
                if parentheses_depth > 0:
                    parentheses_depth -= 1

            elif char == "[":
                bracket_depth += 1

            elif char == "]":
                if bracket_depth > 0:
                    bracket_depth -= 1

            if (
                char == ","
                and parentheses_depth == 0
                and bracket_depth == 0
            ):
                selector = "".join(current).strip()

                if selector:
                    selectors.append(selector)

                current = []

            else:
                current.append(char)

        selector = "".join(current).strip()

        if selector:
            selectors.append(selector)

        return selectors