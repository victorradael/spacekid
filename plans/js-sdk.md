# JS SDK — Implementation Plan

Implements: `specs/js-sdk.md`
Status: Done

## Approach

Add a second, independent package to this repo: `js/`, a plain-JavaScript
npm package that mirrors `src/spacekid`'s behavior for Node projects. It
lives alongside the Python package rather than inside it, so each ecosystem
keeps its own manifest (`pyproject.toml` vs. `package.json`) and can be
published to its own registry without one toolchain needing to parse the
other's files.

The package ships one console command, `spacekid init`, with a `--path`
and `--name` flag — functionally identical to the Python CLI — implemented
with Node's built-in `util.parseArgs` (stable since Node 20), no CLI
framework dependency, same reasoning as the Python side's choice of
`argparse` over a third-party parser.

The three scaffolded files' content and append/skip semantics are ported
function-for-function from `src/spacekid/scaffold.py`: `detectAppName`,
`renderRootAgents`, `writeOrSkip`, `writeOrAppend`, `scaffold`. The template
Markdown files are already stack-agnostic (nothing in them mentions Python),
so they're copied verbatim into `js/src/templates/`.

To satisfy the TypeScript-support requirement without a build step, the
package's programmatic surface is isolated in `js/src/index.js` (what
`require('spacekid')` resolves to) and paired with a hand-written
`js/types/index.d.ts` — a small, stable surface (one interface, five
functions) cheap enough to maintain by hand, keeping the package pure
JavaScript with zero transpilation.

## Steps

1. Create `js/package.json`:
   - `name: "spacekid"`, `version: "0.1.0"`, matching description/license to
     the Python package.
   - `bin: { "spacekid": "bin/spacekid.js" }`.
   - `main: "src/index.js"`, `types: "types/index.d.ts"`, and an `exports`
     map (`"."` → `{ types, default }`) so both legacy and modern Node
     resolution find the same files.
   - `files: ["bin", "src", "types"]` (publish whitelist; excludes `test/`).
   - `engines: { "node": ">=20.0.0" }` (the version `util.parseArgs`
     stabilized in).
   - `scripts.test: "node --test"`.
   - No dependencies, no devDependencies.
2. Create `js/src/templates/`, copied verbatim from
   `src/spacekid/templates/`:
   - `root-agents.md` (keeps the `{{APP_NAME}}` placeholder).
   - `specs-agents.md`, `plans-agents.md` (unchanged).
3. Implement `js/src/scaffold.js`:
   - `detectAppName(projectRoot)`: read `name` from `package.json` in
     `projectRoot` if it exists and parses as JSON with a non-empty string
     `name`; otherwise fall back to `path.basename(path.resolve(projectRoot))`.
   - `renderRootAgents(appName)`: load `root-agents.md`, replace every
     `{{APP_NAME}}` occurrence.
   - `writeOrSkip(filePath, content)`: if `filePath` exists, return
     `{ path: filePath, status: 'skipped' }`; else create parent
     directories and write `content`, returning `status: 'created'`.
   - `writeOrAppend(filePath, content)`: if `filePath` exists, append
     `"\n" + content`, returning `status: 'appended'`; else create parent
     directories and write `content`, returning `status: 'created'`.
   - `scaffold(projectRoot, appName)`: resolves `appName ||
     detectAppName(root)`, then runs the three file operations (root
     `AGENTS.md` via `writeOrSkip`, `specs/AGENTS.md` and `plans/AGENTS.md`
     via `writeOrAppend`), returning the three `FileResult` objects.
   - Exported via `module.exports`.
4. Implement `js/src/cli.js` and `js/bin/spacekid.js`:
   - `cli.js` exports `main(argv)`: reads the subcommand (`argv[0]`);
     for `init`, parses the remaining args with `util.parseArgs` using
     options `{ path: { type: 'string', default: '.' }, name: { type:
     'string' } }`; resolves `projectRoot = path.resolve(values.path)`;
     calls `scaffold(projectRoot, values.name)`; prints one status line per
     result (`created` / `appended to` / `skipped (already exists)` +
     relative path); returns exit code `0`. Any other/missing subcommand
     prints usage to stderr and returns `1`.
   - `bin/spacekid.js`: `#!/usr/bin/env node` shebang script that requires
     `../src/cli.js` and sets `process.exitCode = main(process.argv.slice(2))`.
