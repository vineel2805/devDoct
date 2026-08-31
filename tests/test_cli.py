from cli.main import build_parser


def test_cli_parser_has_scan_command():

    parser = build_parser()

    args = parser.parse_args(
        ["scan", "."]
    )

    assert args.command == "scan"
    assert args.path == "."


def test_cli_scan_accepts_custom_path():

    parser = build_parser()

    args = parser.parse_args(
        ["scan", "my-project"]
    )

    assert args.command == "scan"
    assert args.path == "my-project"