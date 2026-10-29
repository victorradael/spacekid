import os
import subprocess
from pathlib import Path

from spacekid.scaffold import scaffold

_GIT_ENV = {
    **os.environ,
    "GIT_AUTHOR_NAME": "t",
    "GIT_AUTHOR_EMAIL": "t@t",
    "GIT_COMMITTER_NAME": "t",
    "GIT_COMMITTER_EMAIL": "t@t",
}


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, check=True, capture_output=True, text=True, env=_GIT_ENV
    ).stdout.strip()


def _clone(parent: Path, name: str) -> tuple[Path, Path]:
    """Create repo `name` under `parent` with a bare origin; return (repo, origin)."""
    origin = parent.parent / f"{parent.name}-{name}-origin.git"
    _git(parent.parent, "init", "-q", "--bare", "-b", "main", str(origin))
    repo = parent / name
    _git(parent.parent, "clone", "-q", str(origin), str(repo))
    _git(repo, "checkout", "-q", "-b", "main")
    (repo / "a.txt").write_text("1\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "one")
    _git(repo, "push", "-q", "-u", "origin", "main")
    return repo, origin


def _advance(origin: Path, tmp: Path, name: str) -> None:
    """Push a new commit to `origin` from a throwaway clone."""
    other = tmp / f"other-{name}"
    _git(tmp, "clone", "-q", str(origin), str(other))
    (other / "b.txt").write_text("2\n")
    _git(other, "add", ".")
    _git(other, "commit", "-q", "-m", "two")
    _git(other, "push", "-q", "origin", "main")


def _sync(mv: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [str(mv / "sync.sh"), *args], capture_output=True, text=True, cwd=mv, env=_GIT_ENV, stdin=subprocess.DEVNULL
    )


def _workspace(tmp_path: Path) -> Path:
    ws = tmp_path / "ws"
    ws.mkdir()
    scaffold(ws, app_name="ws")
    return ws / "miniverse"


def test_logs_branch_and_pulls_each_sibling_repository(tmp_path: Path) -> None:
    mv = _workspace(tmp_path)
    api, api_origin = _clone(mv.parent, "api")
    web, _ = _clone(mv.parent, "web")
    _advance(api_origin, tmp_path, "api")

    result = _sync(mv)

    assert result.returncode == 0, result.stdout
    assert "../api  branch=main\n  updated" in result.stdout
    assert "../web  branch=main\n  up to date" in result.stdout
    assert (api / "b.txt").exists()
    assert "2 repositories, all up to date" in result.stdout


def test_repositories_at_every_nested_level_are_found_through_the_catalog(tmp_path: Path) -> None:
    mv = _workspace(tmp_path)
    mid = mv.parent / "mid"
    (mid / "leaf").mkdir(parents=True)
    scaffold(mid, app_name="mid")
    scaffold(mid / "leaf", app_name="leaf")
    _clone(mid, "svc")
    _clone(mid / "leaf", "deep")

    result = _sync(mv)

    assert "../mid/svc  branch=main" in result.stdout
    assert "../mid/leaf/deep  branch=main" in result.stdout


def test_main_option_moves_clean_repos_and_skips_dirty_ones(tmp_path: Path) -> None:
    mv = _workspace(tmp_path)
    clean, _ = _clone(mv.parent, "clean")
    dirty, _ = _clone(mv.parent, "dirty")
    for repo in (clean, dirty):
        _git(repo, "checkout", "-q", "-b", "feature")
    (dirty / "a.txt").write_text("uncommitted\n")

    result = _sync(mv, "--main")

    assert _git(clean, "branch", "--show-current") == "main"
    assert "../clean  branch=feature -> main" in result.stdout
    assert _git(dirty, "branch", "--show-current") == "feature"
    assert (dirty / "a.txt").read_text() == "uncommitted\n"
    assert "../dirty  branch=feature  skipped: uncommitted changes" in result.stdout
    assert result.returncode == 1


def test_a_problem_in_one_repository_does_not_stop_the_others(tmp_path: Path) -> None:
    mv = _workspace(tmp_path)
    broken = mv.parent / "a-broken"
    _git(mv.parent, "init", "-q", "-b", "main", str(broken))
    _clone(mv.parent, "ok")

    result = _sync(mv)

    assert "../a-broken  branch=main\n  failed:" in result.stdout
    assert "../ok  branch=main\n  up to date" in result.stdout
    assert "1 need attention" in result.stdout
    assert result.returncode == 1


def test_diverged_branch_is_not_merged(tmp_path: Path) -> None:
    mv = _workspace(tmp_path)
    repo, origin = _clone(mv.parent, "api")
    _advance(origin, tmp_path, "api")
    (repo / "c.txt").write_text("local\n")
    _git(repo, "add", ".")
    _git(repo, "commit", "-q", "-m", "local")
    head = _git(repo, "rev-parse", "HEAD")

    result = _sync(mv)

    assert result.returncode == 1
    assert _git(repo, "rev-parse", "HEAD") == head


def test_unknown_option_prints_usage(tmp_path: Path) -> None:
    result = _sync(_workspace(tmp_path), "--nope")

    assert result.returncode == 2
    assert "usage" in result.stderr


def test_works_without_spacekid_from_any_directory(tmp_path: Path) -> None:
    mv = _workspace(tmp_path)
    _clone(mv.parent, "api")
    path = os.environ["PATH"]

    result = subprocess.run(
        ["sh", str(mv / "sync.sh")], capture_output=True, text=True, cwd="/", env={**_GIT_ENV, "PATH": path}
    )

    assert "../api  branch=main" in result.stdout
    assert not [p for p in mv.iterdir() if p.name.startswith(".sync.")]


def _run_on_terminal(script: Path, extra_env: dict[str, str] | None = None) -> str:
    import pty

    env = {**_GIT_ENV, "TERM": "xterm-256color", **(extra_env or {})}
    pid, fd = pty.fork()
    if pid == 0:
        os.chdir(script.parent)
        os.execve("/bin/sh", ["sh", str(script)], env)
    out = b""
    while True:
        try:
            chunk = os.read(fd, 4096)
        except OSError:
            break
        if not chunk:
            break
        out += chunk
    os.waitpid(pid, 0)
    return out.decode()


def test_output_is_colorful_on_a_terminal_and_plain_otherwise(tmp_path: Path) -> None:
    mv = _workspace(tmp_path)
    _clone(mv.parent, "api")

    colored = _run_on_terminal(mv / "sync.sh")
    opted_out = _run_on_terminal(mv / "sync.sh", {"NO_COLOR": "1"})
    piped = _sync(mv).stdout

    assert "\033[" in colored and "◆" in colored and "✔" in colored
    assert "✦" in colored and "repository sync" in colored
    assert "____" not in colored  # compact mark, not the big logo
    assert "\033[" not in opted_out and "◆" not in opted_out and "✦" not in opted_out
    assert "\033[" not in piped and "✦" not in piped


def test_scan_output_is_colorful_on_a_terminal_and_plain_otherwise(tmp_path: Path) -> None:
    mv = _workspace(tmp_path)

    colored = _run_on_terminal(mv / "scan.sh")
    opted_out = _run_on_terminal(mv / "scan.sh", {"NO_COLOR": "1"})
    piped = subprocess.run([str(mv / "scan.sh")], capture_output=True, text=True).stdout

    assert "\033[" in colored and "catalog.md unchanged" in colored and "✦" in colored and "____" not in colored
    assert "\033[" not in opted_out and "\033[" not in piped
    assert piped == "catalog.md unchanged\n"
