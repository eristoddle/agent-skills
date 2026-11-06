# The Four Axes

An angle is a point in four dimensions. Change any one and it's a genuinely different article. Change none and you've written the same post twice.

## Contents

- Axis 1 — SUBJECT (derived, not chosen)
  - Mode A — evidence clusters *(default)*
  - Mode B — inversion *(one how → N whys)*
- Axis 2 — ALTITUDE (fixed — always walk all five)
  - A5 — Thesis  *(the top — narrow, and hardest to earn)*
  - A4 — Practice
  - A3 — Project story  *(usually the pillar for material-driven boards)*
  - A2 — Tutorial
  - A1 — Weeds  *(the wide base)*
  - The evidence gate — enforce it
- Axis 3 — LENS (sampled — never the same list twice)
- Axis 4 — READER (named, always — the axis that prevents duplicates)
- Evidence rating (assign to every angle)
  - Rating in mode B — evidence means *demand*, not experience
- Pillar and spokes

---

## Axis 1 — SUBJECT (derived, not chosen)

**Subjects come out of the material, not out of your imagination** — but there are two ways material yields subjects, and they are different operations. Pick the one that fits what you were handed. A board may use both.

| | **Mode A — evidence clusters** | **Mode B — inversion** |
|---|---|---|
| Input | work you already did (a session, notes, a project) | a *how* you haven't applied yet (a tutorial, a technique, a capability) |
| Question | what happened here that's worth telling? | what would anyone want this **for**? |
| Fans | vertically — one job, five altitudes | horizontally — one mechanism, N payoffs |
| Evidence means | did you do it? | does anyone want it? |

---

### Mode A — evidence clusters *(default)*

A session isn't one story. It decomposes.

Go looking in the research material for these cluster types:

| Cluster | Where it lives in a research file | What it usually becomes |
|---------|-----------------------------------|-------------------------|
| An error and its recovery arc | `**Problems hit:**` / error_recoveries | a weeds post |
| A checked-off task with a story behind it | `# Recent Wins` | a tutorial or story |
| A tool/skill/model combination | `**Tools/skills used:**` | a practice post |
| A file touched over and over | `**Code anchors:**`, most-touched-files | the real center of gravity — often the subject you didn't notice |
| A parked question / thing you shelved | headings like "the parked question" | a thesis, usually the best one |
| A dead end you abandoned | user prompts that change direction abruptly | a negative-result post |
| A pattern that shows up in *two different projects* | cross-file, corpus-only | a practice or thesis post |

That last row is the one only the corpus can give you. Hunt for it.

**Rule:** a subject that appears in exactly one place in the material and left no artifact behind is not a subject, it's a detail. Fold it into a bigger one.

---

### Mode B — inversion *(one how → N whys)*

Every tutorial ever written answers ***how***. Almost none answer the question the reader actually has — ***why would I want that?*** There isn't one answer. There are several, and **each why is a separate route in, reaching a reader who didn't know they needed the technique.**

So one how is not one post. It's a supply of them. The subject you're deriving is not "scrape eBay" — that how is already written a hundred times and is nobody's article. The subject is a **triple**:

| Component | What it is | eBay example |
|-----------|-----------|--------------|
| **Payoff** | the outcome someone wants. Lean general so more readers recognize themselves — but general ≠ generic. "Automate your business" is not a payoff; "get told when a competitor changes their pricing page" is. | find supply/demand gaps |
| **Actor** | who's holding that payoff, and what their situation is. Feeds Axis 4 but is coarser — a role, not yet a moment. | a reseller sourcing inventory |
| **Signal** | **the discriminator.** The derived metric computed *on top of* the fetched data that turns rows into the payoff. | bid velocity (how fast price climbs, not where it lands); watcher-to-bid ratio; sell-through by category |

Same fetch, three signals, three genuinely different articles:

- *find supply/demand gaps* → bid velocity, watcher-to-bid ratio, sell-through rate
- *spot underpriced auctions to flip* → closing price vs. comparable completed listings, ending-time-of-day penalty
- *time your own listing* → category-level bid density by day and hour

