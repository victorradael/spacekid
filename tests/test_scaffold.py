import pytest

import os
from pathlib import Path

from spacekid import cli
from spacekid.scaffold import scaffold

_GUIDES = (
    "contexts/AGENTS.md",
    "artifacts/AGENTS.md",
    "sdd/specs/AGENTS.md",
    "sdd/plans/AGENTS.md",
)


def _fake_repo(parent: Path, name: str) -> Path:
    repo = parent / name
    (repo / ".git").mkdir(parents=True)
    return repo


def _tree(root: Path) -> set[str]:
    return {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}


def _snapshot(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)): p.read_text(encoding="utf-8")
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def test_fresh_directory_creates_full_miniverse(tmp_path: Path) -> None:
    results = scaffold(tmp_path)

    assert {r.status for r in results} == {"created"}
    mv = tmp_path / "miniverse"
    assert (tmp_path / "AGENTS.md").is_file()
    assert (mv / "AGENTS.md").is_file()
    assert (mv / ".miniverse").is_file()
    assert (mv / "scan.sh").is_file()
    assert (mv / "sync.sh").is_file()
    assert (mv / "catalog.md").is_file()
    for guide in _GUIDES:
        assert (mv / guide).is_file()
    assert (mv / "contexts" / ".gitkeep").is_file()
    assert (mv / "artifacts" / ".gitkeep").is_file()


def test_structure_is_identical_for_repo_multi_repo_and_empty_directories(tmp_path: Path) -> None:
    single = tmp_path / "single"
    (single / ".git").mkdir(parents=True)
    multi = tmp_path / "multi"
    _fake_repo(multi, "api")
    _fake_repo(multi, "web")
    empty = tmp_path / "empty"
    empty.mkdir()

    trees = []
    for directory in (single, multi, empty):
        scaffold(directory, app_name="x")
        trees.append({p for p in _tree(directory) if not p.startswith(("api/", "web/", ".git/"))})

    assert trees[0] == trees[1] == trees[2]


