# Maintaining SpaceKid

Material for maintainers. User documentation lives in `README.md`.

## Releasing

Releases are automatic. Every push to `main` is evaluated from its commit
messages ([Conventional Commits](https://www.conventionalcommits.org/)); if a
user-visible change is found, a GitHub Release with generated notes is
created and the image is published to Docker Hub.

| Commit | Effect |
|---|---|
| `fix: ...` | patch release (`1.2.3` → `1.2.4`) |
| `feat: ...` | minor release (`1.2.3` → `1.3.0`) |
| `BREAKING CHANGE:` footer (or `feat!:`) | major release (`1.2.3` → `2.0.0`) |
| `docs:`, `test:`, `chore:`, `ci:`, `refactor:` | no release |

Pull requests are built and smoke-tested without publishing anything. A
failed release shows as a failed run of the `docker` workflow, which GitHub
notifies maintainers about.

## Docker Hub page

The Docker Hub overview is `DOCKERHUB.md`. The `publish` job pushes it as the
repository's full description at the end of every release, so edits only reach
Docker Hub on the next release (documentation-only commits do not trigger
one). Use absolute URLs in that file: Docker Hub cannot resolve relative links
or images.

## One-time setup

- Tag the current `main` commit `v0.1.0` and push it, so the first automated
  release continues the numbering instead of starting at `1.0.0`.
- Create the `spacekid` repository on Docker Hub.
- Add the secrets `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN`, ideally in a
  `production` environment. The token is scoped to that repository only and
  needs **Read, Write, Delete** permission: updating the description requires
  more than push-only access.
- Protect `main` and require the `test` check.
