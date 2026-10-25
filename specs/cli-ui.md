# CLI Visual Experience

Status: Implemented

## Context

The command-line tool currently prints plain, uncolored text and offers no
guided entry point. First impressions matter: a polished, colorful terminal
experience makes the tool feel trustworthy and easier to use, especially for
people discovering it for the first time.

## Requirements

- When the tool starts interactively, it shows a distinctive, colorful
  presentation of the project name.
- Running the tool with no arguments in an interactive terminal shows a
  colored menu where the user picks what to do (initialize a project,
  initialize a multi-repo directory, see information about the tool, or quit).
- The results of the initialization are shown with colors and symbols that
  make it easy to tell at a glance what was created, extended, or skipped.
- The tool must keep working cleanly where color is unwanted or unsupported:
  when output is piped or redirected, in non-interactive environments, or when
  the user has opted out of color. In those cases output stays plain text.
- Existing commands and their options keep behaving as before.

## Acceptance Criteria

- [x] In an interactive terminal, the project name is displayed in a
      colorful, stylized form.
- [x] Running the tool with no arguments in an interactive terminal shows a
      colored menu with the options above, and each option works.
- [x] Invalid menu input is reported and the user can try again.
- [x] Initialization results are color-coded by outcome (created, extended,
      skipped).
- [x] Piped, redirected, or non-interactive output contains no color codes
      and no decorative banner.
- [x] Opting out of color through the standard environment convention
      disables all color.
- [x] Running the tool with no arguments in a non-interactive context shows
      the usage help instead of failing.

## Out of Scope

- Changing what files are scaffolded.
- Localization of the interface.
