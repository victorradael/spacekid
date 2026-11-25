# Agent Teams — Implementation Plan

Implements: `sdd/specs/agent-teams.md`
Status: Done

## Approach

One new folder guide, `sdd/teams/AGENTS.md`, generated like the other four
guides (`write_or_append`, so re-runs never duplicate it). Each team is saved
next to it as a folder, `sdd/teams/<team>/` (`TEAM.md` plus
`agents/<member>/AGENTS.md` per member): a team is part of the workflow, like
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
- **Ponytail through the miniverse's own copy.** First pointed to the
  upstream skill with per-tool install steps; replaced, at the user's
  request, by `ponytail.md` (see `sdd/plans/ponytail-rules.md`).
- **Paperclip's team layout.** At the user's request, persistence copies
  Paperclip's team packages: `TEAM.md` with `manager`/`includes`
  frontmatter, and one `AGENTS.md` per member with `role`/`reportsTo`. Added
  `status`, `created`, `updated`, `plans` (team) and `model`, `ponytail`
  (member). No `schema: agentcompanies/v1` line: roles like `lead` are not
  Paperclip roles, so importability is not promised.
- **Plans guide untouched.** Changing an appended guide's text would make
  `init` re-append it in existing miniverses; the team document lists the plans
  it executes instead.

## Implementation Notes

- Implemented as planned. README also gained a short bullet on the team
  guide; DOCKERHUB got the same `init` output and tree lines.
- Revised 2026-11-25: the ponytail section no longer installs anything; it
  says how each role applies `ponytail.md`, and the team document's Skills
  column became Ponytail level.
- Team documents are not registered in spec Traceability (the spec format has
  no slot for them); each lists its plans, which are traced from their specs.
- Revised 2026-11-25: the single `sdd/teams/<name>.md` became a folder in
  Paperclip's team layout; the model and ponytail level moved from the team
  table into each member's frontmatter, so they live in one place.
