"""Command-line entry point: `spacekid init`."""

from __future__ import annotations

import argparse
from importlib.metadata import version
import subprocess
import sys
from pathlib import Path

from spacekid import ui
from spacekid.scaffold import scaffold

_STATUS_LABEL = {
    "created": "created",
    "appended": "appended to",
    "skipped": "skipped (already exists)",
}


def _init(args: argparse.Namespace) -> int:
    project_root = Path(args.path).resolve()
    colored = ui.supports_color()
    if colored and getattr(args, "mark", True):
        print(ui.mark("init"))
        print()
    results = scaffold(project_root, app_name=args.name)
    for result in results:
        rel = result.path.relative_to(project_root)
        if colored:
            print(ui.status_line(result.status, rel))
        else:
            print(f"{_STATUS_LABEL[result.status]}: {rel}")
    return 0


def _find_miniverse(path: Path) -> Path | None:
    """The miniverse folder: `path` itself, or the `miniverse/` folder inside it."""
    for candidate in (path, path / "miniverse"):
        if (candidate / ".miniverse").is_file():
            return candidate
    return None


def _run_script(args: argparse.Namespace, script: str, extra: list[str]) -> int:
    """Run a miniverse script as-is: same output, colors and exit status."""
    path = Path(args.path).resolve()
    miniverse = _find_miniverse(path)
    if miniverse is None or not (miniverse / script).is_file():
        print(f"spacekid: no {script} found in {path}: run `spacekid init` there first", file=sys.stderr)
        return 1
    sys.stdout.flush()
    return subprocess.run(["sh", str(miniverse / script), *extra]).returncode


def _scan(args: argparse.Namespace) -> int:
    return _run_script(args, "scan.sh", [])


def _sync(args: argparse.Namespace) -> int:
    return _run_script(args, "sync.sh", ["--main"] if getattr(args, "main", False) else [])


def _about() -> None:
    print("SpaceKid creates a miniverse: a self-contained world of contexts, artifacts,")
    print("and a spec-driven workflow. The flow: context -> spec -> plan ->")
    print("implementation -> close the loop. Run `spacekid --help` for the commands:")
    print("init, scan (refresh the catalog) and sync (update the repositories).")


def _menu() -> int:
    print(ui.banner(version("spacekid")))
    print()
    action = ui.choose_from_menu()
    if action == "quit":
        return 0
    if action == "about":
        _about()
        return 0
    if action == "scan":
        return _scan(argparse.Namespace(path="."))
    if action == "sync":
        return _sync(argparse.Namespace(path=".", main=False))
    return _init(argparse.Namespace(path=".", name=None, mark=False))


class _Parser(argparse.ArgumentParser):
    """Big logo on the main command's help; a one-line mark on subcommands."""

    mark_label: str | None = None

    def print_help(self, file=None) -> None:
        if ui.supports_color():
            print(ui.mark(self.mark_label) if self.mark_label else ui.banner(version("spacekid")), file=file)
            print(file=file)
        super().print_help(file)


def build_parser() -> argparse.ArgumentParser:
    parser = _Parser(prog="spacekid")
    parser.add_argument("--version", action="version", version=f"%(prog)s {version('spacekid')}")
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser(
        "init", help="create a miniverse in a directory"
    )
    init_parser.add_argument(
        "--path", default=".", help="directory to create the miniverse in (default: current directory)"
    )
    init_parser.add_argument(
        "--name", default=None, help="name for the miniverse guides (default: auto-detected)"
    )
    init_parser.mark_label = "init"
    init_parser.set_defaults(func=_init)

    scan_parser = subparsers.add_parser(
        "scan", help="refresh the miniverse catalog (runs the miniverse's scan.sh)"
    )
    scan_parser.add_argument(
        "--path", default=".", help="project or miniverse directory (default: current directory)"
    )
    scan_parser.set_defaults(func=_scan)

    sync_parser = subparsers.add_parser(
        "sync", help="update every repository with git pull --ff-only (runs the miniverse's sync.sh)"
    )
    sync_parser.add_argument(
        "--path", default=".", help="project or miniverse directory (default: current directory)"
    )
    sync_parser.add_argument(
        "--main", action="store_true", help="move every repository to main before updating"
    )
    sync_parser.set_defaults(func=_sync)

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
