# Repository Sync

Status: Draft
Created: 2026-10-29
Updated: 2026-10-29

## Context

Agents read the current state of a project from its repositories. When a
repository is behind its remote, or sits on a branch nobody remembers, the
agent builds its picture of the project on stale or wrong information.

A miniverse can cover several repositories side by side, and miniverses nest:
repositories live at every level below it. Keeping them all current by hand,
one at a time, does not scale and gets skipped.

## Requirements

- Every miniverse must include a ready-to-run script that brings the
  repositories it covers up to date. The script must work on its own, without
  requiring SpaceKid to be available.
- The script must use the miniverse's catalog of nested miniverses (refreshing
  it first) to find every level, and sync the repositories living at the
  miniverse's own level, side by side, and at each nested miniverse's level.
  Wherever it is started, it covers everything from its own level down to the
  lowest one.
- For each repository, the script must report the branch it is on, then update
  that branch from its remote.
- The script must offer an optional mode that first moves every repository to
  the `main` branch and then updates it.
- Work in progress must never be lost or overwritten: a repository with
  uncommitted changes is not moved to another branch, and an update that would
  need a merge is not forced.
- A problem in one repository (no remote, no `main`, uncommitted changes,
  network failure) must be reported for that repository and must not stop the
  others.
- The script must finish with a summary of what was updated and what needs
  attention, and must signal failure when any repository could not be
  updated.
- The script's output must follow the same visual style as the SpaceKid
  command: colors and symbols that make each result readable at a glance. The
  large project logo belongs to the main command only; these scripts show a
  compact one-line mark. Wherever output is piped, redirected, or color is
  opted out, it stays plain text.
- The script must never ask for input, so an agent can run it unattended.
- The miniverse flow must tell agents to run the script before reading the
  state of the projects, so their context is current.

## Acceptance Criteria

- [ ] Every created miniverse contains the script, ready to run.
- [ ] Run from a miniverse covering several repositories, it reports the branch
      of each and updates each from its remote.
- [ ] Repositories at the level of every nested miniverse, at several depths,
      are all found through the catalog.
- [ ] With the `main` option, repositories on another branch end up on `main`
      and updated; repositories with uncommitted changes stay where they are
      and are reported.
- [ ] A repository without a remote or without `main` is reported and the rest
      are still processed.
- [ ] A final summary lists successes and problems; the script fails when there
      was any problem.
- [ ] Running it never modifies uncommitted work and never creates merge
      commits.
- [ ] On a terminal, the output shows a compact one-line mark (not the large logo) and
      color-coded symbols
      (updated, already current, problem); piped, redirected, or with color
      opted out, it is plain text without decoration.
- [ ] The script works without SpaceKid, from any directory, and never waits
      for input.
- [ ] The miniverse guide requires running the script to refresh the
      repositories before reading the current state of the projects.

## Out of Scope

- Branches other than the current one and `main`.
- Pushing, committing, stashing, or resolving conflicts.
- Updating the script inside miniverses created before this feature.

## Traceability

- Plans: `sdd/plans/repo-sync.md` (added 2026-10-29)
- Contexts: `contexts/architecture.md` (added 2026-10-29)
- Artifacts: —
