---
name: skill-hardener
description: Mine recent Claude Code session transcripts for recurring failure patterns, then harden the responsible skills or CLAUDE.md with targeted guardrails plus a regression test for each. Use when the user wants to learn from past sessions, fix recurring mistakes, "harden a skill", reduce repeat friction, analyze transcripts for failure patterns, or turn frustrating sessions into permanent fixes. Companion to skill-creator (which authors/evals skills); this one diagnoses what to fix from real history.
---

# Skill Hardener

Turn frustrating sessions into permanent fixes. This skill reads your own Claude Code
transcripts, finds the patterns that keep biting you, and proposes concrete guardrails
— each paired with a regression test that proves the fix and catches the regression.

It is the diagnostic complement to **skill-creator** (which authors and evals skills).
skill-hardener decides *what* to harden and *why*; it hands the actual edit + eval to
skill-creator's machinery when that's the right tool.

## The prime directive: this skill edits other skills, so it is dangerous

A tool that rewrites your skills can quietly degrade them. Every safeguard below is
load-bearing — do not skip them to move faster:

1. **Never auto-apply.** Always show a diff and get explicit approval before writing to
   any skill or CLAUDE.md. No exceptions.
2. **Recurrence gate.** Only propose a guardrail for a pattern seen **≥3 times across
   ≥2 distinct sessions** (default; user may lower). One bad session is an anecdote, not
   a pattern. Hardening against an anecdote is how skills rot into brittle patch-piles.
3. **Prefer general over specific.** A guardrail should express a *principle*, not patch
   one transcript. If you can only describe the fix by referencing one session, it's not
   ready.
4. **Cap the blast radius.** Max 3 guardrail edits per run. More than that means the
   diagnosis is too shallow — go narrower.
5. **Git is the undo button.** Refuse to apply edits in a dirty/untracked skill dir
   without warning; every change must be a reviewable, revertible diff. Note the rollback
   command in the changelog.
6. **Don't harden what you can't attribute.** If you can't tie a failure to a specific
   skill or to base/CLAUDE.md behavior, report it — don't guess at a target.

## Workflow

### Phase 1 — MINE & SHOW

**Always lead with the plain-language, skill-first report.** This is what the user
reads: which skills gave them the most grief, ranked, with bars. Do NOT open with raw
signature counts.

```bash
python3 ~/.config/skillshare/skills/skill-hardener/scripts/report.py --days 30
```

`report.py` ranks skills by real-trouble signals only (pushed back / stopped it mid-run /
it kept erroring), keeps the noisy high-volume signals out of the ranking, draws a bar per
skill, and lists however many clear the bar (`--min`, default 2) — so a quiet week shows
fewer than three, which is fine. It also consults the **ledger** (see "Registering fixes"
below): a skill you've already hardened only counts grief dated *after* the fix, so fixed
skills sink to the bottom marked done and the next-worst rises.

Then, under the hood, get the raw events for the diagnosis phases:

```bash
python3 ~/.config/skillshare/skills/skill-hardener/scripts/mine_friction.py \
  --days 30 --json /tmp/friction.json
```

Flags: `--days 0` for all history, `--session FILE` for one transcript, `--project SUB`
for one project, `--min-cluster N` for the raw display floor. Both scripts are read-only
and stdlib-only. Signatures and their false-positive risks: `references/signatures.md`.

### Phase 2 — CONFIRM (filter false positives)
The miner is high-recall. For each cluster above the recurrence gate, read the actual
surrounding turns from `/tmp/friction.json` (the `snippet` + open the `path` at that
`timestamp` if you need more context). Discard events that aren't real friction (user
quoting an error, intentional redirect, expected tool probing). **State your confirmed
count vs. raw count** so the user sees the filtering.

### Phase 3 — DIAGNOSE (signature → root cause)
A signature is a symptom. Name the underlying behavior using the root-cause map in
`references/signatures.md`. For each surviving cluster write a one-line root cause:
*"When X happens, Claude does Y instead of Z."* Use the miner's attribution to pick the
target artifact (a specific skill vs. CLAUDE.md). Cross-skill patterns → CLAUDE.md.

### Phase 4 — PROPOSE (guardrail + regression test, as a plan)
For each diagnosis, draft three things and present them **before editing**:
- **Guardrail**: the minimal, general edit (exact target file + proposed text).
- **Regression test**: a replayable scenario that reproduces the failure. Write it to
  `tests/<signature>.md` in the skill dir using the template in
  `references/test-template.md`. A test is a prompt + the failing behavior to watch for +
  the passing behavior expected. Where a structural check is possible (e.g. "the guardrail
  text now exists in the file"), include that too as a cheap automated assertion.
- **Evidence**: which sessions/timestamps motivate it (confirmed count).

Present all proposals as a single plan and get approval. Honor the blast-radius cap.

### Phase 5 — VERIFY (iterate edit against test until it passes)
For each approved guardrail:
1. Establish the test currently *exposes* the gap (red) — confirm the unhardened artifact
   would exhibit the signature on the scenario. For prompt-shaped tests this means a
   replay; for structural assertions, run the check.
2. Apply the guardrail edit (show the diff first per safeguard #1).
3. Re-run the test. If it still fails, refine the guardrail — **but stop after 3
   attempts** and report it as unresolved rather than thrashing (this skill must not
   commit the very `repeated_edit` sin it diagnoses).
4. For replay-style tests that need a fresh model run, hand off to skill-creator's eval
   harness if available; otherwise mark the test as **manual-replay** and give the user
   the exact prompt to paste. Be honest about which tests are automated vs. manual.

### Phase 6 — REPORT & RECORD
Deliver a changelog, most-impactful first. For each entry:
- Pattern + root cause, confirmed frequency, the session(s) it would have prevented.
- The guardrail (file + diff summary), the test (path + automated/manual), pass status.
- Rollback command (`git -C <dir> checkout -- <file>`).

**Then record every applied fix in the ledger** (this is what gives the skill memory —
do not skip it). Append one line per fixed skill to `hardening-log.jsonl`:

```bash
echo '{"date":"YYYY-MM-DD","skill":"<name>","summary":"<what changed, plainly>","files":["<edited file>"],"based_on_sessions":["<id>","<id>"]}' \
  >> ~/.config/skillshare/skills/skill-hardener/hardening-log.jsonl
```

If you edited a skill that lives in Skillshare, remember to `skillshare sync` so the fix
reaches the synced copies.

End with anything left unhardened (low recurrence, unattributable, or failed-to-verify)
so nothing is silently dropped.

## Registering fixes (the ledger)
`hardening-log.jsonl` is the skill's memory. Each line records a fix: the skill, the date,
what changed, and the sessions it was based on. `report.py` reads it and, for any fixed
skill, **only counts grief dated after the fix** — splitting old (addressed) from new.
So re-running tells you the truth about your last fix:
- **Fix worked** → the skill sinks to the bottom marked `✓ fixed … no new grief since`,
  and the next-worst skill rises to the top for you to tackle.
- **Fix didn't work** → fresh post-fix grief appears as `⚑ … NEW since the fix`, putting
  it back on the list. This is the self-improving loop: skills that stay fixed stay gone.

## When NOT to use this
- One-off mistakes the user is not asking to systematize.
- A brand-new skill with no usage history (use skill-creator to build and eval it first).
- When the user wants to *author* or *eval* a skill, not diagnose recurring failures —
  that's skill-creator's job.
