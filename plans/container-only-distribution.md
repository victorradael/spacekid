# Container-Only Distribution — Implementation Plan

Implements: `specs/container-only-distribution.md`
Status: Done

## Approach

Documentation and metadata change only. The Python package, its console
scripts and the Dockerfile stay as they are: the image installs the package
internally, so behavior cannot change. What goes away is every user-facing
mention of installing through Python.

## Steps

1. `README.md`: delete the "With Python" install section, the "Install"
   split between two methods (keep a single "Install" that points to the
   Quick start and version pinning), the `pipx` troubleshooting entry, and the
   `pipx` fallback in the migration note. Remove "Prefer a local install
   without Docker?" from the Quick start.
2. `README.md` troubleshooting: remove the "use the Python install" fallback
   from the failed-pull entry; keep retry, wait/other network, and the IPv6
   workaround.
3. `README.md`: replace the migration note with one covering former `npm` and
   `pipx`/`pip` users: install the container and the shortcut, then run
   `spacekid init`. State the `sk` short name is no longer part of the
   documented interface.
4. `DOCKERHUB.md`: change the "Full documentation" blurb that mentions
   installing with Python.
5. Contributor-facing text (`MAINTAINING.md` and a short "Contributing" note
   in the README): mention that the CLI is written in Python as an internal
   detail, and how to run tests locally. This is the only place Python
   appears.
6. `pyproject.toml` stays (the Dockerfile builds from it). Remove the `sk`
   console script and the test that asserted it.
7. Update the superseded requirement: in the CLI distribution spec and plan,
   mark the "installed on a machine with Python" way as retired and point to
   this work; in the user-docs spec and plan, drop the Python install from the
   documentation scope.
8. Verify: grep the user-facing files for `pipx`, `pip install` and
   "Python install"; run the test suite; build the image and run `init` in a
   scratch directory.

## Key Decisions

- **Keep Python as the implementation.** Rewriting is out of scope and would
  add risk with no user benefit.
- **Remove the `sk` script, keep the package metadata.** `sk` is no longer an
  interface, so dead code goes; the image still builds from the metadata.
- **No pre-built native binaries for now.** The container is the single
  channel; revisit only if Docker proves too heavy a requirement.

## Implementation Notes

All steps done as planned, with these notes:

- The `pipx`/`pip` mention that remains in the README is the migration note for
  former users, which the spec requires. No install command is shown.
- Step 5 landed as a "Development" section in `MAINTAINING.md` (with the local
  test commands) plus a short note in the README's contributing list.
- Step 7 also updated the specs of the two earlier pairs (statuses unchanged);
  the retired direct-install criterion is struck through, not deleted.
- Step 6 was first left as "keep `sk`, undocumented", then changed on review:
  the script and its test were removed as dead code.
- Verification: 20 tests pass; the image builds and `init` in an empty scratch
  directory prints and creates the same files as before. The Docker Hub text
  only updates on the next release.
