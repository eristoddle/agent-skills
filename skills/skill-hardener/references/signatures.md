# Friction Signature Catalog

The miner (`scripts/mine_friction.py`) emits these signatures from raw transcripts.
Each is **high-recall on purpose** — the workflow's confirmation pass re-reads the
surrounding turns and discards false positives before anything is proposed. Treat a
raw count as a *lead*, never as a verdict.

| Signature | What it detects | How it's detected (heuristic) | Common false positives |
|---|---|---|---|
| `user_frustration` | User pushing back / correcting | Negative lexicon (`no`, `stop`, `wrong`, `don't`, `still broken`, ALL-CAPS ratio >0.5) in a user turn | User quoting an error, discussing the words themselves, terse style |
| `user_interrupt` | User killed Claude mid-action | `[Request interrupted by user]` marker | Intentional redirect, not always a failure |
| `repeated_edit` | Three-failed-fixes loop | Same `file_path` hit by Edit/Write ≥3× in one session | Legitimate iterative authoring of a new file |
| `repeated_tool_error` | Flailing against a broken tool/cmd | `tool_result.is_error` streak ≥3 | Expected probing (e.g. checking if a file exists) |
| `plan_reversal` | Decision locked before user wanted | Negative user turn shortly after `ExitPlanMode` | User refining an approved plan |
| `claimed_done_no_verify` | "Fixed/works" with no run/test | Assistant says done-words with no preceding Bash test/run/build call | Doc-only changes, or verification done in a prior turn |
| `hook_block` | A hook blocked continuation | `system` line with `preventedContinuation` or `hookErrors` | Working-as-intended guardrail hooks |

## Mapping a signature to a root cause (not the same thing)

A signature is a *symptom*. The workflow must read the cluster's examples and name
the underlying behavior before proposing a fix. Reference root causes from the seed
insight:

- **premature decision-locking** → usually surfaces as `plan_reversal` or
  `user_frustration` right after a confident recommendation.
- **three-failed-fixes loop** → `repeated_edit` + `repeated_tool_error` together.
- **missed prompt/fallback sources** → often invisible structurally; found by reading
  `user_frustration` snippets where the user points at a source Claude didn't check.
- **fallback not attempted** (e.g. defuddle → WebFetch) → `repeated_tool_error` on one
  tool with no switch to an alternative.
- **verification skipped** → `claimed_done_no_verify`.

## Attribution rules

The miner tags each event with the last `Skill` invoked before it, or
`(base / CLAUDE.md)` if none. Use this to decide *what* to harden:

- Event under an active skill → candidate guardrail goes in **that skill**.
- Event under `(base / CLAUDE.md)` → candidate goes in **CLAUDE.md** (global or project).
- If the same root cause spans many skills → it's a *behavioral* rule; prefer CLAUDE.md
  over patching every skill.

## Tuning

Lexicon and thresholds live at the top of `mine_friction.py` (`NEG_PATTERNS`,
edit/error count breakpoints). Adjust there; keep this table in sync.