**The signal is what makes this defensible.** Any model can regenerate hows — the training corpus is full of them — and can guess payoffs, because payoffs are cheap. What it can't produce is the specific column that predicts the outcome, because that comes from having looked at real data and worked out which one matters. A post whose middle section is *"here's the signal, and here's why this column and not the obvious one"* isn't regenerable.

**The rules for mode B:**

1. **No named signal, no subject.** A why whose signal is "look at the data" or "now you have the numbers" is a how wearing a why's hat. Find the real signal or fold the triple into a sibling.
2. **Aim for 4–8 triples.** Fewer means you accepted the first obvious uses; more means you're splitting one payoff into near-duplicates.
3. **Walk the ladder *across* the triples, not per triple.** Five rungs × six triples is thirty angles and no pyramid. Treat the triples as the subject set, then run Axis 2 over the whole set exactly as in mode A — one pillar, a cone, the same shape.
4. **The `how` itself is at most one angle**, usually an A2 tutorial, and usually a spoke. It is not the pillar. If the board's pillar is the how, mode B didn't happen.

**Where triples come from.** Read the source how for what it *fetches* (what data the technique puts in your hands), then ask who pays for that data today and what they compute from it. Vendor tutorials, docs, and example repos are excellent raw stock for this and **terrible** evidence of demand — they tell you what's buildable, never what's wanted. Keep the two jobs separate.

---

## Axis 2 — ALTITUDE (fixed — always walk all five)

The abstraction ladder. Always enumerate all five rungs for the material, in order. Coverage is the point.

Altitude and subject are **coupled**, and that coupling is what makes it a pyramid rather than a grid: at the top, every subject collapses into one thesis; at the bottom, one subject fractures into five separate weeds posts. So the board is a cone. Expect roughly 1 / 1–2 / 1–2 / 2–4 / 3–8 as you descend.

### A5 — Thesis  *(the top — narrow, and hardest to earn)*
Where this is all going, or what everyone gets wrong. Not about your project; your project is merely the evidence. ~1200–2000 words.
- **Requires: 3+ independent proof points in the corpus**, ideally spanning multiple projects *and* separated in time.
- Reader leaves with a changed belief, not a working build.

### A4 — Practice
What this says about *how to work*. The method, extracted from the project. Agentic workflow, skill design, how you plan, what you delegate. ~1500–2500 words.
- **Requires: 2+ independent instances** showing the same pattern. One project doing something once is not a practice.

### A3 — Project story  *(usually the pillar for material-driven boards)*
"How I built X, and everything that went wrong." The narrative arc — the thing a personal engineering blog is at its best. ~2000–3000 words.
- Requires: one project's session arc, with real failure in it.
- If there's no failure in the arc, this angle is weak. Go find the failure.

### A2 — Tutorial
Build the thing end to end. Reader finishes with a working version. ~1500–2500 words.
- Requires: one feature + code anchors + enough of the path to reproduce.

### A1 — Weeds  *(the wide base)*
One error, one config, one gotcha, one flag nobody documents. Copy-pasteable. Long-tail search traffic. ~400–1200 words.
- Requires: one concrete failure with a concrete fix.
- These feel too small to write. They are the ones that get found on Google at 1am. Generate several.

### The evidence gate — enforce it

*(In mode B, count demand proof points per the mode-B rating table below — same bars, different currency. The gate is never waived just because the subjects are hypothetical; a thesis about what people want, backed by nothing, is exactly the failure this section exists to prevent.)*

Before you put an A4 or A5 on the board, **count the proof points in the pool.** If you can't hit the bar:

> Do not write the angle anyway. Put the rung on the board as **empty**, and say what's missing.
>
> `**A5 — Thesis: (empty)** — needs 3+ proof points; the corpus has 1 (only the 2026-07-12 session shows this). Come back after another project hits the same wall.`

An empty rung is real information. It tells the author what to go do more of, and which future session will unlock the post. Manufacturing a thought-leader take to fill the slot is the single worst failure mode of this skill.

