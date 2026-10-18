# MCP Setup Command

Status: Draft

## Context

Agents working in a SpaceKid project get much better results when they can
reach external tools, such as up-to-date library documentation. These tools
are plugged into the project through an MCP configuration file. Today every
developer writes that file by hand, copying server definitions from
documentation, and often pastes secrets such as API keys straight into it.

That file is personal: which tools are enabled, and which credentials back
them, varies from developer to developer. It must not be shared through the
repository. SpaceKid should make creating it quick and safe, as a separate,
explicit step that is never part of the default scaffolding.

## Requirements

- SpaceKid provides a dedicated command, separate from the scaffolding
  command, that sets up MCP tooling for the project. Scaffolding itself never
  creates or touches MCP configuration.
- The command is part of the SpaceKid command-line tool and is available
  wherever the tool runs, including the container image.
- The command offers a built-in list of well-known MCP servers and lets the
  user choose which to add, either interactively or by naming them directly.
- The command writes the project's MCP configuration file with the chosen
  servers.
- Credentials are never written to the file. Where a server needs one, the
  file refers to an environment variable, and the command tells the user
  which variable to set.
- Because the file is personal, the command makes sure it is excluded from
  version control, adding the exclusion to the project's ignore list if it is
  missing, without duplicating or damaging existing entries.
- If the configuration file already exists, the command never overwrites it
  or removes existing servers. It adds only the chosen servers that are
  missing and leaves any already-configured server unchanged.
- If the existing configuration file cannot be understood, the command stops
  without modifying it and tells the user why.
- The user is told what happened to the configuration file (created, updated,
  or left unchanged), to the ignore list, and which environment variables
  still need to be set.
- Running the command again with the same choices must not change anything or
  corrupt the file.

## Acceptance Criteria

- [ ] In a project with no MCP configuration, running the command with a
      chosen server creates the configuration file containing that server.
- [ ] No credential value ever appears in the generated file; servers that
      need one reference an environment variable, and the user is told its
      name.
- [ ] After the command runs, the configuration file is excluded from version
      control, and an existing ignore list keeps all its prior entries.
- [ ] On a project that already has a configuration file with other servers,
      those servers remain unchanged and the chosen ones are added.
- [ ] A server that is already configured is not modified or duplicated.
- [ ] An unreadable existing configuration file is left untouched and the
      user gets a clear error.
- [ ] Running the command twice in a row leaves the file and the ignore list
      identical after the second run.
- [ ] The scaffolding command does not create or modify any MCP configuration.
- [ ] The command produces the same results whether the tool is installed
      locally or run from the container image.

## Out of Scope

- Installing, starting, or managing the MCP servers themselves.
- Obtaining or storing credentials for the user.
- Supporting MCP configuration formats of tools other than the project-level
  file described here.
- Letting users register custom servers beyond the built-in list.
- Keeping existing configuration in sync with future changes to the built-in
  list.
