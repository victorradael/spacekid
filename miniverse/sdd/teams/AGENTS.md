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

Move a role up a tier only when it keeps failing at its tier; record why. Each
member's file records its exact model, not only the tier.

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
- Every member follows the miniverse flow, `ponytail.md`, and the guide of
  each folder it writes in. Knowledge found while working becomes a context.

## Ponytail in a team

Every member follows `ponytail.md`, the miniverse's own copy of the ponytail
rules, from its first task to its last. It is part of the miniverse: nothing
is installed, and the upstream skill or plugin is never added on top of it.
The lead puts it in every member's instructions, `agents/<member>/AGENTS.md`,
and the agent tool takes them from there. Each role applies it this way:

- **Lead:** works in `ultra` while writing the spec and the plan, cutting
  scope nobody needs before it reaches an implementer. Runs the codebase
  audit before planning on a codebase no context describes yet. When closing
  the loop, records the team's `shortcut:` markers in the plan.
- **Implementer:** works in `full`. Ends every handoff with what was skipped
  or not checked and any risk; that is the handoff report's last part.
- **Reviewer:** runs the review in `ponytail.md` on every change and hands
  the numbered findings and the verdict back to the lead. Only
  `Verdict: Ship.` lets a change reach the lead as done.
- **Scout:** works in `full`; its reports are short and say what was not
  searched or checked.

The level of each member is recorded in its file.

## Persisting a team

A team is saved in the miniverse as a folder, with the layout Paperclip uses
for its team packages: one manifest for the team and one instructions file
per member. The lead creates each member in the agent tool from its file;
the folder is the source of truth, and the tool's copy follows it.

```text
sdd/teams/<team>/
├── TEAM.md              # the team: purpose, manager, members, handoffs, plans
└── agents/
    └── <member>/
        └── AGENTS.md    # one member: who it is, its model, its instructions
```

Names are kebab-case. The lead writes the folder before the team starts and
keeps it current, refreshing `updated` on every edit. `TEAM.md` lists the
plans the team executes; each plan stays traced from its spec.

`TEAM.md`:

```markdown
---
name: <Team Name>
slug: <team>
description: What this team delivers, in one line.
manager: agents/<lead>/AGENTS.md
includes:
  - agents/<member>/AGENTS.md
status: active
created: YYYY-MM-DD
updated: YYYY-MM-DD
plans:
  - sdd/plans/<name>.md
---

# <Team Name>

## Members
| Member | Role | Responsibility |
|---|---|---|
| `<lead>` | Lead | <one responsibility> |

## Handoffs
Who hands what to whom, in order, and where blockers go.
```

`agents/<member>/AGENTS.md`:

```markdown
---
name: <Member Name>
slug: <member>
role: lead | implementer | reviewer | scout
reportsTo: <lead>
model: <exact model id>
ponytail: lite | full | ultra
---

You are the <role> of the <Team Name> team: <its one responsibility>.

Follow `miniverse/AGENTS.md` and `miniverse/ponytail.md` on every task, at
the <level> level. Take work only from <lead>, and hand every task back with
what changed, how it was verified, what was skipped, and any risk.
```

The frontmatter is what the agent tool needs to create the member; the lead
has no `reportsTo`. The body is the member's instructions and stays short:
the flow and `ponytail.md` carry the rest and are never copied into it. Set
`status: done` when every plan the team executes is done. **English only.**
