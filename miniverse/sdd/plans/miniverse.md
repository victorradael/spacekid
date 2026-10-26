# Miniverse — Implementation Plan

Implements: `sdd/specs/miniverse.md`
Status: Done

## Approach

Collapse the two modes into one by promoting the existing brain scaffold and
dropping everything else. `init` stops resolving a mode and always runs a
single `scaffold` function that writes the miniverse tree plus a short root
`AGENTS.md`. The helpers `write_or_skip` / `write_or_append` and the
`specs_agents.md` / `plans_agents.md` templates are reused unchanged, so
idempotency and SDD rules carry over. Net result is a smaller codebase:
`detect_mode`, `--mode`, and the project branch are deleted.

## Steps

1. **Templates** (`src/spacekid/templates/`)
   - `git mv brain_agents.md miniverse_agents.md`; reword "brain" → "miniverse",
     drop the "several repositories" framing (it applies to one repo too).
   - Rewrite `root_agents.md` as a short pointer: what a miniverse is, "read
     `miniverse/AGENTS.md` before anything else", a one-paragraph statement
     that the flow is the heart of the product, plus the Project Overview
     placeholder (keep the AGENT TODO). Remove the old specs/plans map and
     cycle (they now live in the miniverse guide).
   - `miniverse_agents.md`: put "The Flow" first, right after Purpose. Step 0
     (Context) gains: (a) run `./scan.sh` from the miniverse directory to
     refresh `catalog.md`, and run it again before starting any spec and any
     plan; (b) read `catalog.md` — never search the tree for miniverses; (c)
     reuse the nested `contexts/` it lists; (d) read the nested `sdd/specs/`
     it lists for limitations and decisions; (e) if a lower-level spec
     conflicts with a spec of this (higher) miniverse, surface it and resolve
     before proceeding — the higher-level spec prevails unless deliberately
     updated; (f) read the parent miniverse listed in the catalog, if any, for
     specs this one must respect. Document the marker and `scan.sh`/`catalog.md`
     in the map (`catalog.md` is generated: never edit by hand). Add a
     "Traceability" step to Close the loop: register new
     plans/contexts/artifacts in the originating spec, with the date added,
     and bump `Updated`.
   - `specs_agents.md`: add `Created` and `Updated` (ISO `YYYY-MM-DD`) lines
     to the structure, and a mandatory `## Traceability` section with
     `Plans`, `Contexts`, `Artifacts` lists (paths relative to the miniverse
     root, `—` when empty). Each entry is `` `path` (added YYYY-MM-DD) ``. Relax the "no references to other files" rule:
     only the Traceability section may reference files. State that `Updated`
     must change on every edit of the spec.
   - New `contexts_agents.md` → `miniverse/contexts/AGENTS.md`: one topic per
     file; kebab-case `<topic>.md`; header lines `# Title`, `Summary:` (one
     line, what an agent learns), `Created:`, `Updated:` (ISO dates); body
     sections free but concise; update `Updated` on every edit; never store
     non-knowledge files here; if the context belongs to a spec, register it
     in that spec's Traceability.
   - New `artifacts_agents.md` → `miniverse/artifacts/AGENTS.md`: files
     grouped in a subfolder named after the spec they come from
     (`artifacts/<spec-name>/`), or `artifacts/misc/` when none; descriptive
     kebab-case names; no knowledge here (that is a context); register in the
     originating spec's Traceability with date added.
   - `miniverse_agents.md` map: list all four folder guides and the rule
     "read the folder's `AGENTS.md` before creating or editing anything in
     it" (also in the Rules section).
   - `plans_agents.md`: replace "this is the only direction references flow"
     with "a plan references its spec; the spec references the plan only
     through its Traceability section". Add the registration duty: when a plan
     (or a context/artifact derived from the spec) is created, add it to the
     spec's Traceability and bump `Updated`.
