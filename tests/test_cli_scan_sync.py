import subprocess
from pathlib import Path

import pytest

from spacekid import cli
from spacekid.scaffold import scaffold
from test_sync import _advance, _clone, _git


def _project(tmp_path: Path) -> Path:
    root = tmp_path / "proj"
    root.mkdir()
    scaffold(root, app_name="proj")
    return root


def test_scan_runs_the_miniverse_script(tmp_path: Path, capfd: pytest.CaptureFixture[str]) -> None:
    root = _project(tmp_path)
    (root / "miniverse" / "catalog.md").write_text("stale\n")

    assert cli.main(["scan", "--path", str(root)]) == 0

    assert "stale" not in (root / "miniverse" / "catalog.md").read_text()
    assert "catalog.md" in capfd.readouterr().out


def test_scan_accepts_the_miniverse_folder(tmp_path: Path) -> None:
    root = _project(tmp_path)
    assert cli.main(["scan", "--path", str(root / "miniverse")]) == 0


def test_sync_pulls_repositories(tmp_path: Path, capfd: pytest.CaptureFixture[str]) -> None:
    root = _project(tmp_path)
    repo, origin = _clone(root, "app")
    _advance(origin, tmp_path, "app")

    assert cli.main(["sync", "--path", str(root)]) == 0

    assert (repo / "b.txt").is_file()
    assert "updated" in capfd.readouterr().out


def test_sync_main_moves_repositories(tmp_path: Path) -> None:
    root = _project(tmp_path)
    repo, _ = _clone(root, "app")
    _git(repo, "checkout", "-q", "-b", "feature")

    assert cli.main(["sync", "--main", "--path", str(root)]) == 0

    assert _git(repo, "rev-parse", "--abbrev-ref", "HEAD") == "main"


def test_sync_exit_status_is_the_scripts(tmp_path: Path) -> None:
    root = _project(tmp_path)
    subprocess.run(["git", "init", "-q", str(root / "norem")], check=True)

    assert cli.main(["sync", "--path", str(root)]) == 1


@pytest.mark.parametrize("command", ["scan", "sync"])
def test_missing_miniverse_points_to_init(
    command: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert cli.main([command, "--path", str(tmp_path)]) == 1
    assert "spacekid init" in capsys.readouterr().err


@pytest.mark.parametrize("command", ["scan", "sync"])
def test_missing_script_points_to_init(
    command: str, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = _project(tmp_path)
    (root / "miniverse" / f"{command}.sh").unlink()

    assert cli.main([command, "--path", str(root)]) == 1
    assert "spacekid init" in capsys.readouterr().err
