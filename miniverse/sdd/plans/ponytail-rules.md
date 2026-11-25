# Ponytail Rules, Always On — Implementation Plan

Implements: `sdd/specs/ponytail-rules.md`
Status: Done

## Approach

One new generated file, `miniverse/ponytail.md`, holding the ponytail rules
adapted from upstream v5.3.3 (commit `ebd8654`): `AGENTS.md`/`SKILL.md` for
the rules and levels, `ponytail-review`, `ponytail-audit` and `ponytail-debt`
condensed into procedures tied to the flow. Written with `write_or_skip`, like
the main guide, so a tailored copy is never touched. The main guide makes it
always on; the entry guide and the team guide point to it.

## Steps

1. **Template** `src/spacekid/templates/ponytail.md`: always-on statement,
   credit, levels (lead in `ultra` for spec and plan), before you write,
   smallest complete change, never cut (plus the flow's steps), the closing
   reply as the handoff's skipped/risk part, review (gates "done"; reviewer in
   a team, self-review when alone), audit (before planning on an undescribed
   codebase; report is an artifact, knowledge becomes contexts), shortcut
   ledger in the plan's Implementation Notes, MIT notice.
2. **Scaffold**: `write_or_skip(miniverse / "ponytail.md", ...)`.
3. **Main guide** (`miniverse_agents.md`): "Always On: Ponytail" before the
   flow, step 3 (build by it, review gates done), step 4 (shortcut ledger),
   map entry, two never-break rules.
4. **Entry guide** (`root_agents.md`): one line pointing to the rules.
5. **Team guide**: replace the install section with per-role use of
   `ponytail.md`; the team document records each member's level.
6. **Dogfood**: same files in this repo, root `AGENTS.md` included.
7. **Tests**: the file is created, holds every section and the license, is
   never overwritten, and the main and entry guides make it always on.
8. **Docs and close**: README, DOCKERHUB, `contexts/ponytail.md`,
   `contexts/architecture.md`, `agent-teams` spec and plan.

## Key Decisions

- **Vendor, adapted, not installed.** One copy inside the miniverse works for
  every agent tool, is visible to every agent, and fits the flow; the user
  asked for nothing to be installed. Cost: updates from upstream are manual.
- **Root of the miniverse, not `sdd/teams/`.** The rules bind every agent,
  not only teams.
- **`write_or_skip`, not `write_or_append`.** It is a full document, not a
  folder guide; appending a new version to a tailored copy would duplicate
  rules.
- **Dropped upstream parts:** install steps, `/ponytail-gain` (benchmark
  stats), `/ponytail-help`, the slash commands themselves; the procedures are
  plain text any agent can follow.

## Implementation Notes

- Implemented as planned. Review and audit output formats were condensed to
  one paragraph each, keeping every rule but the worked example.
- No `shortcut:` markers added.
- 2026-11-25, user decision: this repository checks upstream for a newer
  ponytail release at the start of every task (flow step 0.7 in its own
  `miniverse/AGENTS.md`, procedure in `contexts/ponytail.md`). Manual and
  done by agents, nothing installed. Repo-only: the template guide is unchanged.
