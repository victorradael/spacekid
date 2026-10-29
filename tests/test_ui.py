from pathlib import Path

import pytest

from spacekid import cli, ui


@pytest.fixture
def tty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setenv("TERM", "xterm-256color")
    monkeypatch.setattr(ui, "_stdout_is_tty", lambda: True)


def test_supports_color_on_tty(tty: None) -> None:
    assert ui.supports_color() is True


def test_supports_color_honors_no_color(tty: None, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    assert ui.supports_color() is False


def test_supports_color_false_for_dumb_terminal(tty: None, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TERM", "dumb")
    assert ui.supports_color() is False


def test_supports_color_false_when_not_a_tty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("NO_COLOR", raising=False)
    monkeypatch.setattr(ui, "_stdout_is_tty", lambda: False)
    assert ui.supports_color() is False


def test_paint_is_identity_without_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ui, "supports_color", lambda: False)
    assert ui.paint("hello", 42, bold=True) == "hello"
    assert ui.status_line("created", "AGENTS.md") == "✔ created AGENTS.md"


def test_paint_adds_codes_with_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ui, "supports_color", lambda: True)
    assert ui.paint("hi", 42).startswith("\033[")


def test_no_args_non_interactive_prints_help(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(ui, "is_interactive", lambda: False)

    assert cli.main([]) == 0

    out = capsys.readouterr().out
    assert "usage: spacekid" in out
    assert "\033[" not in out


def test_piped_init_output_is_plain(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    cli.main(["init", "--path", str(tmp_path)])

    out = capsys.readouterr().out
    assert "\033[" not in out
    assert "mode" not in out
    assert "created: AGENTS.md" in out
    assert "created: miniverse/AGENTS.md" in out


def test_menu_rejects_invalid_input_then_accepts_valid(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(ui, "supports_color", lambda: False)
    answers = iter(["9", "nope", "1"])
    output: list[str] = []

    choice = ui.choose_from_menu(read=lambda _: next(answers), write=output.append)

    assert choice == "init"
    assert sum("Invalid choice" in line for line in output) == 2


def test_menu_treats_eof_as_quit(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(ui, "supports_color", lambda: False)

    def raise_eof(_: str) -> str:
        raise EOFError

    assert ui.choose_from_menu(read=raise_eof, write=lambda _: None) == "quit"


def test_interactive_menu_runs_init(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(ui, "is_interactive", lambda: True)
    monkeypatch.setattr(ui, "supports_color", lambda: False)
    monkeypatch.setattr("builtins.input", lambda _="": "1")

    assert cli.main([]) == 0

    assert (tmp_path / "AGENTS.md").is_file()
    assert (tmp_path / "miniverse" / "AGENTS.md").is_file()
    assert "created: AGENTS.md" in capsys.readouterr().out


def test_interactive_menu_about_and_quit(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(ui, "is_interactive", lambda: True)
    monkeypatch.setattr(ui, "supports_color", lambda: False)

    monkeypatch.setattr("builtins.input", lambda _="": "4")
    assert cli.main([]) == 0
    assert "SpaceKid creates a miniverse" in capsys.readouterr().out

    monkeypatch.setattr("builtins.input", lambda _="": "5")
    assert cli.main([]) == 0


def test_help_shows_banner_with_color(tty: None, capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        cli.main(["--help"])

    out = capsys.readouterr().out
    assert "\033[" in out
    assert "usage: spacekid" in out


def test_help_has_no_banner_without_color(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit):
        cli.main(["init", "--help"])

    out = capsys.readouterr().out
    assert "\033[" not in out
    assert "|_" not in out


def test_big_logo_only_on_the_main_command(
    tty: None, monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    with pytest.raises(SystemExit):
        cli.main(["--help"])
    main_help = capsys.readouterr().out

    with pytest.raises(SystemExit):
        cli.main(["init", "--help"])
    init_help = capsys.readouterr().out

    cli.main(["init", "--path", str(tmp_path)])
    init_run = capsys.readouterr().out

    monkeypatch.setattr(ui, "is_interactive", lambda: True)
    monkeypatch.setattr("builtins.input", lambda _="": "2")
    cli.main([])
    menu_about = capsys.readouterr().out

    assert "|_" in main_help
    assert "|_" in menu_about and menu_about.count("a minimalist spec kit") == 1
    for compact in (init_help, init_run):
        assert "|_" not in compact
        assert "✦" in compact