2. **`scaffold.py`**
   - Delete `detect_mode` and `scaffold_brain`.
   - Rewrite `scaffold(root, app_name)`: root `AGENTS.md` (`write_or_skip`),
     `miniverse/AGENTS.md` (`write_or_skip`), and the four folder guides
     `miniverse/{contexts,artifacts}/AGENTS.md`,
     `miniverse/sdd/{specs,plans}/AGENTS.md` (`write_or_append`),
     `miniverse/contexts/.gitkeep` and `miniverse/artifacts/.gitkeep`
     (`write_or_skip`).
   - New generated files, all `write_or_skip`:
     - `miniverse/.miniverse` — the marker; one line with the app name
       (`{{APP_NAME}}`). Detection is by this file, never by folder name.
     - `miniverse/scan.sh` — the scanner (see step 2b), written with mode
       `0755`. Add a `executable: bool` param to `write_or_skip`.
     - `miniverse/catalog.md` — initial catalog with the empty-state content
       (so the first agent run produces a diff-free result when nothing is
       nested).
2b. **Scanner** (`templates/scan.sh`, POSIX `sh`, no dependencies beyond
   `find`, `sort`, `sed`, `grep`; works without SpaceKid or Docker):
   - Resolves its own directory (`$0`) as the miniverse; the covered root is
     that directory's parent.
   - **Discovery (one `find`, no symlink following):**
     `find "$root" -name .miniverse -type f` pruning `.git`, `node_modules`,
     `.venv`, `venv`, `dist`, `build`, `target`, `__pycache__`; sorted. Each
     hit `<C>/<folder>/.miniverse` defines a node: miniverse dir
     `D=<C>/<folder>`, covered dir `C`. Excludes self.
   - **Descendant tree:** a node's parent is the deepest node (self
     included) whose covered dir `C_p` is a strict path prefix of its own
     `C`; level = parent level + 1 (self is the reference; descendants of
     self start at +1). Computed in a single sorted pass in `sh`/`awk`
     (sorting by path puts parents before children).
   - **Ancestor chain:** walk up from `C(self)`'s parent to `/`; at each
     directory check the glob `<dir>/*/.miniverse`; every hit is an ancestor.
     Emitted nearest first; the last is the top-most. Self level =
     number of ancestors (top-most known = level 0).
   - **Per-node content:** contexts from `D/contexts/*.md` (excluding
     `AGENTS.md`) with `Title` (first `# ` line), `Summary:`, `Updated:`
     parsed by `sed`; specs from `D/sdd/specs/*.md` (excluding `AGENTS.md`)
     with title, `Status:`, `Created:`, `Updated:`. Missing field → `?`.
   - **Catalog layout (`catalog.md`)**, all paths relative to the miniverse
     folder itself (so `cd miniverse` then follow them as written, e.g.
     `../backend/miniverse/contexts/x.md`):
     1. a 3-line "how to use" note and a "never edit" notice;
     2. `## Position` — own name, `Level: N`, ancestor and descendant counts;
     3. `## Ancestors (nearest first)` — numbered; each with path, name, level,
        then its contexts and specs;
     4. `## Descendants` — an indented tree outline first (one line per node:
        path, name, level, parent path), then one detail block per node in the
        same order, listing contexts and specs;
     5. no timestamps; sections show `none` when empty.
   - Writes `catalog.md` atomically (temp file + `mv`) and only if content
     changed. No timestamps in the output, so runs are idempotent.
   - Paths are relative, so the catalog stays valid on every machine.
   - Each miniverse's catalog is self-sufficient: it does not read other
     catalogs (which could be stale), only markers, contexts and specs.
3. **`cli.py`**
   - Remove `--mode`, mode resolution, and the mode heading; keep per-file
     status output. Update help strings and `_about` copy.
   - `_menu` no longer returns a mode: it runs `_init` with `path="."` or quits.
4. **`ui.py`**: reduce `_MENU` to: initialize a miniverse here / about / quit;
   renumber; remove `heading` mode usage if now unused.
