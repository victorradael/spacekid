"""Command-line entry point: `spacekid init`."""

from __future__ import annotations

import argparse
from pathlib import Path

from spacekid.scaffold import scaffold

_STATUS_LABEL = {
    "created": "created",
    "appended": "appended to",
    "skipped": "skipped (already exists)",
}


def _init(args: argparse.Namespace) -> int:
    project_root = Path(args.path).resolve()
    results = scaffold(project_root, app_name=args.name)
    for result in results:
        rel = result.path.relative_to(project_root)
        print(f"{_STATUS_LABEL[result.status]}: {rel}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="spacekid")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init", help="scaffold the SpaceKid AGENTS.md cycle in a project"
    )
    init_parser.add_argument(
        "--path", default=".", help="project root to scaffold into (default: current directory)"
    )
    init_parser.add_argument(
        "--name", default=None, help="project name for AGENTS.md (default: auto-detected)"
    )
    init_parser.set_defaults(func=_init)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
