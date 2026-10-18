# Brain Mode

Status: Implemented

## Context

SpaceKid today serves a single project: it scaffolds the spec → plan →
implementation cycle at the root of one repository. Many real efforts,
however, span several repositories that live side by side in one parent
directory (for example a backend, a frontend, and shared infrastructure).
Work in that setting needs knowledge that no single repository owns: how the
pieces relate, what was decided and why, what was already learned.

Without a shared home for that knowledge, every agent session starts cold
and re-discovers the same facts, and specs and plans have nowhere to live
that is not tied to one repository.

SpaceKid should therefore support a second way of being used: a "brain" — a
knowledge base placed in a directory that contains multiple repositories,
within which the same spec/plan workflow runs on top of accumulated context.

## Requirements

- SpaceKid must support two usage modes:
  - **Project mode** — the existing behavior, for one isolated project.
  - **Brain mode** — new, for a directory that contains more than one
    repository.
- SpaceKid must recognize on its own which mode applies to the directory it
  is run in. The user must also be able to choose the mode explicitly,
  overriding the automatic choice.
- In brain mode, SpaceKid must create a `brain` folder in that directory
  containing:
  - `AGENTS.md` — describes the purpose of each folder inside the brain and
    the working rules for agents.
  - `contexts/` — holds every piece of knowledge produced while working
    (findings, decisions, how repositories relate, domain explanations).
  - `artifacts/` — holds every other file generated along the way that is
    not knowledge itself (diagrams, exports, reports, drafts, and similar).
  - `sdd/` — holds the spec-driven development workflow, containing
    `specs/` and `plans/`. Each of these two folders has its own
    `AGENTS.md` with the rules for writing that kind of document, exactly as
    in project mode: `sdd/specs/AGENTS.md` for specs and
    `sdd/plans/AGENTS.md` for plans.
- The rule for where things go must be explicit in the brain's `AGENTS.md`:
  anything that is knowledge is saved as a context; any other file produced
  is an artifact.
- In brain mode the workflow must begin with context: before executing any
  work, the agent must consult the existing contexts, and create the missing
  ones the task depends on. The brain's `AGENTS.md` must state this as a
  mandatory first step, ahead of the spec/plan/implementation/status-update
  cycle.
- The brain's `AGENTS.md` must also keep the existing status-update
  discipline: when work finishes, specs, plans, and contexts affected by it
  are brought up to date.
- Running the command must never destroy existing content: files that
  already exist are preserved, with the same skip/append behavior users
  already know from project mode, and the user is told what happened to each
  file.
- Running the command twice must not corrupt the brain.

## Acceptance Criteria

- [x] Run in a directory that contains more than one repository, SpaceKid
      selects brain mode without being told to.
- [x] Run in a single project (one repository, or none), SpaceKid keeps
      selecting project mode, with unchanged behavior.
- [x] The user can force either mode explicitly.
- [x] In brain mode, the `brain` folder is created with `AGENTS.md`,
      `contexts/`, `artifacts/`, and `sdd/` containing `specs/` and `plans/`.
- [x] The brain's `AGENTS.md` explains the purpose of every folder and states
      that knowledge goes to contexts and all other generated files go to
      artifacts.
- [x] The brain's `AGENTS.md` makes "consult or create context" a mandatory
      step before any execution.
- [x] `sdd/specs/` and `sdd/plans/` each contain their own `AGENTS.md`, and
      their writing rules match those used in project mode.
- [x] Existing brain files are never overwritten, and the user is told for
      each file whether it was created, appended to, or skipped.
- [x] Empty folders are preserved when the brain is committed to version
      control.

## Out of Scope

- Changing, moving, or scanning the repositories inside the directory.
- Automatically producing contexts; agents write them as they work.
- Creating a root-level project guide in the parent directory.
- Keeping an existing brain in sync with future template changes.
