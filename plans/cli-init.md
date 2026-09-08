# CLI Init — Implementation Plan

Implements: `specs/cli-init.md`
Status: Done

## Approach

Package SpaceKid as a standard `src/`-layout Python package built with a
`pyproject.toml` (setuptools backend, no build-time dependency beyond
setuptools). Expose one console-script entry point, `spacekid`, with a single
subcommand, `init`, implemented with the standard-library `argparse` — no
CLI framework dependency is justified for one subcommand with two optional
flags.

The three files SpaceKid scaffolds are shipped as package data (plain
Markdown template files under `spacekid/templates/`) and are read with
`importlib.resources` at run time, so the installed wheel is the single
source of truth and there's no risk of the CLI's copy drifting from the
version checked into this repo's own root/`specs`/`plans` `AGENTS.md` files.

This keeps the whole feature to: package metadata, one CLI module, three
template files, and a scaffolding function with one branch per file (create
if absent, append if the "append" rule applies, skip-and-report if it
doesn't).

## Steps

1. Add `pyproject.toml` with project metadata, setuptools `src` layout, and
   a `spacekid = "spacekid.cli:main"` console-script entry point.
2. Create `src/spacekid/templates/`:
   - `root_agents.md` — the root `AGENTS.md` template, with an `{{APP_NAME}}`
     placeholder, copied from this repo's own `AGENTS.md`.
   - `specs_agents.md` — copied verbatim from this repo's `specs/AGENTS.md`.
   - `plans_agents.md` — copied verbatim from this repo's `plans/AGENTS.md`.
3. Implement `src/spacekid/scaffold.py`:
   - `detect_app_name(project_root)`: read `[project].name` from
     `pyproject.toml` if present; else fall back to the project root
     directory's basename.
   - `render_root_agents(app_name)`: load `root_agents.md`, replace
     `{{APP_NAME}}`.
   - `write_or_skip(path, content)`: if `path` doesn't exist, create parent
     dirs and write `content`; if it exists, skip and return a `"skipped"`
     status — used for root `AGENTS.md`.
   - `write_or_append(path, content)`: if `path` doesn't exist, create parent
     dirs and write `content`; if it exists, append `content` to the end
     (separated by a blank line) — used for `specs/AGENTS.md` and
     `plans/AGENTS.md`.
   - `scaffold(project_root, app_name=None)`: runs the three file operations
     above and returns a list of `(path, status)` results where status is
     one of `created` / `appended` / `skipped`.
4. Implement `src/spacekid/cli.py`:
   - `spacekid init [--path PATH] [--name NAME]`, default `PATH` = cwd.
   - Calls `scaffold(...)` and prints one line per file with its status.
5. Add `tests/test_scaffold.py` covering, against a temp directory:
   - fresh project → all three files created, app name filled in from
     `pyproject.toml` and, separately, from directory-name fallback.
   - existing root `AGENTS.md` → left byte-for-byte untouched, reported as
     skipped.
   - existing `specs/AGENTS.md` / `plans/AGENTS.md` → original content
     preserved, standard content appended after it.
   - missing `specs/` / `plans/` directories → created as needed.
6. Update this repo's own `README.md` with install/usage instructions
   (`pip install spacekid`, then `spacekid init`).

## Key Decisions

- **argparse, not a CLI framework.** One subcommand, two flags — a
  dependency like Click/Typer would outweigh what it buys here (KISS).
- **Never overwrite root `AGENTS.md`.** Unlike the two guide files, the root
  file is meant to accumulate project-specific content (the "Project
  Overview" section, any project-specific rules an agent adds later).
  Overwriting it on a re-run would destroy that. The spec only mandates
  append-semantics for `specs/AGENTS.md` and `plans/AGENTS.md`; for the root
  file, skip-and-report is the safe default matching "never destroy existing
  project documentation."
- **App name source order:** `pyproject.toml` `[project].name` first, since
  that's the standard, explicit declaration of a Python project's name;
  directory basename as a fallback for projects without one yet. A `--name`
  flag overrides both — no interactive prompt, keeping `init` scriptable.
- **Package data via `importlib.resources`**, not string constants in
  `cli.py`, so the Markdown templates stay diffable and reusable if a future
  command needs them.

## Implementation Notes

Built as planned, with one addition not in the original steps: a
`.gitignore` (`.venv/`, `__pycache__/`, `*.egg-info/`, `build/`, `dist/`,
`.pytest_cache/`) since setting up the package for local testing produces
these artifacts in the repo root.

Verified end-to-end with a local editable install (`pip install -e ".[test]"`
in a `.venv`) against a scratch directory: fresh scaffolding creates all
three files with the name pulled from `pyproject.toml`; running `spacekid
init` again on the same directory correctly skips the existing root
`AGENTS.md` and appends to `specs/AGENTS.md` / `plans/AGENTS.md`. All 6
`tests/test_scaffold.py` cases pass.

No deviation from the planned design otherwise.
