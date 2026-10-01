# Agent Guide — {{APP_NAME}}

## Project Overview

<!--
AGENT TODO: This section is a placeholder. Replace it as soon as you have
enough context about this specific project — its purpose, its intended
users, and any key constraints or decisions that shape it. Do this the
first time you work on a real feature here, not before you actually know
the answers. Once this section reflects the real project, delete this
comment block; a placeholder left in place after that point is a bug in
this file, not a feature.
-->

_Not yet described. Fill in what this project does, who it's for, and any
constraints that matter before writing the first spec._

## Purpose

This file orients any agent working in this repository. It maps where the rules live and defines the mandatory cycle that connects business intent, engineering planning, and implementation.

## Project Map

- `AGENTS.md` (this file) — the map, the cycle, and this project's overview.
- `specs/AGENTS.md` — how to write a spec. Read this before writing or editing anything in `specs/`.
- `specs/*.md` — one spec per feature. Business-only, self-contained.
- `plans/AGENTS.md` — how to write an implementation plan. Read this before writing or editing anything in `plans/`.
- `plans/*.md` — one implementation plan per feature, paired with its spec by matching slug (e.g. `specs/foo-spec.md` ↔ `plans/foo-plan.md`).
- This project's own architecture or coding-convention guide, if one has been added — read it before writing or editing implementation code.

## The Cycle

Every non-trivial feature must flow through these steps, in order:

1. **Spec.** Write or update a spec in `specs/`, following `specs/AGENTS.md`. It captures the business problem, what must be delivered, and acceptance criteria — nothing about how.
2. **Plan.** Write or update an implementation plan in `plans/`, following `plans/AGENTS.md`. It references the spec and lays out the engineering approach.
3. **Implementation.** Build the feature following the plan and this project's own conventions.
4. **Close the loop.** As soon as implementation finishes:
   - Update the plan's Status and its Adaptations Log with anything that changed from the original plan during the build.
   - Update the spec's Status to reflect that it is now implemented.
5. **Stay current.** If later work touches an area already covered by an existing spec or plan — even when that wasn't the original goal of the task — revisit and update those files too, so they never go stale.

## Rules Agents Must Never Break

- Never implement a non-trivial feature without a spec in `specs/` and a plan in `plans/` already in place.
- Never finish an implementation task without updating the Status of both the plan and its spec.
- Never let a spec or plan go stale after a related change lands elsewhere in the codebase — step 5 is not optional.
- Never write a spec that contains implementation details, or a plan that skips referencing its spec.
- Never leave the Project Overview placeholder above unfilled once the project's purpose is actually known.
