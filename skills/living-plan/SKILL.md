---
name: living-plan
description: Manage the lifecycle of a project's planning docs (PLAN.md + TASKS.md + an implementer agent). Detects project state and routes to one of five actions — GRILL the user round-by-round to generate the decision record itself (a design-tree interview; the only action that creates material instead of reshaping it), SCAFFOLD a fresh project with the planning/implementation workflow, ADOPT/backfill the missing pieces in a project that already uses it, REBALANCE a bloated planning doc by relocating cooled material (old session logs, settled decisions, futures, reference) into linked docs/ files and leaving one-line pointers (progressive disclosure, same pattern as a MEMORY.md index), or EVICT completed task queues out of a task doc that has become an append-only log. Formerly named **plan-rebalance** — that older name still refers to this skill and should route here. Trigger on "living plan", "living-plan", "plan-rebalance", "rebalance", "rebalance the plan", "scaffold the planning workflow", "set up the PLAN/TASK workflow", "clean up TASKS.md", "the task file is huge", "grill me", "stress-test this", "poke holes in this", "what am I missing", or when a PLAN.md or TASKS.md has grown heavy to read every session.
---

# living-plan

This skill owns the **planning-doc workflow**: a hot, lean `PLAN.md` (the every-session
decision record) paired with a `TASKS.md` handoff contract and an `implementer` agent, with
**cooled** material progressively disclosed into a `docs/` tree so the hot layer stays
cheap to carry in context.

Five actions, and one is different in kind. **`grill` generates** the material: it interviews
the user round-by-round until the design tree has been *visited*, and writes the result into
the decision record. The other four (`scaffold`, `adopt`, `rebalance`, `evict-tasks`) only
reshape what already exists. Grill is also the only thing that ever moves an item *out* of the
cold containers — threads ripen along a ladder (parking lot → open question → decision → task
queue) and nothing else here promotes one. That ladder is the point for the audience this
serves: someone experimenting, who does not know the shape up front and needs a breadcrumb
trail of where the thinking has already been.

The handoff contract treats the active task as a **serial queue of numbered pieces** — stack
a few (pacing: plan ahead while the agent grinds) or many (unattended: queue work and walk
away). The agent works the queue top-to-bottom, skips a blocked piece rather than halting,
and logs run-state into the task doc on every stop so a killed session is recoverable. (Full
shape in `templates/TASKS.template.md` + the agent template.)

It is **portable across projects** and **tolerant of naming variance** (`TASKS.md` vs
`TASK.md`, `CLAUDE.md` vs `AGENTS.md`). It does NOT assume this skill's home project.

## External task mirrors

Some projects keep a second copy of the task list outside the repo — a note in a notes app, a
shared doc, a tracker — because items get captured when the user is away from the machine.
This skill supports exactly one thing for that case: **an optional pointer line in the
conductor**, named at scaffold time (or backfilled by `adopt`), saying where the mirror is and
that it must be reconciled at the start and end of a queue.

**That pointer is the whole feature, and it lives only in the conductor.** Never write an ID,
a marker, a sync timestamp, or frontmatter into the planning doc or the task doc to serve a
mirror. Whatever tool performs the reconciliation owns that state on its own side, so these
docs stay standalone and portable for projects with no mirror at all — which is most of them.
A mirror nobody reconciles is worse than no mirror, so the pointer states *when* to reconcile
rather than merely that a mirror exists.

## Operating principle

The planning/orchestrating agent must stay **light** — it only orchestrates and plans.
So all the heavy process logic lives in this skill's `workflows/` and `references/` and is
**lazy-loaded**: read only the one file for the path you're on. Never inline these into a
project's `PLAN.md` or `CLAUDE.md` — projects get a one-line pointer to invoke this skill,
not a copy of the process.

Every mutating action is **propose-then-confirm**. Never overwrite or relocate without
showing the user a manifest first. Never clobber existing docs.

`grill` carries one extra constraint: it **must run in the primary agent, never a subagent.**
Its contract is a human pause, and in a subagent that pause is a no-op — the agent answers the
design questions on the user's behalf, which is the exact failure it exists to prevent.

## Step 1 — Detect project state (always do this first)

Inspect the current project (run from its root) and classify it. Discover names; don't
assume them.

