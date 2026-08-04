"""
DevDoctor Entry Point
"""

from scanner.file_scanner import FileScanner


def main():

    project_path = input("Enter project path: ").strip()

    scanner = FileScanner(project_path)

    project = scanner.scan()

    print("\nProject Scan Complete\n")

    print(f"PHP Files  : {len(project.php)}")
    print(f"HTML Files : {len(project.html)}")
    print(f"CSS Files  : {len(project.css)}")
    print(f"JS Files   : {len(project.js)}")

    print("-" * 30)
    print(f"Total Files: {project.total}")


if __name__ == "__main__":
    main()