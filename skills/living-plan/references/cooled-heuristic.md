# Cooled heuristic — what to move, and how the judgment matures

The trigger answers *when* to rebalance. This answers *what* to move. Each content
category has a different lifecycle, so each gets a different rule.

## By category

### Session-log entries — recency (mechanical, safest)
Keep the last **N sessions** inline (default N=3). Archive older entries to
`docs/sessions/` (one file per session, or grouped by range, e.g. `sessions-01-10.md`).
Leave a one-line pointer in PLAN.md's session-log header: `Sessions 1–17 archived → docs/sessions/`.
No judgment required. This is usually where most of the bloat is — do it first.

### Open questions & parking-lot — born as pointers (no classification)
These don't cool; they're *deferred by nature*. From the moment they're created, PLAN.md
shows only the heading (the question / the parking-lot hook, one line) + a link to a file
in `docs/questions/` or `docs/parking-lot/` that holds the discussion. When a question
resolves it becomes a decision; when a parking-lot item is picked up it moves into the hot
flow. Nothing to relocate at rebalance time — they were never carrying their bulk inline.

### Decisions — whole until cold, then collapse to a pointer
A decision stays **whole and inline** while hot. It **cools** when BOTH of these hold and
it is NOT flagged foundational:

1. **Reference test (mechanical):** nothing *currently active* points at it — no open
   question, no parking-lot item, not the live TASK, not a session-log entry within the
   recency window. Compute this from the `[[Dxx]]` back-reference graph (grep), the same
   way a MEMORY index works. If the link graph isn't built yet, this is a read-through (see
   "maturity curve" below) — that's expected early on.
2. **Not foundational.** Some decisions are load-bearing even when unreferenced (e.g. an
   architectural split that a *future* feature depends on). Those carry a `🔒 foundational`
   marker on their heading and **never auto-cool**. Set it once when the decision is made.

Cold decision → collapse to a one-line heading + link, body moved to `docs/decisions/Dxx.md`.
A **superseded** decision (replaced/revised by a later one) is cold by definition — archive
it and note the supersession (`[[D19]] supersedes this`).

**Unbuilt-work marker (`🔨`).** A decision can be *cold by reference* (nothing active points at
it) yet describe work that is **decided but not yet built**. Cooling its body is still correct —
but the inline pointer heading MUST carry a `🔨` marker so the decisions index doubles as a
**pending-build list**: the marker is the "remember to build this" reminder that survives
archival. Drop the `🔨` when the work ships. Distinct from `🔒 foundational` (which prevents
cooling entirely); `🔨` still cools — it just flags status. When a rebalance cools a decision,
ask "is the work it describes built yet?" and mark accordingly.

> Don't use plain recency for decisions. An old foundational decision is rarely mentioned
> but still load-bearing; recency would wrongly archive it. Reference + foundational-flag
> is the correct test.

## The maturity curve — per-run now, automated later

Do NOT design the automation up front. **Mine it from your own runs** (same move as
skill-hardener: learn the rules from real history). The bridge is the **ledger**
(`references/ledger.md`).

- **Early (runs 1–N):** fully manual. For each decision you read it and make the hot/cold
  call by hand. The skill logs every call + its reason to the ledger. You also tag the
  cross-references you actually touch (`[[D19]] supersedes [[D14]]`), so the link graph the
  reference test needs **accretes organically** instead of as an up-front chore.
- **Mid:** the skill (active mode) re-reads the ledger each run, clusters the reasons, and
  **pitches a promotion**: "you've cooled superseded decisions 4 runs straight — make that
  an automatic rule?" You approve; the rule moves to the ledger's Rules section.
- **Late:** agreed rules run mechanically; you only adjudicate the leftovers.

It never stops being **propose-then-confirm** — automation just shrinks what needs your eyes.

## Output of a rebalance pass: a manifest, then confirm

Always produce a manifest before moving anything:

```
REBALANCE MANIFEST — PLAN.md (27.6k → ~9k words est.)
  sessions 1–14        → docs/sessions/sessions-01-14.md   (recency, keep last 3)
  D7  Pipeline framework → docs/decisions/D07.md            (cooled: nothing references)
  D14 (old budget calc)  → docs/decisions/D14.md            (cooled: superseded by D19)
  D23 engine/content split → KEEP (🔒 foundational)
  PROMOTE RULE? superseded → auto-cool  (seen 4 runs)
```

Wait for approval. Then move each item, leave its pointer, append to the ledger, and make
the relocation **its own git commit** (`docs: rebalance PLAN.md → docs/ (sessions 1–14, D7, D14)`)
so it's diffable and revertable.
