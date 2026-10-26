# macOS Support

Status: Implemented

## Context

SpaceKid is used through its container image. Many developers work on Macs,
and a large share of those use Apple Silicon. Today the image is published for
one processor family only, so on those Macs it either runs through slow
emulation with a warning, or does not run at all. The documented shortcut and
troubleshooting also assume a Linux machine.

Developers on a Mac should get the same experience as everyone else: pull the
image, add the shortcut, run the command.

## Requirements

- The same image name and version tags work on Macs with Apple Silicon and
  Macs with Intel processors, as well as on Linux machines, with no extra
  flags and no emulation.
- Running the tool on a Mac produces the same results as on Linux: same
  commands, same output, same files created.
- Files created in the user's project on a Mac belong to the user.
- The documentation tells Mac users what they need installed to run
  containers, and gives a shortcut and troubleshooting steps that work on
  their system.
- Documentation that is specific to Linux is labeled as such.
- Every release is checked on both processor families before it is published,
  so a broken build for one of them is never released.
- If one image cannot serve every platform well, it is acceptable to build
  and publish distinct image versions through separate release flows, as long
  as users still see one name and are never asked to pick a platform.
- The tool's behavior, commands and results are unchanged.
- All documentation is written in English.

## Acceptance Criteria

- [ ] Pulling the image on an Apple Silicon Mac gives a native image, with no
      platform warning.
- [ ] Pulling the image on an Intel Mac and on Linux still works.
- [ ] `init` run on a Mac creates the expected files, owned by the user.
- [ ] The README and Docker Hub page explain what a Mac user needs and show a
      shortcut that works on macOS.
- [ ] Linux-only troubleshooting steps are clearly marked as Linux-only, and a
      Mac equivalent is given where one exists.
- [ ] A release is not published if the image fails its checks on either
      processor family.

## Out of Scope

- Native macOS installers or binaries.
- Windows support.
- Changing what the tool does.
