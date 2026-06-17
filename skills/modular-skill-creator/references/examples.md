# Canonical Examples

Two reference skills that exemplify the modular pattern at its best. Read these when you need a concrete model to sanity-check generated output or explain the pattern to the user.

---

## ct-humanizer — Menu-Driven Router

**Path:** `~/.config/skillshare/skills/ct-humanizer/`

**Why it's canonical:**
- Router is ~100 lines. Intake uses AskUserQuestion to present two named options (Full humanize, Quick scan). Routing section maps each option to one workflow file in two lines.
- `workflows/full-humanize.md` — 200 lines of 6-pass sequential procedure. Completely self-contained.
- `workflows/quick-scan.md` — shorter diagnostic-only workflow.
- References cover data the workflows consult: word blacklist, structural patterns, before/after examples, manual checklist.
- Description field is long and trigger-rich; lists synonyms for the task.

**Best for illustrating:** how to split "all the logic" into focused workflows; how to use AskUserQuestion as the routing mechanism; how reference files hold data while workflows hold procedure.

---

## ct-fact-checker — Input-Shape / Autonomous Loop Router

**Path:** `~/.config/skillshare/skills/ct-fact-checker/`

**Why it's canonical:**
- Router intake is 4 lines: "run immediately; if called from another skill, no prompting; if direct, ask for path; go to verify-claims.md."
- `<instructions>` block is a 4-step numbered loop (EXTRACT → FIX → RE-VERIFY → CLEAR or LOOP). Each step names one workflow file.
- `workflows/verify-claims.md` — extracts all claims, fetches primary sources, produces JSON report. Standalone: could run without knowing anything else about the skill.
- Pinned to `claude-haiku-4-5` — illustrates when model pinning makes sense (high-iteration autonomous loop).
- The "Wiring Into Other Skills" section in `<instructions>` shows how to make a skill callable as a silent post-step from other skills.

**Best for illustrating:** input-shape routing (no user choice needed); pinning a model for performance; designing a skill to be called from other skills; looping workflows (loop back to step 2 until done).