---

## Axis 3 — LENS (sampled — never the same list twice)

The frame you put on a fixed subject. **Do not walk this list top to bottom.** Sample 3–5 per board, weight toward ones that fit the actual material, and **invent at least one lens that isn't in this bank.** If a board comes out with the same lenses as the last board, the axis has failed.

If you have a verbalized-sampling or similar diversity technique, use it here — this is exactly the axis where mode collapse produces the same seven boring articles forever.

Seed bank (a starting point, not a menu):

- **Build-along** — here's how, follow me
- **Postmortem** — here's what broke and the autopsy
- **Contrarian** — everyone says X; I shipped Y and X is wrong
- **Bake-off** — I tried three, here's what actually won
- **Receipts** — the numbers: cost, tokens, hours, retries
- **Confession** — I did the dumb thing for three weeks
- **Artifact-first** — here's the repo/skill, go take it, here's why it exists
- **Archaeology** — why the old way existed, and what it was protecting against
- **Negative result** — this didn't work, and that's the useful part
- **The interrogation** — I asked the model for X and it gave me Y, over and over

---

## Axis 4 — READER (named, always — the axis that prevents duplicates)

Same subject, same altitude, same lens, different person on the other end — and it's a different article. This is the axis that makes a pyramid of posts feel genuinely distinct instead of re-skinned.

**Rule: name the person AND the moment they're in.** If you can't name the moment, the angle isn't real yet.

- Bad: "developers"
- Bad: "people interested in AI coding"
- Good: "the guy who just got `context_length_exceeded` at 1am and is pasting it into Google"
- Good: "the skeptic who's been told agentic coding is magic and has watched it produce garbage twice"
- Good: "someone three weeks into the same refactor, wondering if they should bail"

---

## Evidence rating (assign to every angle)

| Rating | Bar | Emoji on the task line |
|--------|-----|------------------------|
| `strong` | 3+ concrete artifacts — session beat, commit hash, error text, file path, a number | 🔺 pillar / ⏫ spoke |
| `medium` | 1–2 concrete artifacts | 🔼 |
| `thin` | 0 — real angle, but the author would write it from memory | 🔽 + tag `#ev/needs-you` |

**Never silently drop a thin angle.** Some of an author's best takes have zero session evidence and live entirely in their head. Flag them so they know they're on their own for the receipts — don't withhold them.

### Rating in mode B — evidence means *demand*, not experience

An inverted subject is a job you haven't done yet, so "did you do it?" rates everything `thin` and the axis stops discriminating. In mode B the rating answers **does anyone actually want this?** instead:

| Rating | Bar in mode B |
|--------|---------------|
| `strong` | someone is visibly paying for this outcome already — a paid tool that does exactly it, a job posting, a forum thread asking for it by name, a repo built for it |
| `medium` | the need is stated but nobody's built for it — one good complaint thread, a vendor doc hinting at it, an adjacent product |
| `thin` | you believe it and it's plausible, no external signal. Tag `#ev/needs-you` as usual |

A `thin` mode-B angle is a *hypothesis about demand*, and that's a legitimate thing to publish — just label it so the pitch doesn't claim a market that hasn't been checked. **Vendor tutorials never count as demand evidence at any tier**, however many of them exist; they're the raw stock being inverted, not proof anyone wanted the output.

---

## Pillar and spokes

The pyramid *is* hub-and-spoke. Map it:

- **A3 / A4 / A5** → pillar candidates (broad, evergreen, things link *up* into)
- **A1 / A2** → spokes (specific, long-tail, link *back up*)

Designate exactly **one pillar** per board — normally the strongest-evidence A3, unless the corpus has genuinely earned an A4/A5, in which case that outranks it.

Every spoke carries a **don't-restate constraint** naming the pillar: the spoke must drill *deeper* into one slice, never re-summarize the pillar from a different angle. Four posts off one session will cannibalize each other unless this is enforced at brief time. (a de-duplication pass over finished drafts is the downstream backstop, but the constraint belongs in the brief.)
