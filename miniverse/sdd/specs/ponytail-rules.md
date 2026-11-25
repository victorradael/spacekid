# Ponytail Rules, Always On

Status: Implemented
Created: 2026-11-25
Updated: 2026-11-25

## Context

Agents spend tokens writing code nobody asked for, rewriting what already
exists, and replying at length. The ponytail skill, an open-source MIT prompt,
fixes this with one discipline: the smallest change that fully solves the
task, a short reply that names what was skipped, and a review before work is
done. Its own benchmark reports about 45% fewer output tokens at equal or
better test coverage.

Installing it per agent tool is uneven: each tool installs it differently,
some cannot, and nobody can tell which agents actually carry it. The
discipline should instead live inside the miniverse itself, adapted to its
flow and to agent teams, and every agent working in a miniverse should follow
it on every task, with nothing to install.

## Requirements

- Every new miniverse must contain its own copy of the ponytail rules,
  adapted to the miniverse flow and to agent teams: the rules for the smallest
  complete change, the levels, the reply that names what was skipped, the
  review of a change, the audit of a codebase, and the ledger of shortcuts.
- The copy must credit the original project and carry its license notice.
- Nothing is installed: no skill, plugin, or package. The rules must say not
  to install the original skill on top of them.
- Every agent working in a miniverse must follow the rules on every task,
  alone or in a team, whatever its model or agent tool. The main guide must
  say so before the flow, and list it among the rules agents must never
  break.
- The flow must use the rules: implementation follows them, no change is done
  before it passes their review, and closing the loop records the shortcuts
  taken in the plan.
- The project's entry guide must tell agents to follow the rules too.
- Running the command again must never overwrite a copy the user tailored.

## Acceptance Criteria

- [x] A new miniverse contains the rules, with credit and the license notice.
- [x] The rules cover the levels, the smallest complete change, the closing
      reply, the review, the audit, and the shortcut ledger, each tied to a
      step of the flow or a team role.
- [x] The rules say nothing is installed and the original skill must not be
      added on top.
- [x] The main guide makes the rules always on, before the flow, and lists
      them among the rules never to break; the entry guide points to them.
- [x] The flow requires the review before a change is done and the shortcut
      ledger when closing the loop.
- [x] Running the command again leaves an existing copy untouched.
- [x] SpaceKid's own miniverse follows the same rules.

## Out of Scope

- Installing or updating the original ponytail skill.
- Its token-savings measurement and help commands.
- Updating the main guide of miniverses created by older versions.

## Traceability

Paths are relative to the miniverse root; use `—` when a list is empty.

- Plans: `sdd/plans/ponytail-rules.md` (added 2026-11-25)
- Contexts: `contexts/ponytail.md` (added 2026-11-25), `contexts/architecture.md` (added 2026-11-25)
- Artifacts: —
