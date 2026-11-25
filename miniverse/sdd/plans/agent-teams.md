# Agent Teams — Implementation Plan

Implements: `sdd/specs/agent-teams.md`
Status: Done

## Approach

One new folder guide, `sdd/teams/AGENTS.md`, generated like the other four
guides (`write_or_append`, so re-runs never duplicate it). Team documents live
next to it as `sdd/teams/<name>.md`: a team is part of the workflow, like
specs and plans. The miniverse guide points to it from step 3 of the flow
(form the team before building, when the plan needs one) and from the map.
No code beyond one scaffold entry; the guidance is text.

## Steps

1. **Template** `src/spacekid/templates/teams_agents.md`: when to form a team,
   roles (lead, implementer, reviewer, scout), model tier per role with the
   reason, organization and handoff contents, escalation, ponytail (official
   sources, install per tool, per-role use, version pinning), team document
   structure.
2. **Scaffold**: add `write_or_append(miniverse / "sdd" / "teams" /
   "AGENTS.md", ...)` after the plans guide.
3. **Miniverse guide** (`miniverse_agents.md`): step 3 of the flow and a map
   entry for `sdd/teams/`.
4. **Dogfood**: same edits in this repo's `miniverse/AGENTS.md`, plus
   `miniverse/sdd/teams/AGENTS.md`.
5. **Tests** (`tests/test_scaffold.py`): the guide is in the created tree and
   in `_GUIDES` (idempotency and append tests pick it up), the main guide names
   it, and the guide holds the key rules (no agent creation, tiers, handoff,
   ponytail sources).
6. **Docs**: README `init` output, tree, and the append table; DOCKERHUB if
   it lists the tree.
7. **Close the loop**: spec status and Traceability, architecture context.

## Key Decisions

- **`sdd/teams/`, not `contexts/`.** A team document is a working agreement
  read before building, like a plan, and needs a fixed structure; contexts are
  free-form knowledge.
- **Tiers, not model names, in the guide.** Model names age fast; the team
  document records the exact model each member uses.
- **Point to ponytail, never vendor it.** Its install differs per tool and it
  ships updates; copying it would go stale and blur its license and origin.
- **Plans guide untouched.** Changing an appended guide's text would make
  `init` re-append it in existing miniverses; the team document lists the plans
  it executes instead.

## Implementation Notes

- Implemented as planned. README also gained a short bullet on the team
  guide; DOCKERHUB got the same `init` output and tree lines.
- Team documents are not registered in spec Traceability (the spec format has
  no slot for them); each lists its plans, which are traced from their specs.
