#!/bin/sh
# Brings every git repository covered by this miniverse up to date: reports
# the branch each one is on, then runs a fast-forward-only pull. With --main,
# each repository is first moved to the main branch. Refreshes catalog.md and
# uses it to find every level: the directory above this miniverse and the one
# above each nested miniverse, at any depth; the repositories at those levels
# are synced.
# Self-contained: needs only POSIX sh plus git, sort and sed.
# Never asks for input; a problem in one repository never stops the others.
# Exit status: 0 all good, 1 some repository needs attention, 2 bad usage.
set -u
LC_ALL=C
export LC_ALL
GIT_TERMINAL_PROMPT=0
export GIT_TERMINAL_PROMPT

main_only=0
case ${1:-} in
  "") ;;
  --main) main_only=1 ;;
  *)
    echo "usage: ./sync.sh [--main]" >&2
    echo "  --main  move every repository to the main branch before updating" >&2
    exit 2
    ;;
esac

self=$(cd "$(dirname "$0")" && pwd -P)
root=$(dirname "$self")
work="$self/.sync.$$"
trap 'rm -f "$work".*' EXIT
trap 'exit 1' INT TERM HUP

# Presentation, in the style of `spacekid init`: colors and symbols on a
# terminal; plain text when piped, redirected, with NO_COLOR, or TERM=dumb.
if [ -t 1 ] && [ -z "${NO_COLOR+x}" ] && [ "${TERM:-}" != dumb ]; then
  color=1
else
  color=0
fi

# paint <sgr codes> <text>
paint() {
  if [ "$color" -eq 1 ]; then
    printf '\033[%sm%s\033[0m' "$1" "$2"
  else
    printf '%s' "$2"
  fi
}

# Compact one-line mark: the big logo is only for the first contact (`spacekid init`).
banner() {
  [ "$color" -eq 1 ] || return 0
  printf '\033[1;38;5;51m✦ \033[0m'
  i=0
  for ch in S P A C E K I D; do
    case $i in 0|1) c=51 ;; 2|3) c=45 ;; 4) c=39 ;; 5|6) c=99 ;; *) c=135 ;; esac
    printf '\033[1;38;5;%sm%s\033[0m' "$c" "$ch"
    i=$((i + 1))
  done
  printf '  \033[2;38;5;245m·  %s\033[0m\n\n' "$1"
}

# Repository header: "<path>  <branch label>".
head() {
  if [ "$color" -eq 1 ]; then
    printf '%s %s  %s\n' "$(paint '1;38;5;51' ◆)" "$(paint 1 "$1")" "$(paint '38;5;213' "$2")"
  else
    printf '%s  branch=%s\n' "$1" "$2"
  fi
}

# Result line under a header: <kind> is ok, same, or bad.
result() {
  if [ "$color" -eq 0 ]; then
    printf '  %s\n' "$2"
    return
  fi
  case $1 in
    ok) printf '  %s %s\n' "$(paint '1;38;5;42' ✔)" "$(paint '38;5;42' "$2")" ;;
    same) printf '  %s %s\n' "$(paint '1;38;5;244' •)" "$(paint '38;5;244' "$2")" ;;
    *) printf '  %s %s\n' "$(paint '1;38;5;203' ✘)" "$(paint '38;5;203' "$2")" ;;
  esac
}

# A repository that is skipped or fails before the pull: <path> <label> <text>.
stop() {
  if [ "$color" -eq 1 ]; then
    head "$1" "$2"
    result bad "$3"
  else
    printf '%s  branch=%s  %s\n' "$1" "$2" "$3"
  fi
}

banner "repository sync"

# Refresh the catalog, then use it to learn which directories hold the levels
# of this miniverse: the directory above it, plus the one above every nested
# miniverse the catalog lists, at any depth.
[ -x "$self/scan.sh" ] && "$self/scan.sh" >/dev/null 2>&1 || true
{
  printf '%s\n' "$root"
  sed -n '/^## Nested miniverses/,$ s/^ *- `\(\.\.\/[^`]*\)`.*/\1/p' "$self/catalog.md" 2>/dev/null |
    while IFS= read -r rel; do
      c=$root/${rel#../}
      printf '%s\n' "${c%/*}"
    done
} | sort -u > "$work.levels"

# Repositories: each level directory and its direct subdirectories (the
# projects living side by side at that level) that hold a ".git" (directory
# or file, so worktrees and submodules count).
while IFS= read -r level; do
  printf '%s\n' "$level"
  for sub in "$level"/* "$level"/.[!.]*; do
    [ -d "$sub" ] && printf '%s\n' "$sub"
  done
done < "$work.levels" | sort -u |
  while IFS= read -r dir; do
    [ -e "$dir/.git" ] && printf '%s\n' "$dir"
  done > "$work.repos"

# Runs git inside the repository being processed.
g() {
  git -C "$repo" "$@"
}

# First line of the combined output of a failed command, for the report.
reason() {
  printf '%s' "$1" | sed -n '1p'
}

repos=0
problems=0
while IFS= read -r repo; do
  [ -n "$repo" ] || continue
  repos=$((repos + 1))
  if [ "$repo" = "$root" ]; then
    rel=..
  else
    rel=../${repo#"$root"/}
  fi

  branch=$(g symbolic-ref --short -q HEAD 2>/dev/null || true)
  if [ -z "$branch" ]; then
    sha=$(g rev-parse --short HEAD 2>/dev/null || echo "no commits")
    stop "$rel" "detached @ $sha" "skipped: not on a branch"
    problems=$((problems + 1))
    continue
  fi

  if [ "$main_only" -eq 1 ] && [ "$branch" != main ]; then
    if [ -n "$(g status --porcelain 2>/dev/null)" ]; then
      stop "$rel" "$branch" "skipped: uncommitted changes, not moved to main"
      problems=$((problems + 1))
      continue
    fi
    if out=$(g checkout main 2>&1); then
      head "$rel" "$branch -> main"
      branch=main
    else
      stop "$rel" "$branch" "failed: cannot switch to main ($(reason "$out"))"
      problems=$((problems + 1))
      continue
    fi
  else
    head "$rel" "$branch"
  fi

  if out=$(g pull --ff-only 2>&1); then
    case $out in
      *"Already up to date"*) result same "up to date" ;;
      *) result ok "updated" ;;
    esac
  else
    result bad "failed: $(reason "$out")"
    problems=$((problems + 1))
  fi
done < "$work.repos"

echo
if [ "$repos" -eq 0 ]; then
  echo "no repositories found"
elif [ "$problems" -eq 0 ]; then
  if [ "$color" -eq 1 ]; then
    printf '%s %s\n' "$(paint '1;38;5;42' ✔)" "$(paint '1;38;5;42' "$repos repositories, all up to date")"
  else
    echo "$repos repositories, all up to date"
  fi
else
  if [ "$color" -eq 1 ]; then
    printf '%s %s\n' "$(paint '1;38;5;203' ✘)" "$(paint '1;38;5;203' "$repos repositories, $problems need attention")"
  else
    echo "$repos repositories, $problems need attention"
  fi
  exit 1
fi
