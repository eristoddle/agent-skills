# Board Format

The board is a **markdown file with real checkbox task lines** — not a JSON state file.

## Contents

- Template
- Pillar
- Spokes
- Higher altitude
- Thin ice (real angles, no receipts — you'd write these from memory)
- Open questions for the author
- Rules for writing the board

Why it matters: real `- [ ]` lines, priority emoji, and tags mean any task tool (an editor's todo extension, grep) can track status and answer "what do I write next", and a plain editor still reads it fine. Write the file so that works: top-level `- [ ]` lines in each section, priority emoji, and tags.

**Path:** `<slug>-angles-YYYY-MM-DD.md` in the output path resolved in build-board Step 0.
**Slug:** from the project or topic, lowercased, non-alphanumerics → hyphens.

---

## Template

````markdown
---
date: YYYY-MM-DD
type: angle-board
project: [Project or topic name]
voice: path/to/voice-profile.md   # or a one-line description of the voice used
subject-mode: A        # A (evidence clusters) | B (inversion) | A+B
source-research:
  - notes/billing-service-research-2026-07-12.md
  - notes/billing-service-research-2026-05-18.md
corpus-span: 2026-05-18 → 2026-07-12
pillar: A3-01
tags:
  - angle-board
source-skill: angle-board
---

# Angle Board — [Project] ([date])

[Two or three sentences: what material this is built from, how many files in the pool, what the
through-line across them is. If a pattern only became visible because of the corpus, say so here —
that's the whole point of the pool.]

## Pillar

- [ ] **A3-01 — [Working title]** 🔺 #altitude/story #lens/postmortem #ev/strong
	- **Pitch:** One or two sentences. What the post argues or delivers.
	- **Reader:** The specific person, in the specific moment they're in.
	- **Evidence:** `notes/billing-service-research-2026-07-12.md` § Session 2026-07-12 — the "three weeks of retries" arc; commit `a1b2c3d`; the `MaxTokens` retry loop
	- **Spokes:** A1-01, A1-03, A2-01

## Spokes

- [ ] **A2-01 — [Working title]** ⏫ #altitude/tutorial #lens/build-along #ev/strong
	- **Pitch:** ...
	- **Reader:** ...
	- **Evidence:** ...
	- **Don't restate:** stays on the how-to; the *why it broke* belongs to A3-01

- [ ] **A1-01 — [Working title]** ⏫ #altitude/weeds #lens/receipts #ev/strong
	- **Pitch:** ...
	- **Reader:** ...
	- **Evidence:** ...
	- **Don't restate:** one error, one fix — no project narrative, that's A3-01

*(mode B spoke — note the extra `Signal:` line)*

- [ ] **A2-02 — Find what eBay can't keep in stock** ⏫ #altitude/tutorial #lens/receipts #ev/medium
	- **Pitch:** Scrape a category's active and completed listings, then rank by the gap between demand and supply to find what to source.
	- **Signal:** bid velocity (price climb per hour, not final price) × watcher-to-bid ratio, normalized by category sell-through
	- **Reader:** a reseller with $2k to spend this month who's tired of guessing, and has been picking categories on vibes
	- **Evidence:** *(demand)* an existing paid tool sells this as a feature; a forum thread asking for it by name
	- **Don't restate:** the fetch and the auth dance belong to A2-05; this post starts with rows already in hand

## Higher altitude

- [ ] **A4-01 — [Working title]** 🔺 #altitude/practice #lens/contrarian #ev/strong
	- **Pitch:** ...
	- **Reader:** ...
	- **Evidence:** *(cross-corpus — this is what the pool unlocked)* `notes/docs-site-research-2026-05-22.md` the model-split section; `notes/billing-service-research-2026-05-18.md` session 2026-05-16; `notes/billing-service-research-2026-07-12.md` session 31
	- **Spoke of:** — *(A4 can be its own pillar; note if it outranks A3-01)*

- **A5 — Thesis: (empty)** — needs 3+ independent proof points; the pool has 1. Only the
  2026-07-12 session shows this. Unlocks when another project hits the same wall.

## Thin ice (real angles, no receipts — you'd write these from memory)

- [ ] **A5-02 — [Working title]** 🔽 #altitude/thesis #lens/contrarian #ev/needs-you
	- **Pitch:** ...
	- **Reader:** ...
	- **What's missing:** no session evidence — you'd be writing this on conviction. Worth it if you believe it.

## Open questions for the author

[3–5 questions only the author can answer, that would upgrade a thin angle to a strong one or
break the tie on which pillar to run.]
````

---

## Rules for writing the board

- **IDs are `A<rung>-<nn>`** — `A1-01`, `A3-02`. Stable; they're how the author picks ("write A1-03").
- **Task lines are top-level `- [ ]`** with the priority emoji from the evidence rating (see `axes.md`). Detail goes in indented sub-bullets, *not* in the task line — task tools read the task line, and stuffing it makes queries ugly.
- **Tags on the task line:** `#altitude/<rung>` `#lens/<lens>` `#ev/<rating>`. Lens tags are open-ended — a lens you invented gets a new tag, that's fine and expected.
- **An empty rung is a bold line, not a task.** It has no checkbox because it isn't writable yet. Say what's missing and what would unlock it.
- **Every spoke needs a `Don't restate:` line** naming what belongs to the pillar. This is the anti-cannibalization constraint and it carries into the brief.
- **Mode B angles carry a `Signal:` sub-bullet** — the derived metric, named concretely, right under `Pitch:`. It is the load-bearing field: it's what makes the angle a different article from its siblings and what the writer builds the middle section around. An angle whose `Signal:` reads "analyze the data" should not have made it onto the board (see `axes.md` Axis 1, mode B rule 1).
- **Mode B evidence pointers point at demand**, not at sessions — the tool that already sells this, the thread asking for it, the repo. Vendor tutorials are never demand evidence.
- **Evidence pointers must be concrete and findable** — the file path with a section name where possible, plus commit hashes, error strings, file paths, numbers. "The session showed this" is not evidence.
- Never delete a board. Boards accumulate; that's the backlog.
