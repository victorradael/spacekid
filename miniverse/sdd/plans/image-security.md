# Image and Supply-Chain Security — Implementation Plan

Implements: `sdd/specs/image-security.md`
Status: Done

## Approach

Most of the exposure comes from the image's OS packages, not from SpaceKid's
own code (standard library only, no third-party runtime dependencies). So
the fix lives mainly in the `Dockerfile` and the `docker` workflow: a newer,
digest-pinned base upgraded at build time, a vulnerability gate in CI, and
releases that actually ship base fixes. The one code change makes `init`
refuse to write through symlinks.

## Steps

1. `Dockerfile`: both stages on `alpine:3.24@sha256:…` (Python 3.14, git
   2.54); `apk upgrade --no-cache` before `apk add`; strip setuid/setgid bits
   (`find / -xdev -perm /6000 -exec chmod a-s`); validate the `VERSION` build
   arg as semver before it goes into `sed`.
2. Workflow `test` job: `docker build --pull --no-cache`; smoke test with
   `--cap-drop=ALL --security-opt no-new-privileges`, adding `scan` and a
   no-setuid check; Grype scan (`anchore/scan-action`, SHA-pinned,
   `severity-cutoff: high`, `only-fixed: true`).
3. `publish` job: same Grype gate on the amd64 check image; `pull: true`;
   layer cache scoped to `github.run_id` (the push reuses the checked layers,
   never older ones); `provenance: mode=max` and `sbom: true`.
4. `scan-published` job on a weekly `schedule` scans `victorradael/spacekid:latest`;
   `test` skips scheduled runs.
5. All checkouts set `persist-credentials: false`.
6. Dependabot: docker updates use the `fix` prefix (patch release);
   github-actions updates use `ci` and a 7-day cooldown.
7. `scaffold.py`: `write_or_skip` / `write_or_append` skip symlinks and create
   files with exclusive open (`"x"`), so a dangling link is never followed.
   Test in `tests/test_scaffold.py`.
8. README / DOCKERHUB alias gains `--cap-drop=ALL --security-opt
   no-new-privileges`, explained in the flags table; MAINTAINING gets a
   Security section.

## Key Decisions

- **Alpine 3.24 over upgrading 3.22.** `apk upgrade` on 3.22 would clear the
  fixable findings too, but 3.24 also drops the count of unfixed ones
  (64 → 42) and supports until 2028-06. The pruned stdlib list still matches
  Python 3.14 (the removed `distutils`/`lib2to3` are simply absent).
- **Gate on fixable high/critical only.** Unfixed CVEs cannot be acted on;
  failing on them would block every release.
- **Run-scoped cache instead of no cache.** A cross-run GHA cache would keep
  stale `apk` layers forever and is a poisoning vector; no cache at all would
  make the pushed image a different build from the checked one.
- **Grype, not Trivy.** Trivy's GitHub Action had a supply-chain compromise in
  2026; Grype via a SHA-pinned action avoids that dependency.
- **`fix:` prefix for base bumps.** Without it, Dependabot commits produce no
  release and users never receive base-image fixes.
- **Not changed:** `scan`/`sync` executing the project's own scripts (by
  design, contained by the container); git hooks in synced repositories (the
  user's own); `sqlite-libs` stays installed as a `python3` dependency, but
  its Python module is pruned, so it is unreachable from SpaceKid.

## Implementation Notes

- No Docker daemon was available in the working environment. Verification
  used an Alpine 3.24 root filesystem built with `apk.static --usermode`:
  Grype on that rootfs (0 critical, 0 fixable; 42 total), the full test suite
  under its Python 3.14 (69 passed), and `--version`, `--help`, `init`,
  `scan`, `sync` on a copy with the stdlib pruned exactly as the
  `Dockerfile` does. The real image build, the smoke test with dropped
  capabilities and the CI scan gate are verified by the first workflow run.
- The workflow passes `actionlint`.
- Published image before the change (alpine 3.22.7): 64 findings, 1 critical
  and 4 high with fixes available. Full numbers in
  `artifacts/image-security/vulnerability-scan-2026-11-23.md`.
