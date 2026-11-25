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
writing only what the task needs. The miniverse carries its own copy of the
ponytail rules for that, so every team member must follow them, each role in
its own way.

## Requirements

### Team guideline

- The miniverse must contain a guide, part of the flow, that orients the
  creation and use of agent teams.
- The guide must state explicitly that the miniverse never creates agents and
  ships no agents or ready-made teams: it is a guideline for the AI tool,
  which builds the team structure and creates the agents itself.
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
- Each team must be persisted in the miniverse as its own folder, following
  the structure Paperclip uses for teams: one manifest for the team (purpose,
  manager, members, handoffs, status, and the plans it executes) and one
  instructions file per member (role, who it reports to, exact model,
  ponytail level, and its instructions), from which the member is created in
  the agent tool.
- The miniverse's main guide must point to the team guide from the flow and
  from its map.

### Ponytail rules

- Every team member must follow the miniverse's own ponytail rules from its
  first task; the lead puts them in each member's instructions.
- Nothing is installed: the guide must say the original skill is never added
  on top of the miniverse's copy.
- The guide must say how each role applies the rules: the lead cuts scope
  while writing the spec and plan, audits an undescribed codebase, and records
  the shortcuts taken; implementers end every handoff with what was skipped
  and any risk; the reviewer runs the rules' review on every change, and only
  its approval lets a change count as done.
- The level each member works at must be recorded in its member file.
- The rules never justify cutting validation, error handling, security,
  accessibility, or the flow's own steps.

## Acceptance Criteria

- [x] A new miniverse contains the team guide, and the main guide names it in
      the flow and in the map.
- [x] The team guide states that the miniverse does not create agents.
- [x] The team guide covers when to form a team, the roles and their single
      responsibilities, the model tier of each role with its reason, the
      organization, the handoff contents, and escalation.
- [x] The team guide defines how a team is persisted: a folder with a team
      manifest and one file per member, recording the exact model and the
      ponytail level of each member, in the layout Paperclip uses for teams.
- [x] The team guide requires the miniverse's ponytail rules for every member,
      explains how each role applies them, and installs nothing.
- [x] Running the command again on an existing miniverse never duplicates or
      overwrites the team guide.
- [x] SpaceKid's own miniverse follows the same guidance.

## Out of Scope

- Creating, launching, or configuring agents.
- Choosing a specific agent tool or model vendor for the user.
- Installing the ponytail skill, in any form.
- Updating the main guide of miniverses created by older versions.

## Traceability

Paths are relative to the miniverse root; use `—` when a list is empty.

- Plans: `sdd/plans/agent-teams.md` (added 2026-11-25)
- Contexts: `contexts/ponytail.md` (added 2026-11-25), `contexts/architecture.md` (added 2026-11-25)
- Artifacts: —
