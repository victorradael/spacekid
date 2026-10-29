# CLI Scan and Sync

Status: Implemented
Created: 2026-10-29
Updated: 2026-10-29

## Context

Refreshing the catalog and bringing repositories up to date are part of every
miniverse flow, and today they exist only as scripts inside the miniverse. A
user (or an agent) working through the SpaceKid command naturally types
`spacekid scan` or `spacekid sync` and gets an "invalid choice" error. The
command should offer these actions too, without changing what the scripts do.

## Requirements

- The SpaceKid command must offer a `scan` action that refreshes the
  miniverse's catalog, with the same behavior and output as the miniverse's own
  scan script.
- The SpaceKid command must offer a `sync` action that updates the miniverse's
  repositories, with the same behavior and output as the miniverse's own sync
  script, including the option to move every repository to `main` first.
- Both actions must work on the current directory by default and accept a
  directory to act on, like the init action.
- The miniverse can be given as its project directory (the one that contains
  the miniverse folder) or as the miniverse folder itself.
- The result must be exactly what the script reports: its output, its colors
  (or plain text when piped), and its exit status (success, needs attention,
  bad usage).
- When there is no miniverse in the directory, or it lacks the script, the
  action must say so clearly, point the user to the init action, and fail.
- The container image must be able to run both actions, including the
  repository updates.
- The actions must appear in the command's help and in the interactive menu.
- User documentation must describe both actions.

## Acceptance Criteria

- [ ] `scan` refreshes the catalog and prints what the scan script prints.
- [ ] `sync` updates the repositories and prints what the sync script prints.
- [ ] `sync --main` moves repositories to `main` before updating.
- [ ] Both accept a directory to act on and work from the project directory or
      the miniverse folder.
- [ ] The exit status matches the script's.
- [ ] Without a miniverse, or without the script, the user gets a clear message
      pointing to init, and the action fails.
- [ ] The container image can run `sync` against a mounted project.
- [ ] Help and the interactive menu list both actions.
- [ ] README and Docker Hub page describe them.

## Out of Scope

- Changing what the scripts do.
- Creating a miniverse implicitly when none exists.

## Traceability

- Plans: `sdd/plans/cli-scan-sync.md` (added 2026-10-29)
- Contexts: `contexts/architecture.md` (added 2026-10-29)
- Artifacts: —
