# CLI Visual Experience — Implementation Plan

Implements: `specs/cli-ui.md`
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
   - `status_line()` / `heading()`: icon + color per `created` / `appended` /
     `skipped`.
   - `render_menu()` / `choose_from_menu()`: numbered menu
     (init auto, init project, init brain, about, quit) with an input loop
     that re-prompts on invalid input and treats EOF/Ctrl-C as quit.
2. `cli.py`:
   - Make the subcommand optional. With no command: interactive (color TTY on
     stdin and stdout) → menu; otherwise print help and return 0.
   - Print the banner before `init` only when color is supported.
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
- Typing the action word (`auto`, `project`, `brain`, `about`, `quit`) is
  accepted in addition to the number.
- Tests also cover the menu running init/about/quit and plain piped `init`
  output. No other spec/plan pair needed changes; `init` output off-TTY is
  unchanged.
