# Ponytail Skill

Summary: what the ponytail skill is, which upstream parts the miniverse vendors in `ponytail.md`, and how to refresh that copy.
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

## Refreshing the copy

Compare upstream `skills/ponytail*/SKILL.md` against the tag recorded in
`ponytail.md`, carry real rule changes into the template and this repo's
copy, and bump the version line. Existing miniverses keep their copy
(`write_or_skip`); users refresh it by hand.
