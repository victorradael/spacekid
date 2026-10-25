# User Documentation

Status: Implemented

## Context

SpaceKid is a command-line tool that people discover on GitHub and on Docker
Hub, and most run from the container image. Today the documentation mixes
usage with the philosophy behind the workflow and with maintainer-only
release notes, and the image instructions contain a placeholder instead of
the real image name. A newcomer cannot copy a command and have it work, and
the Docker Hub page has no content of its own.

Running the container today takes one long command with several unexplained
flags, and a shorter everyday form is only mentioned as an optional tip. The
first contact feels heavy and unclear, and when the image download fails
midway (a common network hiccup) the newcomer has no guidance on how to
continue.

People should be able to understand what the tool does, run it successfully
within a minute, and find answers to common problems, on whichever of the two
sites they arrive from.

## Requirements

- The GitHub page must lead with usage: what the tool is, a quick start, then
  details. The reasoning behind the workflow remains, but after usage and
  shorter.
- Every command shown must work as written, with the real published image
  name and no placeholders.
- Container usage must be presented as three short, separate steps: download
  the image once, set up a short everyday command, then use that command. The
  long form of the run command must not be the first thing a newcomer sees.
- The short everyday command must be set up in a way that persists across
  terminal sessions, with instructions for the common shells, and each part
  of the long form must be explained in plain words.
- The documentation must tell the user what to do when the image download
  fails or is interrupted, including that retrying resumes the download.
- The documentation must cover:
  - What SpaceKid is and the project's study-project status.
  - Installation with the container image, including how to pin a version.
  - The quick start: from an empty project to a scaffolded one.
  - Every command and option, with a short description of each.
  - What gets created in each usage mode, with an example of the resulting
    file tree and of the messages the tool prints.
  - How existing files are treated (preserved, appended to, or skipped) and
    what happens when the command is run again.
  - How to choose between project mode and brain mode, and how automatic
    detection decides.
  - The working loop itself: spec, plan, implementation, update.
  - Common problems and their fixes (for example, files created owned by the
    wrong user when running the container).
  - Where to report issues and how to contribute.
- Docker Hub must have its own page, written for someone who only wants to
  run the container: image tags, the run command, the options, examples, and
  a link to the full documentation on GitHub.
- The Docker Hub page must stay current with the repository without manual
  copying.
- Maintainer-only material (release process, one-time setup) must be
  separated from user-facing material so users are not distracted by it.
- All documentation is written in English.

## Acceptance Criteria

- [x] A newcomer can follow the quick start from the GitHub page and end with
      a scaffolded project, copying commands unchanged.
- [x] No placeholder remains in any command shown to users.
- [x] Every command and option the tool offers is documented.
- [x] Both usage modes are documented with example output and file tree.
- [x] The behavior for existing files and repeated runs is documented,
      including that a repeated run leaves the project unchanged.
- [x] A troubleshooting section covers the most common problems.
- [x] The Docker Hub page exists, is self-sufficient for running the
      container, and links to the full documentation.
- [x] Changing the Docker Hub page content in the repository updates the
      published page after the next release, with no manual step.
- [x] Release and maintainer setup material is clearly separated from
      user-facing documentation.
- [x] The container quick start is three separate steps (download once, set up
      the short command, use it), and the long command is not the first
      command shown.
- [x] A user can make the short command permanent for their shell by
      following the documentation alone.
- [x] Every part of the long form of the container command is explained.
- [x] Failed or interrupted image downloads are covered in troubleshooting,
      with a fallback that does not need the container.
- [x] When a download fails because of a broken IPv6 route, troubleshooting
      gives a temporary workaround and an explicit step to undo it.

## Out of Scope

- Documentation in languages other than English.
- A hosted documentation website.
- Documenting features that do not exist yet.
