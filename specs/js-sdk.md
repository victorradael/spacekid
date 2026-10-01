# JS SDK

Status: Implemented

## Context

SpaceKid today only reaches Python projects: it ships as a Python package
and its one command, `spacekid init`, only runs inside a Python
environment. A large share of projects that would benefit from the SpaceKid
cycle — specs, plans, and the `AGENTS.md` rules that enforce the loop — are
JavaScript/TypeScript projects (Node backends, frontend apps, npm
libraries). Their maintainers have no way to adopt SpaceKid without manually
copying the three guide files by hand, which is exactly the friction
SpaceKid was built to remove for Python.

SpaceKid should also be distributable as a package these projects can
install the way they install everything else — through npm and
`node_modules` — and run with the same one-command scaffolding experience
Python users already have.

Because a large share of the JavaScript ecosystem writes in TypeScript, and
authors expect installed packages to have correct type information in their
editor, the package must also provide accurate TypeScript type information,
even though its source stays plain JavaScript.

## Requirements

- SpaceKid must be installable into a JavaScript or TypeScript project as an
  npm package (direct dependency, dev dependency, or a one-off run without
  installing it permanently).
- After installing it (or running it on demand), the user must be able to
  run a single command, `spacekid init`, from their project's root — the
  same command name the Python version uses — that sets up the SpaceKid
  cycle there.
- Running this command must produce, in the target project's root, the same
  three files and the same content rules already defined for the Python
  version:
  - A root `AGENTS.md` naming the project, mapping `specs/`, `plans/`, and
    stating the mandatory spec → plan → implementation → status-update
    cycle.
  - A `specs/AGENTS.md` with the rules for writing a spec.
  - A `plans/AGENTS.md` with the rules for writing an implementation plan.
- If the target project does not yet have a root `AGENTS.md`, the command
  creates one, with the project's own name filled in. The name must be
  detected automatically from the project's own `package.json` when
  present, falling back to the project directory's name otherwise, with a
  way to override it explicitly.
- If the target project already has a root `AGENTS.md`, the command must not
  overwrite or discard it, and must clearly tell the user it was skipped.
- If the target project already has `specs/AGENTS.md` and/or
  `plans/AGENTS.md`, the command must not overwrite them: it appends the
  standard SpaceKid content to the end of the existing file instead of
  replacing it.
- If `specs/AGENTS.md` and/or `plans/AGENTS.md` do not yet exist, the
  command creates the `specs/` and/or `plans/` directories (if needed) and
  the files, with the standard content.
- Running the command again on a project that already has all three files
  fully set up must not corrupt any of them.
- The resulting `AGENTS.md`, `specs/AGENTS.md`, and `plans/AGENTS.md` content
  must describe the same cycle and rules as the Python version produces, so
  a mixed-stack organization gets one consistent workflow regardless of
  which projects are Python and which are JavaScript/TypeScript.
- A developer in a TypeScript project must get correct type information
  (editor autocomplete, type checking) for anything the package exposes for
  code to import, without needing to install or write any separate type
  definitions themselves.

## Acceptance Criteria

- [x] A JavaScript or TypeScript project can install SpaceKid with a
      standard npm-compatible package manager, or invoke it without a
      permanent install.
- [x] From a project's root directory, a user can run one command,
      `spacekid init`, to scaffold the SpaceKid files.
- [x] On a project with none of the three files present, running the command
      creates `AGENTS.md` (with the project's name filled in from
      `package.json`, or the directory name otherwise), `specs/AGENTS.md`,
      and `plans/AGENTS.md`, each with the expected content.
- [x] On a project that already has a root `AGENTS.md`, running the command
      leaves that file's content completely untouched and clearly informs
      the user it was skipped.
- [x] On a project that already has `specs/AGENTS.md` and/or
      `plans/AGENTS.md`, running the command preserves the existing content
      of those files and adds the standard SpaceKid content after it.
- [x] The user is told, for each of the three files, whether it was created,
      appended to, or skipped.
- [x] Running the command twice in a row on the same project never corrupts
      any of the three files.
- [x] A TypeScript project importing the package gets accurate type
      information without any extra setup.

## Out of Scope

- Automatically running the scaffolding as a side effect of installing the
  package (e.g. via an npm lifecycle/postinstall script). The user always
  triggers scaffolding explicitly by running a command.
- Keeping a project's `AGENTS.md` in sync with future SpaceKid template
  changes after the initial scaffolding.
- Any content or structure of the project's own `specs/<name>.md` or
  `plans/<name>.md` feature files — this only covers the two `AGENTS.md`
  guide files and the root `AGENTS.md`.
- Publishing or distribution mechanics (which registry, versioning scheme,
  release process).
