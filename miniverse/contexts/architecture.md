# SpaceKid Architecture

Summary: how the CLI, its templates, and the generated miniverse fit together.
Created: 2026-10-26
Updated: 2026-10-26

## Shape

- A small Python CLI (`src/spacekid/`): `cli.py` (argparse, one `init`
  command, interactive menu), `ui.py` (colors, banner, menu), `scaffold.py`
  (writes the miniverse).
- Everything written to a user's directory comes from `src/spacekid/templates/`:
  the guides (`*_agents.md`), the initial `catalog.md`, and the standalone
  `scan.sh`. `{{APP_NAME}}` is the only placeholder.
- Distribution is container-only; Python is an internal detail.

## Write behavior

- `write_or_skip` for files owned by the user once created (root and miniverse
  guides, marker, scanner, catalog, `.gitkeep`).
- `write_or_append` for the four folder guides: appended only when the file
  lacks the standard text, so repeated runs change nothing.

## The scanner

`scan.sh` is POSIX `sh` and runs without SpaceKid. It finds miniverses by the
`.miniverse` marker, computes level, ancestors, and the descendant tree, and
rewrites `catalog.md` only when content changed. Its output has no timestamps,
so it is deterministic. Tests in `tests/test_scanner.py` run it in temp trees.

## Dogfooding

This repo's own specs and plans live in `miniverse/sdd/`; a test keeps them
compliant with the spec rules and ensures no root `specs/` or `plans/` return.
