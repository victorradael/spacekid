# Lean Container Image

Status: Implemented
Created: 2026-10-31
Updated: 2026-10-31

## Context

SpaceKid is a small tool, yet its container image is far larger than the work
it does. Since the image is the only way to use SpaceKid, every user pays for
its size on first download, on every version update, and in disk space. A
heavy image also sends the wrong message about a minimalist tool.

## Requirements

- The container image is drastically smaller than the current one: at most
  half of its previous size, on disk and when downloaded.
- Every command, option, menu action and result stays exactly as before,
  including `init`, `scan`, `sync` and `sync --main`.
- Running as the host user on a mounted project keeps working, and files
  created belong to that user.
- The version reported by the tool stays correct, including releases.
- Release publishing keeps working for the same platforms as before.

## Acceptance Criteria

- [x] The image is at most half the size of the previous one, on disk and
      compressed.
- [x] `--help`, `--version`, `init`, `scan`, `sync` and `sync --main` behave
      as before.
- [x] `init` on a mounted project run as the host user creates files owned by
      that user.
- [x] `sync` can update repositories in a mounted project.
- [x] The existing automated tests still pass.

## Out of Scope

- Changing what the tool does.
- Rewriting the tool in another language.

## Traceability

- Plans: `sdd/plans/lean-image.md` (added 2026-10-31)
- Contexts: `contexts/architecture.md` (added 2026-10-31)
- Artifacts: —
