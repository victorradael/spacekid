# Idempotent Scaffolding — Implementation Plan

Implements: `specs/idempotent-init.md`
Status: Done

## Approach

Make `write_or_append` skip when the file already contains the template
content. A substring check is the simplest rule that satisfies the spec, needs
no markers or state, and tolerates user edits before or after the block.

## Steps

1. In `scaffold.py`, `write_or_append`: if the file exists, read it; if
   `content.strip()` is in it, return `FileResult(path, "skipped")`; otherwise
   append as before.
2. Tests in `tests/test_scaffold.py`: second run in project mode and in brain
   mode leaves files byte-identical and reports only `skipped`; existing file
   without the rules is appended once; rules with user text before and after
   are not appended again.
3. `README.md` and `DOCKERHUB.md`: replace the repeated-run warning with the
   idempotent behavior; fix the table and example output.
4. Update the status notes of the specs/plans that describe re-run behavior.

## Key Decisions

- **Compare `content.strip()`**, not the raw template: the append adds a
  leading newline, and editors may trim trailing whitespace.
- **Reuse the `skipped` status** rather than adding a new one: the CLI output
  and its documented messages stay unchanged. The message text, "skipped
  (already exists)", remains accurate.
- **No version marker.** Detecting outdated rules is out of scope; a changed
  template will be appended once in files that carry the old text.

## Implementation Notes

Implemented as planned.
