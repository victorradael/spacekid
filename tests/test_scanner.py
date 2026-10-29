import subprocess
from pathlib import Path

from spacekid.scaffold import scaffold


def _mv(directory: Path, name: str, folder: str = "miniverse") -> Path:
    """Create a minimal miniverse in `directory`; return the miniverse folder."""
    scaffold(directory, app_name=name)
    mv = directory / "miniverse"
    if folder != "miniverse":
        mv = mv.rename(directory / folder)
    return mv


def _scan(mv: Path) -> str:
    subprocess.run([str(mv / "scan.sh")], check=True, capture_output=True, cwd=mv)
    return (mv / "catalog.md").read_text(encoding="utf-8")


def _context(mv: Path, name: str, summary: str) -> None:
    (mv / "contexts" / f"{name}.md").write_text(
        f"# {name.title()}\n\nSummary: {summary}\nCreated: 2026-01-01\nUpdated: 2026-02-02\n",
        encoding="utf-8",
    )


def _spec(mv: Path, name: str, status: str) -> None:
    (mv / "sdd" / "specs" / f"{name}.md").write_text(
        f"# {name.title()}\n\nStatus: {status}\nCreated: 2026-03-03\nUpdated: 2026-04-04\n",
        encoding="utf-8",
    )


def _tree(catalog: str) -> list[str]:
    return [ln for ln in catalog.splitlines() if ln.lstrip().startswith("- `../")]


def _lines(catalog: str) -> list[str]:
    return catalog.splitlines()


def test_fresh_miniverse_catalog_is_already_current(tmp_path: Path) -> None:
    scaffold(tmp_path, app_name="solo")
    mv = tmp_path / "miniverse"
    before = (mv / "catalog.md").read_text(encoding="utf-8")

    assert _scan(mv) == before
    assert "## Nested miniverses\n\nnone" in before


def test_nested_miniverse_found_by_marker_even_if_folder_is_renamed(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    inner = tmp_path / "backend"
    inner.mkdir()
    _mv(inner, "backend", folder="knowledge-base")

    assert "- `../backend/knowledge-base` — backend\n" in _scan(top)


def test_unmarked_folder_named_miniverse_is_not_a_miniverse(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    (tmp_path / "x" / "miniverse").mkdir(parents=True)

    assert "## Nested miniverses\n\nnone" in _scan(top)


def test_catalog_holds_only_paths_never_contexts_specs_or_ancestors(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    inner = tmp_path / "api"
    inner.mkdir()
    api = _mv(inner, "api")
    _context(api, "auth", "how tokens work")
    _spec(api, "login", "Approved")
    _context(top, "own", "top knowledge")

    catalog = _scan(top)
    api_catalog = _scan(api)

    assert "- `../api/miniverse` — api" in catalog
    for leaked in ("auth", "login", "how tokens work", "Approved", "own", "created", "Level", "Ancestors"):
        assert leaked not in catalog.split("## Nested miniverses")[1], leaked
    assert "top" not in api_catalog.split("## Nested miniverses")[1]
    assert "## Nested miniverses\n\nnone" in api_catalog


def test_hierarchy_is_an_indented_tree_of_paths(tmp_path: Path) -> None:
    #  top ── mid ── leaf
    #     └── side
    top = _mv(tmp_path, "top")
    (tmp_path / "mid" / "leaf").mkdir(parents=True)
    mid = _mv(tmp_path / "mid", "mid")
    _mv(tmp_path / "mid" / "leaf", "leaf")
    (tmp_path / "side").mkdir()
    _mv(tmp_path / "side", "side")

    assert _tree(_scan(top)) == [
        "- `../mid/miniverse` — mid",
        "  - `../mid/leaf/miniverse` — leaf",
        "- `../side/miniverse` — side",
    ]
    assert _tree(_scan(mid)) == ["- `../leaf/miniverse` — leaf"]


def test_catalog_paths_resolve_from_the_miniverse_folder(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    (tmp_path / "a" / "b").mkdir(parents=True)
    a = _mv(tmp_path / "a", "a")
    _mv(tmp_path / "a" / "b", "b")

    for origin in (top, a):
        paths = [seg for ln in _tree(_scan(origin)) for seg in ln.split("`")[1::2]]
        assert paths
        for rel in paths:
            assert (origin / rel / "AGENTS.md").exists(), f"{rel} from {origin}"


def test_ignored_directories_are_pruned(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    for ignored in (".git", "node_modules", ".venv", "venv", "dist", "build", "target", "__pycache__"):
        hidden = tmp_path / ignored / "pkg"
        hidden.mkdir(parents=True)
        _mv(hidden, "hidden")

    assert "## Nested miniverses\n\nnone" in _scan(top)


def test_second_run_is_byte_identical(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    (tmp_path / "a" / "b").mkdir(parents=True)
    _mv(tmp_path / "a", "a")
    _mv(tmp_path / "a" / "b", "b")

    first = _scan(top)
    result = subprocess.run([str(top / "scan.sh")], capture_output=True, text=True, cwd=top)

    assert (top / "catalog.md").read_text(encoding="utf-8") == first
    assert "unchanged" in result.stdout
    assert not [p for p in top.iterdir() if p.name.startswith(".scan.")]


def test_script_works_without_spacekid_from_any_directory(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    (tmp_path / "a").mkdir()
    _mv(tmp_path / "a", "a")

    subprocess.run(["sh", str(top / "scan.sh")], check=True, capture_output=True, cwd="/", env={"PATH": "/usr/bin:/bin"})

    assert "`../a/miniverse` — a" in (top / "catalog.md").read_text(encoding="utf-8")
