"""Command-line entry point: `spacekid init`."""

from __future__ import annotations

import argparse
from importlib.metadata import version
from pathlib import Path

from spacekid import ui
from spacekid.scaffold import detect_mode, scaffold, scaffold_brain

_STATUS_LABEL = {
    "created": "created",
    "appended": "appended to",
    "skipped": "skipped (already exists)",
}


def _init(args: argparse.Namespace) -> int:
    project_root = Path(args.path).resolve()
    colored = ui.supports_color()
    if colored:
        print(ui.banner(version("spacekid")))
        print()
    mode = detect_mode(project_root) if args.mode == "auto" else args.mode
    print(ui.heading(mode) if colored else f"mode: {mode}")
    run = scaffold_brain if mode == "brain" else scaffold
    results = run(project_root, app_name=args.name)
    for result in results:
        rel = result.path.relative_to(project_root)
        if colored:
            print(ui.status_line(result.status, rel))
        else:
            print(f"{_STATUS_LABEL[result.status]}: {rel}")
    return 0


def _about() -> None:
    print(ui.banner(version("spacekid")))
    print()
    print("SpaceKid scaffolds the spec -> plan -> implementation cycle for agentic")
    print("development. Run `spacekid init --help` for the command-line options.")


def _menu() -> int:
    print(ui.banner(version("spacekid")))
    print()
    action = ui.choose_from_menu()
    if action == "quit":
        return 0
    if action == "about":
        _about()
        return 0
    return _init(argparse.Namespace(path=".", name=None, mode=action))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="spacekid")
    parser.add_argument("--version", action="version", version=f"%(prog)s {version('spacekid')}")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser(
        "init", help="scaffold the SpaceKid AGENTS.md cycle in a project"
    )
    init_parser.add_argument(
        "--path", default=".", help="project root to scaffold into (default: current directory)"
    )
    init_parser.add_argument(
        "--name", default=None, help="project name for AGENTS.md (default: auto-detected)"
    )
    init_parser.add_argument(
        "--mode",
        choices=["auto", "project", "brain"],
        default="auto",
        help="usage mode: project, brain (multi-repo directory), or auto-detect (default)",
    )
    init_parser.set_defaults(func=_init)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command is None:
        if ui.is_interactive():
            return _menu()
        parser.print_help()
        return 0
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
