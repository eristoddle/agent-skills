# TASKS — {{PROJECT}}

> The unit of implementation work. Written by the planning thread once a decision in the
> planning doc is concrete enough to build, executed by the `{{AGENT}}` agent in its own
> context window.
>
> **The active task is a serial QUEUE of numbered pieces** (1, 2, 3…) — tightly-related
> steps of one job, or a stack of independent jobs; doesn't matter, stack as many as you
> want. Two rhythms this serves:
> - **Pacing** — queue a little, plan the next batch while the agent grinds.
> - **Unattended** — queue a lot and walk away; the agent chews the whole queue.
>
> **Execution (default = synchronous, one agent):** work the queue top-to-bottom. A blocked
> piece does **not** halt the queue — skip it and continue with any piece that doesn't
> depend on it (mark deps inline: `depends on #2`); halt only when nothing remaining can
> proceed. **Always log run-state on stop** (done or blocked): flip each piece's status box
> as you go and update the ▶ Run state note, so a killed/forgotten session is recoverable
> from this file on disk. (Running *parallel* agents across disjoint files is a separate
> opt-in burst tactic, not this default — the objective is pacing, not throughput.)
>
> **Contract:** fill every section before launching. Mark a section `—` only if it genuinely
> doesn't apply. The agent is *cold on the planning conversation* but *warm on the project*
> (it has the conductor + the codebase) — reference decisions and files by pointer; don't
> re-explain the repo.
>
> Completed work collapses to a one-block summary with a stable `[tag]` under **✅ Done**;
> the full detail lives in the planning doc's session log.

---

# ⏭ NEXT ACTIVE TASK — <title>

## Goal

## Why (pointer)

### ▶ Run state (the agent keeps this current on every stop)
_<last updated · what's done · what's blocked and why · what remains · resume from>_

## Design — numbered pieces (status: `[ ]` not started · `[x]` done · `[!]` blocked)
- [ ] **1.** <piece>
- [ ] **2.** <piece>  _(depends on #1)_

## Files

## Tests (add; keep the suite green)

## Out of scope (do NOT do)

## Report back

---

## ✅ Done (collapsed — full detail in the planning doc's session log)
_<nothing yet>_
