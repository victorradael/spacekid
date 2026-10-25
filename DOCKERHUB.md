![SpaceKid](https://raw.githubusercontent.com/victorradael/spacekid/main/assets/spacekid_logo.jpg)

A minimalist spec kit for agentic development. One command adds `AGENTS.md`
files to your project so AI agents (and humans) follow a closed loop:
**spec → plan → implementation → update**. Works with projects in any
language.

> Study project: not a supported product. Expect rough edges and breaking
> changes.

## Quick start

Run from the root of your project:

```bash
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/project" victorradael/spacekid init
```

```
mode: project
created: AGENTS.md
created: specs/AGENTS.md
created: plans/AGENTS.md
```

- `-v "$PWD:/project"` mounts your current directory as the project.
- `-u "$(id -u):$(id -g)"` makes the created files belong to you. Without it
  they may be owned by another user.

## Tags

| Tag | Meaning |
|---|---|
| `1.2.3` | an exact release |
| `1.2` | the latest patch of that minor version |
| `latest` | the most recent release |

```bash
docker run --rm victorradael/spacekid:1.2.3 --version
```

## Options

Everything after the image name is passed to `spacekid`.

| Option | Description |
|---|---|
| `--version` | Print the version and exit. |
| `-h`, `--help` | Show help. |
| `init` | Scaffold the SpaceKid files. |
| `init --name NAME` | Project name for `AGENTS.md` (default: detected from `pyproject.toml`, else the directory name). |
| `init --mode MODE` | `project`, `brain` or `auto` (default). |
| `init --path PATH` | Directory to scaffold; must exist. Default: the mounted project. |

## Modes

**Project mode** (a single repository) creates `AGENTS.md`, `specs/AGENTS.md`
and `plans/AGENTS.md`.

**Brain mode** is for a folder holding several repositories side by side. It
creates a `brain/` folder:

```
brain/
├── AGENTS.md
├── contexts/
├── artifacts/
└── sdd/
    ├── specs/AGENTS.md
    └── plans/AGENTS.md
```

`auto` picks brain mode when the directory has no `.git` of its own and two or
more child folders do; otherwise project mode. Force one with `--mode`:

```bash
docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/project" victorradael/spacekid init --mode brain
```

## Existing files

Nothing is overwritten. `AGENTS.md` and `brain/AGENTS.md` are left alone
(`skipped (already exists)`); the spec and plan rule files are added to the
end if they exist without the SpaceKid rules (`appended to`). Running `init`
again is safe: files that already have the rules are left as they are.

## Tip: shell alias

```bash
alias spacekid='docker run --rm -u "$(id -u):$(id -g)" -v "$PWD:/project" victorradael/spacekid'
spacekid init
```

## Full documentation

Installing with Python, troubleshooting, the working loop and how to
contribute: <https://github.com/victorradael/spacekid#readme>

Issues: <https://github.com/victorradael/spacekid/issues>
