# JS Package Automated Release — Implementation Plan

Implements: `specs/js-release.md`
Status: Implemented in code (steps 0–5), then revised for npm staged publishing (step 7, see Implementation Notes). Step 6 (manual setup and first live release) is pending the maintainer. The staged flow has not been exercised against the real registry yet.

## Approach

One GitHub Actions workflow, `.github/workflows/js.yml`, with two jobs:

- `test` runs on every pull request and on pushes to `main`: `npm ci` and
  `npm test` in `js/`, on a Node 20 / 22 matrix (20 is the `engines` floor).
  It has no path filter, so the required `test` check is always reported
  (a path-filtered workflow never reports on unrelated PRs and would block
  their merge). The job is cheap.
- `release` runs only on pushes to `main`, `needs: test`, on Node 24, and runs
  `semantic-release` from `js/`. Node 24 ships npm 11, which satisfies the
  trusted-publishing requirements (npm >= 11.5.1, Node >= 22.14) and the
  semantic-release engines range (`^22.14.0 || >=24.10.0`), so no explicit npm
  upgrade step is needed.

Release tooling is added to `js/` as `devDependencies` (with a committed
lockfile so `npm ci` is reproducible). The published tarball is unaffected:
`files` already whitelists only `bin`, `src`, `types`.

Authentication uses **npm trusted publishing (OIDC)**: the `release` job gets
`id-token: write`, npm exchanges the workflow's OIDC identity for a
short-lived credential, and provenance attestations are generated
automatically. No `NPM_TOKEN` secret is stored (a stage-only token was
considered and rejected, see Key Decisions).

Publishing is **staged**: the job runs `npm stage publish`, which uploads the
version without making it public, and a maintainer promotes it with
`npm stage approve <stage-id>` (2FA). `@semantic-release/npm` has no staging
option, so it runs with `npmPublish: false` (it only sets the version and
packs the tarball) and `@semantic-release/exec` runs the stage command in the
`publish` step. Staging needs npm >= 11.15.0, so the `release` job upgrades
npm explicitly (Node 24 bundles an older npm). The job's only other
permission is `contents: write` (tags and GitHub Releases).

Semantic-release configuration lives in `js/.releaserc.json`:

- `branches: ["main"]`.
- `tagFormat: "js-v${version}"`, so JS tags never collide with a future
  Python release tag scheme.
- Plugins: `commit-analyzer` (Angular preset), `release-notes-generator`,
  `npm` (`npmPublish: false`), `exec` (`npm stage publish`), `github` (with `successComment` / `failComment` disabled so no
  issue/PR write permission is needed). No `git` or `changelog` plugin: the
  release never commits back to `main`, which keeps branch protection simple
  and honors the spec's out-of-scope item.
- Path scoping via `semantic-release-monorepo`, so only commits touching
  `js/` count toward a JS release (Python-only, root docs, and spec/plan
  commits produce nothing). See Risks: this plugin is not verified.

## Steps

0. **Spike (before anything else).** In a scratch branch, validate the two
   unverified assumptions with `semantic-release --dry-run`:
   - `semantic-release-monorepo` works with the current semantic-release
     major, only counts `js/` commits, and does not override
     `tagFormat: "js-v${version}"`.
   - `@semantic-release/npm` (record the minimum working version) publishes
     through OIDC without `NPM_TOKEN`; its `verifyConditions` must not demand
     a token. If either fails, apply the fallback in Risks and update this
     plan before continuing.
1. Add `devDependencies` to `js/package.json`: `semantic-release` and
   `semantic-release-monorepo` (pinned), plus the lockfile
   (`js/package-lock.json`). Add `repository`, `bugs`, `homepage` fields and
   `publishConfig: { access: "public", provenance: true }`. Provenance and
   trusted publishing require `repository.url` to match the GitHub repo
   exactly.
