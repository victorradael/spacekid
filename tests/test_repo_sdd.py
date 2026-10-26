"""SpaceKid follows its own workflow: its specs and plans live in its miniverse."""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MINIVERSE = ROOT / "miniverse"
_DATE = r"\d{4}-\d{2}-\d{2}"


def _docs(kind: str) -> list[Path]:
    return sorted(p for p in (MINIVERSE / "sdd" / kind).glob("*.md") if p.name != "AGENTS.md")


def test_no_specs_or_plans_remain_outside_the_miniverse() -> None:
    assert not (ROOT / "specs").exists()
    assert not (ROOT / "plans").exists()


def test_every_spec_has_dates_and_traceability() -> None:
    specs = _docs("specs")
    assert specs
    for spec in specs:
        text = spec.read_text(encoding="utf-8")
        assert re.search(rf"(?m)^Created: {_DATE}$", text), spec.name
        assert re.search(rf"(?m)^Updated: {_DATE}$", text), spec.name
        assert "\n## Traceability\n" in text, spec.name


def test_traceability_entries_are_dated_and_point_to_existing_files() -> None:
    for spec in _docs("specs"):
        section = spec.read_text(encoding="utf-8").split("## Traceability", 1)[1]
        for path, added in re.findall(rf"`([^`]+)` \(added ({_DATE})\)", section):
            assert (MINIVERSE / path).is_file(), f"{spec.name}: {path}"
        for line in section.splitlines():
            if line.startswith("- ") and "—" not in line.split(":", 1)[1][:3]:
                assert re.search(r"\(added ", line), f"{spec.name}: undated entry: {line}"


def test_every_spec_has_a_plan_that_is_registered() -> None:
    for plan in _docs("plans"):
        spec = MINIVERSE / "sdd" / "specs" / plan.name
        assert spec.is_file(), plan.name
        assert f"`sdd/plans/{plan.name}`" in spec.read_text(encoding="utf-8")


def test_root_agents_points_to_the_miniverse() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

    assert "miniverse/AGENTS.md" in text
    assert len(text.splitlines()) < 40


def test_own_catalog_is_current() -> None:
    before = (MINIVERSE / "catalog.md").read_text(encoding="utf-8")

    subprocess.run([str(MINIVERSE / "scan.sh")], check=True, capture_output=True)

    assert (MINIVERSE / "catalog.md").read_text(encoding="utf-8") == before
