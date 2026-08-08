"""
DevDoctor Entry Point
"""


from scanner.file_scanner import FileScanner
from scanner.html_scanner import HTMLScanner
from scanner.css_scanner import CSSScanner
from analyzers.usage import UsageAnalyzer

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
        project.php + project.html,
        project.root
    )

    print("\nHTML Scan Complete\n")
    print("\nHTML Scan")
    print("-" * 30)

    print(f"Classes Found : {html_result.total_classes}")
    print(f"IDs Found     : {html_result.total_ids}")
    print(f"Elements Found: {html_result.total_elements}")
    print(f"Files Scanned : {html_result.total_files}")

    print("\nElements")

    for element in sorted(html_result.elements):
        print(f"  {element}")
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

    #
    # Analyze CSS usage
    #
    usage_analyzer = UsageAnalyzer()
    usage_result = usage_analyzer.analyze(
        html_result,
        css_result
    )
    print("\nUsage Analysis")
    print("-" * 30)

    print(f"Used Classes    : {len(usage_result.used_classes)}")
    print(f"Unused Classes  : {len(usage_result.unused_classes)}")
    print(f"Missing Classes : {len(usage_result.missing_classes)}")

    print(f"Used IDs        : {len(usage_result.used_ids)}")
    print(f"Unused IDs      : {len(usage_result.unused_ids)}")
    print(f"Missing IDs     : {len(usage_result.missing_ids)}")
    print("\nUnused Classes")

    for cls in sorted(usage_result.unused_classes):
        print(f"  .{cls}")

    print("\nUnused IDs")

    for tag_id in sorted(usage_result.unused_ids):
        print(f"  #{tag_id}")

    print("\nMissing Classes")

    for cls in sorted(usage_result.missing_classes):
        print(f"  .{cls}")

    print("\nMissing IDs")

    for tag_id in sorted(usage_result.missing_ids):
        print(f"  #{tag_id}")
if __name__ == "__main__":
    main()