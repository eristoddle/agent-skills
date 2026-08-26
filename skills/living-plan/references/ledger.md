# The rebalance ledger

A small append-only record at `docs/rebalance-log.md` that turns per-run judgment into
eventual automation. It does triple duty:

1. **Audit trail / reversibility** — every relocation is logged with a reason, so nothing
   silently vanishes and any move can be traced and reverted.
2. **Seed corpus for automation** — recurring manual calls become mechanical rules.
3. **Per-project config** — records the threshold override and the discovered doc names so
   later runs are deterministic.

## Format

```markdown
# Rebalance log

## Config
- planning_doc: PLAN.md
- task_doc: TASKS.md            # naming variance recorded once
- conductor: AGENTS.md
- threshold_words: 12000        # override of the 15000 default
- recency_keep_sessions: 3

## Rules (promoted from recurring manual calls — run these automatically)
- superseded decisions → cool        (promoted 2026-07-02, seen 4 runs)

## Runs
### 2026-06-25 — rebalance (PLAN.md 27.6k → 9.1k)
- sessions 1–14 | archived | recency, kept last 3
- D7  | cooled  | nothing active references it
- D14 | cooled  | superseded by D19
- D23 | kept    | 🔒 foundational
```

## Active mode — pitch promotions each run

After logging a run, scan the `## Runs` history for a reason string that has appeared in
≥3 runs and is not already in `## Rules`. Surface ONE such candidate to the user:

> "You've cooled *superseded* decisions in 4 runs. Promote to an automatic rule so I stop
> asking?"

On approval, add it to `## Rules`. From then on, apply it mechanically during the manifest
step (still shown in the manifest, still confirmed in aggregate — just no longer a
per-item question).

Keep this logic here in the skill, never in the project's PLAN.md or conductor — the
planning agent stays light because this only loads when a rebalance runs.
