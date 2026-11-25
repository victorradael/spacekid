# Agent Guide — spacekid

## Project Overview

SpaceKid is a minimalist spec kit for agentic development, distributed as a
container image. Its `init` command creates a miniverse — contexts, artifacts,
and the spec-driven workflow — in any directory. SpaceKid follows its own
flow: its specs, plans, and contexts live in its own `miniverse/` folder.

## Miniverse

This directory works through a **miniverse**: the `miniverse/` folder, a
self-contained world holding the knowledge, the produced files, and the
spec-driven workflow for everything here.

The flow is the heart of it: context → spec → plan → implementation → close
the loop. **Read `miniverse/AGENTS.md` before doing anything else**, and follow
it exactly.
Every agent here also follows `miniverse/ponytail.md` on every task, always,
and checks upstream ponytail for a newer release first (manual, nothing
installed; see `miniverse/contexts/ponytail.md`).
