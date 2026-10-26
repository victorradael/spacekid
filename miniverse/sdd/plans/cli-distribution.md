# CLI Distribution — Implementation Plan

Implements: `sdd/specs/cli-distribution.md`
Status: Done

Note: the direct-install channel described here (the `sk` script, the
"installed on a machine with Python" way) was retired by
`plans/container-only-distribution.md`. The container is the only channel.

## Approach

Keep the single Python package as the only implementation and add two thin
delivery channels around it: a second console script (`sk`) and a Docker image
that simply `pip install`s the package. No new code paths; the image is a
wrapper, so behavior cannot diverge.

## Steps

1. `pyproject.toml`: add `sk = "spacekid.cli:main"` to `[project.scripts]`.
   Test that both entry points resolve to the same callable.
2. `Dockerfile` (repo root): `python:3.12-slim`, install the package from the
   build context, `WORKDIR /project`, `ENTRYPOINT ["spacekid"]`. Run as a
   non-root user; document `docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/project" ghcr.io/victorradael/spacekid init`
   so created files are owned by the caller. Add `.dockerignore` (exclude
   `js/`, `.git`, tests).
3. `.github/workflows/docker.yml`: build on PRs (no push, smoke test
   `docker run … --help`); on version tags, build and push to GHCR as
   `:X.Y.Z` and `:latest` using `GITHUB_TOKEN` (`packages: write`), actions
   pinned by SHA like the existing workflow.
4. Python release: tag `vX.Y.Z` derived from `pyproject.toml` version drives
   the image tag. Version bumps stay manual (KISS); no semantic-release for
   Python.
5. Retire JS: delete `js/` and `.github/workflows/js.yml`; mark
   `specs/js-sdk.md`, `specs/js-release.md` and their plans as superseded
   (keep them as history, do not delete). Optionally publish a final npm
   release deprecating the package with a message pointing to the new usage
   (`npm deprecate`; maintainer action).
6. Update `specs/mcp-setup.md`/`plans/mcp-setup.md`: drop the JS/TS parity
   requirement and criterion; the command ships only in the Python CLI and
   therefore also in the image.
7. README: restructure around "Install (pipx/pip)" and "Run with Docker",
   remove JS sections and the npm release section, add a migration note.
8. Update statuses in all affected specs and plans.

## Key Decisions

- **Non-root via `-u` flag rather than baked-in UID.** The host UID varies;
  mapping at run time is the simplest way to satisfy file ownership.
- **GHCR over Docker Hub.** Same registry as the repo, no extra secret.
- **Manual versioning for Python.** Avoids bringing back release tooling
  we just chose to drop with the JS package.
- **Keep retired JS specs as history** with a "Superseded" status instead of
  deleting, so the decision trail survives.

## Implementation Notes

All steps done. Deviations:

- Step 1: the entry-point test reads `pyproject.toml` with `tomllib`, so it is
  skipped on Python < 3.11.
- Step 2: `.dockerignore` also excludes `specs/`, `plans/`, `assets/` and
  `.mcp.json`. The image user has UID 1000; `-u` overrides it at run time.
- Step 3: the workflow also checks that the pushed tag matches the
  `pyproject.toml` version, and the PR smoke test asserts that files created
  through the container are owned by the caller. Dependabot now tracks
  `docker` instead of `npm`.
- Step 6: `specs/mcp-setup.md` already contained no JS/TS parity requirement
  and has no plan yet, so nothing needed changing.
- Verified locally: tests, both console scripts, image build, and file
  ownership via `docker run -u`. The publish job has not run against GHCR yet.
- Pending maintainer action: `npm deprecate` on the published package with a
  pointer to the new usage.
- Superseded in part by `plans/release-pipeline.md`: the image is now
  published to Docker Hub (not GHCR), and versions are derived from commit
  messages by `semantic-release` instead of being bumped manually.
- Update (miniverse): `.dockerignore` now excludes `miniverse/` instead of
  the root `specs/` and `plans/` folders, which no longer exist.
