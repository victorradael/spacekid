![SpaceKid](https://raw.githubusercontent.com/victorradael/spacekid/main/assets/spacekid_logo.jpg)

A minimalist spec kit for agentic development. One command adds `AGENTS.md`
files to your project so AI agents (and humans) follow a closed loop:
**spec → plan → implementation → update**. Works with projects in any
language.

> Study project: not a supported product. Expect rough edges and breaking
> changes.

## Quick start

Three steps, from nothing to a scaffolded project. Works on macOS (Apple
Silicon and Intel) and Linux; the image is native on both, with no extra flags.

**Requirements.** A container runtime: Docker Desktop, OrbStack or Colima on
macOS; Docker Engine on Linux.

**1. Download the image (once).**

```bash
docker pull victorradael/spacekid
```

**2. Create the `spacekid` command (once).** This adds a shortcut to your
shell profile so it survives new terminals. Use `~/.zshrc` for zsh (the macOS
default) or `~/.bashrc` for bash (`~/.bash_profile` on macOS):

```bash
cat >> ~/.zshrc <<'EOF'
alias spacekid='docker run -it --rm -e NO_COLOR -u "$(id -u):$(id -g)" -v "$PWD:/project" victorradael/spacekid'
EOF
source ~/.zshrc
```

For fish, run `alias --save spacekid 'docker run -it --rm -e NO_COLOR -u (id -u):(id -g) -v $PWD:/project victorradael/spacekid'` instead.

**3. Use it, from the root of your project.**

```bash
spacekid init
```

```
mode: project
created: AGENTS.md
created: specs/AGENTS.md
created: plans/AGENTS.md
```

From now on, `spacekid` is all you type.

### What the shortcut does

| Part | Meaning |
|---|---|
| `docker run` | Start the SpaceKid container. |
| `--rm` | Delete the container when it finishes. Nothing is left behind. |
| `-it` | Connect your terminal to the container, so colors and the interactive menu work. Without it, SpaceKid prints plain text. |
| `-e NO_COLOR` | Pass your `NO_COLOR` setting through, so opting out of color still works. |
| `-u "$(id -u):$(id -g)"` | Run as you, so created files belong to you instead of `root`. |
| `-v "$PWD:/project"` | Give the container your current folder as `/project`. Without it, files are created inside the container and lost. |
| `victorradael/spacekid` | The image to run. |

If `docker pull` fails midway (for example `connection reset by peer`), run it
again: layers already downloaded are kept, so it resumes.

## Tags

| Tag | Meaning |
|---|---|
| `1.1.1` | an exact release |
| `1.1` | the latest patch of that minor version |
| `latest` | the most recent release |

To pin a version, use the tag in `docker pull` and in the shortcut:

```bash
docker pull victorradael/spacekid:1.1.1
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
spacekid init --mode brain
```

## Existing files

Nothing is overwritten. `AGENTS.md` and `brain/AGENTS.md` are left alone
(`skipped (already exists)`); the spec and plan rule files are added to the
end if they exist without the SpaceKid rules (`appended to`). Running `init`
again is safe: files that already have the rules are left as they are.

## Full documentation

Troubleshooting, the working loop and how to contribute: <https://github.com/victorradael/spacekid#readme>

Issues: <https://github.com/victorradael/spacekid/issues>