5. Implement `js/src/index.js`: re-exports everything from `scaffold.js`.
   This is the package's `require('spacekid')` / `import ... from
   'spacekid'` entry point — deliberately separate from `cli.js` so
   importing the library never touches `process.argv` or `process.exit`.
6. Write `js/types/index.d.ts` by hand, matching `index.js`'s exports
   exactly: a `FileResult` interface (`path: string`, `status: 'created' |
   'appended' | 'skipped'`) and declarations for `detectAppName`,
   `renderRootAgents`, `writeOrSkip`, `writeOrAppend`, `scaffold`.
7. Add `js/test/scaffold.test.js` using the built-in `node:test` /
   `node:assert` runner, against `fs.mkdtempSync` temp directories, covering
   the same cases as `tests/test_scaffold.py`:
   - fresh project → all three files created; name resolved from
     `package.json`, and separately, from the directory-name fallback when
     there's no `package.json`.
   - existing root `AGENTS.md` → left byte-for-byte untouched, reported
     skipped.
   - existing `specs/AGENTS.md` / `plans/AGENTS.md` → original content
     preserved, standard content appended after it.
   - missing `specs/` / `plans/` directories → created as needed.
   - running `scaffold` twice in a row → no corruption.
8. Add `js/.gitignore` (`node_modules/`) and update this repo's root
   `README.md` with an npm install/usage section (`npm install spacekid` or
   `npx spacekid init`) alongside the existing pip instructions.

## Key Decisions

- **Separate `js/` package, not folded into `src/spacekid`.** Each
  ecosystem keeps its own manifest and publish target; neither toolchain
  needs to understand the other's packaging.
- **`util.parseArgs`, not a CLI dependency.** Node's stdlib now has a
  structured arg parser, the direct equivalent of reaching for Python's
  `argparse` instead of pulling in Click/Typer — same reasoning, same
  result: no dependency for one subcommand and two flags. This sets the
  `engines.node >= 20.0.0` floor, where the API is stable (no experimental
  warning).
- **Hand-written `.d.ts`, no build step.** The spec requires the package to
  stay plain JavaScript. The exported surface is small and changes rarely,
  so maintaining a `.d.ts` by hand costs less than introducing `tsc` (or any
  bundler) as a build dependency.
- **Templates duplicated, not shared with the Python package's copies.**
  `src/spacekid/templates/` already duplicates this repo's own root/`specs`/
  `plans` `AGENTS.md` content rather than reading it live — the Python
  plan accepted that drift risk for simplicity. Mirroring that choice here
  avoids packaging problems (symlinks don't survive npm's tarball packing
  reliably) and keeps both packages independently self-contained.
- **`index.js` kept separate from `cli.js`.** The programmatic entry point
  a TypeScript consumer imports must never have a side effect like reading
  `process.argv` or calling `process.exit`; isolating it keeps the library
  surface safe to import for any purpose, CLI or not.
- **Node's built-in test runner over Jest/Mocha.** Zero added dependencies,
  same minimal-dependency posture as the Python package's single `pytest`
  test dependency.

## Implementation Notes

Implemented as planned, with these deviations:

- `scripts.test` is `node --test` instead of `node --test test/`. On Node 24
  the explicit `test/` argument is resolved as a module path and fails;
  with no argument the runner auto-discovers `test/`.
- Template files use kebab-case names (`root-agents.md`, ...) as the plan
  states, differing from the Python package's snake_case names.
- Added a test for a malformed `package.json` falling back to the directory
  name, and one for the explicit `--name` override.
- `cli.js` also catches `parseArgs` errors (unknown flags) and prints usage
  with exit code `1`.
- Like the Python version, running `scaffold` twice appends the standard
  content to `specs/AGENTS.md` and `plans/AGENTS.md` again; no file is
  corrupted and the root `AGENTS.md` is skipped.
