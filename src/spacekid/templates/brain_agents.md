# Brain — {{APP_NAME}}

## Purpose

This folder is the shared brain for a workspace that holds several
repositories side by side. It keeps the knowledge no single repository owns:
how the pieces relate, what was decided and why, and what was already
learned. It also hosts the spec-driven workflow that runs on top of that
knowledge.

## Brain Map

- `AGENTS.md` (this file) — the map, the placement rule, and the mandatory flow.
- `contexts/` — every piece of knowledge produced while working: findings, decisions, how repositories relate, domain explanations.
- `artifacts/` — every other file generated along the way that is not knowledge itself: diagrams, exports, reports, drafts, and similar.
- `sdd/specs/AGENTS.md` — how to write a spec. Read this before writing or editing anything in `sdd/specs/`.
- `sdd/specs/*.md` — one spec per feature. Business-only, self-contained.
- `sdd/plans/AGENTS.md` — how to write an implementation plan. Read this before writing or editing anything in `sdd/plans/`.
- `sdd/plans/*.md` — one implementation plan per spec, paired by matching name.

## Where Things Go

- Anything that is **knowledge** is saved as a context in `contexts/`.
- Any **other file** you produce is an artifact in `artifacts/`.

When in doubt, ask: "Would a future agent need to know this to work well?"
If yes, it is a context. Otherwise, it is an artifact.

## The Flow

Every piece of work must follow these steps, in order:

0. **Context (mandatory first step).** Before executing anything, consult the existing files in `contexts/`. Create the missing contexts the task depends on. Do not proceed until the context the task needs exists.
1. **Spec.** Write or update a spec in `sdd/specs/`, following `sdd/specs/AGENTS.md`.
2. **Plan.** Write or update an implementation plan in `sdd/plans/`, following `sdd/plans/AGENTS.md`.
3. **Implementation.** Build what the plan describes.
4. **Close the loop.** As soon as the work finishes, bring up to date every spec, plan, and context it affected: set the plan and spec statuses, record deviations, and correct any context that is now stale or incomplete.

## Rules Agents Must Never Break

- Never start execution without consulting or creating the context it depends on.
- Never save knowledge outside `contexts/`, or a non-knowledge file outside `artifacts/`.
- Never implement a non-trivial feature without a spec and a plan already in place.
- Never finish a task without updating the status of the affected specs, plans, and contexts.
- Never let a spec, plan, or context go stale after related work lands elsewhere.
- Never write a spec that contains implementation details, or a plan that skips referencing its spec.
