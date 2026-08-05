"""
PHP Cleaner

Removes PHP code from PHP files while preserving the HTML structure.
"""

from __future__ import annotations

import re


class PHPCleaner:
    """Removes PHP blocks before HTML parsing."""

    # Matches:
    # <?php ... ?>
    # <?= ... ?>
    # <? ... ?>
    PHP_PATTERN = re.compile(r"<\?(?:php|=)?[\s\S]*?\?>", re.MULTILINE)

    @classmethod
    def clean(cls, text: str) -> str:
        """
        Replace PHP blocks with spaces.

        Using spaces instead of removing them completely helps preserve
        the surrounding HTML structure.
        """
        return cls.PHP_PATTERN.sub(" ", text)