![SpaceKid](https://raw.githubusercontent.com/victorradael/spacekid/main/assets/spacekid_logo.jpg)

A minimalist spec kit for agentic development. One command creates a
**miniverse** in your directory: a self-contained world of contexts,
artifacts and a spec-driven workflow for AI agents (and humans). Works with
projects in any language.

**The flow** — the heart of SpaceKid: **context → spec → plan → implementation
→ close the loop**. Every piece of work starts by consulting (or creating)
contexts, and ends by bringing specs, plans and contexts up to date.

> Study project: not a supported product. Expect rough edges and breaking
> changes.

## Quick start

Three steps, from nothing to a miniverse. Works on macOS (Apple
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

**3. Use it, from the directory you want to work in** (a repository, several
repositories side by side, or an empty folder).

```bash
spacekid init
```

```
created: AGENTS.md
created: miniverse/AGENTS.md
created: miniverse/.miniverse
created: miniverse/scan.sh
created: miniverse/catalog.md
created: miniverse/contexts/AGENTS.md
created: miniverse/artifacts/AGENTS.md
created: miniverse/sdd/specs/AGENTS.md
created: miniverse/sdd/plans/AGENTS.md
created: miniverse/contexts/.gitkeep
created: miniverse/artifacts/.gitkeep
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
| `init` | Create a miniverse. |
| `init --name NAME` | Name for the guides and marker (default: detected from `pyproject.toml`, else the directory name). |
| `init --path PATH` | Directory to create the miniverse in; must exist. Default: the mounted project. |

## The miniverse

`init` always creates the same `miniverse/` folder, plus a short root
`AGENTS.md` pointing agents to it:

```
miniverse/
├── AGENTS.md        # the flow, folder map, rules
├── .miniverse       # marker
├── scan.sh          # standalone script that writes catalog.md
├── sync.sh          # standalone script: git pull every repo (--main for main)
├── catalog.md       # generated list of nested miniverses (paths)
├── contexts/        # knowledge (each folder has its own AGENTS.md)
├── artifacts/       # every other generated file
└── sdd/
    ├── specs/
    └── plans/
```

Miniverses nest to any depth; `scan.sh` lists the ones below; `sync.sh` pulls every repository.

## Existing files

Nothing is overwritten. `AGENTS.md`, `miniverse/AGENTS.md`, `scan.sh` and the
other generated files are left alone (`skipped (already exists)`); the folder
guides are added to the end if they exist without the SpaceKid rules
(`appended to`). Running `init`
again is safe: files that already have everything are left as they are.

## Full documentation

Troubleshooting, the working loop and how to contribute: <https://github.com/victorradael/spacekid#readme>

Issues: <https://github.com/victorradael/spacekid/issues>
