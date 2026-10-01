# AGENTS.md — Writing Specs

A spec captures the **business intent** of a feature: why it exists, what it
must do, and how we know it's done. Nothing more.

## Rules

- **Self-contained.** A reader must understand the full spec without opening
  any other file. Do not reference other specs, plans, code files, or paths.
- **No implementation detail.** No code, no technology choices, no
  architecture, no data models. That belongs exclusively in the matching
  `plans/<name>.md`.
- **Concise and clear.** Say only what's needed to preserve the core idea.
  Prefer short sentences and bullet lists over long prose. Cut anything that
  doesn't change what gets built or how it's accepted.
- **Business-only scope.** A spec centralizes business points: context,
  problem, what must be delivered, and acceptance criteria. It does not
  belong to engineering.
- **English only.**

## Structure

```markdown
# <Feature Name>

Status: Draft | Approved | Implemented

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
```

## What happens next

The implementation plan for this spec is written in `plans/<name>.md`
(same `<name>`), following `plans/AGENTS.md`. The plan file is the only place
allowed to reference this spec — this spec must never reference the plan or
any code.

## Status updates

Once the feature is implemented, the `Status` field here must be updated to
`Implemented`. If real-world constraints forced any acceptance criteria to
change during implementation, update this file to reflect what was actually
delivered.
