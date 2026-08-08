"""
CSS selector matcher.

Matches compiled cssselect2 selectors against HTML documents.
"""

from lxml import html
from lxml.etree import ParserError
from cssselect2 import ElementWrapper

from parsers.css_parser import ParsedSelector


class CSSMatcher:
    """Matches CSS selectors against HTML documents."""

    def matches(
        self,
        selector: ParsedSelector,
        document: str
    ) -> bool:
        """
        Return True if the CSS selector matches at least
        one element in the supplied HTML document.
        """

        if not selector.valid:
            return False

        if selector.compiled is None:
            return False

        #
        # Empty document cannot contain a matching element.
        #
        if not document or not document.strip():
            return False

        try:

            root_element = html.fromstring(
                document
            )

            root = ElementWrapper.from_html_root(
                root_element
            )

            for element in root.iter_subtree():

                if selector.compiled.test(element):
                    return True

        except (
            ParserError,
            ValueError,
            TypeError
        ):
            return False

        return False