"""
DevDoctor Entry Point
"""


from scanner.file_scanner import FileScanner
from scanner.html_scanner import HTMLScanner


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
if __name__ == "__main__":
    main()