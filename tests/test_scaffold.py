from pathlib import Path

from spacekid.scaffold import scaffold


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
