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


def _lines(catalog: str) -> list[str]:
    return catalog.splitlines()


def test_fresh_miniverse_catalog_is_already_current(tmp_path: Path) -> None:
    scaffold(tmp_path, app_name="solo")
    mv = tmp_path / "miniverse"
    before = (mv / "catalog.md").read_text(encoding="utf-8")

    assert _scan(mv) == before
    assert "- Level: 0" in before
    assert "## Ancestors (nearest first)\n\nnone" in before
    assert "## Descendants\n\nnone" in before


def test_nested_miniverse_found_by_marker_even_if_folder_is_renamed(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    inner = tmp_path / "backend"
    inner.mkdir()
    _mv(inner, "backend", folder="knowledge-base")

    catalog = _scan(top)

    assert "`../backend/knowledge-base` — backend (level 1, parent `.`)" in catalog


def test_unmarked_folder_named_miniverse_is_not_a_miniverse(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    (tmp_path / "x" / "miniverse").mkdir(parents=True)

    assert "- Descendants: 0" in _scan(top)


def test_contexts_and_specs_are_listed_with_summary_status_and_dates(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    inner = tmp_path / "api"
    inner.mkdir()
    api = _mv(inner, "api")
    _context(api, "auth", "how tokens work")
    _spec(api, "login", "Approved")

    catalog = _scan(top)

    assert (
        "- `../api/miniverse/contexts/auth.md` — Auth — how tokens work "
        "(created 2026-01-01, updated 2026-02-02)"
    ) in catalog
    assert (
        "- `../api/miniverse/sdd/specs/login.md` — Login — Approved "
        "(created 2026-03-03, updated 2026-04-04)"
    ) in catalog
    assert "AGENTS.md" not in catalog


def test_missing_header_fields_show_question_mark(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    inner = tmp_path / "api"
    inner.mkdir()
    api = _mv(inner, "api")
    (api / "contexts" / "bare.md").write_text("# Bare\n", encoding="utf-8")

    assert "— Bare — ? (created ?, updated ?)" in _scan(top)


def test_four_level_hierarchy_from_every_node(tmp_path: Path) -> None:
    #  top ── mid ── leaf
    #     └── side
    top = _mv(tmp_path, "top")
    (tmp_path / "mid").mkdir()
    mid = _mv(tmp_path / "mid", "mid")
    (tmp_path / "mid" / "leaf").mkdir()
    leaf = _mv(tmp_path / "mid" / "leaf", "leaf")
    (tmp_path / "side").mkdir()
    side = _mv(tmp_path / "side", "side")
    _context(mid, "mid-ctx", "mid knowledge")
    _spec(top, "root-rule", "Implemented")

    top_cat, mid_cat, leaf_cat, side_cat = (_scan(m) for m in (top, mid, leaf, side))

    assert "- Level: 0" in top_cat and "- Descendants: 3" in top_cat
    tree = [ln for ln in _lines(top_cat) if ln.lstrip().startswith("- `../") and "(level" in ln]
    assert tree == [
        "- `../mid/miniverse` — mid (level 1, parent `.`)",
        "  - `../mid/leaf/miniverse` — leaf (level 2, parent `../mid/miniverse`)",
        "- `../side/miniverse` — side (level 1, parent `.`)",
    ]

    assert "- Level: 1" in mid_cat and "- Ancestors: 1" in mid_cat
    assert "1. `../../miniverse` — top (level 0)" in mid_cat
    assert "- `../leaf/miniverse` — leaf (level 2, parent `.`)" in mid_cat
    assert "`../../miniverse/sdd/specs/root-rule.md` — Root-Rule — Implemented" in mid_cat

    assert "- Level: 2" in leaf_cat
    assert "1. `../../miniverse` — mid (level 1)" in leaf_cat
    assert "2. `../../../miniverse` — top (level 0)" in leaf_cat
    assert leaf_cat.index("— mid (level 1)") < leaf_cat.index("— top (level 0)")
    assert "mid knowledge" in leaf_cat

    assert "- Level: 1" in side_cat and "- Descendants: 0" in side_cat
    assert "1. `../../miniverse` — top (level 0)" in side_cat


def test_catalog_paths_resolve_from_the_miniverse_folder(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    (tmp_path / "a" / "b").mkdir(parents=True)
    a = _mv(tmp_path / "a", "a")
    b = _mv(tmp_path / "a" / "b", "b")
    _context(b, "deep", "deep one")
    _spec(a, "s", "Draft")

    for origin in (top, a, b):
        catalog = _scan(origin)
        paths = [seg for ln in _lines(catalog) for seg in ln.split("`")[1::2] if seg.startswith(".")]
        assert paths
        for rel in paths:
            assert (origin / rel).exists(), f"{rel} from {origin}"


def test_ignored_directories_are_pruned(tmp_path: Path) -> None:
    top = _mv(tmp_path, "top")
    for ignored in (".git", "node_modules", ".venv", "venv", "dist", "build", "target", "__pycache__"):
        hidden = tmp_path / ignored / "pkg"
        hidden.mkdir(parents=True)
        _mv(hidden, "hidden")

    assert "- Descendants: 0" in _scan(top)


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
