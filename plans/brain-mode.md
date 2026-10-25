# Brain Mode — Implementation Plan

Implements: `specs/brain-mode.md`
Status: Done

## Approach

Extend the existing `spacekid init` command rather than adding a new one.
`init` first resolves a mode (`project` or `brain`), then dispatches to the
matching scaffold function. Project mode is untouched. Brain mode reuses the
existing `write_or_skip` / `write_or_append` helpers and the existing
`specs_agents.md` / `plans_agents.md` templates, so the SDD rules cannot
drift between modes. Only two things are new: mode detection and one new
template, `brain_agents.md`.

## Steps

1. Add `detect_mode(path)` to `scaffold.py`:
   - Return `brain` if `path` is not itself a git repository (no `.git`) and
     has at least two immediate subdirectories that each contain `.git`.
   - Otherwise return `project`.
2. Add template `src/spacekid/templates/brain_agents.md`, with `{{APP_NAME}}`
   placeholder, containing:
   - Purpose of the brain and a folder map: `contexts/`, `artifacts/`,
     `sdd/specs/`, `sdd/plans/`.
   - Placement rule: knowledge → `contexts/`; any other generated file →
     `artifacts/`.
   - Mandatory flow: **0. Context** (consult existing contexts, create the
     missing ones the task needs) → Spec → Plan → Implementation → Close the
     loop (update plan, spec, and any affected context).
   - "Never break" rules, mirroring the project-mode root file, plus "never
     start execution without consulting or creating context".
3. Add `scaffold_brain(root, app_name=None)` to `scaffold.py`, operating on
   `root/brain/`:
   - `AGENTS.md` via `write_or_skip` (rendered from `brain_agents.md`).
   - `sdd/specs/AGENTS.md` and `sdd/plans/AGENTS.md` via `write_or_append`,
     using the existing `specs_agents.md` and `plans_agents.md` templates, so
     each folder carries its own `AGENTS.md` just like project mode.
   - `contexts/.gitkeep` and `artifacts/.gitkeep` via `write_or_skip`
     (empty content), so empty folders survive version control.
   - Returns the same `FileResult` list shape as `scaffold`.
4. Update the `sdd` template wording: the existing `specs_agents.md` and
   `plans_agents.md` mention `specs/<name>.md` and `plans/<name>.md` paths
   relative to a project root, which stay valid inside `sdd/`; no template
   change is needed. Verify during implementation and adjust only if a
   rendered path becomes misleading.
5. Update `cli.py`: add `--mode {auto,project,brain}` (default `auto`) to
   `init`; resolve via `detect_mode` when `auto`; print the resolved mode;
   dispatch to `scaffold` or `scaffold_brain`.
6. Add tests in `tests/test_scaffold.py` (temp dirs, `.git` dirs faked with
   `mkdir`):
   - `detect_mode`: two repos → brain; one repo → project; no repos →
     project; the directory itself a repo containing repos → project.
   - Fresh brain scaffold creates the full tree, including `.gitkeep` files.
   - Existing `brain/AGENTS.md` untouched; existing `sdd/*/AGENTS.md`
     appended to.
   - `brain_agents.md` mentions the context-first step and the
     contexts/artifacts rule.
   - CLI: `--mode brain` forces brain in a plain directory; `--mode project`
     forces project in a multi-repo directory.
7. Update `README.md` with a "Brain mode" usage section.

## Key Decisions

- **Detection by `.git` children.** A repository is the one unambiguous
  signal of "a project". Two or more child repos and no `.git` on the
  directory itself is the shape of a workspace. Requiring two avoids
  misclassifying a project that merely vendors one nested repo. Explicit
  `--mode` covers every edge case, so the heuristic stays simple.
- **Same command, new flag** rather than a new subcommand: users keep one
  entry point, and the automatic choice is the default path the spec asks
  for.
- **Reuse existing SDD templates** rather than copying them, keeping a single
  source of truth for spec/plan rules.
- **`.gitkeep` placeholders** over a README per folder: minimal, and the
  purpose of each folder already lives in `brain/AGENTS.md`.
- **Append for `sdd/*/AGENTS.md`** keeps parity with project mode. A re-run
  no longer duplicates the guidance: files already containing it are skipped.

## Implementation Notes

Implemented as planned, with no deviations.

- Step 4 verified: the existing `specs_agents.md` / `plans_agents.md` render
  correctly inside `sdd/`; no template change was needed. A test asserts the
  brain copies are identical to project mode.
- The CLI prints `mode: <resolved mode>` before the per-file results.
- `.gitkeep` files are reported in the per-file output like any other file.
- Other specs/plans (`cli-init`) describe project-mode behavior, which is
  unchanged; the new `--mode` flag is documented here and in the README.
