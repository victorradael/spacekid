# JS Package Automated Release

Status: Implemented, awaiting first live release (requires one-time maintainer setup). No acceptance criteria changed.

## Context

The JavaScript package can only be used with a one-line command or a normal
install once it is published to the public npm registry. Today nothing
publishes it: a maintainer would have to do it by hand from their own
machine, using personal credentials, and decide each version number
manually. That is slow, easy to get wrong, and puts publishing rights in the
hands of whoever happens to have a laptop logged in.

Publishing should be automatic, repeatable, and safe: a change merged to the
main branch that deserves a release produces one, with the right version
number, without anyone handling publishing credentials.

## Requirements

- Every change merged to the main branch is evaluated automatically; if it
  contains a user-visible change to the JavaScript package, a new version is
  published to the public npm registry with no manual step.
- The version number follows semantic versioning and is derived from the
  commit history: fixes produce a patch release, new features a minor
  release, and breaking changes a major release. Changes that do not affect
  the JavaScript package (including Python-only changes, documentation, and
  tests) never produce a release.
- Each release has release notes generated from its commits, visible to
  users alongside the version.
- Tests must pass before anything is published. A failing test run blocks
  the release.
- Publishing must not depend on a long-lived secret stored with the
  project. Credentials used to publish must be short-lived and tied to this
  repository's automated pipeline only.
- Users must be able to verify that a published package came from this
  repository's pipeline and from the commit it claims.
- The same checks (tests) also run on proposed changes before they are
  merged, without publishing anything.
- The first automated release continues the package's existing version
  numbering; it does not restart from a lower or arbitrary number.
- A failed release is visible to maintainers without them having to look for
  it.
- Once the first version is live, the documented commands for installing and
  running the package (install as a dependency, or run on demand without
  installing) work as written.

## Acceptance Criteria

- [ ] Merging a fix affecting the JavaScript package to the main branch
      publishes a new patch version with no manual action.
- [ ] Merging a new feature publishes a new minor version; merging a
      breaking change publishes a new major version.
- [ ] Merging a change that does not affect the JavaScript package publishes
      nothing.
- [ ] Each published version has release notes listing its changes.
- [ ] A failing test run prevents publishing.
- [ ] Once the pipeline is set up and the first release is done, no
      long-lived publishing secret exists in the project's settings (any
      temporary credential used to get started has been revoked).
- [ ] The first automated release continues the existing version numbering.
- [ ] A failed release is clearly visible to maintainers.
- [ ] A published version can be verified as originating from this
      repository's pipeline.
- [ ] Tests run on proposed changes before merge and publish nothing.
- [ ] After the first release, running the package on demand without
      installing it, and installing it as a dependency, both work as
      documented.

## Out of Scope

- Releasing the Python package.
- Publishing from any branch other than the main branch (e.g. pre-release
  or beta channels).
- Automatically rewriting the repository's own files (such as a changelog
  file) as part of a release.
