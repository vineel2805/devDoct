"""
Global configuration for DevDoctor.
"""

from pathlib import Path

# Directories that should not be scanned
IGNORE_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "node_modules",
    "vendor",
    "dist",
    "build",
    "output",
    "logs",
}

# Supported file extensions
SUPPORTED_EXTENSIONS = {
    ".php": "php",
    ".html": "html",
    ".css": "css",
    ".js": "js",
}