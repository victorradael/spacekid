# Miniverse — spacekid

## Purpose

This folder is a miniverse: a self-contained world holding everything an agent
needs to work well here — the knowledge gathered along the way, the files
produced, and the spec-driven workflow that turns intent into software.

## The Flow

The flow is the heart of this miniverse. Every piece of work follows these
steps, in order, with no skipping:

0. **Context (mandatory first step).** Before executing anything:
   1. Run `./scan.sh` from this folder to refresh `catalog.md`. Run it again
      before starting any spec and before starting any plan.
   2. Read `catalog.md`. Use it — never search the file tree — to reach the
      parent miniverses and the nested miniverses below this one, at any depth.
   3. Reuse the nested `contexts/` the catalog lists instead of rediscovering
      what is already documented.
   4. Read the nested `sdd/specs/` the catalog lists, looking for limitations
      and decisions already taken that may conflict with a spec of this
      miniverse. Read the specs of the miniverses above this one that this
      work must respect.
   5. Consult the existing files in `contexts/` and create the missing contexts
      the task depends on. Do not proceed until they exist.
1. **Spec.** Write or update a spec in `sdd/specs/`, following
   `sdd/specs/AGENTS.md`.
2. **Plan.** Write or update an implementation plan in `sdd/plans/`, following
   `sdd/plans/AGENTS.md`.
3. **Implementation.** Build what the plan describes.
4. **Close the loop.** As soon as the work finishes:
   - set the plan and spec statuses and record any deviation;
   - bring up to date every spec, plan, and context the work affected;
   - register every plan, context, and artifact created from a spec in that
     spec's Traceability section, with the date it was added, and refresh the
     spec's `Updated` date.

### Conflicts between levels

Miniverses nest: one may sit inside a directory covered by another, to any
depth. When a spec of a lower-level miniverse conflicts with a spec of a
higher-level one, surface the conflict and resolve it before work proceeds.
The higher-level spec prevails unless it is itself deliberately updated. With
several levels, the higher the level, the higher the precedence.

## Map

- `AGENTS.md` (this file) — the flow, the map, the placement rule, and the rules.
- `.miniverse` — marker file. A folder is a miniverse because it holds this
  file, not because of its name. Never delete it.
- `scan.sh` — self-contained script (POSIX `sh`, no SpaceKid needed). It scans
  the directories this miniverse covers and rewrites `catalog.md`.
- `catalog.md` — generated map of the hierarchy: this miniverse's level, its
  ancestors, and the full tree of nested miniverses, with their contexts and
  specs. Never edit it by hand.
- `contexts/` — every piece of knowledge produced while working: findings,
  decisions, how things relate, domain explanations.
- `contexts/AGENTS.md` — how to write a context.
- `artifacts/` — every other generated file that is not knowledge itself:
  diagrams, exports, reports, drafts, and similar.
- `artifacts/AGENTS.md` — how to organize artifacts.
- `sdd/specs/` — one spec per feature. Business-only, self-contained.
- `sdd/specs/AGENTS.md` — how to write a spec.
- `sdd/plans/` — one implementation plan per spec, paired by matching name.
- `sdd/plans/AGENTS.md` — how to write an implementation plan.

Before creating or editing anything in a folder, read that folder's
`AGENTS.md`.

## Where Things Go

- Anything that is **knowledge** is saved as a context in `contexts/`.
- Any **other file** you produce is an artifact in `artifacts/`.

When in doubt, ask: "Would a future agent need to know this to work well?"
If yes, it is a context. Otherwise, it is an artifact.

## Rules Agents Must Never Break

- Never start execution without consulting or creating the context it depends on.
- Never start a spec or a plan without running `./scan.sh` first.
- Never search the file tree for nested miniverses; use `catalog.md`.
- Never create or edit anything in a folder without reading that folder's `AGENTS.md`.
- Never save knowledge outside `contexts/`, or a non-knowledge file outside `artifacts/`.
- Never implement a non-trivial feature without a spec and a plan already in place.
- Never finish a task without updating the status of the affected specs, plans, and contexts.
- Never let a spec, plan, or context go stale after related work lands elsewhere.
- Never change a spec without refreshing its `Updated` date.
- Never create a plan, context, or artifact for a spec without registering it in that spec's Traceability.
- Never carry on past a conflict between specs of different levels; resolve it first, in favor of the higher level.
- Never write a spec that contains implementation details, or a plan that skips referencing its spec.
