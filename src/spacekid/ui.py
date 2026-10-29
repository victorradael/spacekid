"""Terminal presentation: colors, banner, result lines, and the interactive menu."""

from __future__ import annotations

import os
import sys
from typing import Callable

_RESET = "\033[0m"

_BANNER_LINES = [
    r"  ____  ____   _    ____ _____ _  _____ ____  ",
    r" / ___||  _ \ / \  / ___| ____| |/ /_ _|  _ \ ",
    r" \___ \| |_) / _ \| |   |  _| | ' / | || | | |",
    r"  ___) |  __/ ___ \ |___| |___| . \ | || |_| |",
    r" |____/|_| /_/   \_\____|_____|_|\_\___|____/ ",
]
_GRADIENT = (51, 45, 39, 99, 135)
_TAGLINE = "a minimalist spec kit for agentic development"

# status -> (icon, 256-color code, heading text)
_STATUS_STYLE = {
    "created": ("✔", 42, "created"),
    "appended": ("✚", 214, "appended to"),
    "skipped": ("•", 244, "skipped (already exists)"),
}

_MENU = (
    ("1", "Create a miniverse here", "init"),
    ("2", "About SpaceKid", "about"),
    ("3", "Quit", "quit"),
)


def supports_color() -> bool:
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    return _stdout_is_tty()


def _stdout_is_tty() -> bool:
    return sys.stdout.isatty()


def is_interactive() -> bool:
    return sys.stdin.isatty() and supports_color()


def paint(text: str, color: int | None = None, bold: bool = False, dim: bool = False) -> str:
    if not supports_color():
        return text
    codes = []
    if bold:
        codes.append("1")
    if dim:
        codes.append("2")
    if color is not None:
        codes.append(f"38;5;{color}")
    if not codes:
        return text
    return f"\033[{';'.join(codes)}m{text}{_RESET}"


def banner(version: str) -> str:
    lines = [paint(line, color, bold=True) for line, color in zip(_BANNER_LINES, _GRADIENT)]
    lines.append(paint(f" {_TAGLINE}  ·  v{version}", 245, dim=True))
    return "\n".join(lines)


def mark(label: str) -> str:
    """One-line SpaceKid mark for commands other than the main one."""
    letters = "SPACEKID"
    colors = (51, 51, 45, 45, 39, 99, 99, 135)
    name = "".join(paint(ch, color, bold=True) for ch, color in zip(letters, colors))
    return f"{paint('✦', 51, bold=True)} {name}  {paint(f'·  {label}', 245, dim=True)}"


def status_line(status: str, rel_path: object) -> str:
    icon, color, text = _STATUS_STYLE[status]
    return f"{paint(icon, color, bold=True)} {paint(text, color)} {rel_path}"


def render_menu() -> str:
    rows = [paint("What would you like to do?", 255, bold=True)]
    for key, label, _ in _MENU:
        rows.append(f"  {paint(key, 213, bold=True)}) {label}")
    return "\n".join(rows)


def choose_from_menu(
    read: Callable[[str], str] | None = None, write: Callable[[str], None] = print
) -> str:
    """Show the menu until a valid choice is made; return its action key."""
    read = read or input
    actions = {key: action for key, _, action in _MENU}
    write(render_menu())
    while True:
        try:
            raw = read(paint("> ", 213, bold=True)).strip()
        except (EOFError, KeyboardInterrupt):
            write("")
            return "quit"
        if raw in actions:
            return actions[raw]
        if raw.lower() in actions.values():
            return raw.lower()
        write(paint(f"Invalid choice: {raw!r}. Enter a number from 1 to {len(_MENU)}.", 203))