2. Create `js/.releaserc.json` as described in Approach.
3. Create `.github/workflows/js.yml`:
   - Trigger: `pull_request` and `push` to `main`, no path filter.
   - Top-level `permissions: contents: read`; the `release` job overrides to
     `contents: write` and `id-token: write`.
   - `actions/checkout` with `fetch-depth: 0` (semantic-release needs full
     history and tags) and `persist-credentials: false` (semantic-release
     pushes tags using `GITHUB_TOKEN`).
   - `actions/setup-node` with `registry-url: https://registry.npmjs.org` and
     `package-manager-cache: false` in the `release` job (no caching in
     release builds).
   - Release step: `npx semantic-release` with `GITHUB_TOKEN` from the
     workflow; no npm token is passed.
   - Third-party actions pinned to full commit SHAs (looked up at
     implementation time), kept current by Dependabot.
4. Add `.github/dependabot.yml` for `github-actions` and the `js/` npm
   ecosystem (weekly).
5. Update the root `README.md`: keep the npm install/usage section, and add
   a short "Releasing" note explaining that releases are automatic from
   conventional commits touching `js/`: `fix` → patch, `feat` → minor, and a
   `BREAKING CHANGE:` footer → major. The Angular preset does not recognize
   the `feat!:` shorthand, so the note must say the footer is required.
6. Manual repository setup, documented in the README and performed by the
   maintainer (cannot be done from code):
   - On npmjs.com, after the package exists, configure a **Trusted
     Publisher** for `victorradael/spacekid`, workflow `js.yml`. This
     configuration is not verified on save; mistakes only surface at publish
     time.
   - In the Trusted Publisher / package publishing settings, make sure the
     trust relationship is allowed to stage (OIDC tokens can stage only if the
     trust configuration permits it).
   - In GitHub, protect `main` (required `test` check) and restrict the
     workflow's default token to read-only.
   - After the first successful release, confirm no `NPM_TOKEN` secret
     exists, and revoke the bootstrap token on npmjs.com.
   - For every release: a maintainer runs `npm stage list`, then
     `npm stage approve <stage-id>` with 2FA. Staged versions share the semver
     uniqueness index, so a failed or rejected stage must be rejected
     (`npm stage reject`) before that version can be staged again.

## Key Decisions

- **Trusted publishing over a stored `NPM_TOKEN`.** It is the only option
  that satisfies "no long-lived secret" and gives provenance for free.
  Trade-off: a trusted publisher can only be configured on a package that
  already exists on npm, so the very first publish needs a bootstrap (see
  Decisions Taken).
- **`semantic-release-monorepo` for path scoping.** The repo holds both
  Python and JS packages; plain semantic-release would count every commit.
  Scope-only rules (`feat(js)`) were rejected because an unscoped breaking
  change would silently be ignored or mis-released. release-please was
  rejected because it releases through a "release PR", which is a manual
  step the spec forbids. Trade-off: a small, older third-party plugin.
- **Staged publishing with human 2FA approval.** npm is moving to require
  proof of presence for publishing; stage-only tokens cannot publish directly.
  The pipeline therefore only stages, and a maintainer approves. A stage-only
  `NPM_TOKEN` secret was rejected: it is a long-lived secret and OIDC can
  stage without one. Trade-off: a manual approval step, and the GitHub
  Release and tag exist before the version is live on npm until approved.
- **No commit-back to `main`.** `package.json` keeps its checked-in version
  as a placeholder; the real version is set in the published tarball and
  recorded in the git tag and GitHub Release. This avoids needing a bypass
  for branch protection.
- **One workflow, two jobs.** Keeps the trusted-publisher binding to a
  single workflow filename and guarantees `release` can never run without
  `test` passing.
- **Unfiltered `test` job.** Trades a few seconds of CI on non-JS PRs for a
  required check that always reports.

## Risks

- **`semantic-release-monorepo` is unverified.** It is small and older, and
  modern semantic-release is ESM with newer Node requirements. It may also
  derive its own tag format from the package name, overriding `tagFormat`.
  Step 0 decides. Fallback: a small in-repo plugin that filters commits by
  path (`js/`), or releasing only from commits whose files touch `js/`.