5. **Tests**: remove detection/mode/project tests; rewrite the brain tests for
   the single miniverse flow (fresh tree in single-repo, multi-repo and empty
   dirs; root `AGENTS.md` skip; append behavior for sdd rules; second run
   snapshot unchanged; context-first and placement rule text; menu). Add
   template-content assertions: the miniverse guide puts the flow first and
   mentions nested-miniverse check, context reuse, and the conflict rule; the
   specs rules mention `Created`, `Updated`, and `Traceability`; the plans
   rules require registering in Traceability. Add a repo-level test that every
   file in `miniverse/sdd/specs/` (except `AGENTS.md`) has `Created:`,
   `Updated:`, and `## Traceability`, and that no `specs/` or `plans/`
   remain at the repo root. Scanner tests (run `scan.sh` via `subprocess` in
   `tmp_path`): nested miniverse found by marker even when its folder is
   renamed; contexts (summary, dates) and specs (status, dates) listed; a
   four-level fixture (top → mid → leaf, plus a sibling branch) checked from
   each node: correct level, ancestor order nearest-first, full descendant
   tree with right parents, relative paths that resolve to existing files;
   ignored dirs pruned; no-nesting case yields `none`; second run
   byte-identical; all four folder `AGENTS.md` files exist after init and are
   appended-to, not overwritten, on re-init; script is executable; `scan.sh` and `.miniverse` are
   skipped, not overwritten, on re-init.
6. **Migrate SpaceKid's own SDD** (this repo dogfoods the miniverse):
   - Run the new `spacekid init` in the repo to generate `miniverse/`.
   - `git mv specs/*.md plans/*.md` into `miniverse/sdd/specs/` and
     `miniverse/sdd/plans/` (keeping each file's own `AGENTS.md` from the
     generated tree; remove the old root `specs/AGENTS.md` and
     `plans/AGENTS.md` once identical content is in place).
   - Adapt each migrated spec/plan to the miniverse model:
     `brain-mode` → mark Status superseded by `miniverse` (keep as history);
     `cli-init`, `idempotent-init`, `cli-ui`, `user-docs`, `macos-support`,
     `container-only-distribution`, and others → edit only where they
     describe modes, root `specs/`/`plans/`, or menu items. Specs stay
     business-only; plans stay the only place referencing paths.
   - Add the new metadata to every migrated spec: `Created` = date of the
     file's first commit, `Updated` = today (each is being edited), found via
     `git log --diff-filter=A --follow --format=%as -- <file> | tail -1`. Add
     a `## Traceability` section listing its plan (`sdd/plans/<name>.md`) and
     any context/artifact related to it; each entry dated with the plan's
     first-commit date (migration date for new files). Add `Created`/`Updated`/Traceability
     to `specs/miniverse.md` itself when it moves.
   - Seed `miniverse/contexts/` with a short context on SpaceKid's
     architecture and the miniverse decision (why one model), following the
     context header format (`Summary`, `Created`, `Updated`).
   - Replace the repo's root `AGENTS.md` with the new short pointer form.
7. **Docs**: open the README with "The flow" (context → spec → plan →
   implementation → close the loop) as the core idea, including nested
   miniverses, reuse of contexts, conflict handling, spec dates, and
   traceability. Then rewrite the old "Choosing a mode / Project mode / Brain
   mode" sections into a single "The miniverse" section, plus quick start,
   commands/options (no `--mode`), existing-files section, working loop, and
   repository layout. Update `DOCKERHUB.md` and
   `MAINTAINING.md` where they mention modes or paths (grep for `brain`,
   `specs/`, `plans/`, `--mode`).
8. **Close the loop** (mandatory per root rules): set this plan to Done, fill
   Implementation Notes, set the spec to Implemented, and update all
   other affected specs/plans.

## Key Decisions

- **Single `scaffold`, no flag.** Fewer branches and no detection heuristic to
  maintain; the one behavior is the same for every directory. Trade-off: the
  breaking change for users of `--mode` (accepted in the spec).
