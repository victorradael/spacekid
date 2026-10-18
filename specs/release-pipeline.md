# Automated Releases and Container Image Publishing

Status: Implemented

## Context

SpaceKid is a command-line tool that most people run from a container image.
Today, releasing means a maintainer manually choosing a version number,
editing it, tagging it, and publishing the image to a registry that most users
do not search first. This is slow, error-prone, and makes version numbers
inconsistent with what actually changed.

Releases should happen as a natural consequence of merging reviewed changes,
with version numbers that communicate the impact of each change, and the image
should be available on Docker Hub, where users expect to find it.

## Requirements

- Every change merged to the main branch is evaluated automatically. If it
  contains a user-visible change, a new release is created with no manual
  step.
- The version number follows semantic versioning and is derived from the
  change history: fixes produce a patch release, new features a minor release,
  and breaking changes a major release. Changes with no user-visible effect
  (documentation, tests, internal tooling) never produce a release.
- Each release has release notes generated from its changes, visible to users
  alongside the version.
- Each release publishes a container image to Docker Hub, tagged with the
  full version, the major.minor version, and `latest`, so users can pin as
  tightly or as loosely as they want.
- The version reported by the tool inside a released image matches the
  release version.
- Proposed changes are built and smoke-tested before they are merged, without
  publishing anything. A failing build or test blocks the release.
- Publishing credentials are limited to the registry and stored as protected
  repository secrets; no other credentials are needed to release.
- A failed release is visible to maintainers without them having to look for
  it.
- The first automated release continues the existing version numbering; it
  does not restart from a lower or arbitrary number.
- Documentation explains how to use the image from Docker Hub, how to pin a
  version, and which commit message conventions drive releases.

## Acceptance Criteria

- [ ] Merging a fix to the main branch publishes a new patch version image
      with no other manual action.
- [ ] Merging a new feature publishes a new minor version; merging a breaking
      change publishes a new major version.
- [ ] Merging a documentation-only or test-only change publishes nothing.
- [ ] Each release has release notes listing its changes.
- [ ] The image is available on Docker Hub under the full version,
      major.minor, and `latest` tags.
- [ ] Running the released image reports the same version as the release.
- [ ] A failing build or test on a proposed change is reported before merge
      and nothing is published.
- [ ] A failed release is clearly visible to maintainers.
- [ ] The first automated release continues the existing version numbering.
- [ ] Documentation covers Docker Hub usage, version pinning, and commit
      conventions.

## Out of Scope

- Publishing to registries other than Docker Hub.
- Publishing the tool to a package index.
- Pre-release or beta channels.
- Automatically rewriting repository files (such as a changelog) as part of a
  release.
