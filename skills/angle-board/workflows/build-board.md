# Workflow: Build Board

Turn material (or just a topic) into a pyramid of angles, and persist it.

## Contents

- Step 0 — Resolve the setup
- Step 1 — Resolve the primary material
- Step 2 — Scan the corpus (the step that unlocks the top of the pyramid)
- Step 3 — Decompose into subjects
- Step 4 — Walk the ladder, sample the lenses, name the readers
- Step 5 — Designate the pillar and wire the spokes
- Step 6 — Write the board
- Step 7 — Report and offer the handoff

**Read `reference/axes.md` before you generate a single angle.** The evidence gate is the point of this skill; skipping it produces a board of confident-sounding bluffs.

---

## Step 0 — Resolve the setup

Per the setup table in `SKILL.md`. Pin down all three before generating anything, and **state them back** so a wrong assumption gets caught before you've written a board:

- **Voice** — a voice profile or style guide if one exists (look for `voice-profile*.md`, a style guide, or past posts near the material; ask if you can't find one). None → pitch neutrally and say so. Never borrow another author's voice by default.
- **Evidence pool** — what corpus is Step 2 scanning? Research notes, session write-ups, prior posts, docs, whatever was handed over. Ask if it isn't obvious.
- **Output path** — next to the material, or the current directory. State it.
- **Writer handoff** — the writing skill the project uses, if any. If there is none, the skill stops at the brief.

Then note which **subject mode** you're in (A, B, or both) — it decides how Step 2 and Step 3 run.

---

## Step 1 — Resolve the primary material

You were given one of:

- **A file path** → that's `PRIMARY`. Read it.
- **A project/topic name** → find its notes in the evidence pool:
  ```bash
  ls <pool-dir> | grep -i "<name>"
  ```
  One match → `PRIMARY`. Several → the newest is `PRIMARY`, the rest join the pool (they're the same project over time — that's a gift, not a duplicate). None → ask whether to gather notes first or build corpus-only.
- **A bare topic, no material** → `PRIMARY` is empty. Corpus-only mode. Say so plainly: the board will lean on the pool and on what the author tells you, and low-altitude rungs will be thin because there's no session to mine.

If invoked directly after a research or notes skill wrote a file in this conversation, that file is `PRIMARY` — don't ask.

**In subject mode B**, `PRIMARY` is the *how* being inverted — a tutorial, a technique, a capability, a vendor post, a URL. Read it for **what data or capability it puts in the reader's hands**, not for how it works; the mechanics are the one thing you're *not* varying. If it's a URL, fetch it with whatever web-fetch tool you have.

---

## Step 2 — Scan the corpus (the step that unlocks the top of the pyramid)

**This is not optional, and it is not the same as reading `PRIMARY`.** High-altitude angles exist only if the pool corroborates them.

Keep it bounded — never read every file whole.

Scan the pool you resolved in Step 0. Adapt the greps to that material's shape; for markdown notes a cheap structural pass looks like this:

```bash
cd <pool-dir>
ls -la *.md
# cheap structural pass over every file in the pool:
for f in *.md; do
  echo "=== $f"
  grep -n "^project:\|^date:\|^# \|^## " "$f"
done
```

That gives you every file's project, date, and section map for a few KB. From it, decide which files are *relevant to `PRIMARY`'s subjects* — same project, same tools, same class of problem, same wall hit twice.

Then read **only the relevant slices** of those files, using the line numbers from the grep (`Read` with `offset`/`limit`). Prioritize the sections that carry narrative and problems: suggested angles, session narratives, "problems hit" lists, and any hand-written through-line sections.

Now do the thing only the corpus can do:

> **Hunt for repeats.** What wall got hit in two different projects? What tool combination shows up across months? What did the author park in May and hit again in July? What did they claim in one file and contradict in another?

Every repeat you find is a candidate A4 or A5. A repeat across *different projects, separated in time* is the strongest evidence this pipeline can produce — flag it loudly.

If the pool is thin (one or two files), say so, and expect the top of the pyramid to come out empty. That's a correct result.

**In subject mode B the corpus is doing a different job.** You're not hunting repeats across sessions — you're hunting **demand evidence** for candidate payoffs (per the mode-B rating table in `axes.md`): who is paying for this outcome, who is asking for it, who already built something adjacent. Search the pool for the *outcome* language, not the technique's name. And do not count vendor tutorials or docs as demand, however many turn up — they're the stock being inverted.

---

## Step 3 — Decompose into subjects

Branch on the subject mode (`axes.md` Axis 1 defines both — read it there, not from this summary).

### Mode A — cluster the material

From `PRIMARY` + the relevant pool slices, cluster the material into subjects using the cluster table in `axes.md`. Look hardest at:

- the file touched over and over (often the real center of gravity, and usually not what the author thinks the session was about)
- the parked question / the thing they shelved
- the direction change — where the prompts abruptly pivot, something failed
- the pattern that shows up in two projects

Aim for 3–6 subjects. Fewer means you didn't decompose; more means you're calling details subjects.

### Mode B — invert the how into triples

From `PRIMARY` (the how), derive **payoff / actor / signal** triples. Each triple is one subject.

1. Name what the technique actually puts in the reader's hands — the *data or capability*, stated plainly. ("A structured feed of every active listing in a category, refreshed on demand.")
2. Ask who pays for that today, and what they compute from it. Each distinct computed thing is a candidate signal.
3. Write the triple. **Reject any candidate whose signal is "look at the data"** — that's the how again. Either find the real derived metric or fold it into a sibling triple.
4. Aim for **4–8 triples**. Use a verbalized-sampling or similar diversity technique here if you have one — the first three payoffs anyone thinks of are the same three everyone else published.
5. Sanity-check the set: if two triples would produce articles with the same middle section, they're one subject.

Then hand the triple set to Step 4 as the subject list and walk the ladder **across** it — not five rungs per triple. The board stays a cone with one pillar.

---

## Step 4 — Walk the ladder, sample the lenses, name the readers

For each of the five rungs, in order (A5 down to A1):

1. Which subjects can carry it *at this altitude*?
2. **Count proof points against the evidence gate.** A4 needs 2+, A5 needs 3+. If it fails, the rung is **empty** — write the empty line, say what's missing and what would unlock it, and move on. Do not fill the slot.
3. For the ones that pass, sample a lens — do not walk the seed bank in order, and invent at least one lens that isn't in it. Use a verbalized-sampling or similar diversity technique here if you have one; this axis is where mode collapse ruins the board.
4. Name the reader and the *moment* they're in. If you can't name the moment, the angle isn't real — cut it or fix it.
5. Rate the evidence (`strong` / `medium` / `thin`) and attach concrete pointers: session beat, commit hash, error text, file path, number.

Expect the shape to widen going down: roughly 1 thesis, 1–2 practice, 1–2 story, 2–4 tutorial, 3–8 weeds. The weeds rung will feel too small to write. Generate them anyway — they're the ones found on Google at 1am.

Keep any angle that's a real take with no receipts. It goes in **Thin ice**, tagged `#ev/needs-you`. Don't withhold it.

---

## Step 5 — Designate the pillar and wire the spokes

- Pillar = strongest-evidence A3, *unless* the corpus genuinely earned an A4/A5, which outranks it.
- A1s and A2s become spokes of that pillar.
- Every spoke gets a **`Don't restate:`** line naming what belongs to the pillar. Without this, four posts off one session cannibalize each other.
- If a second cluster is strong enough to be its own pillar, say so — but don't designate two. Suggest a second board.
- **Mode B guard:** the *how* itself is not the pillar. If the pillar came out as "here's how to do the technique," the inversion didn't happen — go back to Step 3. The how is usually one A2 spoke, and every other spoke's `Don't restate:` line points the mechanics at it, so six recipes don't each re-explain the same setup.

---

## Step 6 — Write the board

Read `reference/board-format.md` and follow the template exactly. Real `- [ ]` task lines, priority emoji, `#altitude/` `#lens/` `#ev/` tags, evidence pointers, stable `A<rung>-<nn>` IDs.

Write to the output path resolved in Step 0, named `<slug>-angles-YYYY-MM-DD.md`.

---

## Step 7 — Report and offer the handoff

Show the author the board's shape, not its full text — they can open the file. Lead with what the corpus unlocked, because that's the part they can't get any other way:

> Built 11 angles from 3 research files spanning May 18 → July 12.
>
> **The corpus earned you a practice post:** the plan-with-one-model, build-with-another split shows up in *both* the billing-service and docs-site projects, two months apart — that's A4-01, and it wasn't writable from either session alone.
>
> **A5 (thesis) came out empty** — needs a third proof point. One more project hitting the planning wall unlocks it.
>
> Pillar is A3-01 (the July 12 struggle). 6 spokes under it, 4 of them weeds posts.
>
> Board: `...-angles-2026-07-12.md`

In mode B, lead with the **signals** instead of the corpus — they're the part that proves the fan is real rather than one post cut into six:

> Inverted "scrape eBay listings" into 6 payoffs. The three that carry a real signal:
>
> **A2-01** supply/demand gaps → bid velocity + watcher-to-bid ratio. `#ev/strong` — three paid tools already sell exactly this.
>
> **A2-02** flip underpriced auctions → closing price vs. completed comps. `#ev/medium`.
>
> **A1-04** time your listing → bid density by hour. `#ev/thin`, you'd be asserting it.
>
> **Dropped 2** — "monitor prices" and "track competitors" had no signal past "look at the data," so they were the how again. Folded into A2-01.
>
> Pillar is A3-01 (what the data actually said when you ran it). The how-to itself is A2-05, a spoke.

Then ask which to write. They can pick more than one — that's the whole point. Go to `pick-and-brief.md`.
