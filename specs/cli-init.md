# CLI Init

Status: Implemented

## Context

SpaceKid is currently a set of documentation files meant to be copied by hand
into a project. That's friction: a user who wants the SpaceKid workflow in a
Python project has to manually recreate `AGENTS.md`, `specs/AGENTS.md`, and
`plans/AGENTS.md` themselves, with no guarantee they copy the latest version
or avoid clobbering files that already exist.

SpaceKid should instead be an installable Python package that a user adds to
any Python project and runs once to scaffold the SpaceKid cycle in that
project's root, so adopting the workflow takes one command instead of manual
file copying.

## Requirements

- SpaceKid must be installable into a Python project as a package.
- After installing it, the user must be able to run a single command from
  their project's root directory that sets up the SpaceKid cycle there.
- Running this command must produce, in the target project's root:
  - An `AGENTS.md` file that plays the same role as SpaceKid's own root
    `AGENTS.md`: it names the project, maps `specs/`, `plans/`, and any of
    the project's own convention docs, states the mandatory spec → plan →
    implementation → status-update cycle, and includes an unfilled "Project
    Overview" section for the agent to complete once it knows the project.
  - A `specs/AGENTS.md` file containing the rules for writing a spec
    (business intent only, no implementation detail).
  - A `plans/AGENTS.md` file containing the rules for writing an
    implementation plan (technical design that satisfies a spec).
- If the target project does not yet have a root `AGENTS.md`, the command
  creates one, with the project's own name filled in wherever the template
  expects a project name.
- If the target project already has a root `AGENTS.md`, the command must not
  overwrite or discard it — a user's existing project documentation is never
  destroyed by running this command.
- If the target project already has `specs/AGENTS.md` and/or
  `plans/AGENTS.md`, the command must not overwrite them: it appends the
  standard SpaceKid content to the end of the existing file instead of
  replacing it.
- If `specs/AGENTS.md` and/or `plans/AGENTS.md` do not yet exist, the command
  creates the `specs/` and/or `plans/` directories (if needed) and the files,
  with the standard content.
- Running the command again on a project that already has all three files
  fully set up must not duplicate the appended content endlessly — running
  it twice back to back should not corrupt the files, even though appending
  guidance content twice is not itself harmful.

## Acceptance Criteria

- [x] A Python project can declare SpaceKid as a dependency and install it
      with a standard Python package installer.
- [x] From a project's root directory, a user can run one command to
      scaffold the SpaceKid files.
- [x] On a project with none of the three files present, running the
      command creates `AGENTS.md` (with the project's name filled in),
      `specs/AGENTS.md`, and `plans/AGENTS.md`, each with the expected
      content.
- [x] On a project that already has a root `AGENTS.md`, running the command
      leaves that file's content completely untouched and clearly informs
      the user it was skipped.
- [x] On a project that already has `specs/AGENTS.md` and/or
      `plans/AGENTS.md`, running the command preserves the existing content
      of those files and adds the standard SpaceKid content after it.
- [x] The user is told, for each of the three files, whether it was created,
      appended to, or skipped.

## Out of Scope

- Automatically running the scaffolding as a side effect of installing the
  package (e.g. via a package-manager post-install hook). The user always
  triggers scaffolding explicitly by running a command.
- Keeping a project's `AGENTS.md` in sync with future SpaceKid template
  changes after the initial scaffolding.
- Any content or structure of the project's own `specs/<name>.md` or
  `plans/<name>.md` feature files — this only covers the two `AGENTS.md`
  guide files and the root `AGENTS.md`.
