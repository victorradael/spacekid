# AGENTS.md — Writing Specs

A spec captures the **business intent** of a feature: why it exists, what it
must do, and how we know it's done. Nothing more. A spec is the rule of the
product.

## Rules

- **Self-contained.** A reader must understand the full spec without opening
  any other file. Do not reference other specs, plans, code files, or paths.
  The one exception is the Traceability section (see below).
- **No implementation detail.** No code, no technology choices, no
  architecture, no data models. That belongs exclusively in the matching
  `sdd/plans/<name>.md`.
- **Concise and clear.** Say only what's needed to preserve the core idea.
  Prefer short sentences and bullet lists over long prose. Cut anything that
  doesn't change what gets built or how it's accepted.
- **Business-only scope.** A spec centralizes business points: context,
  problem, what must be delivered, and acceptance criteria. It does not
  belong to engineering.
- **Dates.** `Created` is set once. `Updated` must change on every edit of the
  spec, so readers know how current the rule is. Use ISO dates (`YYYY-MM-DD`).
- **Traceability.** Every spec indexes the plans, contexts, and artifacts
  created from it. This is the only place a spec may point to other files.
  Whenever a plan, context, or artifact is created from the spec, add it here
  with the date it was added, and refresh `Updated`.
- **Levels.** If the spec conflicts with a spec of a higher-level miniverse,
  the higher-level spec prevails unless it is deliberately updated.
- **English only.**

## Structure

```markdown
# <Feature Name>

Status: Draft | Approved | Implemented | Superseded
Created: YYYY-MM-DD
Updated: YYYY-MM-DD

## Context
Why this is needed. The problem or opportunity, in business terms.

## Requirements
What must exist or happen once this is delivered. Plain, unambiguous
statements — no solution design.

## Acceptance Criteria
A checklist of verifiable conditions that define "done".

## Out of Scope
What this spec explicitly does not cover (optional, only if it prevents
ambiguity).

## Traceability
Paths are relative to the miniverse root; use `—` when a list is empty.

- Plans: `sdd/plans/<name>.md` (added YYYY-MM-DD)
- Contexts: `contexts/<topic>.md` (added YYYY-MM-DD)
- Artifacts: `artifacts/<name>/<file>` (added YYYY-MM-DD)
```

## What happens next

The implementation plan for this spec is written in `sdd/plans/<name>.md`
(same `<name>`), following `sdd/plans/AGENTS.md`. Register it in the
Traceability section as soon as it exists.

## Status updates

Once the feature is implemented, the `Status` field here must be updated to
`Implemented`. If real-world constraints forced any acceptance criteria to
change during implementation, update this file to reflect what was actually
delivered. A spec replaced by a newer one is marked `Superseded`, not deleted.
Refresh `Updated` every time.
