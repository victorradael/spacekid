# Idempotent Scaffolding

Status: Implemented

## Context

Running the scaffolding command again on a project that already has the
SpaceKid rules adds the same rules a second time to the files that exist.
Users who re-run the command by habit, or to pick up a missing file, end up
with duplicated guidance and have to clean it by hand. Repeating the command
should be safe.

## Requirements

- Running the command again must leave an already scaffolded project exactly
  as it is.
- A rule file that already contains the standard SpaceKid rules must not
  receive them again, in either usage mode.
- A rule file that exists without the standard rules still receives them at
  the end, keeping the user's content.
- The tool reports, for each file, that nothing was changed when the rules
  are already present.
- Files the user has edited around or after the standard rules still count as
  already containing them.

## Acceptance Criteria

- [x] Running the command twice in a row in project mode leaves every file
      identical after the second run.
- [x] Running the command twice in a row in brain mode leaves every file
      identical after the second run.
- [x] A pre-existing rule file without the standard rules is still appended
      to, once.
- [x] A rule file where the user added text before or after the standard rules
      is not appended to again.
- [x] The second run reports every file as skipped.

## Out of Scope

- Updating the standard rules in files scaffolded by an older version.
- Changing how the project name is applied.
