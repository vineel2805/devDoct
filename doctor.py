"""
DevDoctor Entry Point
"""


from scanner.file_scanner import FileScanner
from scanner.html_scanner import HTMLScanner
from scanner.css_scanner import CSSScanner


def main():

    project_path = input("Enter project path: ").strip()

    #
    # Scan Files
    #
    file_scanner = FileScanner(project_path)

    project = file_scanner.scan()

    print("\nProject Scan Complete\n")

    print(f"PHP Files  : {len(project.php)}")
    print(f"HTML Files : {len(project.html)}")
    print(f"CSS Files  : {len(project.css)}")
    print(f"JS Files   : {len(project.js)}")

    #
    # Scan HTML
    #
    html_scanner = HTMLScanner()

    html_result = html_scanner.scan(
        project.php + project.html
    )

    print("\nHTML Scan Complete\n")

    #
    # Scan CSS
    #
    css_scanner = CSSScanner()

    css_result = css_scanner.scan(project.css)
    print("\nCSS Scan")
    print("-" * 30)

    print(f"Classes Found : {css_result.total_classes}")
    print(f"IDs Found     : {css_result.total_ids}")
    print(f"Elements Found: {css_result.total_elements}")
    print(f"Files Scanned : {css_result.total_files}")
    print("\nCSS Scan Complete\n")

if __name__ == "__main__":
    main()