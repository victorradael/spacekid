from pathlib import Path

import pytest

from spacekid import cli


def test_spacekid_and_sk_resolve_to_the_same_callable() -> None:
    tomllib = pytest.importorskip("tomllib")
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    scripts = tomllib.loads(pyproject.read_text(encoding="utf-8"))["project"]["scripts"]

    assert scripts["spacekid"] == scripts["sk"] == "spacekid.cli:main"
    assert cli.main is not None


def test_version_flag_reports_installed_version(capsys: pytest.CaptureFixture[str]) -> None:
    from importlib.metadata import version

    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])

    assert exc.value.code == 0
    assert capsys.readouterr().out.strip() == f"spacekid {version('spacekid')}"
