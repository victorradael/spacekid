# Image and Supply-Chain Security

Status: Implemented
Created: 2026-11-23
Updated: 2026-11-23

## Context

SpaceKid is used only through its container image, and that image runs inside
users' projects with access to their files and repositories. A scan of the
published image found 64 known vulnerabilities, including one critical and
four high-severity ones that already had fixes available, because the image
is built on an older base and is only rebuilt when the tool itself changes.
Nothing in the release process detects this, and base-image updates never
produce a release. Users inherit every known flaw of the image they pull.

## Requirements

- The published image carries no known critical or high-severity
  vulnerability for which a fix is available at build time.
- Every build installs the latest security fixes of its base, and the base is
  identified immutably, so a build is reproducible and cannot be silently
  swapped.
- Every proposed change and every release is scanned for known
  vulnerabilities; a fixable critical or high finding blocks the merge and the
  release.
- The scan also runs on a regular schedule, so new vulnerabilities in an
  unchanged image are reported to maintainers without anyone looking.
- Base-image updates reach users: accepting one publishes a patch release.
- Release builds start clean, never reusing layers built by earlier runs.
- Each published image comes with a verifiable record of how it was built and
  what it contains.
- The image has no programs able to gain privileges, and runs as an
  unprivileged user.
- The documented way to run SpaceKid drops every privilege the tool does not
  need, without changing what it does.
- Running `init` never writes through a link that points elsewhere: a linked
  file is treated as existing and left untouched.
- The build and release automation keeps credentials out of places they are
  not needed, and newly released automation dependencies are not adopted the
  moment they appear.
- Every command, option and result stays as before.

## Acceptance Criteria

- [x] A scan of the new image shows no critical finding and no fixable
      critical or high finding (64 → 42 findings, all without an available
      fix).
- [x] The base image is pinned immutably and upgraded at build time.
- [ ] Pull requests, releases and a weekly schedule scan the image and fail on
      fixable critical or high findings.
- [ ] Accepting a base-image update produces a patch release.
- [ ] Release builds reuse no layers from earlier runs and publish build
      provenance and a software bill of materials.
- [ ] The image contains no setuid or setgid programs.
- [x] The documented run command drops all capabilities and forbids privilege
      escalation, and the smoke test runs with it.
- [x] `init` skips a linked file instead of writing through it.
- [x] Source checkouts in automation do not keep credentials.
- [x] `--help`, `--version`, `init`, `scan` and `sync` behave as before, and
      the automated tests pass.

Unchecked items are in place and are confirmed by the first run of the
release automation.

## Out of Scope

- Vulnerabilities with no fix available upstream; they are reported, not
  blocked on.
- Protecting users from running the scripts of a miniverse they do not trust:
  `scan` and `sync` run the project's own scripts by design.
- Signing images with a separate signing service.

## Traceability

- Plans: `sdd/plans/image-security.md` (added 2026-11-23)
- Contexts: `contexts/container-security.md` (added 2026-11-23)
- Artifacts: `artifacts/image-security/vulnerability-scan-2026-11-23.md` (added 2026-11-23)
