# AGENTS.md — Project Orientation

This file is the entry point for any agent working in this repository. Read it
first, before touching any code.

## File map

- `specs/AGENTS.md` — rules for writing specs (business intent, no code).
- `plans/AGENTS.md` — rules for writing implementation plans (technical design).
- `specs/<name>.md` — one spec per feature/initiative.
- `plans/<name>.md` — one implementation plan per spec, same `<name>`.

## The development cycle

Every feature follows this exact sequence. Do not skip steps or reorder them.

1. **Spec** — Write or update `specs/<name>.md` following `specs/AGENTS.md`.
   Pure business intent: context, requirements, acceptance criteria. No code,
   no implementation detail, no references to other files.
2. **Plan** — Write or update `plans/<name>.md` following `plans/AGENTS.md`.
   Technical design that fulfills the spec. This is the only file allowed to
   reference the spec (e.g. "implements `specs/<name>.md`").
3. **Implementation** — Only start coding once both the spec and the plan
   exist and are approved. Implement exactly what the plan describes.
4. **Update** — As soon as the implementation is done, go back and update:
   - `plans/<name>.md`: mark status as done, record any deviation from the
     original plan and why it was necessary.
   - `specs/<name>.md`: mark status as implemented, note any acceptance
     criteria that changed.

## Mandatory rule — never forget this

After finishing **any** implementation, the agent must update the
corresponding spec and plan files with their current status. This also
applies when the work touches or changes behavior described in a
**different, already-implemented** spec/plan — go back and update those too.
Never leave `specs/` or `plans/` out of sync with the actual state of the
code.

## Language

All documentation (specs, plans, this file) must be written in English,
regardless of the language used in conversation.
