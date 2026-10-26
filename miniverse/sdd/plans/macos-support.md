# macOS Support — Implementation Plan

Implements: `sdd/specs/macos-support.md`
Status: Done

## Approach

Publish a multi-arch image (`linux/amd64` + `linux/arm64`) under the existing
tags. Docker on a Mac picks the native variant from the manifest list, so no
flag or tag change is needed. The Dockerfile already builds on
`python:3.14-slim`, which is multi-arch, and the package is pure Python, so
no Dockerfile change is expected. The rest is CI and documentation.

## Steps

1. `.github/workflows/docker.yml`, `publish` job: add
   `docker/setup-qemu-action` (pinned by SHA, like the other actions) before
   buildx, and set `platforms: linux/amd64,linux/arm64` on
   `build-push-action`.
2. Same job: `load: true` cannot load a multi-platform image. Replace the
   "Check image reports the release version" step so it runs against each
   platform after the push, with
   `docker run --rm --platform <p> "$IMAGE:$VERSION" --version`, for both
   platforms. A failure fails the job after push, so also reorder: build and
   verify per platform first (see Key Decisions), push only when both pass.
3. `test` job: build and smoke-test both platforms on PRs. amd64 runs on
   `ubuntu-latest` as today; arm64 runs on `ubuntu-24.04-arm` (native
   runner, no emulation) via a matrix on `runs-on`.
4. `README.md` and `DOCKERHUB.md`:
   - Add a "Requirements" note: Docker Desktop, OrbStack or Colima on macOS;
     Docker Engine on Linux.
   - Keep the zsh alias (zsh is the macOS default); mention `~/.zshrc` vs
     `~/.bash_profile` for bash on macOS.
   - Verify that `-u "$(id -u):$(id -g)"` works on macOS (UID 501, GID 20)
     with Docker Desktop and document the result; if file ownership needs a
     different flag there, document it.
   - Mark the IPv6 `sysctl` / `ip -br link` troubleshooting as Linux-only and
     add the macOS note (Docker Desktop network settings / restart) if one
     applies.
5. Verify: build both platforms locally with buildx, run `--version` and
   `init` under each (arm64 via QEMU here); test on a real Mac if available,
   since this machine is Linux.
6. After implementing: update this plan and the spec statuses, and revisit
   the release-pipeline and container-only-distribution plans, since they
   describe the publish job and the install docs.

## Key Decisions

- **Multi-arch manifest, not separate tags.** One name works everywhere; users
  never choose an architecture.
- **Native arm64 runner for PR tests, QEMU only for the publish build.**
  Testing under emulation is slow and can hide or invent failures; the native
  runner is faster and more faithful. QEMU is needed only to build the arm64
  image on an amd64 runner. Alternative: build arm64 natively in a matrix and
  merge manifests, which is more moving parts; rejected for KISS while build
  time stays acceptable (pure Python, small image).
- **Verify before pushing.** The current flow pushes, then checks. With two
  platforms, a broken variant would already be on `latest`. Build with
  `load` per platform and test, then push.
- **Separate pipelines per platform are allowed if needed.** The single
  multi-arch build is the starting point, not a commitment. If it proves too
  slow, flaky under QEMU, or needs platform-specific build steps (or even a
  platform-specific Dockerfile), split it: one job or workflow per platform,
  each building natively and pushing a platform-suffixed tag (for example
  `<version>-arm64`), followed by a final job that merges them into the
  user-facing tags (`<version>`, `<major>.<minor>`, `latest`) with
  `docker buildx imagetools create`. The merge job runs only if every
  platform job passed. Users keep pulling the same name; the per-platform
  tags are an internal detail and are not documented as an install option.
- **No Dockerfile change unless the verification shows one is needed.**

## Implementation Notes

- Step 2: instead of reordering around a single build, `publish` builds and
  checks `linux/amd64` and `linux/arm64` one at a time (`load: true`, run with
  `--platform`, QEMU for arm64), then pushes both in one multi-platform build
  that reuses the layer cache. Nothing is pushed unless both checks pass.
- `setup-qemu-action` is pinned to the v4.4.0 commit SHA.
- Step 4: the ownership behavior on macOS (UID 501) is documented from how
  Docker Desktop shares folders; it was **not** verified on a real Mac, since
  this machine is Linux. Likewise the workflow has not run in CI yet; the first
  PR will exercise the `test` matrix, the first release the `publish` job.
- No Dockerfile change. Docs for the release-pipeline and
  container-only-distribution plans were not edited: their descriptions of the
  publish job (single-platform `load: true` check) are now superseded by this
  plan.
