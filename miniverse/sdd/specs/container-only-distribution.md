# Container-Only Distribution

Status: Implemented
Created: 2026-10-25
Updated: 2026-10-26

## Context

SpaceKid serves projects of any language and stack. Offering a way to install
it that is tied to one language ecosystem sends the wrong message: it suggests
the tool is meant for projects of that stack and asks everyone else to set up
tooling they do not use. The JavaScript distribution was already retired for
this reason. The same applies to installing through the Python ecosystem.

The tool keeps being built with Python internally, but that is an
implementation detail. Users should never need to know it, care about it, or
have it installed. A single, stack-neutral way of using SpaceKid is also
simpler to document, support and keep consistent.

## Requirements

- The container image is the only supported way to use SpaceKid.
- No documentation, message or example may present installing SpaceKid
  through a language ecosystem as an option, and none may favor or assume any
  particular stack for the user's project.
- Users who want a short everyday command get it through a shell shortcut
  that runs the container, as already documented.
- When the container image cannot be downloaded, the documentation must say
  how to resolve it and must not offer a language-ecosystem install as a
  fallback.
- The tool's behavior, commands and results are unchanged.
- Users of the previous install method are told how to move to the container.
- The internal implementation language is not advertised as a user concern;
  where it must be mentioned (for example, for contributors), it is clearly
  described as internal.
- All documentation is written in English.

## Acceptance Criteria

- [x] The user-facing documentation, on both GitHub and Docker Hub, describes
      only the container as the way to use SpaceKid.
- [x] No user-facing page shows a language-ecosystem install command.
- [x] The troubleshooting for failed image downloads offers no
      language-ecosystem fallback.
- [x] A short note explains how former users of the other install method
      switch to the container.
- [x] Mentions of the implementation language appear only in material for
      contributors and state that it is an internal detail.
- [x] Running the container still produces the same results as before.

## Out of Scope

- Changing what the tool does.
- Rewriting the tool in another language.
- Supporting other container runtimes or distribution channels.

## Traceability

- Plans: `sdd/plans/container-only-distribution.md` (added 2026-10-25)
- Contexts: —
- Artifacts: —
