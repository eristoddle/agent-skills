---
name: angle-board
description: Turn one piece of raw material — a coding session, a research file, a topic, a pile of notes, or a single how-to — into a pyramid of distinct article angles instead of one obvious post. Builds an "angle board" of candidate posts across altitudes (weeds → tutorial → story → practice → thesis), each with its own lens, named reader, and evidence pointers, then designates a pillar and its spokes and persists the board as a checkbox task list. Two subject modes: cluster work you already did, or invert one *how* into N *whys* (payoff / actor / signal) to fan one technique into many use-case posts. Voice, evidence pool and output path are resolved up front, so it works for your own blog or for articles you're pitching to someone else. Stops at briefs; hands each to whatever writing skill the project uses. Trigger — "angle board", "what could I write about this", "multiple angles", "one idea many posts", "turn this into a pyramid", "more than one post out of this", "invert this how-to", "what could you use this for", "pitch a client some articles", or right after a research/miner skill produces notes.
---

<essential_principles>
## What this skill is for

One coding session, one research file, one book, one argument — is never one article. It's a pyramid. This skill builds the pyramid and leaves it on disk as a backlog you mine for months.

It sits in the middle of a pipeline:

```
RESEARCH                  THIS SKILL              WRITER
session write-ups      →                       →
saved web clips        →   angle-board         →  your writing skill
book highlights        →   (angle board)       →  (or you)
(or: any notes, any topic, nothing at all)
```

Research produces **notes**. This skill produces an **angle board**. A writer produces prose. Each stage stops at its own boundary. This skill does not write articles and does not mine sessions.

## The one rule that makes this work

**Altitude has an evidence requirement, and it is not negotiable.**

A single session can only honestly support the *bottom* of the pyramid — the weeds, the tutorial, maybe the project story. It cannot support a thesis, because a thesis with one proof point is an anecdote wearing a suit.

High-altitude angles are unlocked by the **corpus**, not by the current file. That is why the board must read the whole evidence pool, not just the one file it was handed. Three sessions across two projects and two months is what makes "here's what everyone gets wrong about subagents" a real post instead of a bluff.

So: if the evidence pool doesn't carry it, **say so**. Never manufacture a thought-leader take to fill a slot in the ladder. An empty rung is information — it tells the author what to go do more of.

## The four axes

Every angle on the board is a point in four dimensions. Full definitions, the altitude ladder, the lens bank, and the evidence gate live in `reference/axes.md` — **read it before generating any angles.**

| Axis | What it varies | Fixed or sampled |
|------|----------------|------------------|
| **Subject** | *which* piece of the material | derived from evidence clusters |
| **Altitude** | how far up the abstraction ladder | **fixed** — always walk all 5 rungs |
| **Lens** | the frame on a fixed subject | **sampled** — never the same 7 every time |
| **Reader** | who's on the other end, and what moment they're in | named per angle, always |

Altitude is fixed so you always get top-to-bottom coverage and the pyramid shape is guaranteed. Lens is sampled so every board doesn't come out as the same seven articles with the nouns swapped.

Structure/form is **not** an axis here — that's a downstream decision, once a brief is picked.

## The setup — three things to resolve before generating anything

The four axes are voice-agnostic. **The outlet is a parameter, not a law.** The same generation works for your own blog or for articles you're pitching to someone else. Before generating any angle, resolve these three inputs and say what you resolved:

| Input | What it is | If it isn't obvious |
|-------|------------|---------------------|
| **Voice** | How angles get *pitched*: the author's tone, what they'd never write. Look for a voice profile or style guide near the material (`voice-profile*.md`, a style guide, past posts). | Ask. If there is none, pitch neutrally and say so. Never borrow another author's voice by default. |
| **Evidence pool** | The corpus the board scans: research notes, session write-ups, prior posts, docs, whatever was handed over. | Ask what the pool is. A single file is a pool of one, and the board must say how thin that makes the upper rungs. |
| **Output path** | Where the board file is written. Default: next to the material, or the current directory. | State the path before writing. |

Optionally there's a **writer handoff**: the skill (or person) that turns a brief into prose. If the project has none, the skill stops at the brief and says so.

**What the setup never changes:** the four axes, the altitude ladder, the evidence gate, the pillar/spoke map, the don't-restate constraint. Those are the skill. Voice affects how an angle is *pitched*, never whether it's honestly supported.
</essential_principles>

<intake>
Two things to work out: the **setup** (voice, pool, output path, from the table above) and the **mode**.

**Mode** — from how the skill was invoked:

- **A path to a research/notes file** (or "use the notes from X", or invoked right after a miner skill ran) → **Build Board**, subject mode A
- **A project or topic name** (`/angle-board Project Name`) → resolve it against the corpus first, then **Build Board**, subject mode A
- **A bare topic with no material** ("angles on why subagents suck") → **Build Board**, corpus-only, subject mode A
- **An existing tutorial, technique, or capability to fan out** — "invert this", "what could you use this for", "N posts out of this one how-to", a vendor tutorial URL, "same technique, different use cases" → **Build Board**, **subject mode B** (see `reference/axes.md` Axis 1)
- **"Write #2" / "let's do the pillar" / a pick against an existing board** → **Pick and Brief**
- **No args** → list existing boards in the resolved output folder with their pending counts, ask whether to resume one (**Pick and Brief**) or build a new one (**Build Board**)

Modes A and B are subject-*derivation* modes, not separate workflows — both run `build-board.md`, which branches at Step 3. A board may legitimately use both (material you produced *and* a technique you haven't applied yet); say so if it does.
</intake>

<routing>
Read the workflow file, then follow it step by step.

| Mode | Workflow file |
|------|---------------|
| Build a board from material or a topic | `workflows/build-board.md` |
| Pick angles off a board → briefs → writer | `workflows/pick-and-brief.md` |

Both workflows depend on `reference/axes.md`. Read it first, every time. Read `reference/board-format.md` before writing a board file.
</routing>

<success_criteria>
Working when:
- The setup was resolved and stated: voice, evidence pool, and output path were all named before any angle was generated, and no other author's voice was borrowed
- The corpus was actually scanned — the board cites evidence from files *other than* the one it was handed, wherever the material supports it
- In subject mode B, every subject is a payoff/actor/**signal** triple and no subject's signal is "look at the data"
- All five altitude rungs were considered, and empty rungs are stated as empty with a reason, not padded
- Every angle names a specific reader in a specific moment — never "developers"
- Every angle carries an evidence rating and concrete pointers (session beat, commit, error, file, number)
- Lenses vary across the board and at least one is not from the seed bank
- One pillar is designated; spokes are linked to it and carry a "don't restate" constraint
- The board is written as a markdown file with real checkbox task lines, so any task tool (or a plain editor) can track it
- Nothing was written as prose — handoff to a writer is the only path to an article
</success_criteria>
