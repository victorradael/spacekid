# CLI Scan and Sync — Implementation Plan

Implements: `sdd/specs/cli-scan-sync.md`
Status: Done

## Approach

`spacekid scan` and `spacekid sync` are thin launchers: they locate the
miniverse's `scan.sh` / `sync.sh` and run them with inherited stdio, returning
the script's exit code. The scripts stay the single implementation (standalone,
no duplicated logic), so output, colors and exit codes are identical by
construction.

## Steps

1. **Launcher** (`cli.py`): `_find_miniverse(path)` returns `path` if it holds
   `.miniverse`, else `path/miniverse` if it does, else none. `_run_script(
   args, script, extra)` resolves it, runs `subprocess.run([sh, script,
   *extra])` with no captured output and returns `returncode`. Missing
   miniverse or script: message on stderr naming the path and suggesting
   `spacekid init`, return `1`.
2. **Parsers**: `scan` (`--path`) and `sync` (`--path`, `--main`), each with a
   `mark_label`-less help (the scripts print their own one-line mark).
3. **Menu** (`ui.py`/`cli.py`): add `scan` and `sync` entries; `sync` runs
   without `--main`.
4. **Dockerfile**: install `git` (needed by `sync.sh`); mark mounted project as
   safe directory is out of scope.
5. **Tests**: `tests/test_cli_scan_sync.py` using scaffolded temp miniverses:
   scan rewrites the catalog; sync pulls a repo (reuse helpers from
   `test_sync.py`); `--main`; both path forms; exit code passthrough (bad
   repo → 1); missing miniverse / missing script → 1 with hint.
6. **Docs**: README and DOCKERHUB usage sections.
7. **Close the loop**: statuses, Traceability, Updated dates, architecture
   context.

## Key Decisions

- **Run the miniverse's script, not an embedded copy.** Keeps a single source
  of truth and respects scripts the user already has. Trade-off: miniverses
  created before the scripts existed need `spacekid init` first (it adds
  missing files without touching existing ones).

## Implementation Notes

- Followed the plan. The interactive menu was renumbered (init, scan, sync,
  about, quit). Scripts run via `sh <script>`, so the executable bit is not
  required. Because the child writes to the real stdout, tests capture with
  `capfd`.
