# CLI Visual Experience — Implementation Plan

Implements: `sdd/specs/cli-ui.md`
Status: Done

## Approach

Add one small module, `src/spacekid/ui.py`, using only ANSI escape codes and
the standard library (no new dependency). `cli.py` calls into it for the
banner, menu, and colored result lines.

## Steps

1. `ui.py`:
   - `supports_color()`: true only if stdout is a TTY, `NO_COLOR` is unset,
     and `TERM` is not `dumb`.
   - `paint()`: wraps text in 256-color/bold/dim codes; returns plain text
     when color is unsupported.
   - `banner(version)`: ASCII-art "SPACEKID" with a per-line gradient plus
     tagline and version.
   - `status_line()` (and, originally, `heading()`, since removed with the modes): icon + color per `created` / `appended` /
     `skipped`.
   - `render_menu()` / `choose_from_menu()`: numbered menu
     (init, about, quit; originally init auto, init project,
     init brain, about, quit — reduced by the miniverse plan) with an input loop
     that re-prompts on invalid input and treats EOF/Ctrl-C as quit.
2. `cli.py`:
   - Make the subcommand optional. With no command: interactive (color TTY on
     stdin and stdout) → menu; otherwise print help and return 0.
   - Print the banner before `init` only when color is supported. (Revised
     2026-10-29: the big banner is only for the main command; see below.)
   - `_init` uses colored output when supported, and the existing plain
     `label: path` lines otherwise, so scripts and tests are unaffected.
3. Tests (`tests/test_ui.py`): `supports_color` honors `NO_COLOR`/non-TTY;
   `paint` is identity without color; no-arg invocation prints help and
   returns 0 when non-interactive; menu rejects invalid input then accepts a
   valid one (monkeypatched `input` and `supports_color`).
4. Update `README.md` usage with the menu; mark this plan and spec done.

## Key Decisions

- **No dependency (Rich/Click).** A banner, a menu, and a few colored lines
  don't justify one (KISS); the package stays dependency-free.
- **Plain output is the default off-TTY**, preserving the current output
  format that tests and scripts rely on.
- **Menu delegates to `_init`** rather than duplicating scaffolding logic.

## Implementation Notes

Implemented as planned, with these deviations:

- `supports_color()` delegates the TTY check to a small `_stdout_is_tty()`
  helper. Pytest swaps `sys.stdout` between test phases, so patching the
  stream directly was unreliable; patching the helper is.
- `choose_from_menu()` resolves `input` at call time (not as a default
  argument) so it can be monkeypatched.
- The menu's init options run against the current directory with the
  auto-detected name; no path/name prompts were added (KISS).
- Typing the action word (`init`, `about`, `quit`; originally `auto`, `project`, `brain`) is
  accepted in addition to the number.
- Tests also cover the menu running init/about/quit and plain piped `init`
  output. No other spec/plan pair needed changes; `init` output off-TTY is
  unchanged.
- Distribution is container-only, and the documented alias ran `docker run`
  without a TTY, so the UI (correctly) fell back to plain output. The alias
  in `README.md` and `DOCKERHUB.md` now uses `-it` and passes `-e NO_COLOR`.
  Scripts and CI that pipe output should call `docker run` without `-it`.
- The banner is also printed before `--help` output (via a small
  `ArgumentParser.print_help` override) whenever color is supported, so users
  see it on the most common first command.

- 2026-10-29 (pending approval of `sdd/specs/cli-ui.md`): the big banner is
  shown only by the main command (the menu, and the root `--help`).
  `ui.mark(label)` renders a one-line gradient mark, used by `spacekid init`
  and `init --help` (`_Parser.mark_label`). The menu's `about` and `init` no
  longer reprint a logo after the menu showed the big one (`_init` takes a
  `mark` flag). `scan.sh` and `sync.sh` use the same mark.
