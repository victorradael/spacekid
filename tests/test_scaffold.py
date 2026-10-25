from pathlib import Path

from spacekid import cli
from spacekid.scaffold import detect_mode, scaffold, scaffold_brain


def test_fresh_project_creates_all_three_files_with_name_from_pyproject(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "widgets"\n', encoding="utf-8")

    results = scaffold(tmp_path)

    assert [r.status for r in results] == ["created", "created", "created"]
    assert "Agent Guide — widgets" in (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert (tmp_path / "specs" / "AGENTS.md").exists()
    assert (tmp_path / "plans" / "AGENTS.md").exists()


def test_fresh_project_falls_back_to_directory_name(tmp_path: Path) -> None:
    project = tmp_path / "my-project"
    project.mkdir()

    scaffold(project)

    assert "Agent Guide — my-project" in (project / "AGENTS.md").read_text(encoding="utf-8")


def test_explicit_name_overrides_detection(tmp_path: Path) -> None:
    (tmp_path / "pyproject.toml").write_text('[project]\nname = "widgets"\n', encoding="utf-8")

    scaffold(tmp_path, app_name="override")

    assert "Agent Guide — override" in (tmp_path / "AGENTS.md").read_text(encoding="utf-8")


def test_existing_root_agents_md_is_left_untouched(tmp_path: Path) -> None:
    existing = "# My own AGENTS.md\n\ncustom content\n"
    (tmp_path / "AGENTS.md").write_text(existing, encoding="utf-8")

    results = scaffold(tmp_path)

    root_result = next(r for r in results if r.path.name == "AGENTS.md" and r.path.parent == tmp_path)
    assert root_result.status == "skipped"
    assert (tmp_path / "AGENTS.md").read_text(encoding="utf-8") == existing


def test_existing_specs_and_plans_agents_md_are_appended_to(tmp_path: Path) -> None:
    (tmp_path / "specs").mkdir()
    (tmp_path / "plans").mkdir()
    existing_specs = "# Our own spec rules\n\ndo it our way\n"
    existing_plans = "# Our own plan rules\n\ndo it our way\n"
    (tmp_path / "specs" / "AGENTS.md").write_text(existing_specs, encoding="utf-8")
    (tmp_path / "plans" / "AGENTS.md").write_text(existing_plans, encoding="utf-8")

    results = scaffold(tmp_path)

    statuses = {r.path.parent.name: r.status for r in results if r.path.name == "AGENTS.md"}
    assert statuses["specs"] == "appended"
    assert statuses["plans"] == "appended"

    specs_content = (tmp_path / "specs" / "AGENTS.md").read_text(encoding="utf-8")
    plans_content = (tmp_path / "plans" / "AGENTS.md").read_text(encoding="utf-8")
    assert specs_content.startswith(existing_specs)
    assert "Writing Specs" in specs_content
    assert plans_content.startswith(existing_plans)
    assert "Writing Implementation Plans" in plans_content


def test_missing_specs_and_plans_directories_are_created(tmp_path: Path) -> None:
    scaffold(tmp_path)

    assert (tmp_path / "specs" / "AGENTS.md").is_dir() is False
    assert (tmp_path / "specs" / "AGENTS.md").exists()
    assert (tmp_path / "plans" / "AGENTS.md").exists()


def _fake_repo(parent: Path, name: str) -> Path:
    repo = parent / name
    (repo / ".git").mkdir(parents=True)
    return repo


def test_detect_mode_two_repos_is_brain(tmp_path: Path) -> None:
    _fake_repo(tmp_path, "api")
    _fake_repo(tmp_path, "web")

    assert detect_mode(tmp_path) == "brain"


def test_detect_mode_one_or_no_repos_is_project(tmp_path: Path) -> None:
    assert detect_mode(tmp_path) == "project"
    _fake_repo(tmp_path, "api")
    assert detect_mode(tmp_path) == "project"


def test_detect_mode_directory_that_is_a_repo_is_project(tmp_path: Path) -> None:
    (tmp_path / ".git").mkdir()
    _fake_repo(tmp_path, "api")
    _fake_repo(tmp_path, "web")

    assert detect_mode(tmp_path) == "project"


def test_fresh_brain_creates_full_tree(tmp_path: Path) -> None:
    results = scaffold_brain(tmp_path)

    assert {r.status for r in results} == {"created"}
    brain = tmp_path / "brain"
    assert (brain / "AGENTS.md").is_file()
    assert (brain / "sdd" / "specs" / "AGENTS.md").is_file()
    assert (brain / "sdd" / "plans" / "AGENTS.md").is_file()
    assert (brain / "contexts" / ".gitkeep").is_file()
    assert (brain / "artifacts" / ".gitkeep").is_file()


def test_brain_sdd_rules_match_project_mode(tmp_path: Path) -> None:
    project = tmp_path / "p"
    brain_root = tmp_path / "b"
    project.mkdir()
    brain_root.mkdir()
    scaffold(project)
    scaffold_brain(brain_root)

    for kind in ("specs", "plans"):
        assert (project / kind / "AGENTS.md").read_text(encoding="utf-8") == (
            brain_root / "brain" / "sdd" / kind / "AGENTS.md"
        ).read_text(encoding="utf-8")


def test_existing_brain_agents_untouched_and_sdd_appended(tmp_path: Path) -> None:
    brain = tmp_path / "brain"
    (brain / "sdd" / "specs").mkdir(parents=True)
    (brain / "AGENTS.md").write_text("mine\n", encoding="utf-8")
    (brain / "sdd" / "specs" / "AGENTS.md").write_text("old\n", encoding="utf-8")

    results = scaffold_brain(tmp_path)

    statuses = {r.path.relative_to(brain).as_posix(): r.status for r in results}
    assert statuses["AGENTS.md"] == "skipped"
    assert statuses["sdd/specs/AGENTS.md"] == "appended"
    assert statuses["sdd/plans/AGENTS.md"] == "created"
    assert (brain / "AGENTS.md").read_text(encoding="utf-8") == "mine\n"
    assert (brain / "sdd" / "specs" / "AGENTS.md").read_text(encoding="utf-8").startswith("old\n")


def test_brain_agents_states_context_first_and_placement_rule(tmp_path: Path) -> None:
    scaffold_brain(tmp_path)
    text = (tmp_path / "brain" / "AGENTS.md").read_text(encoding="utf-8")

    assert "Context (mandatory first step)" in text
    assert "saved as a context" in text
    assert "is an artifact" in text
    assert "{{APP_NAME}}" not in text


def test_cli_mode_flag_overrides_detection(tmp_path: Path) -> None:
    cli.main(["init", "--path", str(tmp_path), "--mode", "brain"])
    assert (tmp_path / "brain" / "AGENTS.md").is_file()

    other = tmp_path / "ws"
    other.mkdir()
    _fake_repo(other, "api")
    _fake_repo(other, "web")
    cli.main(["init", "--path", str(other), "--mode", "project"])
    assert (other / "AGENTS.md").is_file()
    assert not (other / "brain").exists()


def test_cli_auto_selects_brain_for_multi_repo_directory(tmp_path: Path) -> None:
    _fake_repo(tmp_path, "api")
    _fake_repo(tmp_path, "web")

    cli.main(["init", "--path", str(tmp_path)])

    assert (tmp_path / "brain" / "AGENTS.md").is_file()


def _snapshot(root: Path) -> dict[str, str]:
    return {
        str(p.relative_to(root)): p.read_text(encoding="utf-8")
        for p in sorted(root.rglob("*"))
        if p.is_file()
    }


def test_project_second_run_changes_nothing(tmp_path: Path) -> None:
    scaffold(tmp_path)
    before = _snapshot(tmp_path)

    results = scaffold(tmp_path)

    assert {r.status for r in results} == {"skipped"}
    assert _snapshot(tmp_path) == before


def test_brain_second_run_changes_nothing(tmp_path: Path) -> None:
    scaffold_brain(tmp_path)
    before = _snapshot(tmp_path)

    results = scaffold_brain(tmp_path)

    assert {r.status for r in results} == {"skipped"}
    assert _snapshot(tmp_path) == before


def test_user_edits_around_the_rules_do_not_trigger_another_append(tmp_path: Path) -> None:
    scaffold(tmp_path)
    path = tmp_path / "specs" / "AGENTS.md"
    edited = "# Mine\n\n" + path.read_text(encoding="utf-8") + "\nextra notes\n"
    path.write_text(edited, encoding="utf-8")

    scaffold(tmp_path)

    assert path.read_text(encoding="utf-8") == edited