- **Root `AGENTS.md` kept, but only as a pointer.** Agents often load the root
  file by convention, so it is the cheapest way to route them into the
  miniverse. Detailed rules live only in the miniverse guide to avoid drift.
- **Discovery is a generated script plus a catalog, not agent search.** A
  scanner shipped inside the miniverse finds nested miniverses and writes
  `catalog.md`, so agents read one file instead of spending tokens crawling
  the tree. Reuse, conflict detection, date bumps and traceability upkeep stay
  as mandatory guide steps (agent judgement), since only discovery is
  mechanical. Trade-off: compliance (running the script first) still depends
  on agents following the guide, so the wording is covered by template tests.
- **Script is POSIX `sh` inside the miniverse, not a `spacekid` subcommand.**
  Distribution is container-only, so requiring the CLI during agent work would
  force Docker for every scan. A self-contained script works anywhere the
  agent runs and keeps working after the miniverse is copied elsewhere.
  Trade-off: the template is not updated in existing miniverses (out of
  scope) and shell parsing of spec headers is simple line matching, which the
  fixed `Status`/`Created`/`Updated` format makes safe.
- **Catalog is relative to the miniverse folder and self-sufficient.** An
  agent works from inside the miniverse, so paths there are copy-followable;
  ancestors and the descendant tree both carry explicit level and parent so
  depth never has to be inferred. Trade-off: a bigger catalog for large
  hierarchies; contexts show only title/summary/date and specs only
  status/dates to keep each line cheap.
- **Context summaries live in the context header.** The scanner can then show
  relevance without opening files; cost is one extra mandatory header line.
- **Marker file, not folder name.** `.miniverse` makes detection independent
  of how the folder is named or moved; an unmarked folder is not a miniverse.
- **Catalog is generated and committed.** It is deterministic and path-relative
  so diffs only appear when nesting actually changes.
- **Dates are ISO text lines, not front matter.** Matches the existing
  `Status:` line style and stays readable and greppable.
- **Traceability is a one-way index owned by the spec.** Plans keep pointing
  at their spec, and the spec points back only via the Traceability section,
  which is the single, explicit exception to the no-references rule.
- **Higher-level spec prevails on conflict.** Gives agents a deterministic
  tie-breaker; the way out is a deliberate update of the higher spec.
- **Folder name fixed to `miniverse/`.** No option or per-name variants (KISS;
  multiple miniverses are out of scope).
- **Old `brain-mode` spec/plan kept as superseded**, not deleted, so history
  and rationale survive.
- **No migration tooling for legacy `brain/` or root `specs/`.** Out of scope;
  a note in the README is enough.

## Implementation Notes

Implemented as planned, with these deviations:

- **Catalog lines show both dates.** Contexts list `created` and `updated`
  (the plan said only `Updated`), because the spec asks for dates, plural.
- **Scanner sort key.** Nodes are sorted with `sort -t <TAB> -k1,1` on the
  `/`-to-`\001` key. A whole-line sort let the separator tab outrank the low
  byte and broke parent-before-child order; caught by the four-level test.
- **Hidden folders.** The ancestor walk also globs `.[!.]*/.miniverse`, so a
  miniverse in a dot-folder is still found.
- **Initial `catalog.md`.** The template was generated from the scanner's own
  empty-state output, and a test asserts a fresh miniverse needs no rewrite.
- **Spec status vocabulary.** The spec rules gained `Superseded`, already used
  by migrated specs; `brain-mode` (spec and plan) was marked superseded.
- **UI.** `ui.heading` was removed together with the mode line.
- **Migration edits.** Other specs and plans got short update notes or small
  wording changes (menu items, mode checks, root guides) instead of rewrites,
  keeping history readable. `.dockerignore` now excludes `miniverse/`.
- **Docs.** The README's "working loop" section was folded into "The flow",
  which now opens the document. A short manual-migration note for the retired
  modes was added.
- **Repo-level tests** (`tests/test_repo_sdd.py`) also check that traceability
  entries are dated and point to existing files, and that the repo's own
  catalog is current.
