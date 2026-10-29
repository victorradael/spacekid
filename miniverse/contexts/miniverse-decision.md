# Why a Single Miniverse Model

Summary: why SpaceKid dropped project and brain modes in favor of one miniverse.
Created: 2026-10-26
Updated: 2026-10-26

## Decision

SpaceKid has one usage model, the miniverse. The earlier "project" mode (spec
and plan rules at the repo root) and "brain" mode (a shared knowledge folder
for several repositories) were collapsed into it.

## Why

- The brain layout was a strict superset: knowledge next to the spec-driven
  workflow is as useful for one repository as for many.
- Two modes meant a choice, a detection heuristic, and two layouts to document
  and maintain.
- One behavior for every directory is simpler to explain and to test.

## Consequences

- No `--mode` option and no detection. The change is breaking for users of it;
  migration of old layouts is manual and out of scope.
- Nested knowledge is reachable through nesting: `scan.sh` lists the miniverses below a level by path.
- Old `brain-mode` spec and plan are kept as superseded history.
