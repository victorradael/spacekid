# AGENTS.md — Writing Contexts

A context is a piece of **knowledge** a future agent needs to work well:
a finding, a decision and its reason, how things relate, a domain explanation.
Anything that is not knowledge is an artifact, not a context.

## Rules

- **One topic per file.** Split a file that covers two topics.
- **Naming.** Kebab-case, `<topic>.md` (for example `payment-flow.md`).
- **Header.** Every context starts with the lines below, in this order. The
  catalog reads them, so an agent can judge relevance without opening the file.
- **Concise.** Say what a reader must know; cut the rest. Sections are free.
- **Stay current.** Change `Updated` on every edit. Correct or delete a
  context that is no longer true.
- **Knowledge only.** Diagrams, exports, reports, and drafts go in `artifacts/`.
- **Traceability.** When a context is created from a spec, register it in that
  spec's Traceability section, with the date added, and refresh the spec's
  `Updated` date.
- **English only.**

## Structure

```markdown
# <Title>

Summary: <one line: what an agent learns from this context>
Created: YYYY-MM-DD
Updated: YYYY-MM-DD

<Body: concise sections as needed.>
```
