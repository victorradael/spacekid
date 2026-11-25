# Ponytail Skill

Summary: what the ponytail skill is, its official sources, how it installs per agent tool, and its commands.
Created: 2026-11-25
Updated: 2026-11-25

## What it is

An MIT-licensed prompt that makes an agent write only what the task needs:
before coding it climbs a ladder (does it need to exist, is it already in the
codebase, standard library, platform feature, installed dependency, one line,
only then the minimum plus one small test). It never cuts validation, error
handling, security, or accessibility. Its own benchmark reports about -45%
output tokens and -26% cost at equal or better test coverage.

The whole skill is one prompt, `skills/ponytail/SKILL.md`; `AGENTS.md` at the
repo root is the compact rules-file version. Everything else adapts it to
agent tools. Latest release when checked: `v5.3.3` (2026-11-25).

## Official sources only

GitHub `DietrichGebert/ponytail` and npm `@dietrichgebert/ponytail`. The author
states it never ships `.exe` or `.dll`; a copy that does is not official.

## Install

- Claude Code: `/plugin marketplace add DietrichGebert/ponytail`, then
  `/plugin install ponytail@ponytail` (two separate prompts). The plugin also
  injects the rules into subagents.
- Codex: `codex plugin marketplace add DietrichGebert/ponytail` and
  `codex plugin add ponytail@ponytail`; trust its two hooks in `/hooks`.
- Gemini CLI: `gemini extensions install https://github.com/DietrichGebert/ponytail`.
- OpenCode: `opencode plugin add @dietrichgebert/ponytail`.
- Copilot CLI: `copilot plugin marketplace add DietrichGebert/ponytail`, then
  `copilot plugin install ponytail@ponytail`.
- Any other tool: copy the repo's `AGENTS.md` into the agent's rules, or
  install `skills/ponytail/SKILL.md` as a skill. Full list: the repo's
  `INSTALL.md`.

Plugin hooks need `node` on the PATH; without it the skill still works.

## Commands

`/ponytail [lite|full|ultra|off]` (level), `/ponytail-review` (review the diff
and the code it touches: bugs, security, load, missing tests, what to cut),
`/ponytail-audit` (same, whole repo, ranked), `/ponytail-debt` (collect
`shortcut:` comments), `/ponytail-gain`, `/ponytail-help`. Commands need a
skill-capable host; rules-file installs get the always-on rules only.

## How SpaceKid uses it

The team guide (`sdd/teams/AGENTS.md` in a generated miniverse) requires every
team member to carry it and the reviewer to run `/ponytail-review`. SpaceKid
never installs it.