```bash
# planning doc
ls PLAN.md PLAN.MD plan.md 2>/dev/null
# task handoff (tolerate singular/plural)
ls TASK.md TASKS.md 2>/dev/null
# conductor (tolerate Claude/Agents variants; CLAUDE.md is often a SYMLINK to
# AGENTS.md or vice versa — resolve with `readlink`/`realpath` and edit the real
# target, never write through the link)
ls -l CLAUDE.md AGENTS.md 2>/dev/null
# agent catalog
ls .claude/agents/ AGENTS/ 2>/dev/null
# already-rebalanced?
ls docs/decisions docs/sessions docs/questions docs/parking-lot 2>/dev/null
# size proxy (NOT live context % — the agent can't read that reliably; the doc's
# word count is the thing you can measure and control). Measure BOTH docs.
wc -w PLAN.md TASKS.md 2>/dev/null
# how much of the task doc is already finished? (checked vs unchecked boxes)
grep -c '^\s*-\s*\[x\]' TASKS.md 2>/dev/null; grep -c '^\s*-\s*\[ \]' TASKS.md 2>/dev/null
# external task mirror already pointed at from the conductor?
grep -n 'External task mirror' CLAUDE.md AGENTS.md 2>/dev/null
```

Classify into one of four **detected** states — plus `grill`, which is requested rather than
detected (see below):

| State | Signal | Route |
|---|---|---|
| **Greenfield** | no planning doc present | `workflows/grill.md` → `workflows/scaffold.md` |
| **Partial / adopt** | planning doc exists but pieces missing (no TASK file, no implementer agent, no docs/ tree) | `workflows/adopt.md` |
| **Mature** | full system present; planning doc heavy | `workflows/rebalance.md` |
| **Task doc bloated** | task doc heavy and mostly finished work (checked ≫ unchecked, or a `✅ Done` archive that never leaves) | `workflows/evict-tasks.md` |
| **Deciding, not filing** | *not a filesystem state* — asked for, or offered when the user is thinking out loud | `workflows/grill.md` |

The last two are independent: `PLAN.md` and `TASKS.md` bloat for **different reasons** and are
fixed by different workflows. A `PLAN.md` bloats because decisions accumulate; a `TASKS.md`
bloats because completed queues are collapsed but never evicted. Check both.

**Greenfield now runs grill first.** Scaffold used to open with "what is this project?" and
emit a PLAN.md whose Decisions section was empty — which is how a decision record ends up
recording nothing until months later. Grill produces the tree, scaffold emits a planning doc
already populated with it. If the user declines the grill or stops it early, scaffold still
runs on whatever was settled.

**Grill is requested, never detected.** It fires on a phrase ("grill me", "what am I
missing"), or on an uncertainty signal the user gives while thinking out loud — and in that
second case you **offer it in one line and wait**, never launch it. It can run against any of
the other states at any point in a project's life.

A project can need more than one (e.g. mature *and* missing an agent). Report what exists,
what's missing, and what has cooled, then offer the relevant action(s). Let the user pick;
do not chain them silently.

## Step 2 — Confirm and route

Tell the user the detected state in one or two lines, then read the matching workflow file
and follow it. The two triggers that bring you here:

- **Phrase trigger** — the user says "rebalance" / "scaffold the planning workflow" / etc.
  Always honor it regardless of size.
- **Size nudge** — when invoked, if `wc -w PLAN.md` is over the project's threshold
  (default **15000 words**; record per-project overrides in the ledger), surface it:
  "PLAN.md is 27.6k words, ~12k over threshold — want to rebalance?" The phrase is the real
  entry point; the word count is just the nudge.
  For the **task doc** the nudge is different — it's a *ratio*, not a size: when finished
  material is over ~60% of the file, say so concretely ("TASKS.md is 758 lines, ~90% of it
  completed work") and offer `workflows/evict-tasks.md`.

## The model in one screen (so you don't re-derive it)

- **Cooled material goes to `docs/`**, one file per item, in category subfolders:
  `docs/decisions/`, `docs/questions/`, `docs/parking-lot/`, `docs/sessions/`.
- **Questions & parking-lot are born as pointers**: PLAN.md shows the *heading* (the item
  itself, one line) + a link; the file holds the discussion. No classification needed.
- **Decisions stay whole and inline while hot**; when one cools it collapses to a
  heading + link, body moved to `docs/decisions/Dxx.md`.
- **Session-log entries** archive by **recency** (keep last N inline, older → `docs/sessions/`).
  This is usually the heaviest cold mass and the safest move.
- **Threads ripen along a ladder**: parking lot → open question → decision → task queue.
  Only `grill` moves an item up it, and only propose-then-confirm. Thread files
  (`templates/QUESTION.template.md`) are **append-only** — each round adds a dated section
  rather than rewriting, because the sequence of what was thought and when is the breadcrumb
  trail the whole system exists to keep.
- **What "cooled" means** for decisions, and how the per-run judgment matures into automatic
  rules, lives in `references/cooled-heuristic.md` and `references/ledger.md`. Read those
  when running a rebalance.
