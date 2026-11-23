# Container and CI Security

Summary: where SpaceKid's security exposure is, the rules the image and workflow follow, and how to check them.
Created: 2026-11-23
Updated: 2026-11-23

## Where the risk is

- The CLI uses only the standard library: no third-party runtime packages.
  Nearly all known vulnerabilities come from the image's Alpine packages
  (`openssl`, `sqlite-libs`, `python3`, `git`, `busybox`, `expat`).
- A published image never changes, so it goes stale; only a new release
  delivers base fixes.
- `scan` and `sync` execute the mounted project's own `scan.sh` / `sync.sh`,
  and `git` runs that repository's hooks. This is by design; the container
  (non-root, only `/project` mounted, no capabilities) is the containment.

## Rules to keep

- Alpine is pinned by digest in both stages (same release) and the final
  stage runs `apk upgrade`. Dependabot bumps the digest with a `fix:` commit,
  which publishes a patch release.
- No setuid/setgid files in the image; it runs as `spacekid` (uid 1000).
- CI gate: Grype, `severity-cutoff: high`, `only-fixed: true`, on PRs, on
  release (before push), and weekly on the published `latest`.
- Release builds: `pull: true`, layer cache scoped to the run id only,
  provenance (`mode=max`) and SBOM attestations.
- Every action pinned by commit SHA; checkouts with
  `persist-credentials: false`; workflow default `contents: read`.
- The documented `docker run` uses `--cap-drop=ALL --security-opt
  no-new-privileges`; the smoke test runs with the same flags.
- `init` never writes through symlinks (exclusive create, links skipped).

## Checking without Docker

`grype registry:victorradael/spacekid:latest` scans the published image with
no daemon. To test a new base, build a rootfs with `apk.static --usermode
--root <dir> add python3 git` and scan it with `grype dir:<dir>`; its Python
runs via `<dir>/lib/ld-musl-x86_64.so.1 --library-path <dir>/lib:<dir>/usr/lib`.