def test_name_comes_from_pyproject_then_directory_then_override(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "widgets"\n', encoding="utf-8")
    scaffold(tmp_path)
    assert "Agent Guide — widgets" in (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert (tmp_path / "miniverse" / ".miniverse").read_text(encoding="utf-8") == "widgets\n"

    folder = tmp_path / "my-project"
    folder.mkdir()
    scaffold(folder)
    assert "Agent Guide — my-project" in (folder / "AGENTS.md").read_text(encoding="utf-8")

    other = tmp_path / "other"
    other.mkdir()
    scaffold(other, app_name="override")
    assert "Miniverse — override" in (other / "miniverse" / "AGENTS.md").read_text(encoding="utf-8")


def test_root_agents_is_a_short_pointer_to_the_miniverse(tmp_path: Path) -> None:
    scaffold(tmp_path)
    text = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")

    assert "miniverse/AGENTS.md" in text
    assert len(text.splitlines()) < 40
    assert "AGENT TODO" in text
    assert "{{APP_NAME}}" not in text


def test_existing_root_agents_md_is_left_untouched(tmp_path: Path) -> None:
    existing = "# My own AGENTS.md\n\ncustom content\n"
    (tmp_path / "AGENTS.md").write_text(existing, encoding="utf-8")

    results = scaffold(tmp_path)

    root_result = next(r for r in results if r.path == tmp_path / "AGENTS.md")
    assert root_result.status == "skipped"
    assert (tmp_path / "AGENTS.md").read_text(encoding="utf-8") == existing


def test_existing_folder_guides_are_appended_to_and_miniverse_guide_skipped(tmp_path: Path) -> None:
    mv = tmp_path / "miniverse"
    for guide in _GUIDES:
        (mv / guide).parent.mkdir(parents=True, exist_ok=True)
        (mv / guide).write_text("old\n", encoding="utf-8")
    (mv / "AGENTS.md").write_text("mine\n", encoding="utf-8")

    results = scaffold(tmp_path)

    statuses = {r.path.relative_to(mv).as_posix(): r.status for r in results if r.path.is_relative_to(mv)}
    assert statuses["AGENTS.md"] == "skipped"
    for guide in _GUIDES:
        assert statuses[guide] == "appended"
        assert (mv / guide).read_text(encoding="utf-8").startswith("old\n")
    assert (mv / "AGENTS.md").read_text(encoding="utf-8") == "mine\n"


def test_scanner_and_marker_are_never_overwritten(tmp_path: Path) -> None:
    mv = tmp_path / "miniverse"
    mv.mkdir()
    (mv / "scan.sh").write_text("custom\n", encoding="utf-8")
    (mv / ".miniverse").write_text("custom\n", encoding="utf-8")

    results = scaffold(tmp_path)

    statuses = {r.path.name: r.status for r in results}
    assert statuses["scan.sh"] == "skipped"
    assert statuses[".miniverse"] == "skipped"
    assert (mv / "scan.sh").read_text(encoding="utf-8") == "custom\n"
    assert (mv / ".miniverse").read_text(encoding="utf-8") == "custom\n"


def test_scanner_is_executable(tmp_path: Path) -> None:
    scaffold(tmp_path)

    assert os.access(tmp_path / "miniverse" / "scan.sh", os.X_OK)
    assert os.access(tmp_path / "miniverse" / "sync.sh", os.X_OK)


def test_second_run_changes_nothing(tmp_path: Path) -> None:
    scaffold(tmp_path)
    before = _snapshot(tmp_path)

    results = scaffold(tmp_path)

    assert {r.status for r in results} == {"skipped"}
    assert _snapshot(tmp_path) == before


def test_user_edits_around_the_rules_do_not_trigger_another_append(tmp_path: Path) -> None:
    scaffold(tmp_path)
    path = tmp_path / "miniverse" / "sdd" / "specs" / "AGENTS.md"
    edited = "# Mine\n\n" + path.read_text(encoding="utf-8") + "\nextra notes\n"
    path.write_text(edited, encoding="utf-8")

    scaffold(tmp_path)

    assert path.read_text(encoding="utf-8") == edited


def test_cli_init_creates_miniverse_and_has_no_mode_option(
    tmp_path: Path, capsys: "pytest.CaptureFixture[str]"
) -> None:
    cli.main(["init", "--path", str(tmp_path)])

    assert (tmp_path / "miniverse" / "AGENTS.md").is_file()
    assert "mode" not in capsys.readouterr().out


def test_miniverse_guide_puts_the_flow_first_and_states_its_rules(tmp_path: Path) -> None:
    scaffold(tmp_path)
    text = (tmp_path / "miniverse" / "AGENTS.md").read_text(encoding="utf-8")

    assert text.index("## The Flow") < text.index("## Map")
    assert text.index("## The Flow") < text.index("## Where Things Go")
    assert "Context (mandatory first step)" in text
    assert "saved as a context" in text
    assert "is an artifact" in text
    assert "./scan.sh" in text and "catalog.md" in text
    assert "before starting any spec and before starting any plan" in text
    assert "never search the file tree" in text
    assert "reuse its `contexts/`" in text
    assert "./sync.sh" in text and "never read the current state of the projects" in text.lower()
    assert "limitations" in text and "decisions" in text
    assert "higher-level spec prevails" in text
    assert "the higher the level, the higher the precedence" in text
    assert "Traceability" in text
    assert "read that folder's" in text
    for guide in ("contexts/AGENTS.md", "artifacts/AGENTS.md", "sdd/specs/AGENTS.md", "sdd/plans/AGENTS.md"):
        assert guide in text
    assert "{{APP_NAME}}" not in text


def test_spec_rules_require_dates_and_traceability(tmp_path: Path) -> None:
    scaffold(tmp_path)
    text = (tmp_path / "miniverse" / "sdd" / "specs" / "AGENTS.md").read_text(encoding="utf-8")

    assert "Created:" in text and "Updated:" in text
    assert "## Traceability" in text
    assert "only place a spec may point to other files" in text
    assert "(added YYYY-MM-DD)" in text


def test_plan_context_and_artifact_rules_require_registration(tmp_path: Path) -> None:
    scaffold(tmp_path)
    mv = tmp_path / "miniverse"

    for guide in ("sdd/plans", "contexts", "artifacts"):
        text = (mv / guide / "AGENTS.md").read_text(encoding="utf-8")
        assert "Traceability" in text
        assert "`Updated` date" in text


def test_context_rules_require_summary_and_dates(tmp_path: Path) -> None:
    scaffold(tmp_path)
    text = (tmp_path / "miniverse" / "contexts" / "AGENTS.md").read_text(encoding="utf-8")

    assert "Summary:" in text and "Created:" in text and "Updated:" in text
    assert "one line" in text
