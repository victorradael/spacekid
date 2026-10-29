# Repository Sync — Implementation Plan

Implements: `sdd/specs/repo-sync.md`
Status: Draft

## Approach

A second standalone POSIX `sh` script, `sync.sh`, shipped next to `scan.sh`
from `src/spacekid/templates/`. Same reasons as the scanner: container-only
distribution must not be required during agent work, and the script must keep
working after the miniverse is copied elsewhere. It only shells out to `git`
and `scan.sh`.

## Steps

1. **Script** (`templates/sync.sh`, copied to `miniverse/sync.sh`):
   - Covered root = parent of the script's own directory (as in `scan.sh`).
   - Discovery uses `catalog.md`: run `./scan.sh` first to refresh it, read
     the nested miniverse paths from it, and take the directory above each
     (its covered directory) plus the root. Each such level directory and its
     direct subdirectories are candidates; those holding a `.git` (directory
     or file, so worktrees and submodules count) are repositories. No
     file-tree crawl. Sorted with `LC_ALL=C` for stable output.
   - Per repository, with `GIT_TERMINAL_PROMPT=0` and `git -C`:
     1. read the branch (`symbolic-ref --short -q HEAD`; detached HEAD is
        reported as `detached @ <sha>` and not pulled);
     2. with `--main` and branch ≠ `main`: if the tree is dirty
        (`status --porcelain` non-empty) report and skip; otherwise
        `git checkout main` (which also tracks `origin/main` when only the
        remote has it); failure is reported;
     3. `git pull --ff-only` (no merge commits, no prompts).
   - One output line per repository: path relative to the miniverse folder
     (root repository is `..`), branch, and result (`updated`, `up to date`,
     or the reason it was skipped/failed).
   - A failure never aborts the loop. Final summary line with counts; exit
     status `1` when any repository failed or was skipped for a problem.
   - Unknown option → usage message, exit `2`.
2. **Scaffold**: write `miniverse/sync.sh` with `write_or_skip(...,
   executable=True)`.
3. **Guide** (`templates/miniverse_agents.md`, mirrored in
   `miniverse/AGENTS.md`): add `sync.sh` to the map; in Context step 0, run
   `./sync.sh` before reading the state of the projects (mention
   `./sync.sh --main`); add the rule "Never read the state of the projects
   without running `./sync.sh` first".
4. **Tests** (`tests/test_sync.py`, real `git` in `tmp_path` with a bare
   remote): branch reported and pull applied; repos at every nested miniverse level found via the catalog;
   `--main` switches branch and pulls; dirty repo stays on its branch and is
   reported; repo without remote reported while others still run; exit status
   and summary; no input needed; works from `/` with minimal `PATH`;
   scaffold creates it executable and never overwrites it.
4b. **Presentation** (both `sync.sh` and `scan.sh`): same palette as `ui.py`
   with a one-line `✦ SPACEKID · <command>` mark (the big ASCII logo stays in
   the main `spacekid` command only; 256-color gradient, `✔` green, `•` gray, `✘` red, `◆`
   repository marker). Color is on only when stdout is a TTY, `NO_COLOR` is
   unset and `TERM` is not `dumb` (same rule as `ui.supports_color`);
   otherwise the plain text format is unchanged. The helpers are duplicated in
   each script because each must stay standalone. Tests run the scripts under a
   pty.
5. **Docs**: README and DOCKERHUB layout and a short section on `sync.sh`.
6. **Close the loop**: statuses, Traceability, Updated dates, architecture
   context.

## Key Decisions

- **`--ff-only`.** Never creates merges and never needs a decision; a diverged
  branch is reported for a human. Trade-off: some repositories need manual
  attention.
- **`--main` skips dirty repositories instead of stashing.** Protects work in
  progress; stashing would silently move it.
- **Fixed branch name `main`.** Matches the spec; `master` is out of scope.
- **Not a `spacekid` subcommand.** Same reasoning as `scan.sh`.

## Implementation Notes

- Discovery went through `catalog.md` (user request during the work) instead
  of a full `find` for `.git`, so repositories nested inside plain
  directories below a level are not visited: only a level's own directory and
  its direct subdirectories. This matches the miniverse model, where deeper
  levels carry their own miniverse.
- Companion change (see `sdd/specs/miniverse.md`, updated 2026-10-29): the
  catalog now lists only nested miniverse paths, which `sync.sh` and agents
  consume. Ancestors, levels, and per-miniverse contexts/specs were removed
  from `scan.sh`. Consequence: an agent in a lower miniverse no longer sees
  higher-level specs through the catalog; conflicts are caught from the
  higher level, which reads its nested miniverses.
- The `main` fallback is `git checkout main` only; `master` is out of scope.
