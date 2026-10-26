# Miniverse

Status: Implemented
Created: 2026-10-26
Updated: 2026-10-26

## Context

SpaceKid currently offers two usage modes: a "project" mode that scaffolds the
spec → plan → implementation cycle at the root of one repository, and a
"brain" mode that adds a shared knowledge base to a directory holding several
repositories. Users must understand the difference, pick (or trust the
detection of) a mode, and end up with two different layouts and two different
working flows.

The brain model is strictly more capable: it keeps accumulated knowledge
alongside the spec-driven workflow, and that value is just as real for a single
repository as for many. Maintaining two models dilutes the product and the
documentation.

SpaceKid should have one model only. It is called the **miniverse** (a "mini
universe"): a self-contained world holding everything an agent needs to work
well — knowledge, produced files, and the spec-driven workflow. Every use of
SpaceKid creates a miniverse, and all work flows from it.

## Requirements

- SpaceKid must have a single usage model, the miniverse. The "project" and
  "brain" modes, the choice between them, and automatic mode detection must no
  longer exist.
- Running SpaceKid in any directory — a single repository, several
  repositories side by side, or an empty folder — must always create a
  `miniverse` folder there.
- The miniverse folder must contain:
  - `AGENTS.md` — describes the purpose of each folder inside the miniverse and
    the working rules for agents.
  - `contexts/` — every piece of knowledge produced while working (findings,
    decisions, how things relate, domain explanations).
  - `artifacts/` — every other generated file that is not knowledge itself
    (diagrams, exports, reports, drafts, and similar).
  - `sdd/` — the spec-driven workflow, containing `specs/` and `plans/`, each
    with its own `AGENTS.md` holding the rules for writing that kind of
    document.
- The miniverse's `AGENTS.md` must state explicitly that knowledge is saved as
  a context and any other produced file is an artifact.
- Every folder inside the miniverse that holds a kind of document (contexts,
  artifacts, specs, plans) must have its own `AGENTS.md` detailing the
  structure and the patterns its files must follow (naming, required header
  information, organization). Agents must read a folder's `AGENTS.md` before
  creating or editing anything there, and the miniverse's `AGENTS.md` must say
  so.
- Every context must carry a one-line summary, a creation date, and a
  last-updated date, so an agent can judge its relevance from the catalog
  without opening it.
- The miniverse workflow must begin with context: before any work, the agent
  consults existing contexts and creates the missing ones the task depends on.
  This is the mandatory first step, ahead of the spec → plan → implementation →
  status-update cycle.
- When work finishes, specs, plans, and contexts affected by it must be brought
  up to date.
- The well-defined flow is the heart of SpaceKid. The documentation (the
  user-facing guide and every guide generated into the miniverse) must present
  the flow prominently and unambiguously, as the central idea of the product.
- Miniverses can be nested: a miniverse may sit inside a directory that is
  itself covered by a higher-level miniverse, and a higher-level miniverse
  may contain several lower-level ones. Nesting has no depth limit: a
  miniverse may sit inside a parent that sits inside another, and so on. As
  part of the context step, the
  agent must always check the other miniverses inside the directories covered
  by the miniverse it is working in, and consult them:
  - to reuse contexts that were already documented, instead of rediscovering
    them;
  - to read their specs, which may reveal limitations or decisions already
    taken that conflict with a spec at the higher level.
- Every miniverse must be identifiable by a marker file placed in it, so that
  a miniverse is recognized by what it contains, not by what it is called.
- Every miniverse must include a ready-to-run script that scans the
  directories it covers for other miniverses and records what it finds in a
  catalog stored inside the miniverse. The script must work on its own,
  without requiring SpaceKid to be available.
- The catalog must map the full hierarchy around the miniverse so an agent can
  navigate it without getting lost:
  - **Position:** the miniverse's own level in the hierarchy, counted from the
    top-most miniverse above it.
  - **Ancestors:** every higher-level miniverse, in order from the nearest to
    the top-most.
  - **Descendants:** every lower-level miniverse at every depth, shown as a
    tree that makes each one's parent and level clear.
  - **Content:** for every ancestor and descendant, its contexts (with their
    summaries and dates) and its specs (with their status and dates).
  - Locations must be given in a way an agent can follow directly from the
    miniverse, with no guessing.
  The purpose is to let agents reach the contexts and specs of any related
  miniverse, above or below, without spending effort searching for them.
- The flow must require the agent to run the script before starting any spec or
  plan, so the catalog is current, and to use the catalog, rather than
  searching the file tree, to reach nested contexts and specs.
- Running the script repeatedly with no changes in the covered directories must
  produce the same catalog.
- When a spec at a higher level conflicts with a lower-level one, the conflict
  must be surfaced and resolved before work proceeds. The higher-level spec
  prevails unless it is itself deliberately updated. With several levels, the
  higher the level, the higher the precedence.
- Every spec must carry a creation date and a last-updated date. A spec is the
  rule of the product, so the last-updated date must change whenever the spec
  is changed, and it tells readers how current the rule is.
- Every spec must have a traceability section that indexes the plans,
  contexts, and artifacts created from it, so the whole process, from rule to
  result, can be followed. Whenever a plan, context, or artifact is created
  from a spec, it must be added to that index, and the spec's last-updated
  date must be refreshed.
- Every entry in the traceability index must carry the date on which it became
  part of the spec, so it is clear since when each file belongs to it.
- The writing rules for specs must allow the traceability section to point to
  those files, as the one exception to the rule that a spec does not point to
  other files.
- SpaceKid must also place an `AGENTS.md` at the root of the directory. It stays
  short and orients any agent: this directory works through a miniverse, what
  the miniverse is, and that agents must read the miniverse's guide before
  doing anything.
- Running the command must never destroy existing content: files that already
  exist are preserved, with the same skip/append behavior users already know,
  and the user is told what happened to each file.
- Running the command twice must not corrupt the miniverse.
- The interactive menu, help text, and user documentation must describe only
  the miniverse model.
- SpaceKid's own specs and plans must live inside its own miniverse and be
  adapted to the new model, so the product follows the workflow it prescribes.

## Acceptance Criteria

- [x] Run in a single repository, in a directory with several repositories, and
      in an empty directory, SpaceKid creates the same `miniverse` structure.
- [x] No mode option, mode detection, or mode choice remains in the command,
      the menu, or the documentation.
- [x] The `miniverse` folder contains `AGENTS.md`, `contexts/`, `artifacts/`,
      and `sdd/` with `specs/` and `plans/`, each of the four document folders
      with its own `AGENTS.md`.
- [x] The miniverse's `AGENTS.md` explains every folder, states the
      knowledge-vs-artifact rule, and makes "consult or create context" a
      mandatory step before any execution.
- [x] `sdd/specs/` and `sdd/plans/` each contain their own `AGENTS.md` with the
      writing rules.
- [x] The root `AGENTS.md` is created, is short, and directs agents to the
      miniverse; an existing root `AGENTS.md` is never overwritten.
- [x] The user-facing guide and the miniverse's `AGENTS.md` present the flow
      as the core of the product, in a prominent first position.
- [x] Every created miniverse contains a marker file, and a nested miniverse is
      recognized by that marker even if its folder has a different name.
- [x] Every created miniverse contains a script that, run on its own, scans the
      covered directories and writes a catalog inside the miniverse.
- [x] With three or more levels of nesting (a miniverse inside a parent inside
      another), the catalog of each one shows its level, the full chain of
      ancestors from nearest to top-most, and the complete tree of
      descendants with each node's parent and level, with followable
      locations.
- [x] For every ancestor and descendant, the catalog lists contexts (summary,
      dates) and specs (status, dates).
- [x] Contexts, artifacts, specs, and plans folders each contain their own
      `AGENTS.md` describing structure and file patterns, and the
      miniverse's `AGENTS.md` requires reading it before writing there.
- [x] The context rules require a one-line summary, a creation date, and a
      last-updated date in every context.
- [x] Conflicts across several levels are resolved in favor of the higher
      level, as stated in the miniverse's guidance.
- [x] Running the script twice with no changes yields an identical catalog.
- [x] The flow requires running the script before starting any spec or plan,
      and using the catalog instead of searching the file tree.
- [x] The context step explicitly requires consulting nested miniverses through
      the catalog, reusing their contexts, and reading their specs for
      limitations and decisions that may conflict with higher-level specs.
- [x] The conflict rule (surface it, higher-level spec prevails unless
      deliberately updated) is stated in the miniverse's guidance.
- [x] The spec writing rules require a creation date, a last-updated date, and
      a traceability section listing plans, contexts, and artifacts, and they
      permit that section to reference those files, each entry with the date
      it was added.
- [x] The rules for plans, contexts, and artifacts require registering them in
      the originating spec's traceability section and refreshing its
      last-updated date.
- [x] Every one of SpaceKid's own specs has creation and last-updated dates
      and a traceability section that lists its plan and any related contexts
      and artifacts.
- [x] Existing miniverse files are never overwritten, and the user is told for
      each file whether it was created, appended to, or skipped.
- [x] Empty folders are preserved when the miniverse is committed to version
      control.
- [x] A second run changes nothing.
- [x] All of SpaceKid's own specs and plans are inside its miniverse, adapted
      to the miniverse model, and none remain outside it. Obsolete concepts
      (project mode, brain mode) are marked as superseded rather than silently
      dropped.

## Out of Scope

- Changing or moving the repositories inside the directory; the script only
  reads them, looking for miniverses.
- Automatically producing contexts; agents write them as they work.
- Automatically detecting conflicts between specs, or maintaining spec dates
  and traceability indexes; agents do this as part of the flow.
- Supporting more than one miniverse in the same directory.
- Migrating users' existing `brain` folders or root-level `specs/`/`plans/`.
- Keeping an existing miniverse in sync with future template changes.

## Traceability

- Plans: `sdd/plans/miniverse.md` (added 2026-10-26)
- Contexts: `contexts/architecture.md` (added 2026-10-26), `contexts/miniverse-decision.md` (added 2026-10-26)
- Artifacts: —
