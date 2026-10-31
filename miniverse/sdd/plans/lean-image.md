# Lean Container Image — Implementation Plan

Implements: `sdd/specs/lean-image.md`
Status: Done

## Approach

Only the `Dockerfile` changes. The image was `python:3.14-slim` (Debian base
plus a full CPython) with `pip install` and `git` on top: 196MB on disk, 48MB
compressed. The CLI uses the standard library only, so a minimal Alpine base
with the distro's Python and `git` is enough. Two stages keep build tooling
out of the final image, and unused parts of the standard library are removed.

## Steps

1. Build stage (`alpine`): install `python3`, `py3-pip`, `py3-setuptools`;
   apply the `VERSION` build arg as before; `pip install --prefix=/out
   --no-build-isolation .` (no network needed for build deps).
2. Final stage (`alpine`, same release, so Python versions match): install
   `python3` and `git` only; create the `spacekid` user (uid 1000).
3. In the same `RUN`, delete standard-library parts the CLI never imports
   (`ensurepip`, `idlelib`, `lib2to3`, `pydoc_data`, `tkinter`, `test`,
   `unittest`, `asyncio`, `multiprocessing`, `sqlite3`, `curses`, `dbm`, and
   their extension modules) and all `__pycache__`.
4. `COPY --from=build /out/ /usr/` brings the entry script and package
   metadata (needed for the reported version).
5. Keep `USER`, `WORKDIR /project` and `ENTRYPOINT ["spacekid"]`.
6. Verify: build; compare sizes; run `--help`, `--version`, `init`, `scan`,
   `sync` as the host user on a mounted directory; run the test suite.

## Key Decisions

- **Alpine over distroless/scratch.** `scan.sh` and `sync.sh` need `sh`, `find`
  and `git`; Alpine supplies them at a few MB. Distroless would need extra
  work for no further meaningful gain.
- **Distro Python, not the `python` Alpine image.** The official Alpine
  Python image still ships the full library and `pip`; the distro package
  plus pruning is smaller. Python minor version now follows the Alpine release.
- **Pruning list is conservative.** Only modules the CLI and tests do not
  import; `subprocess`, `argparse`, `importlib.metadata`, `dataclasses` and
  `pathlib` stay.
- **Same Alpine release in both stages** so the site-packages path matches.

## Implementation Notes

Result: 196MB → 67.6MB on disk, 48.5MB → 18.3MB compressed (about 65% smaller).
`--version`, `init`, `scan` and `sync` verified in a mounted directory as the
host user, including `sync` against a git repository. Alpine is multi-arch, so
the amd64 and arm64 builds are unchanged in the workflow.
