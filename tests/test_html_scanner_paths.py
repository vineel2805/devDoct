from pathlib import Path

from scanner.html_scanner import HTMLScanner


def test_html_scanner_uses_resolved_file_paths(tmp_path: Path):

    html_file = tmp_path / "index.php"

    html_file.write_text(
        """
        <div class="card">
            Hello
        </div>
        """,
        encoding="utf-8",
    )

    scanner = HTMLScanner()

    result = scanner.scan(
        [html_file],
        tmp_path,
    )

    assert len(result.files) == 1

    stored_path = next(iter(result.files))

    assert stored_path == html_file.resolve()
    assert stored_path.is_absolute()