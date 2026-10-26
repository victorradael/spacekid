# AGENTS.md — Organizing Artifacts

An artifact is any generated file that is **not knowledge** itself: diagrams,
exports, reports, drafts, and similar. Knowledge goes in `contexts/`.

## Rules

- **Group by origin.** Place each artifact in a subfolder named after the spec
  it comes from: `artifacts/<spec-name>/`. Use `artifacts/misc/` when it comes
  from no spec.
- **Naming.** Descriptive kebab-case names (for example
  `checkout-sequence-diagram.svg`).
- **No knowledge here.** If a future agent needs to know it to work well,
  write it as a context instead.
- **Traceability.** When an artifact is created from a spec, register it in
  that spec's Traceability section, with the date added, and refresh the
  spec's `Updated` date.
- **English only** for any text written by the agent.
