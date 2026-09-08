"""Scaffolds the SpaceKid AGENTS.md cycle into a target project."""

from __future__ import annotations

import re
from dataclasses import dataclass
from importlib import resources
from pathlib import Path

_APP_NAME_PLACEHOLDER = "{{APP_NAME}}"

_TEMPLATES = resources.files("spacekid.templates")


@dataclass
class FileResult:
    path: Path
    status: str  # "created" | "appended" | "skipped"


def _load_template(filename: str) -> str:
    return _TEMPLATES.joinpath(filename).read_text(encoding="utf-8")


def detect_app_name(project_root: Path) -> str:
    pyproject = project_root / "pyproject.toml"
    if pyproject.is_file():
        match = re.search(
            r'(?m)^\s*name\s*=\s*["\']([^"\']+)["\']', pyproject.read_text(encoding="utf-8")
        )
        if match:
            return match.group(1)
    return project_root.resolve().name


def render_root_agents(app_name: str) -> str:
    return _load_template("root_agents.md").replace(_APP_NAME_PLACEHOLDER, app_name)


def write_or_skip(path: Path, content: str) -> FileResult:
    if path.exists():
        return FileResult(path, "skipped")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return FileResult(path, "created")


def write_or_append(path: Path, content: str) -> FileResult:
    if path.exists():
        with path.open("a", encoding="utf-8") as f:
            f.write("\n" + content)
        return FileResult(path, "appended")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return FileResult(path, "created")


def scaffold(project_root: Path, app_name: str | None = None) -> list[FileResult]:
    project_root = Path(project_root)
    resolved_name = app_name or detect_app_name(project_root)

    results = [
        write_or_skip(project_root / "AGENTS.md", render_root_agents(resolved_name)),
        write_or_append(project_root / "specs" / "AGENTS.md", _load_template("specs_agents.md")),
        write_or_append(project_root / "plans" / "AGENTS.md", _load_template("plans_agents.md")),
    ]
    return results
