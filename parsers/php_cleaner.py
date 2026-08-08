"""
PHP Cleaner

Removes PHP syntax from PHP files while preserving
static HTML information needed by DevDoctor.
"""

from __future__ import annotations

import re


class PHPCleaner:
    """Cleans PHP while preserving statically known HTML information."""

    # Matches:
    # <?php ... ?>
    # <?= ... ?>
    # <? ... ?>
    PHP_PATTERN = re.compile(
        r"<\?(?:php|=)?[\s\S]*?\?>",
        re.MULTILINE
    )

    # Matches class or id attributes.
    ATTRIBUTE_PATTERN = re.compile(
        r'(?P<name>class|id)\s*=\s*'
        r'(?P<quote>["\'])'
        r'(?P<value>.*?)'
        r'(?P=quote)',
        re.DOTALL | re.IGNORECASE
    )

    # Matches quoted PHP strings.
    STRING_PATTERN = re.compile(
        r"""(['"])(.*?)\1""",
        re.DOTALL
    )

    @classmethod
    def clean(cls, text: str) -> str:
        """
        Remove PHP syntax while preserving static class/id values.

        Example:

            class="<?= $active ? 'active' : '' ?> hero"

        becomes approximately:

            class="active hero"

        Dynamic values such as:

            class="<?= $class ?>"

        cannot be determined statically and are removed.
        """

        text = cls._clean_attributes(text)

        # Remove any remaining PHP blocks.
        text = cls.PHP_PATTERN.sub(" ", text)

        return text

    @classmethod
    def _clean_attributes(cls, text: str) -> str:
        """Clean PHP expressions inside class and id attributes."""

        def replace_attribute(match: re.Match) -> str:

            name = match.group("name")
            quote = match.group("quote")
            value = match.group("value")

            # No PHP in this attribute.
            if "<?" not in value:
                return match.group(0)

            cleaned_value = cls._extract_static_values(value)

            return f'{name}={quote}{cleaned_value}{quote}'

        return cls.ATTRIBUTE_PATTERN.sub(
            replace_attribute,
            text
        )

    @classmethod
    def _extract_static_values(cls, value: str) -> str:
        """
        Extract static string literals from a PHP-containing attribute.

        Example:

            <?= $error ? 'alert alert-danger' : 'd-none' ?>

        becomes:

            alert alert-danger d-none
        """

        static_values: list[str] = []

        for php_match in cls.PHP_PATTERN.finditer(value):

            php_code = php_match.group(0)

            # Remove PHP opening and closing tags.
            php_code = re.sub(
                r"<\?(?:php|=)?",
                "",
                php_code
            )

            php_code = php_code.replace("?>", "")

            # Find quoted PHP strings.
            for string_match in cls.STRING_PATTERN.finditer(
                php_code
            ):

                string_value = string_match.group(2).strip()

                if string_value:
                    static_values.append(string_value)

        # Preserve non-PHP portions of the attribute.
        remaining = cls.PHP_PATTERN.sub(" ", value)

        if remaining.strip():
            static_values.append(remaining.strip())

        # Remove duplicates while preserving order.
        result: list[str] = []

        for value in static_values:

            if value not in result:
                result.append(value)

        return " ".join(result)