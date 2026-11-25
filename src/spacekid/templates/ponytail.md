# Ponytail — How Every Agent Works

Every agent working in this miniverse follows this file on every task,
always: alone or in a team, whatever its model or agent tool, from the first
context to closing the loop. It is part of the miniverse, so there is nothing
to install or enable. It makes an agent solve the whole task with the least
new code and a reply a busy reader understands in one read, so the work
spends fewer tokens and ships less, better-tested code.

These rules come from [ponytail](https://github.com/DietrichGebert/ponytail)
(MIT, v5.3.3), adapted to the miniverse flow and to agent teams. This file is
the source of truth: do not install the upstream skill or plugin on top of
it, because two copies of the rules drift apart.

## Levels

| Level | Behavior |
|---|---|
| **lite** | Build what was asked. Name the smaller option in one line and let whoever assigned the task pick. |
| **full** | The rules below. Default for every agent. |
| **ultra** | Also question the request: before building, push back on any part the need does not justify. |

The level is `full` unless the task, or the agent's row in its team
document, sets another one. The lead works in `ultra` while writing a spec or
a plan: scope nobody needs is cheapest to cut before it is built. Pushback on
a spec goes to the user; it never silently drops a requirement.

## Before you write

Read the task and the code it touches. List every place your change must
reach: callers, tests, fixtures, config, exports. Check what your change
could break for users: data it would destroy or expose, callers that stop
working. That is scope. Extra features are not.

## The smallest complete change

Take the first option that fully works:

1. Does it need to exist? Skip features, options and flexibility nobody
   asked for, and name them in one line. A vague request gets the smallest
   version that does the core job.
2. Already in this codebase (a helper, component, service, pattern)? Use it
   the way the surrounding code does. Check `contexts/` first: it may already
   say where it is.
3. Standard library or a platform feature? Use it, unless the project has
   its own. A house component beats a native widget.
4. An installed dependency? Use it. Never add a dependency for a few lines.
5. Can it be one line a reader gets at a glance? One line.
6. Otherwise: the minimum code that works.

- Be lazy about the solution, never about the change itself: finish every
  part the task needs, including the callers, tests and fixtures your change
  breaks.
- No abstraction, wrapper, type conversion, option, config, boilerplate or
  "for later" code nobody asked for. Keep values in the form the platform
  already gives you. Deletion beats addition. Keep the structure the codebase
  already has: its layers, interfaces and conventions.
- The shortest working diff wins, once you know everything it must touch. A
  one-liner that needs decoding is not short.
- Comment only the why the code cannot show, in one line.
- Bug fix: before you edit, grep every caller of the function you touch, then
  fix the root cause once in the shared code.
- Code you move or merge keeps its error handling and validation.
- Between options of equal size, take the one that is correct on edge cases.
- Lazy code without its check is unfinished: new non-trivial logic (a branch,
  a loop, a parser, money or security, or a whole new script or app) leaves
  one small test or an assert-based self-check. Trivial changes need none.
- A shortcut with a known limit gets a code comment in this form:
  `shortcut: <the limit>, <when to upgrade>`.
- The same discipline applies to specs, plans, contexts and reports: say only
  what changes what gets built or decided.

**Never cut:** validation at trust boundaries, error handling that prevents
data loss, security, accessibility, the calibration real hardware needs,
anything the user asked for, and the steps of the miniverse flow.

## Every reply ends the same way

End every reply with one or two lines: what you skipped or did not check, and
any risk the reader must know. In a team, these lines are the "skipped" and
"risk" parts of the handoff report.

## Review a change

No change is done until it passes this review. In a team, the reviewer runs
it on every change and never reviews its own work; an agent working alone
runs it on its own change before closing the loop. Review like the developer
who will be paged when it breaks. Order of importance: correct, safe, holds
under load, tested, fast, lean. The review lists findings; it changes no code.

1. **Understand first.** Read the diff, then the code it touches: callers of
   every changed function, the functions it calls, the tests, the spec and
   plan it serves. Trace where data comes in, what is stored, what goes out.
   When a signature, return value or behavior changes, grep every caller.
   Find the expected load (README, deploy config, contexts) and say which
   load you assumed.
2. **Look for:**
   1. **Bug:** wrong result, crash, missed edge case (empty, zero, last item,
      rounding, time zones), a caller broken by the change, a fix applied in
      one caller while the shared function stays broken.
   2. **Risk:** security holes (injection, weak randomness, secrets, missing
      checks on user input), data loss (errors swallowed, writes in the wrong
      order, no transaction).
   3. **Scale:** fine for one user, wrong for many: check-then-write races,
      the same work done by every process, memory or lists that only grow, a
      query per item, O(n^2) on big input, per-process state that must be
      shared.
   4. **Missing test:** risky new logic (a branch, a parser, money, security,
      data writes, a bug fix) with no test that fails when it breaks. One good
      test, not coverage.
   5. **Speed:** big slowdowns are problems; small wins are suggestions.
   6. **Lean:** code that should not exist or should be smaller: dead code,
      unused options, speculative features (delete); a helper the repo already
      has (reuse, name the path); what the standard library or platform
      already does; abstraction with one implementation or config nobody sets
      (yagni); near-copies that must change together (merge); one function
      doing unrelated jobs (split by job, never by line count).
3. **Check before you report.** Every finding needs a concrete case: "this
   input or situation leads to this wrong result". No case, no finding.
   Re-read the lines and confirm. A `shortcut:` comment that names its limit
   is a decision, not a finding, unless the expected load already crosses it.
   Propose the smallest fix that works; prefer fixes that delete code. No
   style taste, no "consider", no vague worries.
4. **Report** in plain, short sentences. Start with `What this change does:`
   in two or three sentences. Then numbered findings, grouped as **Must fix**
   (bug, security, data loss, breaks at the expected load), **Should fix**
   (risky code without a test, real slowness, duplication, code that should
   not exist), and **Nice to have**; skip empty groups. Each finding gives
   its location and four short parts: what this is, the problem, the fix, and
   what happens if we skip it. End with `Verdict: Ship.` or
   `Verdict: fix 1 and 3 first.`, `Lean: -<N> lines possible.` when lean
   findings exist, and `Not checked:` when something mattered and could not
   be checked. Nothing found: `Looks good. Ship.` and one line on what was
   checked.

Must-fix findings go back to the agent that owns the change; the change is
reviewed again after the fix.

## Audit a codebase

Before planning work on a codebase that no context in this miniverse
describes yet, the lead (or the agent working alone) audits the part the work
touches. Map first: README, build and deploy config, dependencies, entry
points, tests, and the expected load; trace the main flows end to end and go
deep where a mistake costs the most. Look for the same six things as a review,
check them the same way, and report the same way, starting with
`What this repo does:` and the load assumed, at most 20 findings, ending with
`Verdict:`, `Lean: -<N> lines, -<M> dependencies possible.` and
`Not checked:` for the parts not read. The audit changes no code.

Save the report as an artifact, and turn what a future agent needs to know
about the codebase into contexts. Findings worth fixing become specs or plan
steps; they are not fixed on the side.

## Shortcut debt

When closing the loop, list every `shortcut:` marker the work added or
touched:

`git grep -nE '(#|//|/[*]) ?(shortcut|ponytail):'`

Record each one in the plan's Implementation Notes as
`<file>:<line>, <what was simplified>. ceiling: <the limit>. upgrade: <the trigger>.`
A marker that names no upgrade trigger is fixed before the loop closes, so a
deferral never quietly becomes permanent.

## License

The rules above are adapted from ponytail, used under its license:

```text
MIT License

Copyright (c) 2026 DietrichGebert

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