- **OIDC support in `@semantic-release/npm` is unverified.** The upstream
  semantic-release workflow still passes `NPM_TOKEN`. Step 0 decides.
  Fallback: disable the plugin's publish (`npmPublish: false`) and run
  `npm publish` in a dedicated workflow step after semantic-release computes
  the version, still using OIDC.

## Decisions Taken

- **Bootstrap.** Manually publish `0.1.0` with a temporary, granular npm
  token, create tag `js-v0.1.0` on a commit in `main`'s history, then
  configure the trusted publisher and revoke the token. Releases continue
  from `0.x`.
- **Package name.** `spacekid` (unscoped, in the maintainer's personal npm
  account) is the final name. A scoped `@radaeltech/spacekid` was tried and
  reverted; the bootstrap publish already created `spacekid@0.1.0`.

## Implementation Notes

- **Spike (step 0) passed.** `semantic-release@25.0.9` with
  `semantic-release-monorepo@8.0.2`, run with `--dry-run` in a scratch clone
  with a `js-v0.1.0` tag: only `js/` commits were counted (a root-only commit
  carrying a `BREAKING CHANGE:` footer was ignored), the next version was
  `0.2.0`, and links used `js-v` tags, so `tagFormat` is honored. Cosmetic
  quirk: the monorepo plugin makes the release-notes heading read
  `spacekid-v0.2.0` instead of `js-v0.2.0`; accepted.
- **OIDC needs no fallback.** `@semantic-release/npm@13.2.0` (pulled in by
  `semantic-release@25`) supports trusted publishing natively and skips the
  `NPM_TOKEN` requirement when an OIDC context exists. The `npm publish`
  fallback was not needed. The actual OIDC publish could not be exercised
  locally; it is first proven by the first real release.
- **Release-job installs.** The `release` job runs `npm ci` in `js/` so the
  pinned devDependencies are available to `npx semantic-release`.
- **Node 20 matrix leg.** The release devDependencies require Node >= 22.14;
  on Node 20 `npm ci` only warns (no `engine-strict`) and tests do not use
  them.
- **Action pins.** `actions/checkout` v7.0.1 and `actions/setup-node` v7.0.0,
  pinned by SHA; the `test` job additionally uses npm caching, the `release`
  job does not.
- **Pending (step 6):** bootstrap publish of `0.1.0` and the `js-v0.1.0` tag,
  Trusted Publisher configuration on npm, branch protection, token
  revocation. Documented in the root `README.md`. Without the `js-v0.1.0`
  tag the first run would publish `1.0.0`, so the tag must exist before
  this lands on `main`.
- **Step 7: staged publishing (revision).** Added `@semantic-release/exec`
  (7.1.0, pinned), set `npmPublish: false` on the npm plugin, and added a
  `publishCmd` of `npm stage publish --access public`. The `release` job now
  runs `npm install -g npm@^11.15.0` before `npm ci`. This deviates from the
  original "fully automatic publish" design because npm requires a 2FA
  promotion for stage-only credentials. Not verified against the real
  registry: the OIDC stage permission, the `exec` plugin's cwd and the
  monorepo plugin's interaction with it are first proven by the first release.
- **First live attempt (0.1.1) failed with E401 at `npm stage publish`.**
  The package did not exist on npm yet (bootstrap never done), so no Trusted
  Publisher could be configured and the OIDC exchange failed. The tag
  `js-v0.1.1` had already been pushed by semantic-release (it tags before
  publishing) and must be deleted before retrying. The package was briefly
  renamed to a scoped name and then reverted to `spacekid`. Bootstrap used `npm login` (2FA)
  with `--provenance=false`, no token.
- **Stage moved from `publish` to `prepare`.** semantic-release creates and
  pushes the tag before the `publish` step, so each failed stage left an
  orphan tag (`js-v0.1.1` to `js-v0.1.4`) and bumped the next version. The
  stage command now runs as `prepareCmd` (after the npm plugin sets the
  version, before the tag), so a failed stage leaves no tag. `--loglevel
  verbose` was added temporarily to diagnose the persistent `E401`.
