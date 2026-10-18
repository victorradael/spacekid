# CLI Distribution

Status: Implemented

## Context

SpaceKid exists to serve AI tooling to anything that wants to work with
spec-driven development, regardless of the language or stack of the project.
Maintaining a separate SDK for each language does not scale and fragments the
product. SpaceKid is instead delivered as a single command-line tool with one
behavior, reachable in two ways: installed directly on a machine, or run from
a ready-made container image for people who do not want to install anything.

## Requirements

- SpaceKid has one canonical implementation. There are no per-language SDKs
  or per-language distributions.
- The tool can be installed on any machine that has Python and is then used
  through the `spacekid` command, or the shorter `sk` alias. Both behave
  identically.
- The tool can also be run from a published container image, with no local
  installation beyond a container runtime. The image answers the same
  commands, with the same results, as the installed tool, acting on the
  user's project directory.
- Files the tool creates inside a container run belong to the invoking user,
  not to a privileged account.
- The container image is published automatically for every release and is
  versioned so users can pin a specific version.
- The existing JavaScript/TypeScript distribution is retired: it is no longer
  built, tested, or published, and its users are told how to move to one of
  the two supported ways.
- Documentation describes only the two supported ways of using SpaceKid, with
  copy-paste examples for each.

## Acceptance Criteria

- [x] After installing, both `spacekid` and `sk` run the same commands with
      identical output.
- [x] Running the container image against a project directory produces the
      same result as the installed tool on that directory.
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
