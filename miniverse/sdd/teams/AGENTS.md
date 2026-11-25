# AGENTS.md — Forming Agent Teams

A team is a set of AI agents that carry out the flow together, each with one
responsibility. This guide says when to form one, how to shape it, and how its
members work. **The miniverse never creates agents.** The user, or the lead
agent, creates them in their own agent tool, following this guide.

## When to form a team

- **One agent is enough** for a small, single-area change that one agent can
  hold in its head from spec to close.
- **Form a team** when the plan spans several areas or repositories, when
  steps can run in parallel, or when the work needs an independent review.
- Start with the fewest members that cover the work. Merge or skip roles for
  small work; never give two members the same responsibility.

## Roles

| Role | Responsibility | Model tier |
|---|---|---|
| Lead | Owns the flow: context, spec, plan, splitting the plan into tasks, assigning them, and closing the loop. The only member who changes specs. | Strongest reasoning |
| Implementer | Builds one task of the plan in one area, with its tests. Several may run in parallel, one per area. | Balanced |
| Reviewer | Reviews every change before it is done: bugs, security, load, missing tests, and what to cut. Never reviews its own work. | Strongest reasoning |
| Scout | Mechanical, bounded work: searching code, gathering context, running scans and checks, formatting, docs. | Fast and cheap |

### Model tiers

- **Strongest reasoning** — the most capable model the user has. Mistakes in
  planning and review are the most expensive ones, so these roles get it.
- **Balanced** — a capable mid-tier model. Building a well-planned task needs
  skill, not the top tier, and implementers run the most tokens.
- **Fast and cheap** — the smallest model that does the job. Bounded tasks
  with a clear output do not need deep reasoning.

Move a role up a tier only when it keeps failing at its tier; record why. The
team document records the exact model of each member, not only the tier.

## Organization and handoffs

- The lead coordinates. Members take work only from the lead and report back
  to the lead; they do not reassign work among themselves.
- Every task is handed over with: the spec and plan it serves, the exact
  scope (what to change and what not to touch), the done criteria, and the
  contexts to read first.
- Every handoff back says: what changed, how it was verified, what was
  skipped or not checked, and any risk. Work without this report is not done.
- Implementer → reviewer → lead: no change reaches the lead as done without
  the reviewer's approval. Findings go back to the implementer who owns them.
- Blocked members stop and escalate to the lead with the concrete blocker and
  what they need. The lead escalates to the user what only the user can
  decide.
- Every member follows the miniverse flow and the guide of each folder it
  writes in. Knowledge found while working becomes a context.

## The ponytail skill

Every member is equipped with the ponytail skill before it starts working. It
makes an agent write only what the task needs, so the team spends fewer tokens
and ships less, better-tested code. It never cuts validation, error handling,
security, accessibility, or the steps of the flow.

- **Official sources only:** GitHub `DietrichGebert/ponytail` and npm
  `@dietrichgebert/ponytail`. Record the installed version in the team
  document.
- **Install:**
  - Claude Code: `/plugin marketplace add DietrichGebert/ponytail`, then
    `/plugin install ponytail@ponytail`, as two separate prompts.
  - Codex: `codex plugin marketplace add DietrichGebert/ponytail` and
    `codex plugin add ponytail@ponytail`, then trust its hooks in `/hooks`.
  - Gemini CLI: `gemini extensions install https://github.com/DietrichGebert/ponytail`.
  - OpenCode: `opencode plugin add @dietrichgebert/ponytail`.
  - Any other tool: add the repository's `AGENTS.md` to the agent's rules, or
    install its `skills/ponytail/SKILL.md` as a skill. See its `INSTALL.md`.
- **Use by role:**
  - Lead and implementers: keep it on (default level) for every task.
  - Reviewer: run `/ponytail-review` on every change before approving it.
  - Lead: run `/ponytail-audit` before planning work on an unfamiliar
    codebase, and `/ponytail-debt` when closing the loop.
  - Scouts: keep it on; their output is short by nature.

## Team documents

Each team is described in `sdd/teams/<name>.md`, kebab-case. The lead writes
it before the team starts and keeps it current, refreshing `Updated` on every
edit. It lists the plans it executes; each plan stays traced from its spec.

```markdown
# <Team Name>

Status: Active | Done
Created: YYYY-MM-DD
Updated: YYYY-MM-DD

## Purpose
What this team delivers, in one or two lines.

## Members
| Member | Role | Responsibility | Model | Skills |
|---|---|---|---|---|
| <name> | Lead | <one responsibility> | <exact model id> | ponytail <version> |

## Handoffs
Who hands what to whom, in order, and where blockers go.

## Plans
- `sdd/plans/<name>.md`
```

Set `Status: Done` when every plan it executes is done. **English only.**
