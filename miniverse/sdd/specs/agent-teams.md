# Agent Teams

Status: Implemented
Created: 2026-11-25
Updated: 2026-11-25

## Context

Work in a miniverse is often carried out by several AI agents at once, not by
a single one. Without guidance, each user improvises the team: everyone runs
the most expensive model, responsibilities overlap, work is handed over with
no clear owner, and agents spend tokens rewriting what already exists.

The miniverse should guide how such a team is formed and used, as part of the
flow. It does not create agents: agents are created by whatever agent tool the
user runs. The miniverse only states when a team is worth forming, how it is
shaped, and how its members behave.

Agents also work better and cheaper when they share one discipline for
writing only what the task needs. The ponytail skill provides that discipline
and is available for most agent tools, so every team member must carry it.

## Requirements

### Team guideline

- The miniverse must contain a guide, part of the flow, that orients the
  creation and use of agent teams.
- The guide must state explicitly that the miniverse never creates agents: it
  orients the user or the lead agent, who creates them in their own agent
  tool.
- The guide must say when a team is worth forming and when a single agent is
  enough.
- The guide must define the standard roles of a team, each with one
  responsibility, and allow roles to be merged or skipped for small work.
- The guide must define which kind of language model each role uses, by
  capability tier (strongest reasoning, balanced, fast and cheap), with the
  reason, so cost follows the difficulty of each role. The exact model chosen
  for each member must be recorded.
- The guide must define how the team is organized: who coordinates, who
  assigns work, how work is handed from one member to the next, what every
  handoff must contain, and how blockers are escalated.
- The team must follow the miniverse flow: the spec and plan come before the
  build, and closing the loop is someone's explicit responsibility.
- Each team must be described in a document kept in the miniverse, with a
  fixed structure: purpose, members (role, responsibility, model, skills),
  handoffs, and the plans it executes.
- The miniverse's main guide must point to the team guide from the flow and
  from its map.

### Ponytail skill

- Every team member must be equipped with the ponytail skill before it starts
  working.
- The guide must say how to install it for the common agent tools, and how to
  fall back to its rules file for any other tool.
- The skill must only be obtained from its official sources, and the version
  in use must be recorded in the team document.
- The guide must say how each role uses the skill, including the review of
  changes before work is considered done.
- The skill never justifies cutting validation, error handling, security,
  accessibility, or the flow's own steps.

## Acceptance Criteria

- [x] A new miniverse contains the team guide, and the main guide names it in
      the flow and in the map.
- [x] The team guide states that the miniverse does not create agents.
- [x] The team guide covers when to form a team, the roles and their single
      responsibilities, the model tier of each role with its reason, the
      organization, the handoff contents, and escalation.
- [x] The team guide defines the structure of a team document, including the
      exact model and the ponytail version of each member.
- [x] The team guide requires the ponytail skill for every member, lists its
      official sources, and explains installation and per-role use.
- [x] Running the command again on an existing miniverse never duplicates or
      overwrites the team guide.
- [x] SpaceKid's own miniverse follows the same guidance.

## Out of Scope

- Creating, launching, or configuring agents.
- Choosing a specific agent tool or model vendor for the user.
- Installing the ponytail skill automatically.
- Updating the main guide of miniverses created by older versions.

## Traceability

Paths are relative to the miniverse root; use `—` when a list is empty.

- Plans: `sdd/plans/agent-teams.md` (added 2026-11-25)
- Contexts: `contexts/ponytail.md` (added 2026-11-25), `contexts/architecture.md` (added 2026-11-25)
- Artifacts: —
