# User Documentation — Implementation Plan

Implements: `specs/user-docs.md`
Status: Done

## Approach

Documentation-only change plus one small CI step. No new tooling, no docs
site: plain Markdown files, with the Docker Hub description synced by an
existing, pinned third-party action in the already-present `publish` job.

Files:

- `README.md` — rewritten as the user guide (GitHub landing page; also the
  package `readme`, so it must stay valid standalone Markdown).
- `DOCKERHUB.md` — Docker Hub overview, container-centric, links to the
  README for the rest.
- `MAINTAINING.md` — release process and one-time maintainer setup, moved
  out of the README.

## Steps

1. Verify every documented behavior against the CLI by running it
   (`init` in project mode, brain mode, repeated runs, `--path`, `--name`,
   `--mode`, `--version`) and capture the real output and file trees for the
   examples. Nothing is documented from memory.
2. Rewrite `README.md` in this order: logo and one-line pitch, status note,
   quick start (Docker first, since that is the main path), install
   (Docker, pipx/pip, version pinning), commands and options table, project
   mode, brain mode and detection rules, existing-files behavior, the
   working loop (condensed from the current "why" sections, keeping the
   mermaid diagram), troubleshooting, contributing/issues, repository
   layout, license. Replace every `<dockerhub-user>` with `victorradael`.
3. Write `DOCKERHUB.md`: tags, run command, options, both modes with short
   examples, shell alias tip, user-id flag explanation, link to GitHub.
   Absolute URLs only (Docker Hub cannot resolve relative links or images).
4. Move "Releasing" and "One-time setup" into `MAINTAINING.md`; link it from
   the README's contributing section.
5. In `.github/workflows/docker.yml`, add a step at the end of `publish`
   using a SHA-pinned `peter-evans/dockerhub-description` that pushes
   `DOCKERHUB.md` as the full description and the one-line `short-description`.
   It reuses the existing `DOCKERHUB_USERNAME`/`DOCKERHUB_TOKEN` secrets.
6. Update the status of this plan and spec, and the release-pipeline spec
   and plan, whose documentation requirement now points to the new layout.

## Key Decisions

- **Docker Hub sync runs only on release.** Keeps a single publishing path
  and credential scope. Trade-off: doc-only commits do not update the page
  until the next release, which matches the spec ("after the next release").
- **Docker Hub description token scope.** That action needs a token with
  read/write/delete permission on the repository, broader than push-only.
  Documented in `MAINTAINING.md`; the token remains scoped to this one
  repository.
- **README stays the package `readme`.** The Dockerfile and `pyproject.toml`
  already copy it; the rewrite must not depend on relative images or files
  other than the logo, which is already used today.
- **No `docs/` folder.** One guide of moderate length is easier to scan and
  maintain than several files for a CLI with a single command.

## Implementation Notes

Implemented as planned, with these notes:

- **`init` was not idempotent.** Running the CLI twice appended the standard
  content again to the spec and plan rule files. The docs first stated this
  plainly; the behavior was then fixed (see the idempotent scaffolding
  spec) and the docs now describe repeated runs as safe.
- **`--path` must exist.** A missing directory ends in a traceback; documented
  in the options table and troubleshooting rather than changed here.
- **Logo URL.** The README uses the absolute `raw.githubusercontent.com` URL
  for the logo (also needed for the Docker Hub page) rather than a relative
  path, so it renders on every surface.
- **Action pin.** `peter-evans/dockerhub-description` pinned to the commit of
  `v5.0.0` (`1b9a80c0...`), verified against the GitHub API.
- **Not verified end to end.** The Docker Hub sync only runs on a release; it
  has not been exercised yet. The image owner `victorradael` is assumed to be
  the Docker Hub account behind `DOCKERHUB_USERNAME`.
