"""Scaffolds a miniverse into a target directory."""

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


def write_or_skip(path: Path, content: str, executable: bool = False) -> FileResult:
    if path.exists():
        return FileResult(path, "skipped")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(0o755)
    return FileResult(path, "created")


def write_or_append(path: Path, content: str) -> FileResult:
    if path.exists():
        if content.strip() in path.read_text(encoding="utf-8"):
            return FileResult(path, "skipped")
        with path.open("a", encoding="utf-8") as f:
            f.write("\n" + content)
        return FileResult(path, "appended")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return FileResult(path, "created")


def scaffold(root: Path, app_name: str | None = None) -> list[FileResult]:
    root = Path(root)
    name = app_name or detect_app_name(root)
    miniverse = root / "miniverse"

    def render(template: str) -> str:
        return _load_template(template).replace(_APP_NAME_PLACEHOLDER, name)

    return [
        write_or_skip(root / "AGENTS.md", render("root_agents.md")),
        write_or_skip(miniverse / "AGENTS.md", render("miniverse_agents.md")),
        write_or_skip(miniverse / ".miniverse", f"{name}\n"),
        write_or_skip(miniverse / "scan.sh", _load_template("scan.sh"), executable=True),
        write_or_skip(miniverse / "sync.sh", _load_template("sync.sh"), executable=True),
        write_or_skip(miniverse / "catalog.md", render("miniverse_catalog.md")),
        write_or_append(miniverse / "contexts" / "AGENTS.md", _load_template("contexts_agents.md")),
        write_or_append(
            miniverse / "artifacts" / "AGENTS.md", _load_template("artifacts_agents.md")
        ),
        write_or_append(miniverse / "sdd" / "specs" / "AGENTS.md", _load_template("specs_agents.md")),
        write_or_append(miniverse / "sdd" / "plans" / "AGENTS.md", _load_template("plans_agents.md")),
        write_or_skip(miniverse / "contexts" / ".gitkeep", ""),
        write_or_skip(miniverse / "artifacts" / ".gitkeep", ""),
    ]
