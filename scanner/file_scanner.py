"""
Scans a project directory and collects supported files.
"""

from pathlib import Path

from config import IGNORE_DIRS, SUPPORTED_EXTENSIONS
from models.project_files import ProjectFiles


class FileScanner:
    """Scans a project directory."""

    def __init__(self, root: str | Path):
        self.root = Path(root)

    def scan(self) -> ProjectFiles:
        """
        Scan the project recursively.

        Returns:
            ProjectFiles
        """

        project = ProjectFiles()

        for path in self.root.rglob("*"):

            # Skip directories
            if path.is_dir():
                continue

            # Skip ignored folders
            if any(part in IGNORE_DIRS for part in path.parts):
                continue

            extension = path.suffix.lower()

            if extension not in SUPPORTED_EXTENSIONS:
                continue

            file_type = SUPPORTED_EXTENSIONS[extension]

            getattr(project, file_type).append(path)

        return project