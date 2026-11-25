# Ponytail Skill

Summary: what the ponytail skill is, which upstream parts the miniverse vendors in `ponytail.md`, how this repo checks upstream for updates on every task, and how to refresh that copy.
Created: 2026-11-25
Updated: 2026-11-25

## What it is

An MIT-licensed prompt (GitHub `DietrichGebert/ponytail`) that makes an agent
write only what the task needs: before coding it climbs a ladder (does it
need to exist, is it already in the codebase, standard library, platform
feature, installed dependency, one line, only then the minimum plus one small
test). It never cuts validation, error handling, security, or accessibility.
Its own benchmark reports about -45% output tokens and -26% cost at equal or
better test coverage.

## Upstream layout

- `skills/ponytail/SKILL.md` — the rules plus levels (lite, full, ultra);
  `AGENTS.md` at the root is the same rules without levels.
- `skills/ponytail-review`, `ponytail-audit`, `ponytail-debt` — review of a
  change, audit of a repo, ledger of `shortcut:` comments.
- `ponytail-gain` (benchmark stats), `ponytail-help`, and per-tool plugin
  folders (`.claude-plugin`, `.codex-plugin`, `.cursor`, ...) only package it.

## What the miniverse does with it

SpaceKid vendors it: `miniverse/ponytail.md` (template
`src/spacekid/templates/ponytail.md`) is an adapted copy of v5.3.3, commit
`ebd8654`, with the MIT notice. Nothing is installed, and the upstream plugin
must not be installed on top (two copies drift). Adaptations: the review
gates "done" in the flow, the audit report is an artifact, the shortcut
ledger goes to the plan's Implementation Notes, the closing reply is the
handoff's skipped/risk part, the lead uses `ultra` for spec and plan. Gain,
help, install steps and slash commands are dropped.

## Checking for updates (standard in this repo)

Decided by the user on 2026-11-25: every task in this repository starts by
checking upstream for a newer ponytail release (flow step 0.7). It is a
manual process, done by the agent itself, and nothing is installed. The check
only reads the remote:

```sh
git ls-remote --tags --refs https://github.com/DietrichGebert/ponytail
```

Compare the highest `vX.Y.Z` tag with the version in `ponytail.md`. If equal,
carry on with the task. If newer, tell the user and refresh the copy as its
own change (its own branch and PR, through the flow and the review), not
inside the task at hand.

## Refreshing the copy

Read upstream `AGENTS.md` and `skills/ponytail*/SKILL.md` at the new tag
(for example via `raw.githubusercontent.com`, or a throwaway shallow clone
outside the repo) and diff them against the recorded tag. Carry real rule
changes into the template `src/spacekid/templates/ponytail.md` and this repo's
`miniverse/ponytail.md`, keeping the adaptations above, and bump the version
line there and the version and commit here. Never install the skill or
plugin. Existing miniverses keep their copy (`write_or_skip`); users refresh
it by hand.
