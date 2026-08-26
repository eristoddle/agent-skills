# Workflow: rebalance

Relocate cooled material out of a heavy planning doc into `docs/`, leaving one-line
pointers. Propose-then-confirm; never lossy.

**Read first:** `references/cooled-heuristic.md` (what to move) and `references/ledger.md`
(the log + active promotions).

## Steps

1. **Confirm names + size.** From Step 1 detection you know the planning doc, task doc, and
   conductor names. Run `wc -w <planning-doc>`. If `docs/rebalance-log.md` exists, read its
   `## Config` (threshold, recency_keep_sessions) and `## Rules`.

2. **Ensure the docs tree exists** (create only what's missing):
   `docs/{decisions,questions,parking-lot,sessions}/`.

3. **Scan and classify**, by category:
   - Session log → keep last `recency_keep_sessions` (default 3) inline; rest archive.
   - Decisions → apply the cooled test (reference + foundational flag), plus any promoted
     `## Rules`. Foundational (`🔒`) always kept.
   - Open questions / parking-lot → if any are still carrying full discussion inline
     (legacy, pre-pointer), convert them to heading + link now.

4. **Build the manifest** (see cooled-heuristic.md for the format). Include any
   rule-promotion pitch from the ledger active-mode scan. **Show it to the user. Wait.**

5. **On approval, execute** each move:
   - Write the body to its `docs/<category>/<id>.md` file (give it a short title heading).
   - Replace it in the planning doc with a one-line pointer:
     `- **D7 — Pipeline framework choice** → [docs/decisions/D07.md](docs/decisions/D07.md)`
   - For decisions, preserve the `Dxx` id so back-references keep resolving.

6. **Append to the ledger** — one line per item with its reason; update `## Config` if the
   threshold or names changed; add any approved rule to `## Rules`.

7. **Integrity check** (cheap, deterministic): every pointer in the planning doc resolves to
   a real file; flag orphan files in `docs/` that nothing points to. Report results.

8. **Sync the conductor** (the first rebalance especially). The project's `CLAUDE.md` /
   `AGENTS.md` was written before the `docs/` tree existed and likely still describes the
   planning doc as a single monolith. Grep it for how it describes the planning doc; if it
   doesn't mention the `docs/` layout or this skill, add a short paragraph: PLAN.md is the
   hot layer, cooled material lives in `docs/{decisions,questions,parking-lot,sessions}/`
   behind one-line pointers, and `living-plan` is what relocates it. Propose the wording
   first. **Watch for symlinks** — `CLAUDE.md` is often a symlink to `AGENTS.md` (or vice
   versa); resolve it and edit the real target, never write through the link. Generalize:
   any doc the rebalance reshapes whose *structure is described elsewhere* (a README, a
   QUICKSTART) should have that description checked and updated in the same pass.

9. **Commit the relocation on its own** so it's diffable/revertable:
   `docs: rebalance <planning-doc> → docs/ (<summary>)`. (Only if the user commits here;
   otherwise leave staged and tell them.)

10. **Report** final word count (before → after) and the integrity result.
