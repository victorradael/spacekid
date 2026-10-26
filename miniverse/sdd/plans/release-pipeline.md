# Automated Releases and Container Image Publishing — Implementation Plan

Implements: `sdd/specs/release-pipeline.md`
Status: Done

## Approach

Replace `.github/workflows/docker.yml` with one workflow, modeled on the
author's `aesiron` Docker Hub workflow, and add `semantic-release` to decide
versions. Three jobs:

- `test` (pull requests and pushes to `main`): `docker build`, `--help`
  smoke test and the file-ownership check already in the current workflow.
  No path filter, so the required check always reports.
- `release` (push to `main` only, `needs: test`): runs `semantic-release`
  with `contents: write`. It analyzes commits (Angular preset), creates the
  tag `vX.Y.Z` and the GitHub Release with notes, and exposes the new version
  as a job output. Nothing is committed back to `main`.
- `publish` (`needs: release`, only if a version was released): buildx,
  `docker/metadata-action`, Docker Hub login, `docker/build-push-action` with
  GHA cache. Tags: `X.Y.Z`, `X.Y`, `latest`.

`semantic-release` is configured in `.releaserc.json` (no Node project is
added to the repo; plugins are installed by the action). Plugins:
`commit-analyzer`, `release-notes-generator`, `github` (comments disabled so
no issue/PR write permission is needed). No `git`/`changelog` plugin, so
branch protection needs no bypass.

Version inside the image: `pyproject.toml` keeps a placeholder, since there is
no commit-back. The `publish` job passes the version to the Dockerfile as a
build arg, and the Dockerfile rewrites the `version` line in `pyproject.toml`
before `pip install`. The CLI gains `--version`, reading the installed
package metadata, so the image can report it.

## Steps

1. Create the baseline tag `v0.1.0` on the current `main` commit (maintainer
   action, pushed before the workflow lands); without it the first release
   would be `1.0.0`. Existing `js-v*` tags are ignored by setting
   `tagFormat: "v${version}"` and `branches: ["main"]`.
2. `.releaserc.json` as described above.
3. `src/spacekid/cli.py`: add `--version` (`importlib.metadata.version`),
   plus a test.
4. `Dockerfile`: add `ARG VERSION`; when set, `sed` the `version` line in
   `pyproject.toml` before `pip install`. Local builds without the arg keep
   working.
5. Replace `.github/workflows/docker.yml` with the three-job workflow. Top
   level `permissions: contents: read`; `release` overrides to
   `contents: write`. `release` checks out with `fetch-depth: 0` and
   `persist-credentials: false`. The `test` job adds a check that
   `docker run … --version` runs. The `publish` job uses the `production`
   environment (as in `aesiron`) and a final step asserts
   `docker run <image>:<version> --version` equals the release version.
   Third-party actions pinned by SHA, looked up at implementation time.
6. Failure visibility: a failed workflow run emails maintainers via GitHub's
   default notifications; `release` and `publish` are in the same workflow
   so one red run shows both. No extra tooling.
7. README: replace GHCR references with `<dockerhub-user>/spacekid`, replace
   the "Versions are bumped manually" section with the commit conventions
   (`fix:` → patch, `feat:` → minor, `BREAKING CHANGE:` footer → major;
   `docs:`, `test:`, `chore:`, `ci:` → no release) and the one-time setup.
8. Manual repository setup (documented in the README): secrets
   `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` (access token scoped to this
   repository only, ideally in the `production` environment); Docker Hub
   repository `spacekid` created; `main` protected with the `test` check
   required.
9. Update `specs/cli-distribution.md` and `plans/cli-distribution.md`: the
   GHCR registry and manual versioning decisions are superseded by this
   work. Set statuses on this spec and plan.

## Key Decisions

- **Three jobs instead of building inside semantic-release.** The release
  decision stays in `semantic-release`; image building uses the standard
  Docker actions (cache, metadata, multi-tag). Trade-off: version handoff
  through a job output.
- **No commit-back to `main`.** Same reasoning as the earlier release
  design: no branch-protection bypass. The version is injected at image build
  time instead of being checked in.
- **Docker Hub only, GHCR dropped.** Matches the spec's scope and avoids
  maintaining two registries. Trade-off: existing GHCR tags stop receiving
  updates.
- **Long-lived Docker Hub token.** Docker Hub has no OIDC publishing, so a
  scoped access token in a protected environment is the least-bad option.
- **Unfiltered `test` job**, so the required check always reports.

## Risks

- `semantic-release` counts all commits on `main`, including Python-only and
  docs ones; only the conventional types decide whether a release happens,
  which is what the spec requires (no path scoping needed here).
- If `publish` fails after `release` tagged, the tag exists without an image.
  Recovery: re-run the failed `publish` job (it uses the tag's version).

## Implementation Notes

All steps done, with these deviations and caveats:

- Step 1 and step 8 are maintainer actions and were not performed: the `v0.1.0`
  tag, Docker Hub repository, secrets, `production` environment and branch
  protection must be set up before the first merge to `main`.
- The workflow was not run on GitHub. Locally verified: tests (17 pass) and
  an image build with `--build-arg VERSION=9.9.9` whose `--version` printed
  `spacekid 9.9.9`.
- Action SHAs were resolved with `git ls-remote` (no `gh` available):
  buildx v4.4.1, login v4.6.0, metadata v6.2.0, build-push v7.4.0,
  `cycjimmy/semantic-release-action` v8.1.2.
- `semantic-release` runs through `cycjimmy/semantic-release-action`; the
  plugin list is in `.releaserc.json` as planned.
- The `publish` job checks out the release tag, and builds with `load: true`
  so the final version assertion can run the pushed image locally.
- Docs-only changes still trigger the `release` job, which exits without a
  release; `publish` is skipped.
- The README originally used `<dockerhub-user>` as a placeholder because the
  Docker Hub account name was not recorded in the repository. Superseded: the
  user documentation now uses `victorradael/spacekid`, the release process and
  one-time setup moved to `MAINTAINING.md`, and the `publish` job also syncs
  `DOCKERHUB.md` to the Docker Hub page (token needs Read, Write, Delete).
