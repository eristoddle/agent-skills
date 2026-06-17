# Regression Test Template

A skill-hardener regression test is a small, replayable spec that reproduces a past
failure and defines pass/fail. Two kinds, often combined:

- **Structural** — a grep/script assertion that runs instantly and deterministically
  (e.g. "the guardrail clause now exists in the target file", "the fallback tool is named
  in the skill"). Cheap; automate these.
- **Behavioral (replay)** — a prompt that, run through the hardened artifact, should no
  longer exhibit the signature. Needs a model run; mark **manual-replay** unless wired to
  skill-creator's eval harness.

Copy this into `tests/<signature-or-slug>.md`:

```markdown
# Test: <short name>

- **Signature(s):** <e.g. plan_reversal, user_frustration>
- **Root cause:** When <X> happens, Claude does <Y> instead of <Z>.
- **Motivating sessions:** <session-id @ timestamp>, ... (confirmed count: N)
- **Target artifact:** <path to skill or CLAUDE.md>
- **Kind:** structural | manual-replay | both

## Reproduction (the scenario)
<The minimal prompt/setup that triggered the failure. Paste-ready.>

## FAIL behavior (what went wrong — the red state)
<The observable signature: e.g. "locks the DB choice before asking" / "claims fixed
without running the test" / "retries defuddle 4x, never tries WebFetch".>

## PASS behavior (what the guardrail should produce — the green state)
<The corrected, observable behavior.>

## Structural assertion (if any)
```bash
# returns 0 when hardened, non-zero when the gap is open
grep -q "<guardrail phrase>" "<target file>"
```

## Status
- [ ] Red confirmed (unhardened artifact exhibits FAIL)
- [ ] Guardrail applied (diff reviewed & approved)
- [ ] Green confirmed (test passes)
```

## Principles
- The test must **fail before** the guardrail and **pass after** — a test that's green
  on the unhardened artifact proves nothing.
- Prefer one structural assertion per guardrail; they're the cheap regression net that
  survives across runs.
- Keep behavioral prompts minimal and self-contained so a future run (or skill-creator
  eval) can replay them without this conversation's context.
