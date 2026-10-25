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

## Revision: simpler container usage

Documentation-only; touches `README.md` and `DOCKERHUB.md`.

1. Replace the Docker quick start with three steps: `docker pull
   victorradael/spacekid`; define the `spacekid` alias and persist it
   (`~/.bashrc` / `~/.zshrc` snippets, plus `source` or opening a new
   terminal); then `spacekid init`. The alias is single-quoted so `$PWD` and
   the user ids resolve at call time, not at definition time.
2. Move the long `docker run` form into a "What the alias does" section
   explaining `--rm`, `-u`, `-v` and the working directory, and use the alias
   in all later examples (`spacekid init --name "My App"`).
3. Add troubleshooting entries: interrupted `docker pull` (retry resumes
   cached layers; try again later or from another network; IPv6 as a
   possible cause) and fallback to `pipx install`; and alias not found
   (profile not reloaded).
4. Mirror steps 1-2 in `DOCKERHUB.md`, using absolute links only.
5. Verify the alias by actually defining it in a shell and running `init`
   in a scratch directory, if the image is available locally; otherwise
   verify with the Python install and say so.
6. Mark the spec criteria and this revision as done and record deviations.

### Revision notes

Implemented as planned, with these notes:

- **Verification.** The published image was not available locally (the
  download had failed), so the real container was not run. The alias was
  verified in bash with a stub `docker` command: it expands with the current
  user ids and directory at call time. The fish form was not run.
- **Docker Hub page.** The old "shell alias" tip was removed; the quick start
  now carries the alias, and pull-retry guidance is a short note there. The
  IPv6 workaround lives only in the README troubleshooting.

### Revision notes — IPv6 pull failure

- The README troubleshooting entry for `docker pull` now has a short IPv6
  procedure: disable IPv6 on the interface with `sysctl`, pull, then revert
  with the same command set back to `0`. It notes that a reboot also reverts.
- Reported and confirmed on a real machine: IPv6 to the Docker CloudFront
  host was reset, IPv4 worked, and disabling IPv6 fixed the pull.
- `DOCKERHUB.md` is unchanged: it keeps only the short retry note and the
  IPv6 detail stays in the README, as before.
