import pytest

from spacekid import cli


def test_version_flag_reports_installed_version(capsys: pytest.CaptureFixture[str]) -> None:
    from importlib.metadata import version

    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])

    assert exc.value.code == 0
    assert capsys.readouterr().out.strip() == f"spacekid {version('spacekid')}"
