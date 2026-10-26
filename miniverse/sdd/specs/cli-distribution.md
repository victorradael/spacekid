# CLI Distribution

Status: Implemented
Created: 2026-10-18
Updated: 2026-10-26

## Context

SpaceKid exists to serve AI tooling to anything that wants to work with
spec-driven development, regardless of the language or stack of the project.
Maintaining a separate SDK for each language does not scale and fragments the
product. SpaceKid is instead delivered as a single command-line tool with one
behavior. It was first reachable in two ways: installed directly on a machine,
or run from a ready-made container image. The direct install has since been
retired: the container image is now the only way to use it.

## Requirements

- SpaceKid has one canonical implementation. There are no per-language SDKs
  or per-language distributions.
- Retired: installing the tool on a machine that has Python, and the shorter
  `sk` alias, are no longer supported ways of using it.
- The tool is run from a published container image, with no local
  installation beyond a container runtime. The image acts on the user's
  project directory.
- Files the tool creates inside a container run belong to the invoking user,
  not to a privileged account.
- The container image is published automatically for every release and is
  versioned so users can pin a specific version.
- The existing JavaScript/TypeScript distribution is retired: it is no longer
  built, tested, or published, and its users are told how to move to the
  container.
- Documentation describes only the container as the way of using SpaceKid,
  with copy-paste examples.

## Acceptance Criteria

- [x] ~~After installing, both `spacekid` and `sk` run the same commands with
      identical output.~~ Retired: the direct install is no longer supported.
- [x] Running the container image against a project directory scaffolds the
      project as documented.
- [x] Files created through the container are owned by the invoking user.
- [x] A new release produces a new, version-tagged container image without
      manual steps.
- [x] The repository no longer contains or publishes a JavaScript/TypeScript
      distribution, and documentation explains the migration.
- [x] Documentation covers installation, container usage, and pinning a
      version.

## Out of Scope

- SDKs, libraries, or APIs meant to be imported from code.
- Supporting container runtimes beyond standard ones.
- Distribution through operating-system package managers.

## Traceability

- Plans: `sdd/plans/cli-distribution.md` (added 2026-10-18)
- Contexts: —
- Artifacts: —
