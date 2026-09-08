# AGENTS.md — Writing Implementation Plans

A plan translates a spec into a **technical design**: how it will be built,
with the highest quality and best software engineering practices.

Follow the same writing discipline as `specs/AGENTS.md` — concise, clear,
no fluff — applied here to engineering rather than business content.

## Guiding principles

- **KISS.** The simplest design that correctly satisfies the spec wins.
  Well-executed simplicity beats clever complexity every time.
- **SOLID.** Apply these principles where they add real value — not as
  ceremony.
- **Scalability & maintainability.** Design for the load and change patterns
  the spec actually implies, not speculative future needs. Don't build for
  hypothetical requirements.

## Rules

- **One plan per spec**, named identically: `plans/<name>.md` implements
  `specs/<name>.md`.
- **This file may reference its spec** — it should open by linking to
  `specs/<name>.md`. This is the only direction references flow: specs never
  reference plans.
- **English only.**

## Structure

```markdown
# <Feature Name> — Implementation Plan

Implements: `specs/<name>.md`
Status: Draft | Approved | In Progress | Done

## Approach
The chosen technical approach and why it's the simplest one that satisfies
the spec.

## Steps
Ordered, concrete implementation steps.

## Key Decisions
Notable design/architecture choices and their trade-offs (only if non-obvious).

## Implementation Notes
Filled in after the work is done: what changed vs. the original plan, and
why (edge cases found, constraints discovered, simplifications made).
```

## After implementation — mandatory

As soon as the implementation is finished:

1. Set `Status: Done`.
2. Fill in **Implementation Notes** with any deviation from the original plan
   and the reason for it.
3. Go back to `specs/<name>.md` and update its status per `specs/AGENTS.md`.
4. If this work affected the behavior of any other already-implemented
   spec/plan pair, update those too.

Never consider a task finished while this update step is pending.
